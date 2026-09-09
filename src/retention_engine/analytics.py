"""Business-facing churn and data-quality summaries."""

from __future__ import annotations

import pandas as pd


def data_quality_report(frame: pd.DataFrame) -> pd.DataFrame:
    """Return one row per column with missingness and cardinality checks."""
    return pd.DataFrame(
        {
            "column": frame.columns,
            "dtype": [str(dtype) for dtype in frame.dtypes],
            "missing_count": frame.isna().sum().to_numpy(),
            "missing_rate": frame.isna().mean().to_numpy(),
            "unique_count": frame.nunique(dropna=False).to_numpy(),
        }
    ).sort_values(["missing_rate", "unique_count"], ascending=[False, False])


def segment_churn_summary(
    frame: pd.DataFrame,
    segment: str,
    target: str = "Churn Label",
) -> pd.DataFrame:
    """Calculate customer count, churn rate, and average monthly charges by segment."""
    if segment not in frame or target not in frame:
        raise ValueError(f"Expected columns not found: {segment!r}, {target!r}")
    summary = (
        frame.groupby(segment, dropna=False)
        .agg(
            customers=(target, "size"),
            churn_rate=(target, "mean"),
            average_monthly_charges=("Monthly Charges", "mean"),
        )
        .reset_index()
        .sort_values("churn_rate", ascending=False)
    )
    return summary
