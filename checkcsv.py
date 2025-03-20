import pandas as pd
import os

symbols = [ 'AUCTION','RAY','T','FLOW','ARKM','LAYER','POLYX','ETH','BTT','1INCH','RED','SOL','XRP','BTC','TRX']

path1 = 'data/1-year-data/'
path2 = 'data/testing-data/'
for i in symbols:
    x = pd.read_csv(path1+f"{i}-USD.csv")
    y = pd.read_csv(path2+f"{i}-USD.csv")
    if len(x) == 0 or len(y) == 0:
        print(i, f"x: {len(x)} y: {len(y)}")    
        os.system("rm "+path1+f"{i}-USD.csv"+" "+path2+f"{i}-USD.csv")
     