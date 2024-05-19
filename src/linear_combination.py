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
debug_mode = False
sigma = 10
default_params = False
max_evals = 10000
timeout = 60 * 2

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
if "debug_mode" in params:
    debug_mode = bool(params["debug_mode"])
if "default_params" in params:
    print('default params')
    default_params = bool(params["default_params"])
if "sigma" in params and not default_params:
    sigma = 10 ** float(params["sigma"])

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

true_cost = data["close"]
scaler = preprocessing.MinMaxScaler()
data[data.columns] = scaler.fit_transform(data[data.columns])

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


if default_params:
    options = {
        "seed": seed,  # random number seed for `numpy.random`; `None` and `0` equate to `time`, `np.nan` means \"do nothing\", see also option \"randn\""
    "tolfun": 10
    ** float(
        params.get("tolfun", "-11")
    ),  # v termination criterion: tolerance in function value, quite useful",
    "timeout": timeout,  # v stop after timeout seconds, see also options \"tolfun\" and \"tolx\"",
    "maxfevals": int(params.get("maxfevals", max_evals)),  # v stop after maxfevals",
    # 'AdaptSigma': cma.sigma_adaptation.CMAAdaptSigmaTPA,
}
else:
    options = {
        "CMA_active_injected": float(
            params.get("CMA_active_injected", "0")
        ),  # v weight multiplier for negative weights of injected solutions
        "CMA_cmean": 10 ** float(params.get("CMA_cmean", "1")),  # learning rate for the mean value
        "CMA_on": float(
            params.get("CMA_on", "1")
        ),  # multiplier for all covariance matrix updates
        "CMA_rankmu": float(params.get("CMA_rankmu", "1")),  # multiplier for rank-mu update
        "CMA_rankone": float(
            params.get("CMA_rankone", "0.5")
        ),  # multiplier for rank-one update
        "CSA_dampfac": float(
            params.get("CSA_dampfac", "1")
        ),  # v positive multiplier for step-size damping, 0.3 is close to optimal on the sphere"
        "popsize": int(
            params.get("popsize", "100")
        ),  # population size, AKA lambda, int(popsize) is the number of new solution per iteration",
        "seed": seed,  # random number seed for `numpy.random`; `None` and `0` equate to `time`, `np.nan` means \"do nothing\", see also option \"randn\""
        "tolfun": 0,
        # 10 **
        # ** float(
        #     params.get("tolfun", "-11")
        # ),  # v termination criterion: tolerance in function value, quite useful",
        "timeout": timeout,  # v stop after timeout seconds, see also options \"tolfun\" and \"tolx\"",
        "maxfevals": int(params.get("maxfevals", max_evals)),  # v stop after maxfevals",
        # 'AdaptSigma': cma.sigma_adaptation.CMAAdaptSigmaTPA,
    }

# turn off stdout
if not debug_mode:
    sys.stdout = open("./null", "w")
    # sys.stderr = open("./null", "w")
    

res = cma.fmin2(
    func, np.ones(len(data.columns)), sigma, options, args=(data, true_cost, 1_000_000)
)[0]


# turn on stdout
if not debug_mode:
    sys.stdout = sys.__stdout__
    sys.stderr = sys.__stderr__

print(func(res, data, true_cost, 1_000_000), end="")

if debug_mode:
    logger = Logger(og_data)
    func(res, data, true_cost, 1_000_000, logger=logger)
    # save logs to file logs.csv
    file_name = instance.split('\\')[-1].split('.')[0]
    logger.logs.to_csv(f'./logs/{file_name}-{seed}-logs.csv', index=False)
