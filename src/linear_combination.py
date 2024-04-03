import pandas as pd
from finta import TA
import cma
import sys
import numpy as np
from sklearn import preprocessing

configuration_id = sys.argv[1]
instance_id = sys.argv[2]
seed = sys.argv[3]
# instance = sys.argv[4]
instance = '..\\irace\\Instances\\usd_pln.csv'

# read the parameters
params = {}
for i in range(5, len(sys.argv)):
    if sys.argv[i].startswith('--'):
        param = sys.argv[i][2:]
        value = sys.argv[i+1]
        i += 1
        params[param] = value

# read the instance
data = pd.read_csv(instance)

# transform keys of data to lower case
data.columns = [x.lower() for x in data.columns]

# calculate technical indicators
data['SMA'] = TA.SMA(data, 14)
data['RSI'] = TA.RSI(data)
data['SMM'] = TA.SMM(data)
data['EMA'] = TA.EMA(data)
data['MOM'] = TA.MOM(data)

# drop columns that are not needed
data = data.drop(columns=['date', 'open', 'high', 'low', 'volume', 'adj close'])

# change nan values to 0
data = data.fillna(0)

# create new columns that are products of the original columns
original_columns = data.columns
for col1 in original_columns:
    for col2 in original_columns:
        data[f"{col1}_{col2}"] = data[col1] * data[col2]

# normalize data to have values between 0 and 1
scaler = preprocessing.MinMaxScaler()
data[data.columns] = scaler.fit_transform(data[data.columns])

# print the first 5 rows of the data
print(data.head())


# define the function to optimize
def func(x, data, budget=1_000_000):
    stocks = 0
    for index, row in data.iterrows():
        # amount of stock to buy is the dot product of the metrics and the genotype
        amount_to_buy = int(np.dot(row, x))
        if amount_to_buy < -stocks:
            amount_to_buy = -stocks

        cost = amount_to_buy * row['close']
        if cost > budget:
            amount_to_buy = int(budget / row['close'])
            cost = amount_to_buy * row['close']

        budget -= cost
        stocks += amount_to_buy

    # sell all stock with price from last date
    if stocks > 0:
        budget = budget + stocks * data.iloc[-1]['close']
    return -budget

cma.fmin2(func, np.ones(len(data.columns)), 10, args=(data, 1_000_000))