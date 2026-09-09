"""Capacity-aware retention queue policy."""

from __future__ import annotations

import pandas as pd


def build_retention_queue(
    scored_customers: pd.DataFrame,
    *,
    max_contacts: int = 500,
    minimum_probability: float = 0.5,
) -> pd.DataFrame:
    """Return the highest-value eligible customers within contact capacity."""
    if max_contacts < 1:
        raise ValueError("max_contacts must be positive")
    required = {"churn_probability", "net_retention_value"}
    missing = required - set(scored_customers.columns)
    if missing:
        raise ValueError(f"Missing queue columns: {sorted(missing)}")
    eligible = scored_customers.loc[
        scored_customers["churn_probability"] >= minimum_probability
    ].copy()
    return eligible.sort_values("net_retention_value", ascending=False).head(max_contacts)
