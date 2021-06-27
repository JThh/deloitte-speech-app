CURRENT_YEAR = 2021
TIME_RANGE = 5
EXPLAINABLE_TXT = ['curve', 'peak']

data = pd.read_csv(
    'https://raw.githubusercontent.com/plotly/datasets/master/finance-charts-apple.csv')
data.loc[:, 'Date'] = data.loc[:, 'Date'].apply(
    lambda x: str(int(x[:4])+4)+x[4:])

PEAK_TIME = data.loc[data['AAPL.High'] ==
                     data['AAPL.High'].max(), 'Date'].values[0]
PEAK_VALUE = data['AAPL.High'].max()

CATEGORIES = ["category "+str(n) for n in range(1,9)]
