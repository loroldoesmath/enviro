import sqlite3
import pandas as pd
from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor
from sklearn.metrics import mean_squared_error, r2_score


def load_table_from_sqlite(db_path: str, table_name: str) -> pd.DataFrame:
    """Connect to SQLite database and load the specified table into a DataFrame."""
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query(f"SELECT * FROM {table_name};", conn)
    conn.close()
    
    # print(f"Loaded table '{table_name}' with shape: {df.shape}")
    # print(f"Columns: {df.columns.tolist()}")
    # print(df.head(3))  # show first 3 rows
    
    return df

def convert_columns_to_numeric(df: pd.DataFrame, exclude_cols=None):
    """
    Convert all columns (except excluded ones) to numeric where possible.
    """
    if exclude_cols is None:
        exclude_cols = []

    for col in df.columns:
        if col not in exclude_cols:
            df[col] = pd.to_numeric(df[col], errors='coerce')  # turns bad strings into NaN

    return df

def get_feature_and_target_columns(df: pd.DataFrame, target_col: str, exclude_cols=None):
    """
    Identify numeric feature columns, confirm target column exists.
    
    Returns:
      feature_cols (list of str): numeric columns to use as features
      target_col (str): the target column name (unchanged)
    """
    if exclude_cols is None:
        exclude_cols = []

    # Filter exclude_cols to existing columns only
    exclude_cols = [col for col in exclude_cols if col in df.columns]

    # Select numeric columns
    numeric_cols = df.select_dtypes(include='number').columns.tolist()

    # Remove excluded columns
    feature_cols = [col for col in numeric_cols if col not in exclude_cols and col != target_col]

    if target_col not in df.columns:
        raise ValueError(f"Target column '{target_col}' not found in DataFrame columns.")

    print(f"Features: {feature_cols}")
    print(f"Target: {target_col}")

    return feature_cols, target_col

def prepare_model_data(df: pd.DataFrame, feature_cols: list, target_col: str, test_size=0.2, random_state=42):
    """
    Drop rows with missing target values, and split into train/test sets.
    """
    # Drop rows where the target is missing
    df_clean = df.dropna(subset=[target_col])

    X = df_clean[feature_cols]
    y = df_clean[target_col]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )

    print(f"Training rows: {X_train.shape[0]}, Testing rows: {X_test.shape[0]}")
    return X_train, X_test, y_train, y_test

def train_and_evaluate_xgboost(X_train, X_test, y_train, y_test):
    """
    Train XGBoost on the training set and evaluate on the test set.
    """
    model = XGBRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    preds = model.predict(X_test)
    mse = mean_squared_error(y_test, preds)
    r2 = r2_score(y_test, preds)

    print(f"\nXGBoost Performance:")
    print(f"  Mean Squared Error: {mse:.2f}")
    print(f"  R² Score: {r2:.3f}")

    return model


def main():
    df = load_table_from_sqlite('enviro.db', 'emissions_vs_forests')
    # print(df.head())

    # Convert data types
    df = convert_columns_to_numeric(df, exclude_cols=['country', 'country_and_area'])

    # Split featuers, target
    feature_cols, target_col = get_feature_and_target_columns(
    df,
    target_col='co2_emissions',
    exclude_cols=['country', 'country_and_area']
)
    # print(f"Feature cols: {feature_cols}")
    # print(f"Target_column: {target_col}")

    X_train, X_test, y_train, y_test = prepare_model_data(df, feature_cols, target_col)

    model = train_and_evaluate_xgboost(X_train, X_test, y_train, y_test)


if __name__ == '__main__':
    main()