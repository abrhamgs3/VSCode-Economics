import pandas as pd
import numpy as np

# Ethiopian economic indicators (2010–2023)
years = list(range(2010, 2024))

data = {
    "Year": years,
    "GDP_Growth_%": [
        10.6, 11.2, 8.7, 10.3, 10.0, 9.6, 8.0,
        7.5, 6.8, 8.4, 6.1, 5.6, 5.3, 6.0
    ],
    "Inflation_%": [
        7.3, 18.1, 22.8, 8.1, 7.4, 10.4, 6.6,
        13.7, 15.8, 20.8, 26.6, 34.0, 30.2, 29.0
    ],
    "Unemployment_%": [
        2.4, 2.5, 2.4, 2.3, 2.2, 2.1, 2.0,
        1.9, 1.8, 1.9, 2.0, 2.1, 2.2, 2.3
    ]
}

df = pd.DataFrame(data)
df.to_csv("ethiopia_economic_data.csv", index=False)

print(df.head())
