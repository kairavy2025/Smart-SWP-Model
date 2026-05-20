import pandas as pd


def run_static_swp(
    df,
    initial_corpus=1000000,
    annual_withdrawal_rate=0.04,
    annual_inflation_rate=0.06
):
    corpus = initial_corpus
    monthly_withdrawal = (initial_corpus * annual_withdrawal_rate) / 12

    results = []

    monthly_data = df.resample("ME", on="Date").last().dropna()
    monthly_data["Monthly_Return"] = monthly_data["Close"].pct_change().fillna(0)

    for i, row in monthly_data.iterrows():
        monthly_return = row["Monthly_Return"]

        if len(results) > 0 and len(results) % 12 == 0:
            monthly_withdrawal *= (1 + annual_inflation_rate)

        corpus = corpus * (1 + monthly_return)
        withdrawal = monthly_withdrawal

        corpus -= withdrawal

        if corpus < 0:
            corpus = 0

        results.append({
            "Date": i,
            "Corpus": corpus,
            "Withdrawal": withdrawal,
            "Strategy": "Static SWP",
            "Market_Signal": row["Market_Signal"]
        })

        if corpus <= 0:
            break

    return pd.DataFrame(results)


def run_smart_swp(
    df,
    initial_corpus=1000000,
    annual_withdrawal_rate=0.04,
    annual_inflation_rate=0.06
):
    corpus = initial_corpus
    monthly_withdrawal = (initial_corpus * annual_withdrawal_rate) / 12

    results = []

    monthly_data = df.resample("ME", on="Date").last().dropna()
    monthly_data["Monthly_Return"] = monthly_data["Close"].pct_change().fillna(0)

    for i, row in monthly_data.iterrows():
        monthly_return = row["Monthly_Return"]

        if len(results) > 0 and len(results) % 12 == 0:
            monthly_withdrawal *= (1 + annual_inflation_rate)

        corpus = corpus * (1 + monthly_return)

        withdrawal = monthly_withdrawal

        # Guard logic: reduce withdrawal during bearish/high-risk markets
        if row["Market_Signal"] == "Bearish":
            withdrawal *= 0.60

        if row["Volatility20"] > df["Volatility20"].quantile(0.80):
            withdrawal *= 0.75

        corpus -= withdrawal

        if corpus < 0:
            corpus = 0

        results.append({
            "Date": i,
            "Corpus": corpus,
            "Withdrawal": withdrawal,
            "Strategy": "Smart SWP",
            "Market_Signal": row["Market_Signal"]
        })

        if corpus <= 0:
            break

    return pd.DataFrame(results)


if __name__ == "__main__":
    df = pd.read_csv("data/nifty50_processed.csv")
    df["Date"] = pd.to_datetime(df["Date"])

    static_result = run_static_swp(df)
    smart_result = run_smart_swp(df)

    static_result.to_csv("data/static_swp_result.csv", index=False)
    smart_result.to_csv("data/smart_swp_result.csv", index=False)

    print("Static SWP Result:")
    print(static_result.tail())

    print("\nSmart SWP Result:")
    print(smart_result.tail())

    print("\nSWP results saved.")