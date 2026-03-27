# Gompertz.py
import pandas as pd
import numpy as np
from sklearn.linear_model import Ridge
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_squared_error
import logging
import joblib
from pathlib import Path
from config import config
from ev_forecast_utils import (
    load_and_preprocess_data, forecast_simple_trend, run_validation_phase,
    run_production_forecast, generate_full_forecast_and_plots, plot_and_save_feature_importance
)

logger = logging.getLogger(__name__)

def prepare_gompertz_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df['EV_Penetration_clipped'] = np.clip(df['EV_Penetration'], config.EPSILON, config.K_MAX - config.EPSILON)
    df['y_scaled'] = df['EV_Penetration_clipped'] / config.K_MAX
    df['Gompertz_Target'] = np.log(-np.log(df['y_scaled']))
    df['Gompertz_Target_lag1'] = df.groupby('ONS_code')['Gompertz_Target'].shift(1)
    df['Delta_Gompertz'] = df['Gompertz_Target'] - df['Gompertz_Target_lag1']
    df['Delta_Gompertz'] = df['Delta_Gompertz'].clip(lower=-1.0, upper=1.0)

    for col in config.LAG_FEATURES:
        df[f'{col}_lag1'] = df.groupby('ONS_code')[col].shift(1)
        df[f'log_{col}_lag1'] = np.log1p(np.maximum(0, df[f'{col}_lag1']))

    # Utilize centralized start year
    df['Years_since_base'] = df['Year'] - config.TRAIN_START_YEAR
    
    cat_cols = [c for c in ['Geo_level', 'Country', 'Region'] if c in df.columns]
    if cat_cols: df = pd.get_dummies(df, columns=cat_cols, drop_first=True)
    return df

def train_delta_gompertz_model(data: pd.DataFrame, end_train_year: int) -> dict:
    train_df = data[(data['Year'] <= end_train_year) & (data['Year'] >= config.TRAIN_START_YEAR)].replace(
        [np.inf, -np.inf], np.nan
    ).dropna(subset=['Delta_Gompertz'])
    
    exclude = ['EV_Penetration', 'EV_Penetration_clipped', 'y_scaled', 'Gompertz_Target', 'Delta_Gompertz', 'Year', 'ONS_code', 'ULEV_Total']
    features = [c for c in train_df.select_dtypes(include=['number', 'bool']).columns if c not in exclude]

    X_raw = train_df[features].copy()
    medians = X_raw.median()
    X = X_raw.fillna(medians)
    y = train_df['Delta_Gompertz']

    pipe = Pipeline([('scaler', StandardScaler()), ('ridge', Ridge(alpha=1.0))])
    pipe.fit(X, y)
    rmse = np.sqrt(mean_squared_error(y, pipe.predict(X)))
    logger.info(f"Gompertz Delta Model (up to {end_train_year}) – Training RMSE: {rmse:.4f}")

    model_path = config.get_output_folder("Gompertz") / f"gompertz_model_{end_train_year}.pkl"
    joblib.dump(pipe, model_path)

    return {'model': pipe, 'rmse': rmse, 'features': features, 'imputation_medians': medians}

def _prepare_next_row(current: dict, yr: int, exog_trends: dict, imputation_medians: dict | None, start_year: int) -> dict:
    if imputation_medians is None: imputation_medians = {}
    new_row = current.copy()
    new_row['Year'] = yr
    new_row['Years_since_base'] = yr - config.TRAIN_START_YEAR
    new_row['Gompertz_Target_lag1'] = current.get('Gompertz_Target', 0)

    for col in config.LAG_FEATURES:
        val = current.get(col, imputation_medians.get(col, 0))
        new_row[f'{col}_lag1'] = val
        new_row[f'log_{col}_lag1'] = np.log1p(max(0, val))

    steps_ahead = yr - start_year - 1
    for col, trend_array in exog_trends.items():
        idx = min(steps_ahead, len(trend_array) - 1)
        new_row[col] = trend_array[idx]
    return new_row

def inv_gompertz_func(g: float) -> float:
    """Helper to cleanly inverse Gompertz back to penetration percentage."""
    return config.K_MAX * np.exp(-np.exp(g))

def predict_recursive_gompertz(group: pd.DataFrame, pipeline, rmse: float, *, imputation_medians: dict | None = None, features: list | None = None, start_year: int, end_year: int, **kwargs) -> pd.DataFrame:
    history = group[group['Year'] <= start_year].copy()
    if history.empty or features is None or imputation_medians is None: return pd.DataFrame()

    future_years = np.arange(start_year + 1, end_year + 1)
    exog_trends = {c: forecast_simple_trend(history, c, future_years) for c in config.LAG_FEATURES if c in group.columns}

    results = []
    current = history.iloc[-1].to_dict()
    horizon = 0

    for yr in future_years:
        horizon += 1
        new_row = _prepare_next_row(current, int(yr), exog_trends, imputation_medians, start_year)
        
        # BULLETPROOF REINDEX: Prevents KeyError if a get_dummies column is missing in prediction
        X_new = pd.DataFrame([new_row]).reindex(columns=features, fill_value=0)
        X_new = X_new.fillna(imputation_medians).replace([np.inf, -np.inf], 0)

        delta_g = pipeline.predict(X_new)[0]
        delta_g = min(delta_g, config.GOMPERTZ_DELTA_CAP) 

        g_new = current.get('Gompertz_Target', 0) + delta_g
        margin = config.CI_Z * rmse * np.sqrt(horizon)

        pen = inv_gompertz_func(g_new)
        pen_low = inv_gompertz_func(g_new + margin)
        pen_high = inv_gompertz_func(g_new - margin)

        pen = max(pen, current.get('EV_Penetration', 0))
        pen_low = max(pen_low, current.get('EV_Penetration', 0))
        pen_high = max(pen_high, pen)

        new_row.update({'Gompertz_Target': g_new, 'EV_Penetration': pen})
        results.append({
            'Year': yr, 'EV_Penetration_base': pen,
            'EV_Penetration_lower': pen_low, 'EV_Penetration_upper': pen_high,
            'ONS_code': group['ONS_code'].iloc[0]
        })
        current = new_row
    return pd.DataFrame(results)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logging.getLogger('fontTools').setLevel(logging.WARNING) 

    df_raw = load_and_preprocess_data()
    df = prepare_gompertz_data(df_raw)

    run_validation_phase(df, predict_recursive_gompertz, train_delta_gompertz_model, model_name="Gompertz")
    
    output_path = config.get_output_folder("Gompertz") / f"Final_Gompertz_Forecast_{config.PRODUCTION_YEAR+1}_{config.FORECAST_END_YEAR}.csv"
    run_production_forecast(df, predict_recursive_gompertz, train_delta_gompertz_model, output_path=output_path, model_name="Gompertz")

    model_val = train_delta_gompertz_model(df, config.PRODUCTION_YEAR)
    generate_full_forecast_and_plots(
        df, predict_recursive_gompertz, model_val['model'], model_val['rmse'],
        start_year=config.PRODUCTION_YEAR, output_folder=config.get_output_folder("Gompertz"),
        model_name="Gompertz", ci_color='cornflowerblue', imputation_medians=model_val['imputation_medians'], features=model_val['features']
    )
    plot_and_save_feature_importance(model_val['model'], model_val['features'], "Gompertz", config.get_output_folder("Gompertz"))