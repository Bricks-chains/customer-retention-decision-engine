# Validation result

The package was executed in the open Jupyter notebook against a 3,000-row stratified sample of the IBM Telco Customer Churn workbook.

```text
rows_cleaned: 3000
train_rows: 2400
test_rows: 600
ROC-AUC: 0.833
PR-AUC: 0.656
priority_save_count: 125
```

The validation also confirmed that `Churn Value` and `Churn Score` are excluded before modeling, preventing the perfect-score target leakage found during testing.
