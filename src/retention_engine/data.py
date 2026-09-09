"""Data loading and quality transformations for the telco churn dataset."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

import pandas as pd


TARGET = "Churn Label"


def load_telco_excel(path: str | Path) -> pd.DataFrame:
    """Load the IBM Telco Customer Churn workbook."""
    return pd.read_excel(path)


def clean_telco_data(
    frame: pd.DataFrame,
    *,
    drop_columns: Iterable[str] = ("CustomerID", "Count", "Churn Score", "CLTV", "Churn Reason"),
) -> pd.DataFrame:
    """Return a modeling-ready copy with normalized missing values and labels.

    Churn Score and CLTV are excluded by default because they are derived business
    scores that can introduce target leakage into a new model.
    """
    data = frame.copy()
    data.columns = [str(column).strip() for column in data.columns]
    data = data.drop(columns=[c for c in drop_columns if c in data.columns])
    if TARGET in data:
        data[TARGET] = data[TARGET].map({"Yes": 1, "No": 0}).astype("Int64")
    if "Total Charges" in data:
        data["Total Charges"] = pd.to_numeric(data["Total Charges"], errors="coerce")
    return data
