import os
import pandas as pd

def load_all_csvs(folder_path):
    all_data = {}

    for root, dirs, files in os.walk(folder_path):
        print(f"🔍 Looking inside: {root}")
        for file in files:
            if file.lower().endswith('.csv'):
                full_path = os.path.join(root, file)
                try:
                    df = pd.read_csv(full_path)
                    # Preserve subfolder info relative to root folder
                    relative_path = os.path.relpath(full_path, folder_path)
                    all_data[relative_path] = df
                    print(f"✅ Loaded: {relative_path} ({len(df)} rows)")
                except Exception as e:
                    print(f"❌ Failed to read {full_path}: {e}")

    return all_data

if __name__ == "__main__":
    base_path = os.path.join(os.path.dirname(__file__), "data", "raw")
    print(f"📁 Starting scan from: {base_path}")
    dataframes = load_all_csvs(base_path)
    print(f"\n📊 TOTAL CSV FILES LOADED: {len(dataframes)}")