"""Interactive dashboard for the Ethiopia macroeconomic panel.

Run with:
    streamlit run app/streamlit_app.py
"""
from pathlib import Path

import pandas as pd
import statsmodels.api as sm
import streamlit as st

DATA_PATH = Path("data/processed/ethiopia_economics.csv")

st.set_page_config(page_title="Ethiopia Economic Dashboard", layout="wide")
st.title("Ethiopia Economic Dashboard")
st.caption(
    "GDP growth, inflation, and unemployment, 1991-present. "
    "Source: World Bank World Development Indicators."
)

if not DATA_PATH.exists():
    st.error(
        f"Could not find {DATA_PATH}. Run `python -m ethiopia_econ.extract` "
        "then `python -m ethiopia_econ.clean_merge` to generate it."
    )
    st.stop()

df = pd.read_csv(DATA_PATH)

st.subheader("Economic Trends")
st.line_chart(df.set_index("Year"))

st.subheader("Regression: GDP growth on inflation, unemployment, and a year trend")
st.caption("Descriptive / correlational only — see README for limitations.")

X = df[["Inflation", "Unemployment", "Year"]].copy()
X["Year"] = X["Year"] - X["Year"].min()
X = sm.add_constant(X)
y = df["GDP_Growth"]
model = sm.OLS(y, X).fit(cov_type="HC1")

summary_df = pd.DataFrame(
    {
        "Coef.": model.params,
        "Std. Err. (HC1)": model.bse,
        "t": model.tvalues,
        "P>|t|": model.pvalues,
    }
)
st.table(summary_df)

col1, col2, col3 = st.columns(3)
col1.metric("R-squared", f"{model.rsquared:.3f}")
col2.metric("Adj. R-squared", f"{model.rsquared_adj:.3f}")
col3.metric("N", int(model.nobs))
