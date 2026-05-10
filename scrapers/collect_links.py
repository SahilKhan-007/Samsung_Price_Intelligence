import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
from datetime import datetime, timezone
from pathlib import Path

# ==============================
# CONFIG
# ==============================

BASE_URL = "https://www.gsmarena.com/samsung-phones-9.php"
PAGINATION_URL = "https://www.gsmarena.com/samsung-phones-f-9-0-p{}.php"

HEADERS_LIST = [
    {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0 Safari/537.36"},
    {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) Safari/605.1.15"},
    {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) Chrome/119.0 Safari/537.36"},
]

MAX_RETRIES = 3
SLEEP_RANGE = (1.5, 3.5)


# ==============================
# HELPERS
# ==============================

def get_random_headers():
    return random.choice(HEADERS_LIST)


def fetch_page(url):
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = requests.get(
                url,
                headers=get_random_headers(),
                timeout=15
            )
            status = response.status_code
            
            if status == 200:
                return response.text

            elif status == 429:
                wait_time = 30 * attempt 
                print(f"[429] Too many requests. Sleeping {wait_time}s...")
                time.sleep(wait_time)

            elif status == 404:
                print(f"[404] Page not found: {url}")
                return None

            elif status == 403:
                print(f"[403] Forbidden (possibly blocked): {url}")
                time.sleep(20)

            elif 500 <= status < 600:
                print(f"[{status}] Server error. Retrying...")
                time.sleep(10)

            else:
                print(f"[{status}] Unexpected status code for {url}")
                time.sleep(5)

        except requests.RequestException as e:
            print(f"[ERROR] Network error on attempt {attempt}: {e}")
            time.sleep(5 * attempt)

    print(f"[FAILED] Could not fetch after {MAX_RETRIES} attempts: {url}")
    return None

def parse_listing_page(html):
    """
    Parse a GSMArena listing page for phone info.
    """
    soup = BeautifulSoup(html, "lxml")
    products = []

    makers_div = soup.find("div", class_="makers")
    if not makers_div:
        return products

    items = makers_div.find_all("li")

    for item in items:
        img_tag = item.find("img")
        title = img_tag.get("title") if img_tag else None

        name = item.find("strong").text.strip()
        relative_url = item.find("a")["href"]
        full_url = "https://www.gsmarena.com/" + relative_url

        products.append({
            "name": name,
            "url": full_url,
            "brand": "Samsung",
            "platform": "GSMArena",
            "image": img_tag.get("src") if img_tag else None,
            "title_raw": title,
            "scraped_at": datetime.now(timezone.utc).isoformat()
        })

    return products


# ==============================
# MAIN
# ==============================

def collect_samsung_links(pages=5):
    all_products = []

    for page in range(1, pages + 1):
        url = BASE_URL if page == 1 else PAGINATION_URL.format(page)
        html = fetch_page(url)
        if html:
            page_products = parse_listing_page(html)
            all_products.extend(page_products)
        time.sleep(random.uniform(*SLEEP_RANGE))

    return pd.DataFrame(all_products)


if __name__ == "__main__":
    df = collect_samsung_links(pages=4)  
    project_root = Path(__file__).resolve().parents[1]
    raw_dir = project_root / "data" / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)
    df.to_csv(raw_dir / "samsung_specs_raw.csv", index=False)
    print("Done. Total:", len(df))
