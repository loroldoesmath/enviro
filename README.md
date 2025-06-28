# Environmental Analysis 

A data engineering + MLOps portfolio project using real-world environmental indicators from multiple sources.

## Features

- Loads and normalizes data from 5 key datasets:
  - Update Temperature
  - Forest Area
  - CO₂ Emissions
  - Hazardous Waste
  - Marine & Protected Areas
- Builds a structured SQLite database with foreign key constraints
- Ready for machine learning pipelines and visualizations
- Fully reproducible and Python-driven

## Getting Started

1. Clone the repo:
    ```bash
    git clone https://github.com/loroldoesmath/enviro
    cd enviro
    ```

2. Install Python dependencies:
    ```bash
    pip install pandas
    ```

3. Run the loader:
    ```bash
    python slim_loader.py
    ```

4. Open `slim_enviro.db` in your favorite tool (like DBeaver)

## Folder Structure

enviro/

├── slim_loader.py # script to create tables and load CSVs

├── slim_enviro.db # generated SQLite DB file

└── data/

└── slim/ # cleaned source CSVs



---

## Dataset Overview

| Table Name                                      | Description                                                                 |
|------------------------------------------------|-----------------------------------------------------------------------------|
| `update_temperature`                           | Primary table: year, country, climate metrics, energy & extreme weather     |
| `unified_emissions`                            | CO₂ and GHG emissions per country                                           |
| `forests_forest_area`                          | Forest coverage & land use metrics                                          |
| `waste_hazardous_generated`                    | Hazardous waste generated per country and year                              |
| `biodiversity_terrestrial_marine_protected_areas` | Protected area coverage (land/marine)                                      |

All tables are linked through foreign key relationships to ensure referential integrity and queryability.

---

## Machine Learning Models

Target variable: **Extreme Weather Events**  
Features include:  
- CO₂ emissions (tons per capita)  
- Sea level rise  
- Forest area %  
- Renewable energy %  
- Rainfall  
- Population  
- Average temperature  

### Model Results

| Model           | MSE   | R²    |
|-----------------|--------|--------|
| Linear Regression | 31.45 | 0.715 |
| Random Forest     | 15.65 | 0.858 |
| XGBoost           | 16.23 | 0.853 |

---

## Analysis Opportunities

These results suggest promising predictive power from environmental and socio-economic indicators:

### Forest Coverage and Climate Impact
- Investigate whether countries with declining forest areas have increased extreme weather events.
- Add lag features to capture delayed effects from land use changes.

### Sea Level Rise + Rainfall
- Perform time-series clustering on rainfall + sea level to isolate high-risk regions.
- Investigate regional differences (e.g., island nations vs inland countries).

### Renewable Energy % vs. Events
- Explore thresholds for "protection effect" — e.g., do countries with >30% renewable energy see fewer events?
- Use SHAP values to analyze feature importance more deeply per model.

---

## Visualizations

---

## How to Reproduce

Clone this repo:
   ```bash
   git clone https://github.com/loroldoesmath/enviro
   cd enviro
Explore
