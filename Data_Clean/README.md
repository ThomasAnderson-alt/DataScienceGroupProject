# README: GDHI LAD Panel Dataset (1997-2023)

  This README documents the data engineering process used to create the **`GDHI_LAD_Panel_1997-2023.csv`** dataset. This **primary panel** is a core component of our project, providing the socio-economic foundation to analyze EV adoption drivers across the United Kingdom.

------
  ## 0. Project Structure

```text
.
├── data/                      
│   ├── data_raw/             
│   │   └── regional_gross_disposable_household_income_local_authorities_2023.xlsx
│   └── data_cleaned/          
│       └── GDHI_LAD_Panel_1997-2023.csv
├── data_clean.ipynb
└── README.md             
```

  ## 1. Overview

  - **Filename:** `GDHI_LAD_Panel_1997-2023.csv`
  - **Scope:** UK Local Authority Districts (LADs), 1997–2023.
  - **Format:** Long (Panel Data) for statistical modeling.
  - **Source:** [regional_gross_disposable_household_income_local_authorities_2023.xlsx](https://www.ons.gov.uk/file?uri=/economy/regionalaccounts/grossdisposablehouseholdincome/datasets/regionalgrossdisposablehouseholdincomelocalauthorities/1997to2023/regionalgrossdisposablehouseholdincomelocalauthorities2023.xlsx) (Tables 3, 4, and 6).

------
  ## 2. Data Setup
  Due to file size/storage policy, the raw data is not uploaded to this repository. 
  To run the scripts:
  1. Download the source files from the link above.
  2. Place the raw files into the `data/data_raw/` folder.
  3. Run `data_clean.ipynb` to generate the processed files in `data/data_cleaned/`.

  ## 3. Data Processing Workflow

  1. **Standardization**: Renamed ONS identifiers to `ons_code` and `ons_geography`.

  2. **Geographic Tagging**: Added hierarchical labels:

     - **`national`**: Classified as **GB** (England, Scotland, Wales) or the **UK** (Northern Ireland).
     - **`country`**: England, Scotland, Wales, or Northern Ireland.
     - **`region`**: English regions or constituent countries.
     - **`county`**: Mapped Unitary Authorities to self and London Boroughs to **Greater London**.

  3. **Reshaping**: **Melted** 27 annual columns into a single `year` column.

  4. **Merging**: Integrated absolute values, indices, and growth rates via **Left Join**.

     > **Note**: The 1997 growth rate is `NaN` as it serves as the baseline year for the 1998 calculation.

------

  ## 4. Column Schema 


| **Column Group**     | **Columns & Definitions**                                                                                                                                                 |
|:---------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Identifiers**      | `ons_code`, `ons_geography`, `year`                                                                                                                                       |
| **Geo-Tags**         | `geo_level`, `national`, `country`, `region`, `county`                                                                                                                    |
| **Economic Metrics** | `gdhi_per_head`: Absolute value in GBP (£) <br/>  `gdhi_index`: Index (UK Average = 100) <br/>  `gdhi_growth`: Annual growth rate in percentage points (e.g., 2.5 = 2.5%) |