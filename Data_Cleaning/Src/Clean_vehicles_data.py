from pathlib import Path
import pandas as pd

# Paths (unchanged)
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
RAW_DATA_DIR = PROJECT_ROOT / "Data" / "Raw_Data"
CLEANED_DATA_DIR = PROJECT_ROOT / "Data" / "Cleaned_Data"
CLEANED_DATA_DIR.mkdir(parents=True, exist_ok=True)

VEH0132_PATH = RAW_DATA_DIR / "VEH0132.csv"
VEH0105_PATH = RAW_DATA_DIR / "VEH0105.csv"

OUT_0132 = CLEANED_DATA_DIR / "Total_ULEV.csv"
OUT_0105 = CLEANED_DATA_DIR / "Total_Cars.csv"

# New: LAD code to region mapping (derived from LAD_UK.csv and region sources)
code_to_region = {
    'E06000001': 'North East',
    'E06000002': 'North East',
    'E06000003': 'North East',
    'E06000004': 'North East',
    'E06000005': 'North East',
    'E06000006': 'North West',
    'E06000007': 'North West',
    'E06000008': 'North West',
    'E06000009': 'North West',
    'E06000010': 'Yorkshire and the Humber',
    'E06000011': 'Yorkshire and the Humber',
    'E06000012': 'Yorkshire and the Humber',
    'E06000013': 'Yorkshire and the Humber',
    'E06000014': 'Yorkshire and the Humber',
    'E06000015': 'East Midlands',
    'E06000016': 'East Midlands',
    'E06000017': 'East Midlands',
    'E06000018': 'East Midlands',
    'E06000019': 'West Midlands',
    'E06000020': 'West Midlands',
    'E06000021': 'West Midlands',
    'E06000022': 'South West',
    'E06000023': 'South West',
    'E06000024': 'South West',
    'E06000025': 'South West',
    'E06000026': 'South West',
    'E06000027': 'South West',
    'E06000030': 'South West',
    'E06000031': 'East of England',
    'E06000032': 'East of England',
    'E06000033': 'East of England',
    'E06000034': 'East of England',
    'E06000035': 'South East',
    'E06000036': 'South East',
    'E06000037': 'South East',
    'E06000038': 'South East',
    'E06000039': 'South East',
    'E06000040': 'South East',
    'E06000041': 'South East',
    'E06000042': 'South East',
    'E06000043': 'South East',
    'E06000044': 'South East',
    'E06000045': 'South East',
    'E06000046': 'South East',
    'E06000047': 'North East',
    'E06000049': 'North West',
    'E06000050': 'North West',
    'E06000051': 'West Midlands',
    'E06000052': 'South West',
    'E06000053': 'South West',
    'E06000054': 'South West',
    'E06000055': 'East of England',
    'E06000056': 'East of England',
    'E06000057': 'North East',
    'E06000058': 'South West',
    'E06000059': 'South West',
    'E06000060': 'South East',
    'E06000061': 'East Midlands',
    'E06000062': 'East Midlands',
    'E06000063': 'North West',
    'E06000064': 'North West',
    'E06000065': 'Yorkshire and the Humber',
    'E06000066': 'South West',
    'E07000008': 'East of England',
    'E07000009': 'East of England',
    'E07000010': 'East of England',
    'E07000011': 'East of England',
    'E07000012': 'East of England',
    'E07000032': 'East Midlands',
    'E07000033': 'East Midlands',
    'E07000034': 'East Midlands',
    'E07000035': 'East Midlands',
    'E07000036': 'East Midlands',
    'E07000037': 'East Midlands',
    'E07000038': 'East Midlands',
    'E07000039': 'East Midlands',
    'E07000040': 'South West',
    'E07000041': 'South West',
    'E07000042': 'South West',
    'E07000043': 'South West',
    'E07000044': 'South West',
    'E07000045': 'South West',
    'E07000046': 'South West',
    'E07000047': 'South West',
    'E07000061': 'South East',
    'E07000062': 'South East',
    'E07000063': 'South East',
    'E07000064': 'South East',
    'E07000065': 'South East',
    'E07000066': 'East of England',
    'E07000067': 'East of England',
    'E07000068': 'East of England',
    'E07000069': 'East of England',
    'E07000070': 'East of England',
    'E07000071': 'East of England',
    'E07000072': 'East of England',
    'E07000073': 'East of England',
    'E07000074': 'East of England',
    'E07000075': 'East of England',
    'E07000076': 'East of England',
    'E07000077': 'East of England',
    'E07000078': 'South West',
    'E07000079': 'South West',
    'E07000080': 'South West',
    'E07000081': 'South West',
    'E07000082': 'South West',
    'E07000083': 'South West',
    'E07000084': 'South East',
    'E07000085': 'South East',
    'E07000086': 'South East',
    'E07000087': 'South East',
    'E07000088': 'South East',
    'E07000089': 'South East',
    'E07000090': 'South East',
    'E07000091': 'South East',
    'E07000092': 'South East',
    'E07000093': 'South East',
    'E07000094': 'South East',
    'E07000095': 'East of England',
    'E07000096': 'East of England',
    'E07000098': 'East of England',
    'E07000099': 'East of England',
    'E07000102': 'East of England',
    'E07000103': 'East of England',
    'E07000105': 'South East',
    'E07000106': 'South East',
    'E07000107': 'South East',
    'E07000108': 'South East',
    'E07000109': 'South East',
    'E07000110': 'South East',
    'E07000111': 'South East',
    'E07000112': 'South East',
    'E07000113': 'South East',
    'E07000114': 'South East',
    'E07000115': 'South East',
    'E07000116': 'South East',
    'E07000117': 'North West',
    'E07000118': 'North West',
    'E07000119': 'North West',
    'E07000120': 'North West',
    'E07000121': 'North West',
    'E07000122': 'North West',
    'E07000123': 'North West',
    'E07000124': 'North West',
    'E07000125': 'North West',
    'E07000126': 'North West',
    'E07000127': 'North West',
    'E07000128': 'North West',
    'E07000129': 'East Midlands',
    'E07000130': 'East Midlands',
    'E07000131': 'East Midlands',
    'E07000132': 'East Midlands',
    'E07000133': 'East Midlands',
    'E07000134': 'East Midlands',
    'E07000135': 'East Midlands',
    'E07000136': 'East Midlands',
    'E07000137': 'East Midlands',
    'E07000138': 'East Midlands',
    'E07000139': 'East Midlands',
    'E07000140': 'East Midlands',
    'E07000141': 'East Midlands',
    'E07000142': 'East Midlands',
    'E07000143': 'East of England',
    'E07000144': 'East of England',
    'E07000145': 'East of England',
    'E07000146': 'East of England',
    'E07000147': 'East of England',
    'E07000148': 'East of England',
    'E07000149': 'East of England',
    'E07000170': 'East Midlands',
    'E07000171': 'East Midlands',
    'E07000172': 'East Midlands',
    'E07000173': 'East Midlands',
    'E07000174': 'East Midlands',
    'E07000175': 'East Midlands',
    'E07000176': 'East Midlands',
    'E07000177': 'South East',
    'E07000178': 'South East',
    'E07000179': 'South East',
    'E07000180': 'South East',
    'E07000181': 'South East',
    'E07000192': 'West Midlands',
    'E07000193': 'West Midlands',
    'E07000194': 'West Midlands',
    'E07000195': 'West Midlands',
    'E07000196': 'West Midlands',
    'E07000197': 'West Midlands',
    'E07000198': 'West Midlands',
    'E07000199': 'West Midlands',
    'E07000200': 'East of England',
    'E07000202': 'East of England',
    'E07000203': 'East of England',
    'E07000207': 'South East',
    'E07000208': 'South East',
    'E07000209': 'South East',
    'E07000210': 'South East',
    'E07000211': 'South East',
    'E07000212': 'South East',
    'E07000213': 'South East',
    'E07000214': 'South East',
    'E07000215': 'South East',
    'E07000216': 'South East',
    'E07000217': 'South East',
    'E07000218': 'West Midlands',
    'E07000219': 'West Midlands',
    'E07000220': 'West Midlands',
    'E07000221': 'West Midlands',
    'E07000222': 'West Midlands',
    'E07000223': 'South East',
    'E07000224': 'South East',
    'E07000225': 'South East',
    'E07000226': 'South East',
    'E07000227': 'South East',
    'E07000228': 'South East',
    'E07000229': 'South East',
    'E07000234': 'West Midlands',
    'E07000235': 'West Midlands',
    'E07000236': 'West Midlands',
    'E07000237': 'West Midlands',
    'E07000238': 'West Midlands',
    'E07000239': 'West Midlands',
    'E07000240': 'East of England',
    'E07000241': 'East of England',
    'E07000242': 'East of England',
    'E07000243': 'East of England',
    'E07000244': 'East of England',
    'E07000245': 'East of England',
    'E08000001': 'North West',
    'E08000002': 'North West',
    'E08000003': 'North West',
    'E08000004': 'North West',
    'E08000005': 'North West',
    'E08000006': 'North West',
    'E08000007': 'North West',
    'E08000008': 'North West',
    'E08000009': 'North West',
    'E08000010': 'North West',
    'E08000011': 'North West',
    'E08000012': 'North West',
    'E08000013': 'North West',
    'E08000014': 'North West',
    'E08000015': 'North West',
    'E08000016': 'Yorkshire and the Humber',
    'E08000017': 'Yorkshire and the Humber',
    'E08000018': 'Yorkshire and the Humber',
    'E08000019': 'Yorkshire and the Humber',
    'E08000021': 'North East',
    'E08000022': 'North East',
    'E08000023': 'North East',
    'E08000024': 'North East',
    'E08000025': 'West Midlands',
    'E08000026': 'West Midlands',
    'E08000027': 'West Midlands',
    'E08000028': 'West Midlands',
    'E08000029': 'West Midlands',
    'E08000030': 'West Midlands',
    'E08000031': 'West Midlands',
    'E08000032': 'Yorkshire and the Humber',
    'E08000033': 'Yorkshire and the Humber',
    'E08000034': 'Yorkshire and the Humber',
    'E08000035': 'Yorkshire and the Humber',
    'E08000036': 'Yorkshire and the Humber',
    'E08000037': 'North East',
    'E09000001': 'London',
    'E09000002': 'London',
    'E09000003': 'London',
    'E09000004': 'London',
    'E09000005': 'London',
    'E09000006': 'London',
    'E09000007': 'London',
    'E09000008': 'London',
    'E09000009': 'London',
    'E09000010': 'London',
    'E09000011': 'London',
    'E09000012': 'London',
    'E09000013': 'London',
    'E09000014': 'London',
    'E09000015': 'London',
    'E09000016': 'London',
    'E09000017': 'London',
    'E09000018': 'London',
    'E09000019': 'London',
    'E09000020': 'London',
    'E09000021': 'London',
    'E09000022': 'London',
    'E09000023': 'London',
    'E09000024': 'London',
    'E09000025': 'London',
    'E09000026': 'London',
    'E09000027': 'London',
    'E09000028': 'London',
    'E09000029': 'London',
    'E09000030': 'London',
    'E09000031': 'London',
    'E09000032': 'London',
    'E09000033': 'London',
    'N09000001': 'Northern Ireland',
    'N09000002': 'Northern Ireland',
    'N09000003': 'Northern Ireland',
    'N09000004': 'Northern Ireland',
    'N09000005': 'Northern Ireland',
    'N09000006': 'Northern Ireland',
    'N09000007': 'Northern Ireland',
    'N09000008': 'Northern Ireland',
    'N09000009': 'Northern Ireland',
    'N09000010': 'Northern Ireland',
    'N09000011': 'Northern Ireland',
    'S12000005': 'Scotland',
    'S12000006': 'Scotland',
    'S12000008': 'Scotland',
    'S12000010': 'Scotland',
    'S12000011': 'Scotland',
    'S12000013': 'Scotland',
    'S12000014': 'Scotland',
    'S12000017': 'Scotland',
    'S12000018': 'Scotland',
    'S12000019': 'Scotland',
    'S12000020': 'Scotland',
    'S12000021': 'Scotland',
    'S12000023': 'Scotland',
    'S12000026': 'Scotland',
    'S12000027': 'Scotland',
    'S12000028': 'Scotland',
    'S12000029': 'Scotland',
    'S12000030': 'Scotland',
    'S12000033': 'Scotland',
    'S12000034': 'Scotland',
    'S12000035': 'Scotland',
    'S12000036': 'Scotland',
    'S12000038': 'Scotland',
    'S12000039': 'Scotland',
    'S12000040': 'Scotland',
    'S12000041': 'Scotland',
    'S12000042': 'Scotland',
    'S12000045': 'Scotland',
    'S12000047': 'Scotland',
    'S12000048': 'Scotland',
    'S12000049': 'Scotland',
    'S12000050': 'Scotland',
    'W06000001': 'Wales',
    'W06000002': 'Wales',
    'W06000003': 'Wales',
    'W06000004': 'Wales',
    'W06000005': 'Wales',
    'W06000006': 'Wales',
    'W06000008': 'Wales',
    'W06000009': 'Wales',
    'W06000010': 'Wales',
    'W06000011': 'Wales',
    'W06000012': 'Wales',
    'W06000013': 'Wales',
    'W06000014': 'Wales',
    'W06000015': 'Wales',
    'W06000016': 'Wales',
    'W06000018': 'Wales',
    'W06000019': 'Wales',
    'W06000020': 'Wales',
    'W06000021': 'Wales',
    'W06000022': 'Wales',
    'W06000023': 'Wales',
    'W06000024': 'Wales',
}

def clean_value(x):
    if isinstance(x, str):
        x = x.strip()
        if x in {'[x]', '[z]', '[c]', '', '-', 'n/a', 'NA', '..', '.', '—', '†'}:
            return None
        if x == '[low]':
            return 0.0  # Treat [low] as 0 for analysis
        try:
            return float(x.replace(',', ''))
        except ValueError:
            return x
    return x

def get_geo_info(code):
    code = str(code).strip().upper()
    
    if code == 'K02000001':
        return 'United Kingdom', 'Total', 'National'
    if code == 'K03000001':
        return 'Great Britain', 'Total', 'National'
    
    # Countries / nations
    if code == 'E92000001': return 'England', 'England', 'Country'
    if code == 'S92000003': return 'Scotland', 'Scotland', 'Country'
    if code == 'W92000004': return 'Wales', 'Wales', 'Country'
    if code == 'N92000002': return 'Northern Ireland', 'Northern Ireland', 'Country'
    
    # English regions (E12xxxxxx)
    region_codes = {
        'E12000001': ('England', 'North East', 'Region'),
        'E12000002': ('England', 'North West', 'Region'),
        'E12000003': ('England', 'Yorkshire and The Humber', 'Region'),
        'E12000004': ('England', 'East Midlands', 'Region'),
        'E12000005': ('England', 'West Midlands', 'Region'),
        'E12000006': ('England', 'East of England', 'Region'),
        'E12000007': ('England', 'London', 'Region'),
        'E12000008': ('England', 'South East', 'Region'),
        'E12000009': ('England', 'South West', 'Region'),
    }
    if code in region_codes:
        return region_codes[code]
    
    # English counties and met counties
    subregion_codes = {
        'E10000006': ('England', 'North West', 'County'),  # Cumbria
        'E11000007': ('England', 'North East', 'County'),  # Tyne and Wear
        # Add more as needed from data, e.g., 
        'E11000001': ('England', 'North West', 'County'),  # Greater Manchester
        'E11000002': ('England', 'North West', 'County'),  # Merseyside
        'E10000017': ('England', 'North West', 'County'),  # Lancashire
        'E11000003': ('England', 'Yorkshire and The Humber', 'County'),  # South Yorkshire
        'E11000006': ('England', 'Yorkshire and The Humber', 'County'),  # West Yorkshire
        # ... add complete list if possible
    }
    if code in subregion_codes:
        return subregion_codes[code]
    
    # LADs: Determine country from code prefix
    country = 'Unknown'
    region = 'Unknown (local)'
    level = 'LAD'
    if code.startswith(('E0', 'E1', 'E6', 'E7', 'E8', 'E9')):
        country = 'England'
        region = code_to_region.get(code, 'England (local)')  # Use mapping, fallback to placeholder
    elif code.startswith('W0'):
        country = 'Wales'
        region = 'Wales'
    elif code.startswith(('S0', 'S1')):
        country = 'Scotland'
        region = 'Scotland'
    elif code.startswith('N0'):
        country = 'Northern Ireland'
        region = 'Northern Ireland'
    
    return country, region, level


def process_vehicle_data(path, value_name):
    df = pd.read_csv(path, low_memory=False)
    df['ONS Geography'] = df['ONS Geography'].str.strip()  # Strip spaces from geographies
    
    q_cols = [c for c in df.columns if ' Q' in c]  # Removed restriction to >=2014 Q3 to include all
    
    for col in q_cols:
        df[col] = df[col].apply(clean_value)
    
    if 'BodyType' in df.columns:
        df = df[df['BodyType'] == 'Total']
    
    df = df[(df['Fuel'] == 'Total') & (df['Keepership'] == 'Total')]
    
    df_long = pd.melt(
        df[['ONS Code', 'ONS Geography'] + q_cols],
        id_vars=['ONS Code', 'ONS Geography'],
        value_vars=q_cols,
        var_name='Quarter',
        value_name=value_name
    ).dropna(subset=[value_name])
    
    # Handle [z] special rows (add to parent region / country) - now always applied
    z_mask = df_long['ONS Code'] == '[z]'
    z_df = df_long[z_mask]
    main_df = df_long[~z_mask].copy()
    
    # Define mappings for parents
    english_regions = {
        'North East': 'E12000001',
        'North West': 'E12000002',
        'Yorkshire and The Humber': 'E12000003',
        'East Midlands': 'E12000004',
        'West Midlands': 'E12000005',
        'East': 'E12000006',  # Alias for East of England
        'East of England': 'E12000006',
        'London': 'E12000007',
        'South East': 'E12000008',
        'South West': 'E12000009',
    }
    other_countries = {
        'England': 'E92000001',  # Added
        'Wales': 'W92000004',
        'Scotland': 'S92000003',
        'Northern Ireland': 'N92000002',
    }
    subarea_to_region = {
        'Tyne and Wear': 'E12000001',
        'Greater Manchester': 'E12000002',
        'Lancashire': 'E12000002',
        'Merseyside': 'E12000002',
        'South Yorkshire': 'E12000003',
        'West Yorkshire': 'E12000003',
        'Derbyshire': 'E12000004',
        'Leicestershire': 'E12000004',
        'Lincolnshire': 'E12000004',
        'Nottinghamshire': 'E12000004',
        'Staffordshire': 'E12000005',
        'Warwickshire': 'E12000005',
        'West Midlands': 'E12000005',
        'Worcestershire': 'E12000005',
        'Cambridgeshire': 'E12000006',
        'Essex': 'E12000006',
        'Hertfordshire': 'E12000006',
        'Norfolk': 'E12000006',
        'Suffolk': 'E12000006',
        'East Sussex': 'E12000008',
        'Hampshire': 'E12000008',
        'Kent': 'E12000008',
        'Oxfordshire': 'E12000008',
        'Surrey': 'E12000008',
        'West Sussex': 'E12000008',
        'Devon': 'E12000009',
        'Gloucestershire': 'E12000009',
    }
    
    unmatched = set()
    for _, row in z_df.iterrows():
        geo = row['ONS Geography'].strip()
        target_code = None
        
        if geo.startswith('Local Authority unknown within '):
            area = geo[len('Local Authority unknown within '):].strip()
            if area in english_regions:
                target_code = english_regions[area]
            elif area in other_countries:
                target_code = other_countries[area]
        elif geo.startswith('District unknown within '):
            area = geo[len('District unknown within '):].strip()
            target_code = subarea_to_region.get(area)
        elif geo == 'Vehicle under disposal previously GB':
            target_code = 'K03000001'
        elif geo == 'Vehicle under disposal previously NI':
            target_code = 'N92000002'
        elif geo == 'Region or county unknown':
            target_code = 'K02000001'
        
        if target_code:
            mask = (main_df['ONS Code'] == target_code) & (main_df['Quarter'] == row['Quarter'])
            if mask.any():
                main_df.loc[mask, value_name] += row[value_name]
        else:
            unmatched.add(geo)
    
    if unmatched:
        print(f"Warning: Unmatched [z] geographies skipped: {unmatched}")
    
    df_long = main_df
    
    # Apply geography classification
    geo_info = df_long['ONS Code'].apply(get_geo_info)
    df_long[['Country', 'Region', 'Geo_level']] = pd.DataFrame(geo_info.tolist(), index=df_long.index)
    
    # Pivot → wide format
    wide = df_long.pivot_table(
        index=['ONS Code', 'ONS Geography', 'Country', 'Region', 'Geo_level'],
        columns='Quarter',
        values=value_name,
        aggfunc=lambda x: x.iloc[0]
    ).reset_index()
    
    # Rename columns to match Charging_Port.csv style
    wide = wide.rename(columns={'ONS Code': 'ONS_code', 'ONS Geography': 'ONS_geo'})
    
    # Rename quarter columns to end-of-quarter month-year format (e.g., 2025 Q3 -> Sep-25)
    quarter_map = {
        'Q1': 'Mar',
        'Q2': 'Jun',
        'Q3': 'Sep',
        'Q4': 'Dec'
    }
    rename_dict = {}
    for col in wide.columns[5:]:
        year, q = col.split(' ')
        month = quarter_map[q]
        new_col = f"{month}-{year[-2:]}"
        rename_dict[col] = new_col
    wide = wide.rename(columns=rename_dict)
    
    # Sort quarter columns descending (newest first)
    quarters = sorted(wide.columns[5:], key=lambda x: (int('20' + x.split('-')[1]), list(quarter_map.values()).index(x.split('-')[0])), reverse=True)
    cols = ['ONS_code', 'ONS_geo', 'Country', 'Region', 'Geo_level'] + quarters
    wide = wide[cols]
    
    # Sort rows: National → Countries → Regions → County → LADs
    level_order = {'National': 0, 'Country': 1, 'Region': 2, 'County': 3, 'LAD': 4}
    wide = wide.assign(sort_key=wide['Geo_level'].map(level_order)) \
               .sort_values(['sort_key', 'Country', 'Region', 'ONS_code']) \
               .drop(columns='sort_key')
    
    # Round total cars to 1 decimal (if applicable)
    if "thousands" in value_name.lower():
        for col in quarters:
            wide[col] = wide[col].round(1)
    
    return wide


if __name__ == "__main__":
    print("Generating wide-format vehicle data (calendar quarters)")
    
    ulev = process_vehicle_data(VEH0132_PATH, "Total ULEV Cars")
    ulev.to_csv(OUT_0132, index=False)
    
    total = process_vehicle_data(VEH0105_PATH, "Total All Cars (thousands)")
    total.to_csv(OUT_0105, index=False)
    
    print(f"Created:\n  {OUT_0132.name}  ({len(ulev):,} rows)")
    print(f"  {OUT_0105.name}   ({len(total):,} rows)")