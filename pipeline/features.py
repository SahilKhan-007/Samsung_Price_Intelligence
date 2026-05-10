import pandas as pd
from datetime import datetime
from pathlib import Path
import re


# --------------------------------------------------
# Helper: Extract Samsung series from phone name
# --------------------------------------------------
SMARTPHONE_PATTERN = re.compile(
    r"GALAXY\s+(NOTE|[SAMFZC])(?:\s*[A-Z]*\d+|\b)",
    re.IGNORECASE
)

EXCLUDE_PATTERN = re.compile(
    r"(TAB|WATCH|BUDS|XCOVER|QUANTUM|ACTIVE)",
    re.IGNORECASE
)


def extract_series(name: str) -> str | None:
    """
    Detect Samsung smartphone series from device name.

    Valid:
        S, A, M, F, Z, C, NOTE

    Excludes:
        Tab, Watch, Buds, XCover, Quantum, Active, etc.
    """

    if pd.isna(name):
        return None

    # Remove non-phone devices first
    if EXCLUDE_PATTERN.search(name):
        return None

    match = SMARTPHONE_PATTERN.search(name)

    return match.group(1).upper() if match else None


# --------------------------------------------------
# Helper: Categorize battery capacity
# --------------------------------------------------
def categorize_battery(battery):
    """
    Create battery size category.
    """
    if pd.isna(battery):
        return None

    battery = float(battery)

    if battery <= 4000:
        return "Low"
    elif 4000 < battery <= 5000:
        return "Medium"
    else:
        return "High"


# --------------------------------------------------
# Helper: Compute simple performance score
# --------------------------------------------------
def compute_performance_score(row):
    """
    Heuristic performance score using:
    RAM + Storage + Display
    """
    ram = row.get("ram_raw")
    storage = row.get("storage_raw")
    display = row.get("display_raw")

    if pd.isna(ram) or pd.isna(storage) or pd.isna(display):
        return None

    # Simple weighted formula
    score = (ram * 2) + (storage / 128) + display
    return round(score, 2)


# --------------------------------------------------
# Main feature engineering function
# --------------------------------------------------
def create_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Generate analytical features from clean dataset.
    """

    current_year = datetime.now().year

    # 1️⃣ Samsung series
    df["series"] = df["name"].apply(extract_series)

    # 2️⃣ Device age
    df["device_age"] = current_year - df["release_year"]

    # 3️⃣ Battery category
    df["battery_category"] = df["battery_raw"].apply(categorize_battery)

    # 4️⃣ Performance score
    df["performance_score"] = df.apply(compute_performance_score, axis=1)

    return df


# --------------------------------------------------
# Main processing function
# --------------------------------------------------
def process_and_save_features(clean_file: str, feature_file: str):
    """
    Read cleaned CSV → create features → save new CSV
    """

    df_clean = pd.read_csv(clean_file)

    df_features = create_features(df_clean)

    df_features.to_csv(feature_file, index=False)

    print(f"✅ Feature dataset saved to: {feature_file}")
    print("\n📊 New columns created:")
    print(["series", "device_age", "battery_category", "performance_score"])

    print("\n🔎 Missing values after feature creation:\n")
    print(df_features.isna().sum())


# --------------------------------------------------
# Script entry point
# --------------------------------------------------
if __name__ == "__main__":
    project_root = Path(__file__).resolve().parents[1]

    clean_file = project_root / "data" / "processed" / "samsung_specs_clean.csv"
    feature_file = project_root / "data" / "processed" / "samsung_features.csv"

    process_and_save_features(clean_file, feature_file)
