import pandas as pd
import re

def clean_column_names(df):
    # Convert all column names to lowercase_snake_case
    df.columns = [
        re.sub(r'\W+', '_', col.strip().lower()).strip('_')
        for col in df.columns
    ]
    return df

def basic_clean(df):
    # Drop completely empty rows/columns
    df = df.dropna(how='all')           # remove rows where all cells are empty
    df = df.dropna(axis=1, how='all')   # remove columns where all cells are empty

    # Clean column names
    df = clean_column_names(df)

    # Preview missing values
    missing = df.isnull().sum()
    if missing.any():
        print("Missing values:")
        print(missing[missing > 0])

    return df
