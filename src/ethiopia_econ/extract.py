"""Pull raw macroeconomic indicator series for Ethiopia from the World Bank API.

Usage
-----
    python -m ethiopia_econ.extract
    python -m ethiopia_econ.extract --country KEN --start 2000 --end 2024

The World Bank Indicators API (v2) returns a two-element JSON array:
``[metadata, records]``. This module fetches one series per indicator,
writes each to ``data/raw/<Indicator>.csv``, and prints a short summary.
"""
from __future__ import annotations

import argparse
import logging
from pathlib import Path

import pandas as pd
import requests

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

BASE_URL = "https://api.worldbank.org/v2/country/{country}/indicator/{code}"

# World Bank indicator codes for the series used in this project.
INDICATORS = {
    "GDP_Growth": "NY.GDP.MKTP.KD.ZG",   # GDP growth (annual %)
    "Inflation": "FP.CPI.TOTL.ZG",       # Inflation, consumer prices (annual %)
    "Unemployment": "SL.UEM.TOTL.ZS",    # Unemployment (% of total labor force)
}


def fetch_indicator(code: str, country: str = "ETH", per_page: int = 1000) -> pd.DataFrame:
    """Fetch one World Bank indicator series as a tidy (Year, Value) DataFrame.

    Raises
    ------
    requests.HTTPError
        If the API request fails.
    ValueError
        If the API returns no usable records for the given indicator/country.
    """
    url = BASE_URL.format(country=country, code=code)
    response = requests.get(url, params={"format": "json", "per_page": per_page}, timeout=30)
    response.raise_for_status()

    payload = response.json()
    if len(payload) < 2 or not payload[1]:
        raise ValueError(f"No records returned for indicator {code!r} in {country!r}")

    records = payload[1]
    df = pd.DataFrame(
        {
            "Year": [int(r["date"]) for r in records if r["value"] is not None],
            "Value": [r["value"] for r in records if r["value"] is not None],
        }
    ).sort_values("Year").reset_index(drop=True)
    return df


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--country", default="ETH", help="ISO3 country code (default: ETH)")
    parser.add_argument("--out", default="data/raw", help="Output directory (default: data/raw)")
    args = parser.parse_args()

    raw_dir = Path(args.out)
    raw_dir.mkdir(parents=True, exist_ok=True)

    for name, code in INDICATORS.items():
        logger.info("Fetching %s (%s) for %s...", name, code, args.country)
        df = fetch_indicator(code, country=args.country)
        out_path = raw_dir / f"{name}.csv"
        df.to_csv(out_path, index=False)
        logger.info("  -> wrote %d rows to %s", len(df), out_path)

    logger.info("Done. Raw series written to %s", raw_dir)


if __name__ == "__main__":
    main()
