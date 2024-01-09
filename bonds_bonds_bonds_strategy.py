#Algo link: https://app.composer.trade/symphony/ASni0LjBDGE7Y3R8D5MS/details
import yfinance as yf
import pandas as pd
import pandas_ta as ta

# Constants for the assets
ASSETS = ["SPY", "QQQ", "IEI", "SH", "SHV", "TLT", "PSQ", "BND", "XLK", "XLP"]

# Function to fetch historical data for a given ticker
def fetch_data(ticker, start_date, end_date):
    return yf.download(ticker, start=start_date, end=end_date)

# Function to calculate RSI
def calculate_rsi(data, window):
    return ta.rsi(data['Adj Close'], length=window)

# Function to calculate Simple Moving Average (SMA)
def calculate_sma(data, window):
    return ta.sma(data['Adj Close'], length=window)

def calculate_cumulative_return(data, window):
    return data['Adj Close'].pct_change(window).iloc[-1] * 100

# Function to decide the investment based on the provided logic
def decide_investment(data):
    investment_decision = []
     # 20d BND vs 60d SH
    if data['BND_rsi_20'] > data['SH_rsi_60']:
        if data['SPY_current_price'] > data['SPY_sma_200']:
            investment_decision.append(('XLK', 'equal_weight'))
        else:
            if data['QQQ_rsi_10'] < 30:
                investment_decision.append(('XLK', 'equal_weight'))
            else:
                investment_decision.append(('XLP', 'equal_weight'))
    else:
        if data['QQQ_rsi_10'] < 30:
            investment_decision.append(('XLK', 'equal_weight'))
        else:
            investment_decision.append(('SHV', 'equal_weight'))

    # 30d IEI vs 40d SH
    if data['IEI_rsi_30'] > data['SH_rsi_40']:
        if data['SPY_current_price'] > data['SPY_sma_200']:
            investment_decision.append(('SPY', 'equal_weight'))
        else:
            investment_decision.append(('XLP', 'equal_weight'))
    else:
        if data['QQQ_rsi_10'] < 30:
            investment_decision.append(('XLK', 'equal_weight'))
        else:
            investment_decision.append(('SH', 'equal_weight'))

    # Bond Baller
    if data['TLT_rsi_20'] > data['PSQ_rsi_20']:
        investment_decision.append(('QQQ', 'equal_weight'))
    else:
        if data['SPY_current_price'] > data['SPY_sma_200']:
            investment_decision.append(('XLP', 'equal_weight'))
        else:
            if data['QQQ_rsi_10'] < 30:
                investment_decision.append(('XLK', 'equal_weight'))
            else:
                investment_decision.append(('SH', 'equal_weight'))

    return investment_decision

# Function to get recommendations based on a specific date and dollar amount
def get_recommendations(date):
    end_date = pd.to_datetime(date)
    start_date = end_date - pd.DateOffset(months=24)

    data = {}
    for asset in ASSETS:
        df = fetch_data(asset, start_date, end_date)

        # Current Price
        data[f'{asset}_current_price'] = df.iloc[-1]['Adj Close']

        # Calculate RSI for different windows
        for window in [10, 20, 30, 40, 60]:
            data[f'{asset}_rsi_{window}'] = calculate_rsi(df, window).iloc[-1]

        # SMA - 200 days for SPY
        if asset == 'SPY':
            data['SPY_sma_200'] = calculate_sma(df, 200).iloc[-1]

    return decide_investment(data)

# Main execution block
if __name__ == "__main__":
    date_input = input("Enter a date (YYYY-MM-DD) or leave blank for today: ")

    date = pd.to_datetime(date_input) if date_input else pd.Timestamp.today()
    date = date + pd.DateOffset(days=1)  # Adjust for data availability

    recommendations = get_recommendations(date)

    for ticker, weight in recommendations:
        print(f"Invest in {ticker} with weight {weight}")
