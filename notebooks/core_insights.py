"""Core churn insight visualizations for the Jupyter notebook."""

from pathlib import Path
import sys

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = Path(r"C:\Users\Gideon\Downloads\Telco_customer_churn.xlsx")
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from retention_engine.data import load_telco_excel  # noqa: E402


def prepare_insight_frame(path: str | Path = DATA_PATH) -> pd.DataFrame:
    """Load the workbook and add analysis-friendly churn and tenure fields."""
    data = load_telco_excel(path).copy()
    data["churn"] = data["Churn Label"].map({"Yes": 1, "No": 0})
    data["tenure_band"] = pd.cut(
        data["Tenure Months"],
        bins=[-1, 6, 12, 24, 48, 72],
        labels=["0-6", "7-12", "13-24", "25-48", "49-72"],
    )
    return data


def build_core_insights(data: pd.DataFrame) -> dict[str, pd.DataFrame]:
    """Return the four aggregates used by the dashboard."""
    return {
        "contract": data.groupby("Contract", as_index=False)["churn"].mean().sort_values("churn", ascending=False),
        "payment": data.groupby("Payment Method", as_index=False)["churn"].mean().sort_values("churn", ascending=False),
        "tenure": data.groupby("tenure_band", observed=False, as_index=False)["churn"].mean(),
        "charges": data[["Churn Label", "Monthly Charges"]].dropna(),
    }


def plot_core_insights(data: pd.DataFrame) -> tuple[plt.Figure, dict[str, pd.DataFrame]]:
    """Create and return the core-insight figure plus its source aggregates."""
    insights = build_core_insights(data)
    sns.set_theme(style="whitegrid", context="notebook")
    fig, axes = plt.subplots(2, 2, figsize=(14, 9), constrained_layout=True)

    sns.barplot(data=insights["contract"], x="churn", y="Contract", ax=axes[0, 0], color="#4472C4")
    axes[0, 0].set(title="Churn rate by contract", xlabel="Churn rate", ylabel="Contract")
    axes[0, 0].xaxis.set_major_formatter(lambda value, _: f"{value:.0%}")

    sns.barplot(data=insights["payment"], x="churn", y="Payment Method", ax=axes[0, 1], color="#ED7D31")
    axes[0, 1].set(title="Churn rate by payment method", xlabel="Churn rate", ylabel="Payment method")
    axes[0, 1].xaxis.set_major_formatter(lambda value, _: f"{value:.0%}")

    sns.barplot(data=insights["tenure"], x="tenure_band", y="churn", ax=axes[1, 0], color="#70AD47")
    axes[1, 0].set(title="Churn rate by tenure", xlabel="Tenure months", ylabel="Churn rate")
    axes[1, 0].yaxis.set_major_formatter(lambda value, _: f"{value:.0%}")

    sns.boxplot(data=insights["charges"], x="Churn Label", y="Monthly Charges", ax=axes[1, 1], color="#A5A5A5")
    axes[1, 1].set(title="Monthly charges by churn outcome", xlabel="Churn label", ylabel="Monthly charges")
    fig.suptitle("Customer retention: core churn insights", fontsize=16, fontweight="bold")
    return fig, insights


if __name__ == "__main__":
    frame = prepare_insight_frame()
    figure, summaries = plot_core_insights(frame)
    print({
        "highest_contract_churn": summaries["contract"].iloc[0].to_dict(),
        "highest_payment_churn": summaries["payment"].iloc[0].to_dict(),
        "highest_tenure_churn": summaries["tenure"].dropna().sort_values("churn", ascending=False).iloc[0].to_dict(),
    })
    plt.show()
