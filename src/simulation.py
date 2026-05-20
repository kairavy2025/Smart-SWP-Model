import numpy as np
import pandas as pd


def monte_carlo_simulation(
    df,
    initial_corpus=1000000,
    annual_withdrawal_rate=0.04,
    annual_inflation_rate=0.06,
    years=30,
    simulations=10000
):
    daily_returns = df["Returns"].dropna()

    monthly_mean = daily_returns.mean() * 21
    monthly_std = daily_returns.std() * np.sqrt(21)

    months = years * 12
    monthly_withdrawal_start = (initial_corpus * annual_withdrawal_rate) / 12

    returns = np.random.normal(monthly_mean, monthly_std, size=(simulations, months))
    returns = np.clip(returns, -0.95, None)

    corpus = np.full(simulations, initial_corpus, dtype=float)
    survived = np.ones(simulations, dtype=bool)

    for month in range(months):
        yearly_inflation_steps = month // 12
        monthly_withdrawal = monthly_withdrawal_start * ((1 + annual_inflation_rate) ** yearly_inflation_steps)

        active = corpus > 0
        corpus[active] = corpus[active] * (1 + returns[active, month]) - monthly_withdrawal
        corpus = np.maximum(corpus, 0)
        survived &= corpus > 0

    final_corpus_values = corpus.tolist()
    survival_results = survived.tolist()

    result = {
        "Average Final Corpus": np.mean(final_corpus_values),
        "Median Final Corpus": np.median(final_corpus_values),
        "Minimum Final Corpus": np.min(final_corpus_values),
        "Maximum Final Corpus": np.max(final_corpus_values),
        "Survival Probability": np.mean(survival_results) * 100
    }

    return result, final_corpus_values


if __name__ == "__main__":
    df = pd.read_csv("data/nifty50_processed.csv")

    result, final_values = monte_carlo_simulation(df)

    print("Monte Carlo Simulation Result")
    print("-----------------------------")

    for key, value in result.items():
        if "Probability" in key:
            print(f"{key}: {value:.2f}%")
        else:
            print(f"{key}: ₹{value:,.2f}")
