import pandas as pd
import re


# --------------------------------------------------
# Function to extract information from title_raw
# --------------------------------------------------
def extract_data_from_title(title):
    data = {
        "release_month": None,
        "release_year": None,
        "display_raw": None,
        "chipset_raw": None,
        "battery_raw": None,
        "storage_raw": None,
        "ram_raw": None
    }

    if pd.isna(title):
        return data

    t = title.lower()

    # Release date
    m = re.search(r"announced\s+([a-z]+)\s+(\d{4})", t)
    if m:
        data["release_month"] = m.group(1).capitalize()
        data["release_year"] = int(m.group(2))

    # Display size (inches)
    m = re.search(r"(\d+(?:\.\d+)?)\s*(?:\"|″)\s*display", t)
    if m:
        data["display_raw"] = float(m.group(1))

    # Chipset (robust extraction)
    m = re.search(r"features.*?,\s*([a-z0-9\s\+\-]+?)\s+chipset", t)
    if m:
        data["chipset_raw"] = m.group(1).strip().title()

    # Battery (mAh)
    m = re.search(r"(\d{3,5})\s*mah", t)
    if m:
        data["battery_raw"] = int(m.group(1))

    # Storage (GB)
    m = re.search(r"(\d+)\s*gb\s*storage", t)
    if m:
        data["storage_raw"] = int(m.group(1))

    # RAM (GB)
    m = re.search(r"(\d+)\s*gb\s*ram", t)
    if m:
        data["ram_raw"] = int(m.group(1))

    return data


# --------------------------------------------------
# Function to clean missing values using title_raw
# --------------------------------------------------
def clean_data(df_raw):

    # Ensure required columns exist BEFORE filling
    required_cols = [
        "release_month",
        "release_year",
        "display_raw",
        "chipset_raw",
        "battery_raw",
        "storage_raw",
        "ram_raw",
    ]

    for col in required_cols:
        if col not in df_raw.columns:
            df_raw[col] = None

    # Parse title_raw for EVERY row
    for idx, row in df_raw.iterrows():

        extracted_data = extract_data_from_title(row.get("title_raw"))

        for key, value in extracted_data.items():
            if pd.isna(df_raw.loc[idx, key]) and value is not None:
                df_raw.loc[idx, key] = value

    # Convert numeric columns safely
    numeric_cols = ["display_raw", "battery_raw", "storage_raw", "ram_raw", "release_year"]

    for col in numeric_cols:
        df_raw[col] = pd.to_numeric(df_raw[col], errors="coerce")

    return df_raw



def filter_only_phones(df):
    """
    Keep only real Samsung smartphones.
    Remove tablets, watches, rugged, and special devices.
    """

    exclude_keywords = ["TAB", "WATCH", "XCOVER", "QUANTUM"]

    mask = ~df["name"].str.upper().str.contains("|".join(exclude_keywords), na=False)

    return df[mask].reset_index(drop=True)


# --------------------------------------------------
# Main processing function
# --------------------------------------------------
def process_and_save_cleaned_data(raw_file, clean_file):

    # Read raw CSV
    df_raw = pd.read_csv(raw_file)

    # STEP 1 → keep only phones
    df_raw = filter_only_phones(df_raw)

    # STEP 2 → clean missing values
    df_clean = clean_data(df_raw)

    # STEP 3 → save
    df_clean.to_csv(clean_file, index=False)

    print(f"✅ Cleaned data saved to: {clean_file}")
    print("\n🔎 Remaining missing values per column:\n")
    print(df_clean.isna().sum())


# --------------------------------------------------
# Script entry point
# --------------------------------------------------
if __name__ == "__main__":
    raw_file = "data/raw/samsung_specs_raw.csv"
    clean_file = "data/processed/samsung_specs_clean.csv"

    process_and_save_cleaned_data(raw_file, clean_file)
