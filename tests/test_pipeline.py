"""Sanity tests for the ethiopia_econ pipeline.

Run with: pytest
"""
from pathlib import Path

import pandas as pd
import pytest

from ethiopia_econ.clean_merge import build_panel
from ethiopia_econ.analyze import fit_model

RAW_DIR = Path(__file__).resolve().parent.parent / "data" / "raw"


@pytest.fixture(scope="module")
def panel():
    if not RAW_DIR.exists() or not any(RAW_DIR.iterdir()):
        pytest.skip("No raw data present; run `python -m ethiopia_econ.extract` first.")
    return build_panel(RAW_DIR)


def test_panel_has_expected_columns(panel):
    assert set(["Year", "GDP_Growth", "Inflation", "Unemployment"]).issubset(panel.columns)


def test_panel_has_no_missing_values(panel):
    assert not panel.isna().any().any()


def test_panel_years_are_sorted_and_unique(panel):
    years = panel["Year"].tolist()
    assert years == sorted(years)
    assert len(years) == len(set(years))


def test_model_fits_and_reports_expected_terms(panel):
    model = fit_model(panel)
    for term in ["const", "Inflation", "Unemployment", "Year"]:
        assert term in model.params.index
    assert 0 <= model.rsquared <= 1
