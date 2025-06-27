# 🌎 EnviroLens

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

