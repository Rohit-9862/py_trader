import pandas as pd
import numpy as np
import ta  # panda-ta (technical analysis)
from xgboost import XGBClassifier
from sklearn.metrics import mean_absolute_error, mean_squared_error, accuracy_score


symbols = ['AUCTION','RAY','T','FIM','PEPE','FLOW','ARKM','RENER','LAYER','POLYX','ETH','BTT','1INCH','RED','SOL','XRP','BTC','TRX']
# Define paths for training and testing data
train_path = "data/1-year-data/"  # Add the actual path
test_path = "data/testing-data/"   # Add the actual path


# Function to calculate technical indicators
def add_technical_indicators(df):
    df = df.copy()

    # Moving Averages
    df["SMA_10"] = ta.trend.sma_indicator(df["Close"], window=10)
    df["EMA_10"] = ta.trend.ema_indicator(df["Close"], window=10)

    # Volatility Indicators
    df["ATR"] = ta.volatility.average_true_range(df["High"], df["Low"], df["Close"], window=14)
    df["Bollinger_Upper"], df["Bollinger_Middle"], df["Bollinger_Lower"] = ta.volatility.bollinger_hband(df["Close"], window=20), ta.volatility.bollinger_mavg(df["Close"], window=20), ta.volatility.bollinger_lband(df["Close"], window=20)

    # Momentum Indicators
    df["RSI"] = ta.momentum.rsi(df["Close"], window=14)
    df["MACD"] = ta.trend.macd(df["Close"])

    # Volume Indicator
    df["OBV"] = ta.volume.on_balance_volume(df["Close"], df["Volume"])

    # Drop NaN values generated from indicators
    df = df.dropna()
    
    return df

for i in symbols:
    # Read CSV files
    train_df = pd.read_csv(train_path+f'{i}-USD.csv')
    test_df = pd.read_csv(test_path+f"{i}-USD.csv")

    # Add indicators to datasets
    train_df = add_technical_indicators(train_df)
    test_df = add_technical_indicators(test_df)

    # Define target variable (Price increase by 3%)
    train_df["Target"] = np.where(train_df["Close"].shift(-1) >= train_df["Close"] * 1.03, 1, 0)

    # Remove the last row as it does not contain a valid target
    train_df = train_df.iloc[:-1]

    # Prepare features and target for training
    X_train = train_df.drop(columns=["Target", "Datetime"])  # Assuming 'Date' column exists
    y_train = train_df["Target"]

    # Prepare features for testing
    X_test = test_df.drop(columns=["Datetime","Target"])  # Assuming 'Date' column exists
    y_test = test_df["Target"]
    # Train XGBoost Classifier
    model = XGBClassifier(use_label_encoder=False, eval_metric='logloss')
    model.fit(X_train, y_train)

    # Make predictions
    y_pred = model.predict(X_test)

    # Calculate error metrics
    error_max = np.max(np.abs(y_test - y_pred))
    error_min = np.min(np.abs(y_test - y_pred))
    error_avg = np.mean(np.abs(y_test - y_pred))

    # Accuracy
    accuracy = accuracy_score(y_test, y_pred)

    # Print results
    print(f"Max Error: {error_max}")
    print(f"Min Error: {error_min}")
    print(f"Average Error: {error_avg}")
    print(f"Accuracy: {accuracy}")