import pandas as pd
import plotly.graph_objects as go


def plot_corpus_comparison(static_file, smart_file):
    static_df = pd.read_csv(static_file)
    smart_df = pd.read_csv(smart_file)

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=static_df["Date"],
        y=static_df["Corpus"],
        mode="lines",
        name="Static SWP"
    ))

    fig.add_trace(go.Scatter(
        x=smart_df["Date"],
        y=smart_df["Corpus"],
        mode="lines",
        name="Smart SWP"
    ))

    fig.update_layout(
        title="Static SWP vs Smart SWP Corpus Comparison",
        xaxis_title="Date",
        yaxis_title="Portfolio Corpus",
        template="plotly_white"
    )

    return fig


def plot_withdrawal_comparison(static_file, smart_file):
    static_df = pd.read_csv(static_file)
    smart_df = pd.read_csv(smart_file)

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=static_df["Date"],
        y=static_df["Withdrawal"],
        mode="lines",
        name="Static Withdrawal"
    ))

    fig.add_trace(go.Scatter(
        x=smart_df["Date"],
        y=smart_df["Withdrawal"],
        mode="lines",
        name="Smart Withdrawal"
    ))

    fig.update_layout(
        title="Withdrawal Comparison",
        xaxis_title="Date",
        yaxis_title="Monthly Withdrawal",
        template="plotly_white"
    )

    return fig


if __name__ == "__main__":
    corpus_fig = plot_corpus_comparison(
        "data/static_swp_result.csv",
        "data/smart_swp_result.csv"
    )

    withdrawal_fig = plot_withdrawal_comparison(
        "data/static_swp_result.csv",
        "data/smart_swp_result.csv"
    )

    corpus_fig.show()
    withdrawal_fig.show()