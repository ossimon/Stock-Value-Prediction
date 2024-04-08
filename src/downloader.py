import yfinance as yf

data = yf.download("EURUSD=X", start="2023-01-01", end="2024-01-01", auto_adjust=True)
# save to csv
data.to_csv("data.csv")
