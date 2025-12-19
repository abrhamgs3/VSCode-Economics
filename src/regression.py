import pandas as pd
import statsmodels.api as sm

df = pd.read_csv("data/processed/ethiopia_economics.csv")

X = df[["Inflation", "Unemployment"]]
X = sm.add_constant(X)
y = df["GDP_Growth"]

model = sm.OLS(y, X).fit()
print(model.summary())
