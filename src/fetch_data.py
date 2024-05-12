import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

import yfinance as yf

# Define the ticker symbol
ticker_symbol = 'BA.L'  # Example for Apple Inc.

# Fetch data using a predefined period
data = yf.download(ticker_symbol, period='5y', interval='1d')

data.to_csv("BAE_Stock_Data_5y.csv")