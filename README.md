# Intelligent SWP Model using Market Risk and Monte Carlo Simulation

## Project Overview

This project is an intelligent Systematic Withdrawal Plan (SWP) model designed to compare a traditional fixed withdrawal strategy with a smart market-aware withdrawal strategy. The model uses historical NIFTY 50 data, market signals, volatility analysis, inflation adjustment, Monte Carlo simulation, and K-Fold validation to support better withdrawal planning.

The project also provides a web-based dashboard where users can enter investment details and view portfolio corpus comparison, withdrawal comparison, survival probability, validation results, and future 3-month withdrawal suggestions.

## Problem Statement

Traditional SWP methods usually withdraw a fixed amount from the investment corpus without considering market conditions. During bearish markets or high volatility periods, fixed withdrawals can reduce the portfolio faster and increase the risk of corpus depletion.

This project solves the problem by building a smart SWP model that adjusts withdrawals based on market risk indicators and provides a more informed withdrawal strategy.

## Objectives

- To compare Static SWP and Smart SWP strategies.
- To use market signals and volatility for risk-aware withdrawal decisions.
- To include inflation adjustment in withdrawal planning.
- To estimate portfolio survival probability using Monte Carlo simulation.
- To validate the smart strategy using K-Fold validation.
- To provide future 3-month withdrawal suggestions from the current date.
- To present results through a professional web dashboard.

## Technologies Used

- Python
- Flask
- Pandas
- NumPy
- Scikit-learn
- Plotly
- HTML
- CSS
- JavaScript

## Dataset

The project uses historical NIFTY 50 market data.

Dataset files:

- `data/nifty50.csv`
- `data/nifty50_processed.csv`

The dataset includes market price information such as date, open price, high price, low price, close price, and volume. After preprocessing, additional columns such as returns, moving averages, volatility, and market signal are generated.

## Methodology

1. Load historical NIFTY 50 data.
2. Preprocess the dataset by cleaning data and calculating returns.
3. Generate moving averages and volatility indicators.
4. Classify market condition as Bullish or Bearish.
5. Run Static SWP strategy using fixed inflation-adjusted withdrawals.
6. Run Smart SWP strategy using market guard logic.
7. Apply Monte Carlo simulation to estimate future portfolio survival probability.
8. Use K-Fold validation to test strategy performance across different historical periods.
9. Generate future 3-month withdrawal suggestions based on the current date and latest market risk condition.
10. Display all outputs in a Flask web dashboard.

## Key Features

- Static SWP vs Smart SWP comparison
- Portfolio corpus chart
- Monthly withdrawal comparison chart
- Monte Carlo simulation summary
- Survival probability calculation
- K-Fold validation results
- Future 3-month withdrawal suggestion
- Responsive and professional web dashboard

## Smart SWP Logic

The smart withdrawal strategy adjusts withdrawals based on market risk:

- If the market signal is Bearish, withdrawal is reduced.
- If volatility is high, withdrawal is reduced further.
- If market conditions are normal, planned withdrawal continues.

This helps protect the investment corpus during risky market periods.

## Project Structure

```text
swp
├── app.py
├── requirements.txt
├── README.md
├── data
│   ├── nifty50.csv
│   ├── nifty50_processed.csv
│   ├── smart_swp_result.csv
│   └── static_swp_result.csv
├── src
│   ├── data_loader.py
│   ├── preprocessing.py
│   ├── simulation.py
│   ├── swp_logic.py
│   ├── validation.py
│   └── visualization.py
├── static
│   ├── css
│   │   └── style.css
│   └── js
│       └── script.js
└── templates
    └── index.html
```

## How to Run the Project

### 1. Clone or Download the Project

Download the project folder or clone it from GitHub.

```bash
git clone https://github.com/kairavy2025/Intelligent-SWP-Model.git
```

### 2. Open the Project Folder

```bash
cd Intelligent-SWP-Model
```

### 3. Install Required Libraries

```bash
pip install -r requirements.txt
```

### 4. Run the Flask Application

```bash
python app.py
```

### 5. Open in Browser

Open this URL:

```text
http://127.0.0.1:5000/
```

## Input Parameters

The user can enter:

- Initial corpus
- Withdrawal rate
- Inflation rate
- Monte Carlo years
- Number of simulations

## Output

The dashboard displays:

- Static final corpus
- Smart final corpus
- Survival probability
- Corpus comparison chart
- Withdrawal comparison chart
- Monte Carlo final corpus distribution
- K-Fold validation summary
- Future 3-month withdrawal recommendation

## Future Withdrawal Suggestion

The project provides a 3-month future withdrawal suggestion from the current date. The suggestion is based on:

- Current market signal
- Latest volatility condition
- Inflation-adjusted withdrawal
- Historical return assumption
- Smart SWP guard factor

This output is a decision-support suggestion and not a guaranteed financial prediction.

## Conclusion

This project shows how a traditional SWP can be improved using market-aware logic and simulation-based analysis. The Smart SWP strategy helps reduce withdrawals during risky market periods and supports better long-term corpus protection. The dashboard makes the model easy to understand and useful for project demonstration, viva, and portfolio presentation.

## Future Scope

- Add machine learning based market prediction.
- Add more asset classes such as mutual funds and index funds.
- Include user login and saved investment plans.
- Deploy the dashboard online.
- Add downloadable PDF reports.

## Author

Name: Kairavy  Anand Patel
Project Type: GTU Mini Project  
Domain: Data Science / Financial Analytics

