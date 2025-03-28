import ccxt
import pandas as pd

# Initialize Binance exchange
binance = ccxt.binance()

# Fetch 24-hour ticker statistics
tickers = binance.fetch_tickers()

# Extract relevant data
gainers = []
for symbol, data in tickers.items():
	if symbol.endswith("/USDT"):  # Focus on USDT pairs
    		gainers.append({"symbol": symbol,"price_change": float(data["change"]) if data["change"] is not None else 0.0,"percent_change": float(data["percentage"]) if data["percentage"] is not None else 0.0,"last_price": float(data["last"]) if data["last"] is not None else 0.0,"high": float(data["high"]) if data["high"] is not None else 0.0,"low": float(data["low"]) if data["low"] is not None else 0.0,"volume": float(data["quoteVolume"]) if data["quoteVolume"] is not None else 0.0})
            # Convert to DataFrame and sort by percentage chang

df = pd.DataFrame(gainers)
df = df.sort_values(by="percent_change", ascending=False)

# Display the top 10 gainers
print(df.head(10)) 
print(df.shape)
df.to_csv("ticket info.csv")
print("save complete")