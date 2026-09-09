import pandas as pd
import pytest

from retention_engine.data import clean_telco_data
from retention_engine.decisions import prioritize_retention_actions


def test_cleaning_removes_leakage_prone_columns_and_maps_target():
    raw = pd.DataFrame({"CustomerID": ["A"], "Churn Label": ["Yes"], "Churn Score": [90], "Total Charges": ["10.5"]})
    clean = clean_telco_data(raw)
    assert "Churn Score" not in clean
    assert clean.loc[0, "Churn Label"] == 1
    assert clean.loc[0, "Total Charges"] == 10.5


def test_decision_engine_prioritizes_positive_expected_value():
    customers = pd.DataFrame({"id": ["low", "high"], "churn_probability": [0.2, 0.8], "monthly_value": [20, 100]})
    output = prioritize_retention_actions(customers)
    assert output.iloc[0]["id"] == "high"
    assert output.iloc[0]["action_tier"] == "Priority save"


def test_decision_engine_validates_schema():
    with pytest.raises(ValueError, match="Missing decision columns"):
        prioritize_retention_actions(pd.DataFrame({"id": [1]}))
