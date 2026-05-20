import pandas as pd
from sklearn.model_selection import KFold
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.swp_logic import run_static_swp, run_smart_swp


def validate_strategy(
    df,
    initial_corpus=1000000,
    annual_withdrawal_rate=0.04,
    annual_inflation_rate=0.06,
    folds=5
):
    df = df.sort_values("Date").reset_index(drop=True)
    kfold = KFold(n_splits=folds, shuffle=False)

    fold_results = []

    for fold_no, (_, test_index) in enumerate(kfold.split(df), start=1):
        fold_df = df.iloc[test_index].copy()

        static_result = run_static_swp(
            fold_df,
            initial_corpus=initial_corpus,
            annual_withdrawal_rate=annual_withdrawal_rate,
            annual_inflation_rate=annual_inflation_rate
        )
        smart_result = run_smart_swp(
            fold_df,
            initial_corpus=initial_corpus,
            annual_withdrawal_rate=annual_withdrawal_rate,
            annual_inflation_rate=annual_inflation_rate
        )

        static_final = static_result["Corpus"].iloc[-1]
        smart_final = smart_result["Corpus"].iloc[-1]
        improvement = ((smart_final - static_final) / static_final) * 100 if static_final > 0 else 0

        fold_results.append({
            "Fold": fold_no,
            "Start Date": fold_df["Date"].min(),
            "End Date": fold_df["Date"].max(),
            "Static Final Corpus": static_final,
            "Smart Final Corpus": smart_final,
            "Improvement (%)": improvement,
            "Smart Outperformed": smart_final > static_final
        })

    result_df = pd.DataFrame(fold_results)

    summary = {
        "Average Improvement (%)": result_df["Improvement (%)"].mean(),
        "Smart Outperformance Rate (%)": result_df["Smart Outperformed"].mean() * 100,
        "Validation Folds": folds
    }

    return summary, result_df


if __name__ == "__main__":
    data = pd.read_csv("data/nifty50_processed.csv")
    data["Date"] = pd.to_datetime(data["Date"])

    validation_summary, validation_folds = validate_strategy(data)

    print("K-Fold Validation Summary")
    print("-------------------------")
    for key, value in validation_summary.items():
        print(f"{key}: {value:.2f}")

    print("\nFold Results")
    print(validation_folds)
