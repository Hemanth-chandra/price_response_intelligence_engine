# Source structure

`app.py` is the Streamlit presentation layer.

The `data/` folder contains small, deployable aggregate outputs from the current
20M-event feasibility run.

The full raw REES46 files and the 20M-event product-day Parquet are intentionally
not included in GitHub.

Next analytical stage:
- treatment/control construction
- fixed effects
- event study
- pre-trend checks
- placebo tests
- confidence intervals
- category-level causal estimates
