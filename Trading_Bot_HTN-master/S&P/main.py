import yfinance as yf
import datetime
import pickle
import os
import pandas as pd


def stringToDateTime(s):
    return datetime.datetime.strptime(str(s)[:-6], '%Y-%m-%d %H:%M:%S')


def toString(s):
    return str(s)


def store_stock_histories(startDate: datetime.datetime,
                          endDate: datetime.datetime):

    with open(os.path.dirname(os.path.realpath(__file__)) + '/tickers_info/tickers.pickle', "rb") as f:
        tickers = pickle.load(f)

    path_dir = os.path.dirname(os.path.realpath(__file__))
    if not os.path.exists(path_dir + '/tickers_history'):
        os.makedirs(path_dir + '/tickers_history')

    allInfo = []
    for ticker in tickers:
        print('Fetching {}'.format(ticker))
        tickerData = yf.Ticker(ticker)
        tickerDf = tickerData.history(interval='1d', start=startDate, end=endDate)

        tickerDf.to_csv('tickers_history/{}_price.csv'.format(ticker))
        allInfo.append(tickerDf)

    return allInfo

def get_minutely_data(startDate: datetime.datetime,
                      endDate: datetime.datetime,
                      ticker: str):

    return yf.Ticker(ticker).history(interval='1m', start=startDate, end=endDate)


def get_last_30_days_data(tickers: list):

    path_dir = os.path.dirname(os.path.realpath(__file__))
    if not os.path.exists(path_dir + '/minutely_pricing'):
        os.makedirs(path_dir + '/minutely_pricing')

    for ticker in tickers:
        print('Fetching {}'.format(ticker))

        today = datetime.datetime.now()
        oneWeekAgo = today - datetime.timedelta(days=7)
        twoWeeksAgo = today - datetime.timedelta(days=14)
        threeWeeksAgo = today - datetime.timedelta(days=21)
        fourWeeksAgo = today - datetime.timedelta(days=28)
        lastDay = today - datetime.timedelta(days=30)

        firstPeriod = get_minutely_data(lastDay, fourWeeksAgo, ticker)
        firstWeek = get_minutely_data(fourWeeksAgo, threeWeeksAgo, ticker)
        secondWeek = get_minutely_data(threeWeeksAgo, twoWeeksAgo, ticker)
        thirdWeek = get_minutely_data(twoWeeksAgo, oneWeekAgo, ticker)
        fourthWeek = get_minutely_data(oneWeekAgo, today, ticker)

        wholeMonth = pd.concat([firstPeriod, firstWeek, secondWeek, thirdWeek, fourthWeek])
        wholeMonth['DateTimeObj'] = wholeMonth.index.map(stringToDateTime)  # datetime format for conveniency if needed
        wholeMonth['StrDateTime'] = wholeMonth.index.map(toString)  # string format for conveniency if needed

        wholeMonth.to_csv('minutely_pricing/{}_minutely.csv'.format(ticker))

    return wholeMonth

# getting price histories (daily data)
# startDate = datetime.datetime(2020, 7, 1)
# endDate = datetime.datetime(2021, 1, 15)
# store_stock_histories(startDate, endDate)


# getting minutely data
testTickers = ['AAPL', 'DSG']
get_last_30_days_data(testTickers)
