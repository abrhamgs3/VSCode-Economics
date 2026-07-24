"""Fit and report a simple macro regression on the merged Ethiopia panel.

Model
-----
GDP_Growth_t = b0 + b1 * Inflation_t + b2 * Unemployment_t + b3 * Year_t + e_t

This is a descriptive, correlational regression on a short (~34-year)
national time series, using heteroskedasticity-robust (HC1) standard
errors. It is NOT a causal estimate: inflation and unemployment are
plausibly endogenous to GDP growth (reverse causality, omitted variables
such as terms-of-trade shocks, conflict, and drought), and the year trend
is included only as a crude control for common macro trends, not as an
identification strategy. See README "Limitations" for how this would be
extended with a credible identification strategy.

Usage
-----
    python -m ethiopia_econ.analyze
"""
from __future__ import annotations

import argparse
import logging
from pathlib import Path

import pandas as pd
import statsmodels.api as sm

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


def fit_model(panel: pd.DataFrame):
    X = panel[["Inflation", "Unemployment", "Year"]].copy()
    X["Year"] = X["Year"] - X["Year"].min()  # center for interpretability
    X = sm.add_constant(X)
    y = panel["GDP_Growth"]
    model = sm.OLS(y, X).fit(cov_type="HC1")
    return model


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", default="data/processed/ethiopia_economics.csv")
    parser.add_argument("--out", default="results/regression_summary.txt")
    args = parser.parse_args()

    data_path = Path(args.data)
    if not data_path.exists():
        raise FileNotFoundError(f"Missing {data_path}. Run `python -m ethiopia_econ.clean_merge` first.")

    panel = pd.read_csv(data_path)
    model = fit_model(panel)

    summary_text = str(model.summary())
    print(summary_text)

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(summary_text)
    logger.info("Wrote regression summary to %s", out_path)


if __name__ == "__main__":
    main()
