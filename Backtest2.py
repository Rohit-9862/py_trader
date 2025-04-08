# -*- coding: utf-8 -*-
"""
Created on Sun Apr  6 09:48:27 2025

@author: rair1
"""

import numpy as np
import pandas as pd
import xgboost
import warnings

warnings.filterwarnings("ignore")

symbol = ['AAVE', 'ACA',   'ARKM',  'AUDIO',  'BEL',  'BNB',   'BTC', 'CETUS', 'CRV', 'CTK',  'ENS', 'ETH', 'EUR', 'EURI', 'FDUSD',   'G', 'GHST', 'HIVE', 'HMSTR', 'HOOK', 'JST', 'JUV', 'KAIA', 'LOKA',  'OG', 'PAXG', 'PROM', 'PSG', 'QUICK',  'REQ', 'SANTOS',  'SUN', 'SYS', 'TFUEL',  'TUSD', 'USDC', 'USDP',  'VIB',  'VTHO',  'ZEC', 'ZEN']
pram = ['open', 'high', 'low', 'close' ,'volume','SMA_20',
'EMA_20', 'RSI', 'MACD', 'Signal_Line', 'STD_20',
'Upper_Band', 'Lower_Band', 'High-Low', 'High-Close', 'Low-Close',
'True_Range', 'ATR_14', 'Daily_Change', 'OBV', 'Cum_Vol',
'Cum_Vol_Price', 'VWAP',  ]
target = ["fclose"]

model = {}
tt = 169
index = 1
amount = 10
profit = 0
loss = 0 

def write_(Message):
    with open(r"C:\Users\rair1\Rohit\BOT\log.log", 'a') as pen:
        pen.writelines(str(Message)+"\n")
        pen.close()

def calculate_indicators(df): 
    # Simple Moving Average (SMA) 
    df["SMA_20"] = df["close"].rolling(window=20).mean()
    
    # Exponential Moving Average (EMA)
    df["EMA_20"] = df["close"].ewm(span=20, adjust=False).mean()
    
    # Relative Strength Index (RSI)
    delta = df["close"].diff(1)
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    df["RSI"] = 100 - (100 / (1 + rs))
    
    # MACD
    df["EMA_12"] = df["close"].ewm(span=12, adjust=False).mean()
    df["EMA_26"] = df["close"].ewm(span=26, adjust=False).mean()
    df["MACD"] = df["EMA_12"] - df["EMA_26"]
    df["Signal_Line"] = df["MACD"].ewm(span=9, adjust=False).mean()
    
    # Bollinger Bands
    df["STD_20"] = df["close"].rolling(window=20).std()
    df["Upper_Band"] = df["SMA_20"] + (df["STD_20"] * 2)
    df["Lower_Band"] = df["SMA_20"] - (df["STD_20"] * 2)
    
    # Average True Range (ATR)
    df["High-Low"] = df["high"] - df["low"]
    df["High-Close"] = abs(df["high"] - df["close"].shift(1))
    df["Low-Close"] = abs(df["low"] - df["close"].shift(1))
    df["True_Range"] = df[["High-Low", "High-Close", "Low-Close"]].max(axis=1)
    df["ATR_14"] = df["True_Range"].rolling(window=14).mean()
    
    # On-Balance Volume (OBV)
    df["Daily_Change"] = df["close"].diff()
    df["OBV"] = (df["volume"] * np.sign(df["Daily_Change"])).cumsum()
    
    # Volume Weighted Average Price (VWAP)
    df["Cum_Vol"] = df["volume"].cumsum()
    df["Cum_Vol_Price"] = (df["close"] * df["volume"]).cumsum()
    df["VWAP"] = df["Cum_Vol_Price"] / df["Cum_Vol"]
    df["fclose"] = df["close"].shift(-1)
    df["pclose"] = df["close"].shift(1)
    # Target Variable (Price increase by 3% next day)
    #df["Target"] = np.where(df["close"].shift(-1) >= df["close"] * 1.005, 1, 0)
    
    return df


print("STEP 1: Model Trading Session")
for i in symbol:
    train = pd.read_csv(r"C:\Users\rair1\Rohit\BOT\2024-01-01-to-2025-03-01"+f"\\{i}.csv")
    # test = pd.read_csv(r"C:\Users\rair1\Rohit\BOT\2025-03-01-to-2025-03-25"+f"\\{i}.csv")
    # train = pd.concat([train[['open', 'high', 'low', 'close' ,'volume']], test[['open', 'high', 'low', 'close' ,'volume']]])
    train = calculate_indicators(train)
    train = train.iloc[30:-1]
    model[i] = xgboost.XGBRegressor(n_estimators=300, random_state=52, learning_rate=0.2, predictor= "gpu_predictor").fit(train[pram], train[target])

result = {}
while index < tt:
    try:
        mem = {}
        for i in symbol:
            test = pd.read_csv(r"C:\Users\rair1\Rohit\BOT\2025-03-01-to-2025-03-25"+f"\\{i}.csv")
            test = calculate_indicators(test)
            test = test.iloc[20:-1]
            test_ = test.copy()
            test = pd.DataFrame(test[pram].iloc[index], dtype=float).T
            
            pred = model[i].predict(test)
            
            pred = float(pred)
            
            close = float(test[["close"]].to_numpy())
            
            if pred > float(test["close"].to_numpy()):
                mem[i] = (pred - float(test["close"].to_numpy()))/pred
        
        
        print("Trading in ", index)
        sym = 0
        if len(list(mem.values())) >= 3:
            _c = list(mem.values())
            oglist = _c
            _c.sort()
            sym = list(mem.keys())[oglist.index(_c[-1])]
        print("Reading data")
        test = pd.read_csv(r"C:\Users\rair1\Rohit\BOT\2025-03-01-to-2025-03-25"+f"\\{sym}.csv")
        test = calculate_indicators(test)
        test = test.iloc[20:-1]
        test_ = test.copy()
        test = pd.DataFrame(test[pram].iloc[index], dtype=float).T
        
        close = float(test[["close"]].to_numpy())
        future_close = float(test_[["close"]].iloc[index+1].to_numpy())
        
        share = amount/close
        gain = share*(future_close-close)
        if gain>=0:
            profit += gain
        elif gain <0:
            loss += gain
            
        #amount = gain+amount
        print(f"Info\nshares: {share}\nOpening price: {close}\nClosing Price: {future_close}")
        print(f"Total gain: {gain}")
        
     
        index += 1
        print("-"*12, "\n")
    except Exception as e:
        print("[ERROR]")
        print('\n'+str(e)+'\n')
        break
        
print(f"Total profit: {profit}\nTotal loss: {loss}")
print("Total amount:", amount)
