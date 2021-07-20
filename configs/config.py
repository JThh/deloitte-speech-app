import pandas as pd
import numpy as np

np.random.seed(1)

CURRENT_YEAR = 2021
TIME_RANGE = 5
EXPLAINABLE_TXT = ['curve', 'peak', 'Curve']

data = pd.read_csv(
    'https://raw.githubusercontent.com/plotly/datasets/master/finance-charts-apple.csv')
data.loc[:, 'Date'] = data.loc[:, 'Date'].apply(
    lambda x: str(int(x[:4])+4)+x[4:])

data.rename({'Revenue':'营收','Profits':'利润'},axis=1,inplace=True)

PEAK_TIME = data.loc[data['AAPL.High'] ==
                     data['AAPL.High'].max(), 'Date'].values[0]
PEAK_VALUE = data['AAPL.High'].max()

CATEGORIES = ["category "+str(n) for n in range(1,9)]

SALES_DATA = np.random.randn(35, 4)

# import pickle5 as pickle

# DICT_PATH = './dict.txt'
# PICKLE_PATH = './kg_base.p'

# # Dynamically increasing
# STOP_WORDS = ['a','the','report','show','me','you','for','last']

# with open(PICKLE_PATH, 'rb') as handle:
#     KGB = pickle.load(handle)
    

