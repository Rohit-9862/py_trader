import yfinance as yf
import pandas as pd

# Define the list of symbols (empty for now)
symbols = ['BTC-USD']

# Define the date range
start_date = "2024-02-01"
end_date = "2025-03-01"
interval = '1h'

# Function to fetch and clean OHLC data
def fetch(symbol):
    df = yf.download(symbol, start=start_date, end=end_date, interval= interval)
    
    # Rename columns
    df.columns = [i[0] for i in df.columns]
    
    return df

for s in symbols:
    data = fetch(s)
    #for training data i.e, 1-year-data
    data.to_csv(f"data/1-year-data/{s}.csv")
    #for testing data change the date and uncomment this line
    #data.to_csv(f"data/testing-data/{s}.csv")

  