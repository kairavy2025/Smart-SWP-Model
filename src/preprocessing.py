import pandas as pd


def preprocess_data(file_path="data/nifty50.csv"):
    df = pd.read_csv(file_path)

    # Clean column names if yfinance adds extra labels
    df.columns = [str(col).strip() for col in df.columns]

    df["Date"] = pd.to_datetime(df["Date"])
    df = df.sort_values("Date")

    df = df.dropna()
    df = df.drop_duplicates()

    # Remove extreme one-day price moves using the IQR method.
    # This keeps the historical trend intact while filtering abnormal spikes.
    price_change = df["Close"].pct_change()
    q1 = price_change.quantile(0.25)
    q3 = price_change.quantile(0.75)
    iqr = q3 - q1
    lower_limit = q1 - 3 * iqr
    upper_limit = q3 + 3 * iqr
    df = df[(price_change.isna()) | ((price_change >= lower_limit) & (price_change <= upper_limit))]

    # Daily percentage return
    df["Returns"] = df["Close"].pct_change()

    # Moving averages
    df["MA50"] = df["Close"].rolling(window=50).mean()
    df["MA200"] = df["Close"].rolling(window=200).mean()

    # 20-day rolling volatility
    df["Volatility20"] = df["Returns"].rolling(window=20).std()

    # Market signal
    df["Market_Signal"] = "Bearish"
    df.loc[df["MA50"] > df["MA200"], "Market_Signal"] = "Bullish"

    df = df.dropna()

    df.to_csv("data/nifty50_processed.csv", index=False)

    return df


if __name__ == "__main__":
    processed_df = preprocess_data()

    print(processed_df.head())
    print(processed_df.tail())
    print(processed_df.shape)
    print("Processed dataset saved to data/nifty50_processed.csv")
