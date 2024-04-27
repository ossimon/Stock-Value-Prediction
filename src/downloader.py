import yfinance as yf

ticker = "EURUSD=X"
start_date = "2020-01-01"
end_date = "2024-01-01"
file_path = f'../stock-data/{ticker}-{start_date}-{end_date}.csv'

data = yf.download(ticker, start=start_date, end=end_date, auto_adjust=True)

data.to_csv(file_path)