# Customer Retention Decision Engine

An end-to-end Python portfolio project that turns telecom churn data into retention decisions. The project follows four stages: understand the business problem and data, explore churn drivers, build and evaluate a churn model, then translate scores into explainable customer actions.

## Project stages

1. **Stage 1 - Business and data foundation:** define the retention objective, data contract, leakage risks, and reproducible loading.
2. **Stage 2 - Exploratory analytics:** profile data quality and quantify churn by contract, tenure, payment method, support services, and charges.
3. **Stage 3 - Predictive modeling:** build a leakage-aware preprocessing pipeline, compare baseline models, and evaluate ROC-AUC, PR-AUC, recall, and calibration.
4. **Stage 4 - Decision engine:** combine churn probability, customer value, and intervention cost into prioritized, explainable actions.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python -m pytest
```

Place the IBM Telco Customer Churn workbook at `data/raw/Telco_customer_churn.xlsx` (the raw dataset is intentionally excluded from Git). Run the analysis notebook in `notebooks/` or use the modules in `src/retention_engine/`.

## Repository map

```text
customer-retention-decision-engine/
├── data/raw/                  # local-only input data
├── docs/stages/               # stage 1-4 decisions and findings
├── notebooks/                 # analysis narrative
├── src/retention_engine/      # production-style Python package
├── tests/                     # automated checks
├── requirements.txt
└── README.md
```

## Skills demonstrated

Python, pandas, NumPy, scikit-learn pipelines, feature engineering, model evaluation, testing, data quality, explainable decision rules, and business-focused analytics.

## Responsible use

This is a decision-support prototype, not an autonomous customer action system. Thresholds, costs, and offer policies must be reviewed with customer-success, legal, and commercial stakeholders before production use.
