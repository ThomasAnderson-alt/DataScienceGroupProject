# ev_forecast_utils.py
"""
Shared utilities for UK regional EV penetration forecasting models.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams, ticker
import logging
from pathlib import Path
from sklearn.metrics import mean_squared_error, mean_absolute_error
from config import config

logger = logging.getLogger(__name__)

# IEEE / Science publication style
rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['Helvetica', 'Arial', 'DejaVu Sans'],
    'font.size': 10,
    'axes.labelsize': 11,
    'axes.titlesize': 12,
    'xtick.labelsize': 9,
    'ytick.labelsize': 9,
    'legend.fontsize': 9,
    'axes.linewidth': 0.8,
    'lines.linewidth': 1.4,
    'lines.markersize': 4.5,
    'axes.grid': True,
    'grid.linestyle': '--',
    'grid.alpha': 0.35,
    'axes.spines.top': False,
    'axes.spines.right': False,
    'xtick.direction': 'in',
    'ytick.direction': 'in',
    'figure.figsize': (3.5, 2.8),
    'figure.dpi': 300,
    'savefig.dpi': config.DPI_SAVE,
    'legend.frameon': True,
    'legend.edgecolor': 'black',
    'legend.fancybox': False,
})

# National aggregates
AGGREGATES = {
    'UK': 'K02000001',
    'England': 'E92000001',
    'Wales': 'W92000004',
    'Scotland': 'S92000003',
    'NI': 'N92000002'
}

def load_and_preprocess_data(data_path: Path = config.DATA_FILE) -> pd.DataFrame:
    if not data_path.exists():
        raise FileNotFoundError(f"Data file not found: {data_path}")
    df = pd.read_csv(data_path)
    numerical_cols = ['GDHI_per_Capita', 'Population', 'Vehicle_Total', 'Charging Ports', 'EV_Penetration']
    for col in numerical_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col].astype(str).str.replace(',', ''), errors='coerce')
    df['Year'] = df['Year'].astype(int)
    df = df.sort_values(['ONS_code', 'Year'])
    logger.info(f"Loaded {len(df)} rows from {data_path}")
    return df

def forecast_simple_trend(history: pd.DataFrame, col: str, future_years: np.ndarray, n_years: int = 3) -> np.ndarray:
    y = history[col].dropna().values[-n_years:]
    x = history.loc[history[col].notna(), 'Year'].values[-n_years:]
    if len(set(x)) < 2 or len(y) < 2:
        fallback = y[-1] if len(y) > 0 else history[col].median()
        fallback = fallback if not pd.isna(fallback) else 0
        return np.full(len(future_years), fallback)
    coef = np.polyfit(np.asarray(x, dtype=float), np.asarray(y, dtype=float), 1)
    return np.polyval(coef, future_years)

def create_regional_forecasts(df: pd.DataFrame, predict_func, model, rmse: float,
                              start_year: int, end_year: int, **predict_kwargs) -> pd.DataFrame:
    forecasts = []
    for ons, group in df.groupby('ONS_code'):
        if len(group) < 3:
            continue
        fut = predict_func(
            group, model, rmse, start_year=start_year, end_year=end_year, **predict_kwargs
        )
        if not fut.empty:
            forecasts.append(fut)
    
    if not forecasts:
        return pd.DataFrame()
    return pd.concat(forecasts, ignore_index=True)

def run_validation_phase(df: pd.DataFrame, predict_func, model_train_func, model_name: str = "Model"):
    logger.info(f"--- Validation Phase: Training up to {config.VALIDATION_YEAR} ({model_name}) ---")
    train_result = model_train_func(df, end_train_year=config.VALIDATION_YEAR)
    
    forecasts = create_regional_forecasts(
        df, predict_func, train_result['model'], train_result['rmse'],
        start_year=config.VALIDATION_YEAR, end_year=2025,
        **{k: v for k, v in train_result.items() if k not in ['model', 'rmse']}
    )
    
    actual_start = config.VALIDATION_YEAR + 1
    actuals = df[(df['Year'] >= actual_start) & (df['Year'] <= 2025)][['ONS_code', 'Year', 'EV_Penetration']]
    merged = pd.merge(forecasts, actuals, on=['ONS_code', 'Year'], how='inner')
    
    if not merged.empty:
        rmse_oos = np.sqrt(mean_squared_error(merged['EV_Penetration'], merged['EV_Penetration_base']))
        mae_oos  = mean_absolute_error(merged['EV_Penetration'], merged['EV_Penetration_base'])
        logger.info(f"Out-of-sample ({actual_start}–2025): RMSE = {rmse_oos:.2f}%, MAE = {mae_oos:.2f}%")

def run_production_forecast(df: pd.DataFrame, predict_func, model_train_func,
                            output_path: Path, model_name: str = "Model"):
    logger.info(f"--- Production Forecast: Training up to {config.PRODUCTION_YEAR} ({model_name}) ---")
    train_result = model_train_func(df, end_train_year=config.PRODUCTION_YEAR)
    
    forecasts = create_regional_forecasts(
        df, predict_func, train_result['model'], train_result['rmse'],
        start_year=config.PRODUCTION_YEAR, end_year=config.FORECAST_END_YEAR,
        **{k: v for k, v in train_result.items() if k not in ['model', 'rmse']}
    )
    
    if not forecasts.empty:
        forecasts.to_csv(output_path, index=False)
        logger.info(f"Production forecast saved: {output_path}")

def generate_full_forecast_and_plots(df: pd.DataFrame, predict_func, model, rmse: float,
                                     start_year: int, output_folder: Path,
                                     model_name: str = "Model", ci_color: str = 'mediumseagreen',
                                     **predict_kwargs):
    logger.info(f"--- Generating full {model_name} forecast ({start_year+1}–{config.FORECAST_END_YEAR}) ---")
    df_forecast = create_regional_forecasts(
        df, predict_func, model, rmse, start_year=start_year,
        end_year=config.FORECAST_END_YEAR, **predict_kwargs
    )
    
    if df_forecast.empty: return
    
    csv_path = output_folder / f"{model_name}_Forecast_{start_year+1}_{config.FORECAST_END_YEAR}.csv"
    df_forecast.to_csv(csv_path, index=False)
    
    for name, code in AGGREGATES.items():
        hist = df[df['ONS_code'] == code].copy()
        pred = df_forecast[df_forecast['ONS_code'] == code].copy()
        
        # FIX: Force plot history to only show from 2019 onward
        hist_plot = hist[hist['Year'] >= config.TRAIN_START_YEAR]
        
        if hist_plot.empty or pred.empty:
            continue
        
        fig, ax = plt.subplots()
        ax.plot(hist_plot['Year'], hist_plot['EV_Penetration'], 'k-o', label='Actual', zorder=3)
        ax.plot(pred['Year'], pred['EV_Penetration_base'], 'b--o', label=model_name, zorder=3)
        ax.fill_between(pred['Year'], pred['EV_Penetration_lower'], pred['EV_Penetration_upper'],
                        color=ci_color, alpha=0.25, label='95% CI', zorder=2)
        
        last_hist_year = hist_plot['Year'].max()
        last_hist_pen = hist_plot[hist_plot['Year'] == last_hist_year]['EV_Penetration'].iloc[0]
        first_pred_year = pred['Year'].min()
        ax.fill_between([last_hist_year, first_pred_year],
                        [last_hist_pen, pred['EV_Penetration_lower'].iloc[0]],
                        [last_hist_pen, pred['EV_Penetration_upper'].iloc[0]],
                        color=ci_color, alpha=0.25, zorder=2)
        
        ax.axvline(start_year + 1, color='gray', linestyle=':', label='Forecast start')
        ax.axhline(config.K_MAX, color='red', linestyle='--', alpha=0.5, label=f'Ceiling ({config.K_MAX}%)')
        
        # Enforce X-axis boundaries perfectly to 2019-2027
        ax.set_xlim(config.TRAIN_START_YEAR - 0.5, config.FORECAST_END_YEAR + 0.5)
        
        ax.set_title(f'EV Penetration: {name} ({model_name})', pad=8)
        ax.set_xlabel('Year')
        ax.set_ylabel('EV Penetration (%)')
        ax.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))
        ax.legend(loc='upper left', frameon=True, edgecolor='black', fontsize=8.5)
        ax.grid(True, axis='y', zorder=0)
        
        base_path = output_folder / f'{name}_{model_name}_Forecast_CI'
        fig.savefig(base_path.with_suffix('.pdf'), bbox_inches='tight')
        fig.savefig(base_path.with_suffix('.png'), bbox_inches='tight', dpi=config.DPI_SAVE)
        plt.close(fig)

def plot_and_save_feature_importance(model, features_or_params, model_name: str, output_folder: Path):
    if hasattr(model, 'named_steps') and 'ridge' in model.named_steps:
        coef = model.named_steps['ridge'].coef_
        index = features_or_params if features_or_params else [f"X{i}" for i in range(len(coef))]
        imp = pd.Series(np.abs(coef), index=index).sort_values(ascending=False)
        title = f"Feature Importance – {model_name} (Ridge)"
    elif hasattr(model, 'params'):
        imp = pd.Series(np.abs(model.params), index=model.params.index).sort_values(ascending=False)
        title = f"Parameter Importance – {model_name}"
    else:
        return
    
    rename_map = {
        'Vehicle_Total': 'Total Vehicles', 'GDHI_per_Capita': 'GDHI per Capita',
        'ln_time': 'Time Engine (ln(t))', 'ln_GDHI_per_Capita': 'ln(GDHI per Capita)',
        'ln_Vehicle_Total': 'ln(Total Vehicles)', 'ln_Charging Ports': 'ln(Charging Ports)',
        'ln_Population': 'ln(Population)'
    }
    
    imp.index = [rename_map.get(idx, idx.replace('_', ' ')) for idx in imp.index]
    n_show = 15
    imp_top = imp.head(n_show).sort_values(ascending=True)
    
    fig, ax = plt.subplots(figsize=(7.2, 6.0))
    bars = ax.barh(imp_top.index, np.asarray(imp_top.values), color='steelblue', edgecolor='black', linewidth=0.7)
    
    max_val = imp_top.max()
    for bar in bars:
        width = bar.get_width()
        ax.text(width + 0.001 * max_val, bar.get_y() + bar.get_height()/2, f'{width:.4f}', va='center', fontsize=8.5)
    
    ax.set_title(title, fontsize=12, pad=12)
    ax.set_xlabel('Absolute Coefficient Magnitude')
    ax.set_xlim(0, max_val * 1.18)
    ax.grid(True, axis='x', alpha=0.3, linestyle='--')
    fig.tight_layout()
    
    base = output_folder / f'{model_name}_feature_importance'
    fig.savefig(base.with_suffix('.pdf'), bbox_inches='tight')
    fig.savefig(base.with_suffix('.png'), dpi=config.DPI_SAVE, bbox_inches='tight')
    plt.close(fig)