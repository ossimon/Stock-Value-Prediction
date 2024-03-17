# Użyte narzędzia

**CMA-ES** (Covariance Matrix Adaptation Evolution Strategy): Jest to algorytm ewolucyjny, używany do rozwiązywania problemów optymalizacji nieliniowej, które mogą być trudne do rozwiązania za pomocą tradycyjnych metod optymalizacji.

**Pycma** (https://github.com/CMA-ES/pycma): implementacja aglgorytmu CMA-ES w jeżyku python.

**Wykres OHLC** (Open High Low Close Chart): popularny wykres służacy do analizy instrumentów finansowych.

**FinTA** (https://github.com/peerchemist/finta): bibloteka służąca do obliczania wskaźników finansowych na wykresie OHLC.

**Yfinance** (https://github.com/ranaroussi/yfinance): bibloteka służąca do pobierania wykresów OHLC.



# Przykładowy skrypt do zarządzania portfelem 

```python
import yfinance as yf
from finta import TA
import cma

# download data
# DXY is index of US dollar
data = yf.download("DXY", start="2020-01-01", end="2024-01-01", auto_adjust=True)

# transform keys of data to lower case
data.columns = [x.lower() for x in data.columns]

# calculate technical indicators
data['SMA'] = TA.SMA(data, 14)
data['RSI'] = TA.RSI(data)
data['SMM'] = TA.SMM(data)
data['EMA'] = TA.EMA(data)
data['MOM'] = TA.MOM(data)

# print the minimum and maximum values of each column
for col in data.columns:
    print(f"{col} -> Min: {data[col].min()} Max: {data[col].max()}")

# simple function that based on the RSI indicator will either buy one or sell all stocks
def func(x, data, budget=1_000_000):
    stocks = 0
    for index, row in data.iterrows():
        if row['RSI'] > x[0] and budget > row['close']:
            # buy
            budget = budget - row['close']
            stocks = stocks + 1
        elif row['RSI'] < x[1] and stocks > 0:
            # sell
            budget = budget + stocks * row['close']
            stocks = 0
        else:
            pass

    # sell all stock with price from last date
    if stocks > 0:
        budget = budget + stocks * data.iloc[-1]['close']
    return -budget

# run the optimization
cma.fmin2(func, [30, 70], 10, args=(data, 1_000_000), options={'bounds': [data['RSI'].min(), data['RSI'].max()]})
```

Wyniki:
```
(3_w,6)-aCMA-ES (mu_w=2.0,w_1=63%) in dimension 2 (seed=738883, Sun Mar 17 16:28:24 2024)
Iterat #Fevals   function value  axis ratio  sigma  min&max std  t[m:s]
    1      6 -9.986133195190430e+05 1.0e+00 1.06e+01  1e+01  1e+01 0:00.0
    2     12 -9.997357091064453e+05 1.1e+00 1.20e+01  9e+00  2e+01 0:00.0
    3     18 -1.000295699584961e+06 1.7e+00 1.38e+01  9e+00  2e+01 0:00.0
   15     90 -1.000406580200195e+06 1.7e+00 5.32e+00  2e+00  3e+00 0:00.1
termination on tolflatfitness=1 (Sun Mar 17 16:28:24 2024)
final/bestever f-value = -1.000407e+06 -1.000407e+06 after 91/26 evaluations
incumbent solution: [70.00906300794219, 73.74006871447449]
std deviation: [1.6127682765902673, 3.093804252716183]
```

Jak widzimy temu prostemu algorytmowi udało się uzyskać wynik na poziomie 1 000 407.58, co oznacza, że zysk z inwestycji wyniósł 407.58.
Wynik ten jest nierealistyczny gdyż nie uwzględniamy żadnych prowizji a sam algorytm jest bardzo prosty. Powyższy przykład ma na celu pokazać w jaki sposób będziemy korzystać z wybranych przez nas narzedzi.