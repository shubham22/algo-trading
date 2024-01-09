#Algo link: https://app.composer.trade/symphony/Pr5DZoH4Ek7ZEsltzUBc/details
import yfinance as yf
import pandas as pd
import pandas_ta as ta

# Constants for the assets
ASSETS = ["TQQQ", "QQQ", "TECL", "SQQQ", "UVXY", "SHV"]

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
def decide_investment(data, dollar_amount):
    if data['TQQQ_current_price'] > data['TQQQ_sma_200']:
        if data['TQQQ_rsi_10'] < 49:
            if data['TQQQ_cumulative_return_1'] < -2:
                return [('SHV', dollar_amount)]
            else:
                if data['TQQQ_cumulative_return_1'] > 8.5:
                    if data['TQQQ_rsi_10'] < 31:
                        return [('TECL', dollar_amount)]
                    else:
                        return [('SQQQ', dollar_amount)]
                else:
                    return [('TQQQ', dollar_amount)]
        else:
            if data['QQQ_rsi_10'] > 80:
                return [('UVXY', dollar_amount)]
            else:
                return [('SHV', dollar_amount)]
    else:
        if data['TQQQ_rsi_10'] < 31:
            if data['TQQQ_cumulative_return_1'] < -6:
                return [('TECL', dollar_amount)]
            else:
                return [('TECL', dollar_amount)]
        else:
            return [('SHV', dollar_amount)]


# Function to get recommendations based on a specific date and dollar amount
def get_recommendations(date, dollar_amount):
    end_date = pd.to_datetime(date)
    start_date = end_date - pd.DateOffset(months=20)  # Adjust for historical data
    
    data = {}
    for asset in ASSETS:
        df = fetch_data(asset, start_date, end_date)

        # Current Price
        data[f'{asset}_current_price'] = df.iloc[-1]['Adj Close']

        # SMA - 200 days
        data[f'{asset}_sma_200'] = calculate_sma(df, 200).iloc[-1]

        # RSI - 10 days
        data[f'{asset}_rsi_10'] = calculate_rsi(df, 10).iloc[-1]

        # Cumulative Returns - 1 day
        data[f'{asset}_cumulative_return_1'] = calculate_cumulative_return(df, 1)

    return decide_investment(data, dollar_amount)

# Main execution block
if __name__ == "__main__":
    date_input = input("Enter a date (YYYY-MM-DD) or leave blank for today: ")
    dollar_amount_input = input("Enter the dollar amount: ")

    date = pd.to_datetime(date_input) if date_input else pd.Timestamp.today()
    date = date + pd.DateOffset(days=1)  # Adjust for data availability

    dollar_amount_input = float(dollar_amount_input) if dollar_amount_input else 10000

    recommendations = get_recommendations(date, dollar_amount_input)

    for ticker, amount in recommendations:
        print(f"Invest ${amount:.2f} in {ticker}")
