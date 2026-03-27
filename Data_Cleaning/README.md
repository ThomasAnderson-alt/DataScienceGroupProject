# UK Vehicle Licensing Data Cleaning & Analysis

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![pandas](https://img.shields.io/badge/pandas-2.0%2B-150458?logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Cleaned and enriched UK vehicle licensing statistics** from Department for Transport (DfT) datasets VEH0132 and VEH0105, with focus on **Ultra Low Emission Vehicles (ULEVs)** and **total licensed cars**, including quarterly data and financial year summaries.

## Project Overview

This repository contains scripts and processed data for analyzing trends in UK vehicle registrations, with special attention to the transition toward low- and zero-emission vehicles.

### Main Goals

- Clean and standardize raw DfT quarterly vehicle licensing data
- Filter to **total cars** (excluding other vehicle types)
- Separate **total ULEV cars** (battery electric + plug-in hybrid + hybrid)
- Add **financial year (April–March) totals** for easier annual reporting
- Structure data geographically (UK → England → regions → local authorities)
- Prepare data for time series analysis, regional comparisons, and ULEV adoption studies

## Repository Structure

DataScienceGroupProject/
├── Data/
│ ├── Raw_Data/
│ │ ├── VEH0105.csv
│ │ ├── VEH0132.csv
│ │ └── VEH\*.ods (original spreadsheet versions)
│ └── Cleaned_Data/
│ ├── Total_All_Cars_with_FY_VEH0105.csv
│ └── Total_ULEV_Cars_with_FY_VEH0132.csv
├── Src/
│ └── Clean_vehicles_data.py ← Main cleaning script
├── README.md
└── .gitignore

## Data Sources

- **VEH0105**: Licensed vehicles by body type, fuel type, keepership and geography  
  Source: [DfT VEH0105](https://www.gov.uk/government/statistical-data-sets/veh01-licensed-vehicles)  
  Unit: thousands

- **VEH0132**: Ultra low emission vehicles (battery electric, plug-in hybrid, hybrid) by geography  
  Source: [DfT VEH0132](https://www.gov.uk/government/statistical-data-sets/veh01-licensed-vehicles) (ULEV tables)  
  Unit: actual count (not thousands)

Data is filtered from **2014 Q3** onwards (start of consistent ULEV reporting) up to the most recent quarter available in the files (currently 2025 Q3).

## Features of Cleaned Datasets

Both output files share the same structure:

| Column                                                   | Description                                                                       |
| -------------------------------------------------------- | --------------------------------------------------------------------------------- |
| `ONS Code`                                               | ONS geographic code (e.g., K02000001 = UK, E06000001 = Hartlepool, [z] = unknown) |
| `ONS Geography`                                          | Name of the area                                                                  |
| `Country`                                                | United Kingdom / England / Scotland / Wales / Northern Ireland / Other            |
| `Region`                                                 | Detailed region or "England (other/local authority)"                              |
| `Quarter`                                                | e.g. `2014 Q3`, `2025 Q1`, or `FY 2014/15`, `FY 2024/25`                          |
| `Total ULEV Cars (count)` / `Total All Cars (thousands)` | Count or thousands of vehicles                                                    |
| `Type`                                                   | `Quarter` or `Financial Year Total`                                               |

- UK aggregate (`K02000001`) appears first
- Data is sorted by ONS Code, then chronologically
- Financial year totals appear at the end of each geographic group
- Missing / suppressed values (`[x]`, `[z]`, `[low]`) → `NaN`

## How to Use

Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/DataScienceGroupProject.git
cd DataScienceGroupProject
```

Install required libraries

```bash
pip install pandas numpy
```

Run the cleaning script

```bash
python Src/Clean_vehicles_data.py

```
