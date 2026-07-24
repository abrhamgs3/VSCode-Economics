# Ethiopia Macroeconomic Pipeline

A small, reproducible Python pipeline that pulls Ethiopia's GDP growth,
inflation, and unemployment series from the World Bank API, builds an
analysis-ready panel, and explores their relationship with a transparent
regression and an interactive dashboard.

The goal of this repository is not a novel empirical result — it is a
concrete demonstration of a reproducible applied-economics research
workflow: versioned data pull → cleaning → analysis → interactive
reporting, with tests confirming each stage does what it claims.

## Pipeline

```
World Bank API  ─▶  extract.py  ─▶  data/raw/*.csv
                                        │
                                        ▼
                                 clean_merge.py
                                        │
                                        ▼
                       data/processed/ethiopia_economics.csv
                                        │
                          ┌─────────────┴─────────────┐
                          ▼                            ▼
                     analyze.py                 app/streamlit_app.py
                (regression_summary.txt)          (interactive dashboard)
```

## Quickstart

```bash
git clone https://github.com/abrhamgs3/VSCode-Economics.git
cd VSCode-Economics
python -m venv .venv && source .venv/bin/activate
pip install -e .
pip install -r requirements.txt

python -m ethiopia_econ.extract        # pulls fresh data from the World Bank API
python -m ethiopia_econ.clean_merge    # builds data/processed/ethiopia_economics.csv
python -m ethiopia_econ.analyze        # fits the regression, writes results/regression_summary.txt

streamlit run app/streamlit_app.py     # interactive dashboard
pytest                                 # sanity tests on the pipeline
```

Raw CSVs are already committed under `data/raw/` so the pipeline runs
offline without hitting the World Bank API first.

## Results (1991–2024, N = 34)

```
GDP_Growth = 19.34 - 0.14*Inflation - 5.04*Unemployment + 0.25*Year_since_1991
```

| Term | Coef. | HC1 Std. Err. | p |
|---|---|---|---|
| Const | 19.34 | 2.78 | <0.001 |
| Inflation | -0.14 | 0.07 | 0.056 |
| Unemployment | -5.04 | 1.07 | <0.001 |
| Year trend | 0.25 | 0.10 | 0.008 |

R² = 0.45, adj. R² = 0.40. Full output in [`results/regression_summary.txt`](results/regression_summary.txt)
(regenerated each time `analyze.py` runs).

## Limitations

This is a descriptive, correlational regression on a short national time
series — not a causal estimate. Inflation and unemployment are plausibly
endogenous to GDP growth (reverse causality, and omitted shocks such as
drought, conflict, or terms-of-trade movements that move all three at
once). The year trend is included only as a crude control for common
macro trends, not as an identification strategy.

A natural extension — and the direction I'd take this next — is to
exploit a specific policy or shock with plausibly exogenous timing (for
example, a monetary policy regime change or a documented drought year) as
a difference-in-differences or event-study design, rather than relying on
the pooled OLS specification here.

## Repository layout

```
src/ethiopia_econ/   extract.py, clean_merge.py, analyze.py — the pipeline
app/                 Streamlit dashboard
tests/               pytest sanity checks on the pipeline
data/raw/            committed raw World Bank series (regenerable via extract.py)
data/processed/      merged analysis panel
notebooks/           exploratory analysis notebook
```

## Data source

World Bank World Development Indicators, via the public
[World Bank API](https://api.worldbank.org/v2/country/ETH/indicator/):
`NY.GDP.MKTP.KD.ZG` (GDP growth), `FP.CPI.TOTL.ZG` (inflation),
`SL.UEM.TOTL.ZS` (unemployment).

## License

MIT — see [LICENSE](LICENSE).
