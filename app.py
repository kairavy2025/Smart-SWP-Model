import pandas as pd
from flask import Flask, jsonify, render_template, request

from src.swp_logic import run_static_swp, run_smart_swp
from src.simulation import monte_carlo_simulation
from src.validation import validate_strategy


app = Flask(__name__)


def format_currency(value):
    return f"₹{value:,.0f}"


def build_future_withdrawal_plan(df, initial_corpus, annual_withdrawal_rate, annual_inflation_rate, months=3):
    latest_row = df.sort_values("Date").iloc[-1]
    current_date = pd.Timestamp.today().normalize()
    latest_signal = latest_row["Market_Signal"]
    high_volatility_limit = df["Volatility20"].quantile(0.80)
    latest_volatility = latest_row["Volatility20"]

    guard_factor = 1.0
    guard_reasons = []

    if latest_signal == "Bearish":
        guard_factor *= 0.60
        guard_reasons.append("bearish market signal")

    if latest_volatility > high_volatility_limit:
        guard_factor *= 0.75
        guard_reasons.append("high volatility")

    if not guard_reasons:
        guard_reasons.append("normal market risk")

    daily_returns = df["Returns"].dropna()
    expected_monthly_return = daily_returns.mean() * 21
    base_monthly_withdrawal = (initial_corpus * annual_withdrawal_rate) / 12
    projected_corpus = initial_corpus
    plan_rows = []

    for month in range(1, months + 1):
        inflation_step = (month - 1) // 12
        static_withdrawal = base_monthly_withdrawal * ((1 + annual_inflation_rate) ** inflation_step)
        suggested_withdrawal = static_withdrawal * guard_factor
        projected_corpus = max(projected_corpus * (1 + expected_monthly_return) - suggested_withdrawal, 0)
        plan_date = current_date + pd.DateOffset(months=month)

        plan_rows.append({
            "month": month,
            "date": plan_date.strftime("%b %Y"),
            "static_withdrawal": format_currency(static_withdrawal),
            "suggested_withdrawal": format_currency(suggested_withdrawal),
            "projected_corpus": format_currency(projected_corpus)
        })

    if guard_factor < 1:
        recommendation = "Reduce withdrawal temporarily"
        risk_level = "Cautious"
    else:
        recommendation = "Continue planned withdrawal"
        risk_level = "Normal"

    return {
        "recommendation": recommendation,
        "risk_level": risk_level,
        "market_signal": latest_signal,
        "current_date": current_date.strftime("%d %b %Y"),
        "guard_factor": f"{guard_factor * 100:.0f}%",
        "reason": ", ".join(guard_reasons).capitalize(),
        "next_month_withdrawal": plan_rows[0]["suggested_withdrawal"],
        "expected_monthly_return": f"{expected_monthly_return * 100:.2f}%",
        "plan": plan_rows
    }


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/calculate", methods=["POST"])
def calculate():
    data = request.get_json()

    initial_corpus = float(data.get("initial_corpus", 1000000))
    withdrawal_rate = float(data.get("withdrawal_rate", 4)) / 100
    inflation_rate = float(data.get("inflation_rate", 6)) / 100
    years = int(data.get("years", 30))
    simulations = int(data.get("simulations", 10000))

    df = pd.read_csv("data/nifty50_processed.csv")
    df["Date"] = pd.to_datetime(df["Date"])

    static_result = run_static_swp(
        df,
        initial_corpus=initial_corpus,
        annual_withdrawal_rate=withdrawal_rate,
        annual_inflation_rate=inflation_rate
    )

    smart_result = run_smart_swp(
        df,
        initial_corpus=initial_corpus,
        annual_withdrawal_rate=withdrawal_rate,
        annual_inflation_rate=inflation_rate
    )

    mc_result, final_values = monte_carlo_simulation(
        df,
        initial_corpus=initial_corpus,
        annual_withdrawal_rate=withdrawal_rate,
        annual_inflation_rate=inflation_rate,
        years=years,
        simulations=simulations
    )

    validation_summary, validation_folds = validate_strategy(
        df,
        initial_corpus=initial_corpus,
        annual_withdrawal_rate=withdrawal_rate,
        annual_inflation_rate=inflation_rate
    )
    future_plan = build_future_withdrawal_plan(
        df,
        initial_corpus=initial_corpus,
        annual_withdrawal_rate=withdrawal_rate,
        annual_inflation_rate=inflation_rate
    )

    response = {
        "metrics": {
            "static_final_corpus": format_currency(static_result["Corpus"].iloc[-1]),
            "smart_final_corpus": format_currency(smart_result["Corpus"].iloc[-1]),
            "survival_probability": f"{mc_result['Survival Probability']:.2f}%"
        },
        "corpus_chart": {
            "static_dates": static_result["Date"].dt.strftime("%Y-%m-%d").tolist(),
            "smart_dates": smart_result["Date"].dt.strftime("%Y-%m-%d").tolist(),
            "static": static_result["Corpus"].round(2).tolist(),
            "smart": smart_result["Corpus"].round(2).tolist()
        },
        "withdrawal_chart": {
            "static_dates": static_result["Date"].dt.strftime("%Y-%m-%d").tolist(),
            "smart_dates": smart_result["Date"].dt.strftime("%Y-%m-%d").tolist(),
            "static": static_result["Withdrawal"].round(2).tolist(),
            "smart": smart_result["Withdrawal"].round(2).tolist()
        },
        "monte_carlo": {
            "average_final_corpus": format_currency(mc_result["Average Final Corpus"]),
            "median_final_corpus": format_currency(mc_result["Median Final Corpus"]),
            "minimum_final_corpus": format_currency(mc_result["Minimum Final Corpus"]),
            "maximum_final_corpus": format_currency(mc_result["Maximum Final Corpus"]),
            "survival_probability": f"{mc_result['Survival Probability']:.2f}%",
            "final_values": [round(value, 2) for value in final_values[:1000]]
        },
        "validation": {
            "average_improvement": f"{validation_summary['Average Improvement (%)']:.2f}%",
            "outperformance_rate": f"{validation_summary['Smart Outperformance Rate (%)']:.2f}%",
            "folds": int(validation_summary["Validation Folds"]),
            "fold_results": [
                {
                    "fold": int(row["Fold"]),
                    "start_date": row["Start Date"].strftime("%Y-%m-%d"),
                    "end_date": row["End Date"].strftime("%Y-%m-%d"),
                    "static_final": format_currency(row["Static Final Corpus"]),
                    "smart_final": format_currency(row["Smart Final Corpus"]),
                    "improvement": f"{row['Improvement (%)']:.2f}%"
                }
                for _, row in validation_folds.iterrows()
            ]
        },
        "future_plan": future_plan
    }

    return jsonify(response)


if __name__ == "__main__":
    app.run(debug=True)
