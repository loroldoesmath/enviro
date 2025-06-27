import os
import sqlite3
import pandas as pd
import re

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data', 'slim')
DB_PATH = os.path.join(BASE_DIR, 'slim_enviro.db')

# =============== clean col helper ===============
def clean_col(col):
    col = col.strip().lower()
    col = re.sub(r'\W+', '_', col)
    return col

# =============== table creation SQL ===============
SCHEMA_SQL = """
DROP TABLE IF EXISTS update_temperature;
DROP TABLE IF EXISTS unified_emissions;
DROP TABLE IF EXISTS forests_forest_area;
DROP TABLE IF EXISTS waste_hazardous_generated;
DROP TABLE IF EXISTS biodiversity_terrestrial_marine_protected_areas;

CREATE TABLE update_temperature (
    year INTEGER,
    country TEXT PRIMARY KEY,
    avg_temperature_degC REAL,
    co2_emissions_tons_per_capita REAL,
    sea_level_rise_mm REAL,
    rainfall_mm REAL,
    population INTEGER,
    renewable_energy_pct REAL,
    extreme_weather_events INTEGER,
    forest_area_pct REAL
);

CREATE TABLE unified_emissions (
    country_id TEXT,
    country TEXT PRIMARY KEY,
    time_series_co2_total_emissions_without_lulucf_in_1000_t REAL,
    co2_emissions_latest_year REAL,
    co2_emissions_per_capita_latest_year REAL,
    co2_change_since_1990 REAL,
    FOREIGN KEY (country) REFERENCES update_temperature(country) ON DELETE SET NULL
);

CREATE TABLE forests_forest_area (
    countryid TEXT,
    country_and_area TEXT,
    forest_area_1990_1000_ha REAL,
    forest_area_2000_1000_ha REAL,
    forest_area_2010_1000_ha REAL,
    forest_area_2015_1000_ha REAL,
    forest_area_2020_1000_ha REAL,
    total_land_area_2020_1000_ha REAL,
    forest_area_as_a_proportion_of_total_land_area_2020 REAL,
    deforestation_2015_2020_1000_ha_year REAL,
    total_forest_area_affected_by_fire_2015_100_ha REAL,
    FOREIGN KEY (country_and_area) REFERENCES update_temperature(country) ON DELETE SET NULL
);

CREATE TABLE waste_hazardous_generated (
    countryid TEXT,
    country TEXT,
    year_1990 REAL,
    year_1995 REAL,
    year_2000 REAL,
    year_2005 REAL,
    year_2010 REAL,
    year_2015 REAL,
    year_2017 REAL,
    FOREIGN KEY (country) REFERENCES update_temperature(country) ON DELETE SET NULL
);

CREATE TABLE biodiversity_terrestrial_marine_protected_areas (
    countryid TEXT,
    country_and_area TEXT,
    latest_year_available TEXT,
    terrestrial_and_marine_protected_areas_of_total_territorial_area REAL,
    FOREIGN KEY (country_and_area) REFERENCES update_temperature(country) ON DELETE SET NULL
);
"""

# =============== load and insert ===============
def insert_csv_to_table(conn, file_name, table_name, keep_cols=None):
    full_path = os.path.join(DATA_DIR, file_name)
    df = pd.read_csv(full_path)

    # clean and filter columns
    df.columns = [clean_col(c) for c in df.columns]
    if keep_cols:
        df = df[[clean_col(c) for c in keep_cols if clean_col(c) in df.columns]]

    # convert NaN to None for SQLite
    df = df.where(pd.notnull(df), None)

    placeholders = ', '.join(['?'] * len(df.columns))
    col_names = ', '.join([f'"{col}"' for col in df.columns])
    insert_sql = f'INSERT INTO "{table_name}" ({col_names}) VALUES ({placeholders})'
    
    conn.executemany(insert_sql, df.values.tolist())
    print(f"✅ Inserted {len(df)} rows into {table_name}")

# =============== main ===============
def main():
    conn = sqlite3.connect(DB_PATH)
    conn.executescript(SCHEMA_SQL)

    insert_csv_to_table(conn, 'update_temperature.csv', 'update_temperature')

    insert_csv_to_table(conn, 'co2_emissions.csv', 'unified_emissions', keep_cols=[
        'country_id', 'country', 'time_series_co2_total_emissions_without_lulucf_in_1000_t',
        'co2_emissions_latest_year', 'co2_emissions_per_capita_latest_year', 'co2_change_since_1990'
    ])

    insert_csv_to_table(conn, 'forest_area.csv', 'forests_forest_area', keep_cols=[
        'countryid', 'country_and_area', 'forest_area_1990_1000_ha', 'forest_area_2000_1000_ha',
        'forest_area_2010_1000_ha', 'forest_area_2015_1000_ha', 'forest_area_2020_1000_ha',
        'total_land_area_2020_1000_ha', 'forest_area_as_a_proportion_of_total_land_area_2020',
        'deforestation_2015_2020_1000_ha_year', 'total_forest_area_affected_by_fire_2015_100_ha'
    ])

    insert_csv_to_table(conn, 'hazardous_waste_generated.csv', 'waste_hazardous_generated', keep_cols=[
        'countryid', 'country', '1990', '1995', '2000', '2005', '2010', '2015', '2017'
    ])

    insert_csv_to_table(conn, 'terrestrial_marine_protected_areas.csv',
                        'biodiversity_terrestrial_marine_protected_areas', keep_cols=[
                            'countryid', 'country_and_area', 'latest_year_available',
                            'terrestrial_and_marine_protected_areas_of_total_territorial_area'
                        ])

    conn.commit()
    conn.close()
    print("✅ All data inserted successfully into slim_enviro.db")

if __name__ == "__main__":
    main()
