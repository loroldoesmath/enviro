import sqlite3
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# connect to sqlite and load the data table
def load_table(db_path: str, table_name: str) -> pd.DataFrame:
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query(f"SELECT * FROM {table_name};", conn)
    conn.close()
    print(f"loaded '{table_name}' with shape {df.shape}")
    return df

# try converting all columns (except excluded ones) to numbers
def clean_data(df: pd.DataFrame, target_col: str, exclude_cols=None):
    if exclude_cols is None:
        exclude_cols = []

    for col in df.columns:
        if col not in exclude_cols:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    df = df.dropna(subset=[target_col])
    return df

# make a heatmap to show correlation between all numeric columns
def plot_correlation_matrix(df: pd.DataFrame, target_col: str):
    numeric_df = df.select_dtypes(include='number')
    corr = numeric_df.corr()

    plt.figure(figsize=(12, 10))
    sns.set(style="white")

    # draw the heatmap
    ax = sns.heatmap(
        corr,
        annot=True,
        fmt=".2f",
        cmap="rocket_r",
        linewidths=0.5,
        linecolor='gray',
        cbar_kws={"shrink": 0.8},
        square=True
    )

    plt.title("correlation matrix", fontsize=16)
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)
    plt.tight_layout()
    plt.savefig("correlation_matrix.png")
    plt.close()
    print("saved correlation heatmap to correlation_matrix.png")

    if target_col in corr.columns:
        print("\ncorrelation with target (extreme weather events):")
        print(corr[target_col].sort_values(ascending=False))


# split features and target (drop country + year)
def prepare_data(df: pd.DataFrame, target_col: str, exclude_cols=None):
    if exclude_cols is None:
        exclude_cols = []

    exclude_cols = [col for col in exclude_cols if col in df.columns]
    feature_cols = [col for col in df.select_dtypes(include='number').columns if col not in exclude_cols + [target_col]]

    X = df[feature_cols]
    y = df[target_col]

    return train_test_split(X, y, test_size=0.2, random_state=42), feature_cols

# train a model and print performance
def evaluate_model(name, model, X_train, X_test, y_train, y_test):
    model.fit(X_train, y_train)
    preds = model.predict(X_test)
    mse = mean_squared_error(y_test, preds)
    r2 = r2_score(y_test, preds)
    print(f"\n{name}:")
    print(f"  mse: {mse:.2f}")
    print(f"  r²: {r2:.3f}")
    return model

# plot feature importances (for models that support it bc apparently some don't??)
def plot_feature_importance(model, feature_cols, title, filename):
    if hasattr(model, 'feature_importances_'):
        importances = model.feature_importances_
        fi = pd.Series(importances, index=feature_cols).sort_values(ascending=True)

        plt.figure(figsize=(8, 6))
        fi.plot(kind='barh')
        plt.title(title)
        plt.xlabel("importance")
        plt.tight_layout()
        plt.savefig(filename)
        plt.close()
def debug_list_tables(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print("tables in database:", tables)
    conn.close()
# main script to tie it all together
def main():
    
    db_path = 'enviro.db'
    table_name = 'update_temperature'
    target_col = 'Extreme_Weather_Events'
    exclude_cols = ['Country', 'Year']

    df = load_table(db_path, table_name)
    df = clean_data(df, target_col, exclude_cols)

    plot_correlation_matrix(df, target_col)

    (X_train, X_test, y_train, y_test), feature_cols = prepare_data(df, target_col, exclude_cols)

    lr_model = evaluate_model("linear regression", LinearRegression(), X_train, X_test, y_train, y_test)

    rf_model = evaluate_model("random forest", RandomForestRegressor(n_estimators=100, random_state=42), X_train, X_test, y_train, y_test)
    plot_feature_importance(rf_model, feature_cols, "random forest feature importance", "rf_importance.png")

    xgb_model = evaluate_model("xgboost", XGBRegressor(n_estimators=100, random_state=42), X_train, X_test, y_train, y_test)
    plot_feature_importance(xgb_model, feature_cols, "xgboost feature importance", "xgb_importance.png")
    

if __name__ == '__main__':
    main()
