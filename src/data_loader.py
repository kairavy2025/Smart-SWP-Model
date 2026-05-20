import pandas as pd


def load_nifty_data(file_path="data/nifty50.csv"):
    """
    Load the Kaggle Nifty 50 historical dataset used by the project.
    The project CSV is normalized to: Date, Open, High, Low, Close, Volume.
    """
    data = pd.read_csv(file_path)

    required_columns = ["Date", "Open", "High", "Low", "Close", "Volume"]
    missing_columns = [column for column in required_columns if column not in data.columns]

    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

    data = data[required_columns]
    data["Date"] = pd.to_datetime(data["Date"])
    data = data.sort_values("Date").reset_index(drop=True)

    return data


if __name__ == "__main__":
    df = load_nifty_data()

    print(df.head())
    print(df.tail())
    print(df.shape)
    print("Dataset loaded from data/nifty50.csv")
