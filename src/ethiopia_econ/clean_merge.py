"""Clean and merge raw World Bank series into a single analysis-ready panel.

Reads the three raw CSVs produced by ``extract.py`` (GDP growth, inflation,
unemployment), inner-joins them on Year, drops incomplete rows, and writes
``data/processed/ethiopia_economics.csv``.

Usage
-----
    python -m ethiopia_econ.clean_merge
"""
from __future__ import annotations

import argparse
import logging
from pathlib import Path

import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

SERIES = {
    "GDP_Growth.csv": "GDP_Growth",
    "Inflation.csv": "Inflation",
    "Unemployment.csv": "Unemployment",
}


def load_series(raw_dir: Path, filename: str, column_name: str) -> pd.DataFrame:
    path = raw_dir / filename
    if not path.exists():
        raise FileNotFoundError(f"Missing raw file {path}. Run `python -m ethiopia_econ.extract` first.")
    return pd.read_csv(path).rename(columns={"Value": column_name})


def build_panel(raw_dir: Path) -> pd.DataFrame:
    frames = [load_series(raw_dir, fname, col) for fname, col in SERIES.items()]
    panel = frames[0]
    for frame in frames[1:]:
        panel = panel.merge(frame, on="Year", how="inner")
    panel = panel.sort_values("Year").dropna().reset_index(drop=True)
    return panel


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--raw", default="data/raw", help="Raw data directory (default: data/raw)")
    parser.add_argument("--out", default="data/processed", help="Output directory (default: data/processed)")
    args = parser.parse_args()

    raw_dir = Path(args.raw)
    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    panel = build_panel(raw_dir)
    out_path = out_dir / "ethiopia_economics.csv"
    panel.to_csv(out_path, index=False)
    logger.info("Wrote merged panel with %d rows (%d-%d) to %s",
                len(panel), panel["Year"].min(), panel["Year"].max(), out_path)


if __name__ == "__main__":
    main()
