import yfinance as yf
from finta import TA
import cma

# DXY - dollar
# BTC-USD - bitcoin
data = yf.download("DXY", start="2020-01-01", end="2024-01-01", auto_adjust=True)

# transform keys of data to lower case
data.columns = [x.lower() for x in data.columns]

data["SMA"] = TA.SMA(data, 14)
data["RSI"] = TA.RSI(data)
data["SMM"] = TA.SMM(data)
data["EMA"] = TA.EMA(data)
data["MOM"] = TA.MOM(data)

# for each column in data print the min and maximum value of the column
for col in data.columns:
    print(f"{col} -> Min: {data[col].min()} Max: {data[col].max()}")


def func(x, data, budget=1_000_000):
    stocks = 0
    for index, row in data.iterrows():
        if row["RSI"] > x[0] and budget > row["close"]:
            # buy
            budget = budget - row["close"]
            stocks = stocks + 1
        elif row["RSI"] < x[1] and stocks > 0:
            # sell
            budget = budget + stocks * row["close"]
            stocks = 0
        else:
            pass

    # sell all stock with price from last date
    if stocks > 0:
        budget = budget + stocks * data.iloc[-1]["close"]
    return -budget


cma.fmin2(
    func,
    [30, 70],
    10,
    args=(data, 1_000_000),
    options={"bounds": [data["RSI"].min(), data["RSI"].max()]},
)
