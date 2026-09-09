"""Lightweight monitoring summaries for scored populations."""

from __future__ import annotations

import pandas as pd


def score_monitoring_summary(
    scores: pd.Series,
    *,
    population_name: str = "current",
) -> pd.DataFrame:
    """Summarize score distribution for a repeatable monitoring report."""
    numeric = pd.to_numeric(scores, errors="coerce").dropna()
    if numeric.empty:
        raise ValueError("scores must contain at least one numeric value")
    return pd.DataFrame(
        [
            {
                "population": population_name,
                "records": int(numeric.size),
                "mean_score": float(numeric.mean()),
                "median_score": float(numeric.median()),
                "p90_score": float(numeric.quantile(0.90)),
                "high_risk_rate": float((numeric >= 0.70).mean()),
            }
        ]
    )
