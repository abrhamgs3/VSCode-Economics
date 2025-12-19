import pandas as pd
from pathlib import Path

RAW = Path("data/raw")
OUT = Path("data/processed")
OUT.mkdir(exist_ok=True)

gdp = pd.read_csv(RAW / "GDP_Growth.csv").rename(columns={"Value": "GDP_Growth"})
inf = pd.read_csv(RAW / "Inflation.csv").rename(columns={"Value": "Inflation"})
unemp = pd.read_csv(RAW / "Unemployment.csv").rename(columns={"Value": "Unemployment"})

df = gdp.merge(inf, on="Year").merge(unemp, on="Year")
df = df.sort_values("Year").dropna()

df.to_csv(OUT / "ethiopia_economics.csv", index=False)
print("✅ Cleaned & merged dataset saved")
