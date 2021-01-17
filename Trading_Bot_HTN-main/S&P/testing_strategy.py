import pickle
import pandas as pd
from datetime import datetime, timedelta


def stringToDateTime(s):
    return datetime.strptime(str(s), '%Y-%m-%d %H:%M:%S')


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

    if yesterdayPrice is not None and currentPrice <= 0.995 * yesterdayPrice:
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

    if yesterdayPrice is not None and currentPrice >= 1.04 * yesterdayPrice:
        return True
    else:
        return False


def getStockActivity(minutely_price_history: pd.DataFrame,
                     daily_price_history: pd.DataFrame,
                     stock_ticker: str):

    activity = []
    for index in minutely_price_history.index:
        currentTime = stringToDateTime(minutely_price_history.loc[index, 'DateTimeObj'])

        if buyingCondition(minutely_price_history, daily_price_history, currentTime, index):
            activity.append({'stock': stock_ticker, 'action': 'buy', 'time': currentTime})

        elif sellingCondition(minutely_price_history, daily_price_history, currentTime, index):
            activity.append({'stock': stock_ticker, 'action': 'sell', 'time': currentTime})

    return activity # [{stock:, action:, time:}]



with open('tickers_info/shortlisted_tickers', 'rb') as file:
    shortlist = pickle.load(file)


df_dict = {}
for ticker in shortlist:
    minutely = pd.read_csv('minutely_pricing/{}_minutely.csv'.format(ticker))
    daily = pd.read_csv('tickers_history/{}_price.csv'.format(ticker))
    df_dict[ticker] = {'minutely': minutely, 'daily': daily}

allActivity = []
for ticker in df_dict.keys():
    nextArray = getStockActivity(df_dict[ticker]['minutely'], df_dict[ticker]['daily'], ticker)
    allActivity = allActivity + nextArray
    print("{} done".format(ticker))

with open('action/stock_actions.pickle', 'wb') as file:
    pickle.dump(allActivity, file)


#   [  {'stock': ticker_name, 'time': datetime, 'action': buy/sell}    ]