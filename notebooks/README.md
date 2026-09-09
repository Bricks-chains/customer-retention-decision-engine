# Analysis notebook

Use the existing Jupyter notebook as the exploratory front end for this project. The recommended narrative is:

1. Load `data/raw/Telco_customer_churn.xlsx`.
2. Import `clean_telco_data` from `src.retention_engine.data`.
3. Profile missingness and segment churn rates.
4. Fit `build_logistic_pipeline` and record holdout metrics.
5. Pass predictions and monthly value into `prioritize_retention_actions`.

Keeping the notebook focused on the narrative while reusable logic lives in `src/` demonstrates both analysis and software-engineering discipline.
