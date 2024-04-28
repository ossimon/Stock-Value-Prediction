import pandas as pd
from finta import TA
import cma
import sys
import numpy as np
from sklearn import preprocessing


class Logger:
    def __init__(self, initial_data):
        self.logs = pd.DataFrame(
            [],
            columns=[
                "date",
                "stocks",
                "budget",
                "bought_stocks",
                "cost",
                "total_cost",
                "budget_after_trans",
                "stocks_after_trans",
            ],
        )
        self.logs["date"] = initial_data["date"]

    def logValue(self, index, value):
        if value.get("date") is None:
            value["date"] = self.logs["date"][index]
            self.logs.loc[index] = value
        if value.get("date") == "final-transaction":
            print("final transaction")
            # modify the last day row
            self.logs.loc[index, "stocks_after_trans"] = 0  # last day so no more stocks
            self.logs.loc[index, "bought_stocks"] = (
                self.logs.loc[index]["bought_stocks"] + value["bought_stocks"]
            )
            self.logs.loc[index, "total_cost"] = (
                self.logs.loc[index]["total_cost"] + value["total_cost"]
            )
            self.logs.loc[index, "budget_after_trans"] = value["budget_after_trans"]


seed = 0
instance = "./src/data.csv"

# read the parameters
params = {}
for i in range(1, len(sys.argv)):
    if sys.argv[i].startswith("--"):
        param = sys.argv[i][2:]
        value = sys.argv[i + 1]
        i += 1
        params[param] = value

if "instance" in params:
    instance = params["instance"]
if "seed" in params:
    seed = int(params["seed"])

# read the instance
data = pd.read_csv(instance)

# transform keys of data to lower case
data.columns = [x.lower() for x in data.columns]

# calculate technical indicators
data["SMA"] = TA.SMA(data, 14)
data["RSI"] = TA.RSI(data)
data["SMM"] = TA.SMM(data)
data["EMA"] = TA.EMA(data)
data["MOM"] = TA.MOM(data)
data["EMA"] = TA.EMA(data)
data["ROC"] = TA.ROC(data)
data["CCI"] = TA.CCI(data)
data["ATR"] = TA.ATR(data)
data["ADX"] = TA.ADX(data)
data["STOCH"] = TA.STOCH(data)
data["WILLIAMS"] = TA.WILLIAMS(data)
data["OBV"] = TA.OBV(data)
data["TRIX"] = TA.TRIX(data)

# drop columns that are not needed
og_data = data
data = data.drop(columns=["date", "open", "high", "low", "volume"])

# change nan values to 0
data = data.fillna(0)

# defragmentation data
data = data.copy()
og_data = og_data.copy()

# create new columns that are products of the original columns
original_columns = data.columns
new_columns = [data]  # we should avoid appending in loops
for col1 in original_columns:
    for col2 in original_columns:
        new_df = pd.DataFrame()
        new_df[f"{col1}_{col2}"] = data[col1] * data[col2]
        new_columns.append(new_df)
data = pd.concat(new_columns, axis=1)

# normalize data to have values between 0 and 1
# print(f'Num of columns: {len(data.columns)}')

true_cost = data["close"]
scaler = preprocessing.MinMaxScaler()
data[data.columns] = scaler.fit_transform(data[data.columns])

# print the first 5 rows of the data
# print(data.head())


# define the function to optimize
def func(x, data, true_cost, budget=1_000_000, logger=None, fee=0.01):
    stocks = 0
    for index, row in data.iterrows():
        # amount of stock to buy is the dot product of the metrics and the genotype
        amount_to_buy = int(np.dot(row, x))
        if amount_to_buy < -stocks:
            amount_to_buy = -stocks

        sign = 1 if amount_to_buy > 0 else -1
        cost = amount_to_buy * true_cost[index] * (1 + fee * sign)
        if cost > budget:
            amount_to_buy = int(budget / true_cost[index])
            cost = amount_to_buy * true_cost[index]

        if logger:
            # log the date, current stocks, stocks after buying, budget, cost
            logger.logValue(
                index,
                {
                    "stocks": stocks,
                    "budget": budget,
                    "bought_stocks": amount_to_buy,
                    "cost": true_cost[index],
                    "total_cost": cost,
                    "budget_after_trans": budget - cost,
                    "stocks_after_trans": stocks + amount_to_buy,
                },
            )

        budget -= cost
        stocks += amount_to_buy

    # sell all stock with price from last date
    cost = stocks * true_cost.iloc[-1] * (1 - fee)
    if logger:
        logger.logValue(
            len(data) - 1,
            {
                "date": "final-transaction",
                "stocks": stocks,
                "budget": budget,
                "bought_stocks": -stocks,
                "cost": true_cost.iloc[-1],
                "total_cost": cost,
                "budget_after_trans": budget + cost,
                "stocks_after_trans": 0,
            },
        )
    budget = budget + cost
    return -budget


options = {
    "CMA_active_injected": float(
        params.get("CMA_active_injected", "0")
    ),  # v weight multiplier for negative weights of injected solutions
    "CMA_cmean": 10
    ** float(params.get("CMA_cmean", "1")),  # learning rate for the mean value
    "CMA_on": float(
        params.get("CMA_on", "1")
    ),  # multiplier for all covariance matrix updates
    "CMA_rankmu": float(params.get("CMA_rankmu", "1")),  # multiplier for rank-mu update
    "CMA_rankone": float(
        params.get("CMA_rankone", "1")
    ),  # multiplier for rank-one update
    "CSA_dampfac": float(
        params.get("CSA_dampfac", "1")
    ),  # v positive multiplier for step-size damping, 0.3 is close to optimal on the sphere"
    "popsize": int(
        params.get("popsize", "100")
    ),  # population size, AKA lambda, int(popsize) is the number of new solution per iteration",
    "seed": seed,  # random number seed for `numpy.random`; `None` and `0` equate to `time`, `np.nan` means \"do nothing\", see also option \"randn\""
    "tolfun": 10
    ** float(
        params.get("tolfun", "-11")
    ),  # v termination criterion: tolerance in function value, quite useful",
    "timeout": 10,
}
# turn off stdout
sys.stdout = open(".\\null", "w")

res = cma.fmin2(
    func, np.ones(len(data.columns)), 10, options, args=(data, true_cost, 1_000_000)
)[0]

# turn on stdout
sys.stdout = sys.__stdout__

print(func(res, data, true_cost, 1_000_000), end="")

# save res to file res.csv
# np.savetxt(f'./res_{configuration_id}_{instance_id}_{seed}.csv', res, delimiter=',')

# logger = Logger(og_data)
# func(res, data, true_cost, 1_000_000, logger=logger)

# print(logger.logs)

# save logs to file logs.csv
# logger.logs.to_csv(f'./logs_{configuration_id}_{instance_id}_{seed}.csv', index=False)
