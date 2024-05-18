import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

class Stock:
    def __init__(self, ticker:str, period='5y', interval='1d', conversion_ticker=None):
        self.ticker = ticker
        self.period = period
        self.interval = interval
        self.forex_ticker = conversion_ticker
        self._stock_data = None  # Internal storage for stock data

        self.fetch_stock_data()  # Initially fetch stock data

        if self.forex_ticker:
            self.convert_to_gbp()

    def fetch_stock_data(self):
        """Fetches stock data from Yahoo Finance."""
        self._stock_data = yf.download(self.ticker, period=self.period, interval=self.interval)

    @property
    def stock_data(self):
        """Returns the stock data."""
        return self._stock_data

    @stock_data.setter
    def stock_data(self, value):
        self._stock_data = value

    def plot(self):
        """Plots the closing price of the stock along with a 6-month SMA and EMA."""
        if self.stock_data.empty:
            print(f"No data available for {self.ticker}")
            return

        # Calculate the 6-month SMA and EMA
        self.stock_data['6-Month SMA'] = self.stock_data['Adj Close'].rolling(window=120).mean()
        self.stock_data['6-Month EMA'] = self.stock_data['Adj Close'].ewm(span=120, adjust=False).mean()

        # Plotting
        plt.figure(figsize=(14, 7))
        plt.plot(self.stock_data.index, self.stock_data['Adj Close'], label='Close Price', linewidth=1)
        plt.plot(self.stock_data.index, self.stock_data['6-Month SMA'], label='6-Month SMA', color='orange', linewidth=2)
        plt.plot(self.stock_data.index, self.stock_data['6-Month EMA'], label='6-Month EMA', color='green', linewidth=2)
        plt.title(f'{self.ticker}')
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.legend()
        plt.grid(True)
        plt.show()

    def convert_to_gbp(self):
        """Converts stock prices to GBP using the daily exchange rate."""
        forex = Stock(self.forex_ticker)
        forex_data = forex.stock_data[['Close']].rename(columns={'Close': 'Forex_Close'})
        combined_data = self.stock_data.merge(forex_data, how='left', left_index=True, right_index=True)
        combined_data['Close'] = combined_data['Close'] / combined_data['Forex_Close']
        combined_data['Open'] = combined_data['Open'] / combined_data['Forex_Close']
        combined_data['High'] = combined_data['High'] / combined_data['Forex_Close']
        combined_data['Low'] = combined_data['Low'] / combined_data['Forex_Close']
        combined_data['Adj Close'] = combined_data['Adj Close'] / combined_data['Forex_Close']
        self.stock_data = combined_data  # Update stock data with converted prices
        print(self.stock_data.head())
    
    # def get_market_cap(self):
    #     info = yf.Ticker(self.ticker).fast_info
    #     marketcap = info['market_cap']
    #     df = pd.DataFrame()
    #     df = df._append({'Stock':self.ticker,'Marketcap':marketcap}, ignore_index=True)
    #     print(df)

# Usage
BAE = Stock('^GSPC', conversion_ticker='GBPUSD=X')
BAE.plots()
