import pickle
import pandas as pd
from datetime import datetime, timedelta
from math import floor, ceil
# from .Wallet import Wallet
# from .testing_strategy import sellingCondition, buyingCondition, getIndexes


class Wallet:

    total_money = None
    stocks_owned = {}    # {name: number of stocks}
    invested_money = None
    hourly_limit = 0.35

    def __init__(self, initial_balance):
        self.total_money = initial_balance
        self.invested_money = 0

    def buy(self, stock, amount, price):
        if self.total_money > price * amount:
            self.total_money -= price * amount
            self.invested_money += price * amount

            if stock in self.stocks_owned:
                self.stocks_owned[stock] += amount

            else:
                self.stocks_owned[stock] = amount

    def sell(self, stock, amount, price):
        if stock in self.stocks_owned:
            if self.stocks_owned[stock] >= amount:
                self.total_money += price * amount
                self.invested_money -= price * amount
                self.stocks_owned[stock] -= amount

    def get_owned_stocks(self):
        return self.stocks_owned

    def get_available_money(self):
        return self.total_money

    def get_invested_money(self):
        return self.invested_money

    def get_hourly_limit(self):
        return self.hourly_limit


def toString(s):
    return str(s)


def getIndexes(dfObj, value):
    listOfPos = []

    result = dfObj.isin([value])

    seriesObj = result.any()

    columnNames = list(seriesObj[seriesObj == True].index)

    for col in columnNames:
        rows = list(result[col][result[col] == True].index)

        for row in rows:
            listOfPos.append((row, col))

    return listOfPos


def buyingCondition(minutely_price_history: pd.DataFrame,
                    daily_price_history: pd.DataFrame,
                    current_time: datetime,
                    current_time_index: int):

    n_days = 1
    indexes = []
    while len(indexes) == 0 and n_days < 30:
        yesterday = (current_time.date() - timedelta(n_days)).__str__()
        indexes = getIndexes(daily_price_history, yesterday)
        n_days += 1

    yesterdayPrice = daily_price_history.loc[indexes[0][0], 'Low']

    currentPrice = minutely_price_history.loc[current_time_index, 'Close']

    if yesterdayPrice is not None and currentPrice <= 1.01 * yesterdayPrice:
        return True
    else:
        return False


def sellingCondition(minutely_price_history: pd.DataFrame,
                     daily_price_history: pd.DataFrame,
                     current_time: datetime,
                     current_time_index: int):

    n_days = 1
    indexes = []
    while len(indexes) == 0 and n_days < 30:
        yesterday = (current_time.date() - timedelta(n_days)).__str__()
        indexes = getIndexes(daily_price_history, yesterday)
        n_days += 1

    yesterdayPrice = daily_price_history.loc[indexes[0][0], 'Close']


    currentPrice = minutely_price_history.loc[current_time_index, 'Close']

    if yesterdayPrice is not None and currentPrice >= 1.01 * yesterdayPrice:
        return True
    else:
        return False

with open('action/stock_actions.pickle', 'rb') as file:
    activity = pickle.load(file)

# activity = [  {stock:, action:, time:}    ]
#sort activity by time
sortedActivity = sorted(activity, key=lambda k: k['time'])

with open('tickers_info/shortlisted_tickers', 'rb') as file:
    shortlist = pickle.load(file)

df_dict = {}
for ticker in shortlist:
    minutely = pd.read_csv('minutely_pricing/{}_minutely.csv'.format(ticker))
    daily = pd.read_csv('tickers_history/{}_price.csv'.format(ticker))
    df_dict[ticker] = {'minutely': minutely, 'daily': daily}
# {stock_name: }

initial_investment = 10000
wallet = Wallet(initial_investment)
available_money = wallet.get_available_money()
hourly_limit_money = available_money * wallet.get_hourly_limit()
current_price = 0
current_hour = sortedActivity[0]['time'].hour

for action in sortedActivity:
    print(action['time'])

    if action['time'].hour != current_hour:
        available_money = wallet.get_available_money()
        hourly_limit_money = available_money * wallet.get_hourly_limit()
        current_hour = action['time'].hour

    stock_df = df_dict[action['stock']]['minutely']
    current_time = getIndexes(stock_df, str(action['time']) + '-05:00')

    if len(current_time) > 0:
        current_time_index = current_time[0][0]
        currentPrice = stock_df.loc[current_time_index, 'Close']
        if action['action'] == 'buy':
            stocks_to_buy = hourly_limit_money / currentPrice / 60

            if stocks_to_buy < 1:
                stocks_to_buy = 1
            else:
                stocks_to_buy = floor(stocks_to_buy)

            wallet.buy(action['stock'], stocks_to_buy, currentPrice)
            hourly_limit_money -= stocks_to_buy * currentPrice

        elif action['action'] == 'sell':
            if action['stock'] in wallet.get_owned_stocks():
                current_amount = wallet.get_owned_stocks()[action['stock']]
                wallet.sell(action['stock'], current_amount, currentPrice)


# get market value
all_stocks = wallet.get_owned_stocks()
market_value = 0
last_minute = sortedActivity[-1]['time']
# print(all_stocks)
for stock in all_stocks:
    quantity = all_stocks[stock]
    # print(quantity)
    index = getIndexes(df_dict[stock]['minutely'], toString(last_minute) + '-05:00')[0][0]
    currentPrice = df_dict[stock]['minutely'].loc[index, 'Close']
    # print(current_price)

    market_value += quantity * currentPrice

finalAmount = market_value + wallet.get_available_money()

print("Initial Investment: {}\nFinal Market Value: {}\nProfit/Loss: {}".format(initial_investment, finalAmount, finalAmount - initial_investment))
