# Price Response Intelligence Engine

A Streamlit portfolio project for analysing whether **observed price reductions**
are associated with incremental e-commerce purchases.

## Current project status

The online feasibility stage passed:

- 20,000,000 events
- 139,877 products
- 15 days
- 477 >=10% price-reduction episodes
- 4.00% of analysed product-days had >=10% observed price reduction
- same-day >=5% price mixing: 1.31%

The current deployment is deliberately conservative: it presents the verified
feasibility results and does **not** invent a causal estimate.

## Run

```bash
pip install -r requirements.txt
streamlit run app.py
```

## GitHub + Streamlit Cloud

Upload the complete repository to GitHub, then select `app.py` as the main file
when deploying on Streamlit Community Cloud.

## Repository

```text
price-response-intelligence-engine/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── data/
│   ├── project_summary.csv
│   ├── event_types.csv
│   ├── reduction_distribution.csv
│   ├── daily_activity.csv
│   ├── category_results.csv
│   ├── reduction_episodes.csv
│   ├── baseline_sensitivity.csv
│   └── data_quality.csv
└── src/
    └── README.md
```

## Important methodology

The dataset records observed prices and customer behaviour but does not establish
why a price changed. Therefore the project uses the term **observed price
reduction**, not an automatic claim of promotional discount.

Final causal claims should come from fixed-effects/event-study analysis with
pre-trend and placebo checks, followed by A/B testing for business validation.
