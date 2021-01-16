import yfinance as yf
import datetime
import pickle
import os


def store_stock_histories(startDate: datetime.datetime,
                          endDate: datetime.datetime):
    with open(os.path.dirname(os.path.realpath(__file__)) + '/tickers_info/tickers.pickle', "rb") as f:
        tickers = pickle.load(f)

    if not os.path.exists(os.path.dirname(os.path.realpath(__file__)) + '/tickers_history'):
        os.makedirs(os.path.realpath(__file__) + '/tickers_history')

    for ticker in tickers:
        print('Fetching {}'.format(ticker))
        tickerData = yf.Ticker(ticker)
        tickerDf = tickerData.history(interval='1d', start=startDate, end=endDate)

        tickerDf.to_csv('tickers_history/{}_price.csv'.format(ticker))
