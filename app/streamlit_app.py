import streamlit as st
import pandas as pd
import statsmodels.api as sm

st.title("Ethiopia Economic Dashboard")

df = pd.read_csv("data/processed/ethiopia_economics.csv")

st.subheader("Economic Trends")
st.line_chart(df.set_index("Year"))

st.subheader("Regression Results")
X = sm.add_constant(df[["Inflation", "Unemployment"]])
y = df["GDP_Growth"]
model = sm.OLS(y, X).fit()

st.text(model.summary())


import streamlit as st
import statsmodels.api as sm
import pandas as pd

# Load data
df = pd.read_csv("data/processed/ethiopia_economics.csv")

# Regression
X = sm.add_constant(df[["Inflation", "Unemployment"]])
y = df["GDP_Growth"]
model = sm.OLS(y, X).fit()

# Convert summary to DataFrame
summary_df = pd.DataFrame({
    "Coef.": model.params,
    "Std Err": model.bse,
    "t": model.tvalues,
    "P>|t|": model.pvalues
})

st.subheader("Regression Coefficients")
st.table(summary_df)


st.write("R-squared:", model.rsquared)
st.write("Adj. R-squared:", model.rsquared_adj)
st.write("F-statistic:", model.fvalue)


st.markdown(summary_df.to_html(), unsafe_allow_html=True)
