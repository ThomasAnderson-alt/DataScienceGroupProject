# MSc Data Science Group Project: EV Penetration Prediction

[![GitHub repo size](https://img.shields.io/github/repo-size/ThomasAnderson-alt/DataScienceGroupProject)](https://github.com/ThomasAnderson-alt/DataScienceGroupProject)
[![GitHub license](https://img.shields.io/github/license/ThomasAnderson-alt/DataScienceGroupProject)](https://github.com/ThomasAnderson-alt/DataScienceGroupProject)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)

## Overview

This repository contains the group project for the MSc Data Science program, focusing on predicting Electric Vehicle (EV) penetration rates in the UK. The project involves data cleaning, machine learning modeling, and forecasting future EV adoption trends.

## Project Structure

### Analysis/

- **Cleaned_Data/**: Processed datasets ready for analysis
  - `Master_Panel_Data_Final.csv`: Final cleaned panel data
- **ML_Modelling/**: Machine learning scripts and utilities
  - `config.py`: Configuration settings
  - `ev_forecast_utils.py`: Utility functions for EV forecasting
  - `FE_Logit.py`: Fixed Effects Logit model implementation
  - `Gompertz.py`: Gompertz growth model for EV adoption
- **Panel_Fractional_Logit_Model/**: Specialized modeling for penetration prediction
  - `Penetration_Prediction.ipynb`: Jupyter notebook for EV penetration analysis
- **Test_Result/**: Model outputs and forecasts
  - **Master_Panel_Data/**: Results from different models
    - **FE_Panel_Logit/**: Fixed Effects Panel Logit forecasts (2024-2027)
    - **Gompertz/**: Gompertz model forecasts (2024-2027)
    - **PFLM/**: Panel Fractional Logit Model results including future features and predictions up to 2035 (Finished by Jipeng Song)

### Data_Cleaning/

- **Data/**: Raw and cleaned vehicle data
  - **Cleaned_Data/**: `Total_Cars.csv`, `Total_ULEV.csv`
  - **Raw_Data/**: Source datasets (`LAD_UK.csv`, `VEH0105.csv`, `VEH0132.csv`)
- **Src/**: Data cleaning scripts
  - `Clean_vehicles_data.py`: Python script for data preprocessing
- `README.md`: Documentation for data cleaning process

### Final Report/

- `56部分latex.md`: LaTeX content for the final report
- `Weight_Analysis.ipynb`: Jupyter notebook for weight analysis
- `论文提纲.md`: Thesis outline in Chinese

### Week 8 Pre/

- Preliminary work and preparations for Week 8

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/ThomasAnderson-alt/DataScienceGroupProject.git
   cd DataScienceGroupProject
   ```

2. Create a virtual environment:

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt  # If requirements.txt exists, otherwise install necessary packages like pandas, scikit-learn, statsmodels, etc.
   ```

## Usage

### Data Cleaning

Run the data cleaning script:

```bash
python Data_Cleaning/Src/Clean_vehicles_data.py
```

### Running Models

- For Fixed Effects Logit: Execute `Analysis/ML_Modelling/FE_Logit.py`
- For Gompertz Model: Run `Analysis/ML_Modelling/Gompertz.py`
- For Panel Fractional Logit: Open and run `Analysis/Panel_Fractional_Logit_Model/Penetration_Prediction.ipynb`

### Viewing Results

Forecast results are available in `Analysis/Test_Result/Master_Panel_Data/` with CSV files for different models and time periods.

## Dependencies

- Python 3.8+
- pandas
- numpy
- scikit-learn
- statsmodels
- matplotlib
- seaborn
- jupyter

## Branches

- **Main-Project**: Main branch containing the project baseline
- **Yiding-Wang**: Development branch for extended analysis and model improvements

## Contributors

- Yiding Wang - Analysis and model development
- Jipeng Song - Finalising the model and make improvement
## Acknowledgments

This project is part of the MSc Data Science program and focuses on understanding and predicting the adoption of Ultra-Low Emission Vehicles (ULEVs) across different regions in the UK using advanced econometric and machine learning techniques.

## Contributors

- Yiding Wang (Branch: Yiding-Wang)
- Jipeng Song (Branch: Jipeng-Song)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Data sources: UK Department for Transport vehicle statistics
- MSc Data Science Program
