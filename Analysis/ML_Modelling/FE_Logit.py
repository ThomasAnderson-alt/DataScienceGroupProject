# FE_Logit.py
"""
Fixed Effects Fractional Logit Panel Model.
Applies 'Add-Factoring' (intercept shifting) to guarantee the forecasted S-curve 
connects seamlessly to the last observed real-world data point.
"""

import pandas as pd
import numpy as np
import statsmodels.api as sm
from linearmodels.panel import PanelOLS
import logging
import joblib
from pathlib import Path
from sklearn.metrics import mean_squared_error
from config import config
from ev_forecast_utils import (
    load_and_preprocess_data, forecast_simple_trend, run_validation_phase,
    run_production_forecast, generate_full_forecast_and_plots, plot_and_save_feature_importance
)

logger = logging.getLogger(__name__)
RAW_FEATURES = config.LAG_FEATURES

def prepare_fe_panel_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df['EV_Penetration_clipped'] = np.clip(df['EV_Penetration'], config.EPSILON, config.K_MAX - config.EPSILON)
    df['y_scaled'] = df['EV_Penetration_clipped'] / config.K_MAX
    df['Logit_Target'] = np.log(df['y_scaled'] / (1 - df['y_scaled']))
    
    # Utilize centralized base year
    df['ln_time'] = np.log(df['Year'] - config.INNOVATION_BASE_YEAR)
    for col in RAW_FEATURES:
        if col in df.columns:
            df[f'ln_{col}'] = np.log(np.maximum(df[col], 1))
    return df

def train_fe_panel_logit(data: pd.DataFrame, end_train_year: int) -> dict:
    exog_cols = ['ln_time'] + [f'ln_{c}' for c in RAW_FEATURES if f'ln_{c}' in data.columns]
    required_cols = ['Logit_Target'] + exog_cols
    
    train_df = data[(data['Year'] <= end_train_year) & (data['Year'] >= config.TRAIN_START_YEAR)].dropna(subset=required_cols).copy()
    train_panel = train_df.set_index(['ONS_code', 'Year'])
    
    y = train_panel['Logit_Target']
    X = sm.add_constant(train_panel[exog_cols])
    
    model = PanelOLS(y, X, entity_effects=True)
    results = model.fit(cov_type='robust')

    fixed_effects = results.estimated_effects.groupby(level='ONS_code').mean()
    fe_dict = fixed_effects['estimated_effects'].to_dict()
    global_mean_fe = fixed_effects['estimated_effects'].mean()
    
    fitted_values = results.predict(X)
    fitted_full = fitted_values['predictions'] + results.estimated_effects['estimated_effects']
    rmse = np.sqrt(mean_squared_error(y, fitted_full))
    logger.info(f"Training RMSE: {rmse:.4f}")
    
    folder = config.get_output_folder("FE-Panel-Logit")
    model_path = folder / f"fe_panel_model_{end_train_year}.pkl"
    joblib.dump(results, model_path)
    
    return {
        'model': results, 'rmse': rmse, 'features': exog_cols,
        'fixed_effects': fe_dict, 'global_mean_fe': global_mean_fe,
        'imputation_medians': train_df[RAW_FEATURES].median().to_dict()
    }

def inv_logit_func(l: float) -> float:
    """Helper to cleanly inverse logit back to penetration percentage."""
    return config.K_MAX / (1 + np.exp(-np.clip(l, -20, 20)))

def predict_recursive_fe(group: pd.DataFrame, model, rmse: float, start_year: int, end_year: int, **kwargs) -> pd.DataFrame:
    history = group[group['Year'] <= start_year].copy()
    if history.empty: return pd.DataFrame()
    
    ons_code = group['ONS_code'].iloc[0]
    alpha_i = kwargs.get('fixed_effects', {}).get(ons_code, kwargs.get('global_mean_fe', 0.0))
    future_years = np.arange(start_year + 1, end_year + 1)
    
    exog_trends_raw = {
        c: forecast_simple_trend(history, c, future_years) for c in RAW_FEATURES if c in history.columns
    }
    params = model.params
    
    # DRY Helper: Single source of truth for the prediction math
    def _calc_logit(yr: int, value_dict: dict) -> float:
        logit = alpha_i + params.get('const', 0.0)
        if 'ln_time' in params: 
            logit += params['ln_time'] * np.log(yr - config.INNOVATION_BASE_YEAR)
        for c in RAW_FEATURES:
            if f'ln_{c}' in params and c in value_dict:
                logit += params[f'ln_{c}'] * np.log(max(value_dict[c], 1))
        return logit

    # 1. Base prediction for the last known historical year
    last_vals = {c: history[c].iloc[-1] for c in RAW_FEATURES if c in history.columns}
    pred_logit_last = _calc_logit(start_year, last_vals)

    current_pen = history['EV_Penetration'].iloc[-1]
    current_logit_real = history['Logit_Target'].iloc[-1]
    results = []
    horizon = 0
    
    for i, yr in enumerate(future_years):
        horizon += 1
        
        # 2. Mathematical prediction for current year
        current_vals = {c: exog_trends_raw[c][i] for c in RAW_FEATURES if c in exog_trends_raw}
        pred_logit_current = _calc_logit(int(yr), current_vals)
                
        # 3. Add-Factoring
        delta_growth = pred_logit_current - pred_logit_last
        adjusted_logit = current_logit_real + delta_growth
        
        margin = config.CI_Z * rmse * np.sqrt(horizon)
        
        pen = inv_logit_func(adjusted_logit)
        pen_low = inv_logit_func(adjusted_logit - margin)
        pen_high = inv_logit_func(adjusted_logit + margin)
        
        # Enforce monotonically increasing rule
        pen = max(pen, current_pen)
        pen_low = max(pen_low, current_pen)
        pen_high = max(pen_high, pen)
        
        results.append({
            'Year': yr, 'EV_Penetration_base': pen,
            'EV_Penetration_lower': pen_low, 'EV_Penetration_upper': pen_high,
            'ONS_code': ons_code
        })
        
        current_pen = pen
        current_logit_real = adjusted_logit
        pred_logit_last = pred_logit_current
    
    return pd.DataFrame(results)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logging.getLogger('fontTools').setLevel(logging.WARNING) 
    
    df_raw = load_and_preprocess_data()
    df = prepare_fe_panel_data(df_raw)
    
    run_validation_phase(df, predict_func=predict_recursive_fe, model_train_func=train_fe_panel_logit, model_name="FE-Panel-Logit")
    
    output_folder = config.get_output_folder("FE-Panel-Logit")
    run_production_forecast(
        df, predict_func=predict_recursive_fe, model_train_func=train_fe_panel_logit,
        output_path=output_folder / f"Final_FE_Forecast_{config.PRODUCTION_YEAR+1}_{config.FORECAST_END_YEAR}.csv",
        model_name="FE-Panel-Logit"
    )
    
    train_res = train_fe_panel_logit(df, config.PRODUCTION_YEAR)
    generate_full_forecast_and_plots(
        df, predict_func=predict_recursive_fe, model=train_res['model'], rmse=train_res['rmse'],
        start_year=config.PRODUCTION_YEAR, output_folder=output_folder, model_name="FE-Panel-Logit",
        ci_color='teal', fixed_effects=train_res.get('fixed_effects'), global_mean_fe=train_res.get('global_mean_fe')
    )
    
    plot_and_save_feature_importance(train_res['model'], None, "FE-Panel-Logit", output_folder)