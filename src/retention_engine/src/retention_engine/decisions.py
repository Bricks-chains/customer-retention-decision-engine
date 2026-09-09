"""Explainable retention prioritization rules."""

from __future__ import annotations

import pandas as pd


def prioritize_retention_actions(
    customers: pd.DataFrame,
    *,
    probability_column: str = "churn_probability",
    value_column: str = "monthly_value",
    contact_cost: float = 10.0,
) -> pd.DataFrame:
    """Rank customers by expected avoidable value and assign an action tier.

    The score is intentionally transparent: probability x value minus contact cost.
    """
    required = {probability_column, value_column}
    missing = required - set(customers.columns)
    if missing:
        raise ValueError(f"Missing decision columns: {sorted(missing)}")
    result = customers.copy()
    result["expected_value_at_risk"] = result[probability_column] * result[value_column]
    result["net_retention_value"] = result["expected_value_at_risk"] - contact_cost
    result["action_tier"] = "Monitor"
    result.loc[result[probability_column] >= 0.50, "action_tier"] = "Proactive outreach"
    result.loc[(result[probability_column] >= 0.70) & (result["net_retention_value"] > 0), "action_tier"] = "Priority save"
    return result.sort_values("net_retention_value", ascending=False)
