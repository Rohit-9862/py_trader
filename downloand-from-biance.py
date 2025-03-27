import ccxt
import pandas as pd
import time
import os

# Initialize Binance exchange
binance = ccxt.binance()

# Define multiple trading pairs
symbols = ["BTC/USDT", "ETH/USDT", "BNB/USDT"]  # Add more as needed
timeframe = "1h"

# Define date range
since = binance.parse8601('2024-01-01T00:00:00Z')  # Start date
until = binance.parse8601('2025-03-01T00:00:00Z')  # End date

# Create directory to save data
output_dir = "2024-01-01-to-2025-03-01"
os.makedirs(output_dir, exist_ok=True)

# Loop through each symbol and download data
for symbol in symbols:
    print(f"Downloading data for {symbol}...")
    
    # Reset since timestamp for each symbol
    current_since = since  
    ohlcv = []
    
    while current_since < until:
        try:
            data = binance.fetch_ohlcv(symbol, timeframe, current_since, limit=500)
            if not data:
                break
            ohlcv.extend(data)

            # Move to the next batch
            current_since = data[-1][0] + 1

            # Avoid rate limits
            time.sleep(1)
        
        except Exception as e:
            print(f"Error fetching d ata for {symbol}: {e}")
            break

    # Convert to DataFrame and save to CSV
    df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')

    # Define file path
    token_name = symbol.replace("/", "")  # Remove special characters from filename
    file_path = os.path.join(output_dir, f"{token_name}.csv")
    
    df.to_csv(file_path, index=False)
    print(f"Saved {symbol} data to {file_path}")

print("All data downloaded successfully.")