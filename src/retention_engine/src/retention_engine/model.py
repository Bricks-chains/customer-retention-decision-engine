"""Leakage-aware churn modeling utilities."""

from __future__ import annotations

from typing import Any

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


def build_logistic_pipeline(frame: pd.DataFrame, target: str = "Churn Label") -> Pipeline:
    """Build a reproducible baseline pipeline from a cleaned training frame."""
    x = frame.drop(columns=[target])
    numeric = x.select_dtypes(include="number").columns.tolist()
    categorical = x.select_dtypes(exclude="number").columns.tolist()
    numeric_pipe = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler()),
    ])
    categorical_pipe = Pipeline([
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("onehot", OneHotEncoder(handle_unknown="ignore")),
    ])
    preprocess = ColumnTransformer([
        ("numeric", numeric_pipe, numeric),
        ("categorical", categorical_pipe, categorical),
    ])
    return Pipeline([
        ("preprocess", preprocess),
        ("model", LogisticRegression(max_iter=1000, class_weight="balanced")),
    ])


def evaluate_predictions(y_true: pd.Series, probabilities: Any) -> dict[str, float]:
    """Return portfolio-friendly classification metrics."""
    from sklearn.metrics import average_precision_score, roc_auc_score

    return {
        "roc_auc": float(roc_auc_score(y_true, probabilities)),
        "pr_auc": float(average_precision_score(y_true, probabilities)),
    }
