from dataclasses import dataclass, field
from pathlib import Path
from typing import List

@dataclass(frozen=True)
class Config:
    """Central configuration – change once, affects all models."""
    # Paths
    DATA_FILE: Path = Path(r"C:\Downloaded Files\MSc Data Science\Group Project\Analysis\Cleaned_Data\Master_Panel_Data_Final.csv")
    OUTPUT_BASE: Path = Path(r"C:\Downloaded Files\MSc Data Science\Group Project\Analysis\Test_Result\Master_Panel_Data")

    # Model parameters
    K_MAX: float = 50.24                 # Ultimate Fleet Ceiling (%) based on ZEV mandate & fleet turnover
    EPSILON: float = 1e-6                # Prevent log(0) errors
    GOMPERTZ_DELTA_CAP: float = 0.005    # Soft cap for year-over-year Gompertz momentum
    AH_MAX_GROWTH_FACTOR: float = 0.85         

    # Features & time
    LAG_FEATURES: List[str] = field(default_factory=lambda: [
        'GDHI_per_Capita', 'Vehicle_Total', 'Charging Ports', 'Population'
    ])
    
    # Time Anchors
    TRAIN_START_YEAR: int = 2019         # Enforce 2019 start for training and plots (Data quality cutoff)
    INNOVATION_BASE_YEAR: int = 2010     # T=0 for Logarithmic Time Engine (Dawn of modern EV market)
    
    # Forecasting Horizons
    VALIDATION_YEAR: int = 2022          # Train 19-22, Tests against 23, 24, 25 actuals
    PRODUCTION_YEAR: int = 2023          # Train 19-23, Forecasts out to 2027
    FORECAST_END_YEAR: int = 2027        # End horizon

    # Output
    DPI_SAVE: int = 600
    CI_Z: float = 1.96

    def get_output_folder(self, model_name: str) -> Path:
        safe_name = "".join(c if c.isalnum() else "_" for c in model_name)
        folder = self.OUTPUT_BASE / safe_name
        folder.mkdir(parents=True, exist_ok=True)
        return folder

# Global singleton
config = Config()