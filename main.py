"""
Main pipeline runner for Samsung Price Intelligence
Runs full pipeline:
1. Scraping
2. Cleaning
3. Feature engineering
"""

from pathlib import Path

from scrapers.collect_links import collect_samsung_links
from scrapers.clean_data import process_and_save_cleaned_data
from pipeline.features import process_and_save_features


def run_pipeline():
    print("Starting Samsung Price Intelligence pipeline...\n")

    project_root = Path(__file__).resolve().parent

    raw_file = project_root / "data" / "raw" / "samsung_specs_raw.csv"
    clean_file = project_root / "data" / "processed" / "samsung_specs_clean.csv"
    feature_file = project_root / "data" / "processed" / "samsung_features.csv"

    # Scrape data
    print("Collecting Samsung phone data...")
    df = collect_samsung_links(pages=4)
    raw_file.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(raw_file, index=False)
    print("Raw data saved.\n")

    # Clean data
    print("Cleaning data...")
    process_and_save_cleaned_data(raw_file, clean_file)
    print("Cleaned data ready.\n")

    # Feature engineering
    print("Creating analytical features...")
    process_and_save_features(clean_file, feature_file)
    print("Feature dataset ready.\n")

    print("FULL PIPELINE COMPLETED SUCCESSFULLY!")
    print("Now open: analysis/samsung_analysis.ipynb")


if __name__ == "__main__":
    run_pipeline()
