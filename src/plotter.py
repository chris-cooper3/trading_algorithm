import pandas as pd
import yfinance as yf

def price(ticker, period='5y', columns=['Close']):
    '''
    Returns a DataFrame of prices for a ticker from Yahoo Finance API.
    '''
    obj = yf.Ticker(ticker)
    return obj.history(period=period)[columns]

def prices(tickers, period='5y', columns=['Close']):
    '''
    Returns a DataFrame of prices for a list of tickers from Yahoo Finance API.
    Accepts both a single ticker as a string or a list of tickers.
    '''
    if isinstance(tickers, str):
        tickers = [tickers]  # Ensure the tickers are iterable if single ticker is passed
    
    combined_prices = pd.DataFrame()
    for ticker in tickers:
        ticker_prices = price(ticker, period, columns)
        ticker_prices.rename(columns={col: f"{ticker}_{col}" for col in columns}, inplace=True)
        if not ticker_prices.dropna().empty:
            combined_prices = pd.concat([combined_prices, ticker_prices], axis=1)
        else:
            print(f"{ticker} has no data!")
    return combined_prices

# Example usage
test = prices(['GBPUSD=X'], period='5y')  # Ensure ticker is correct, typically for GBP to USD it's 'GBPUSD=X'
print(test)
