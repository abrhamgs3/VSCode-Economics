import requests
import pandas as pd
from pathlib import Path

BASE_URL = "https://api.worldbank.org/v2/country/ETH/indicator/"
INDICATORS = {
    "GDP_Growth": "NY.GDP.MKTP.KD.ZG",
    "Inflation": "FP.CPI.TOTL.ZG",
    "Unemployment": "SL.UEM.TOTL.ZS"
}

RAW_DIR = Path("data/raw")
RAW_DIR.mkdir(parents=True, exist_ok=True)

def fetch_indicator(code):
    url = f"{BASE_URL}{code}?format=json&per_page=100"
    data = requests.get(url).json()[1]
    return pd.DataFrame({
        "Year": [int(x["date"]) for x in data if x["value"] is not None],
        "Value": [x["value"] for x in data if x["value"] is not None]
    })

for name, code in INDICATORS.items():
    df = fetch_indicator(code)
    df.to_csv(RAW_DIR / f"{name}.csv", index=False)

print("✅ Raw World Bank data extracted")
