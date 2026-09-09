"""Notebook-friendly integration check for the retention engine.

Run from Jupyter after placing the Telco workbook at the default path, or
change DATA_PATH before executing:

    %run notebooks/retention_engine_validation.py
"""

from pathlib import Path
import sys

import pandas as pd
from sklearn.model_selection import train_test_split


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = Path(r"C:\Users\Gideon\Downloads\Telco_customer_churn.xlsx")
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from retention_engine.data import clean_telco_data  # noqa: E402
from retention_engine.decisions import prioritize_retention_actions  # noqa: E402
from retention_engine.model import build_logistic_pipeline, evaluate_predictions  # noqa: E402


raw = pd.read_excel(DATA_PATH).sample(n=3000, random_state=42)
clean = clean_telco_data(raw)
assert len(clean) == 3000
assert "Churn Value" not in clean.columns
assert "Churn Score" not in clean.columns

train, test = train_test_split(
    clean,
    test_size=0.2,
    random_state=42,
    stratify=clean["Churn Label"],
)
pipeline = build_logistic_pipeline(train)
pipeline.fit(train.drop(columns=["Churn Label"]), train["Churn Label"])
probabilities = pipeline.predict_proba(test.drop(columns=["Churn Label"]))[:, 1]
metrics = evaluate_predictions(test["Churn Label"], probabilities)

decision_input = pd.DataFrame(
    {
        "customer_id": raw.loc[test.index, "CustomerID"].to_numpy(),
        "monthly_value": test["Monthly Charges"].to_numpy(),
        "churn_probability": probabilities,
    }
)
prioritized = prioritize_retention_actions(decision_input)
assert len(prioritized) == len(test)
assert prioritized["net_retention_value"].notna().all()

print(
    {
        "rows_cleaned": len(clean),
        "train_rows": len(train),
        "test_rows": len(test),
        "roc_auc": round(metrics["roc_auc"], 3),
        "pr_auc": round(metrics["pr_auc"], 3),
        "priority_save_count": int(
            (prioritized["action_tier"] == "Priority save").sum()
        ),
    }
)
