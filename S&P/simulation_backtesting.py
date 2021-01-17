import pickle
import pandas as pd
from datetime import datetime, timedelta
from math import floor, ceil
import tkinter as tk

class Wallet:

    total_money = 0
    stocks_owned = {}    # {name: number of stocks}
    invested_money = 0
    hourly_limit = 0.5

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

    def sell(self, stock, price):
        if stock in self.stocks_owned:
            self.total_money += price * self.stocks_owned[stock]
            self.invested_money -= price * self.stocks_owned[stock]
            self.stocks_owned[stock] = 0

    def get_owned_stocks(self):
        return self.stocks_owned

    def get_available_money(self):
        return self.total_money

    def get_invested_money(self):
        return self.invested_money

    def get_hourly_limit(self):
        return self.hourly_limit


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

def investment(initial):
    with open('action/stock_actions.pickle', 'rb') as file:
        activity = pickle.load(file)

    # activity = [  {stock:, action:, time:}    ]
    #sort activity by time
    sortedActivity = sorted(activity, key=lambda k: k['time'])
    allBuys = []
    allSells = []


    with open('tickers_info/shortlisted_tickers', 'rb') as file:
        shortlist = pickle.load(file)

    df_dict = {}
    for ticker in shortlist:
        minutely = pd.read_csv('minutely_pricing/{}_minutely.csv'.format(ticker))
        daily = pd.read_csv('tickers_history/{}_price.csv'.format(ticker))
        df_dict[ticker] = {'minutely': minutely, 'daily': daily}
    # {stock_name: }

    initial_investment = initial
    wallet = Wallet(initial_investment)
    available_money = wallet.total_money
    print(type(available_money))
    print(type(wallet.hourly_limit))
    hourly_limit_money = float(available_money) * wallet.hourly_limit
    current_hour = sortedActivity[0]['time'].hour

    for action in sortedActivity:

        if action['time'].hour != current_hour:
            available_money = wallet.total_money
            hourly_limit_money = available_money * wallet.hourly_limit
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

                allBuys.append(
                    {'stock': action['stock'], 'time': action['time'], 'price': currentPrice, 'volume': stocks_to_buy, 'action': action['action']})

            elif action['action'] == 'sell':
                allSells.append(
                    {'stock': action['stock'], 'time': action['time'], 'price': currentPrice, 'action': action['action']})
                wallet.sell(action['stock'], currentPrice)

            print('{}: {} {} at {}'.format(action['time'], action['action'], action['stock'], currentPrice))



    # get market value
    all_stocks = wallet.get_owned_stocks()
    market_value = 0
    last_minute = sortedActivity[-1]['time']
    for stock in all_stocks:
        quantity = all_stocks[stock]
        index = getIndexes(df_dict[stock]['minutely'], str(last_minute) + '-05:00')[0][0]
        currentPrice = df_dict[stock]['minutely'].loc[index, 'Close']

        market_value += quantity * currentPrice

    finalAmount = market_value + wallet.get_available_money()

    print("Initial Investment: {}\nFinal Market Value: {}\nProfit/Loss: {}".format(initial_investment, finalAmount, finalAmount - initial_investment))

    with open('action/all_buys.pickle', 'wb') as file:
        pickle.dump(allBuys, file)

    with open('action/all_sells.pickle', 'wb') as file:
        pickle.dump(allSells, file)

    return finalAmount


root = tk.Tk()

canvas1 = tk.Canvas(root, width=400, height=300, relief='raised')
canvas1.pack()

label1 = tk.Label(root, text='Incipere')
label1.config(font=('helvetica', 14))
canvas1.create_window(200, 25, window=label1)

label2 = tk.Label(root, text='Your initial investment')
label2.config(font=('helvetica', 10))
canvas1.create_window(200, 100, window=label2)

entry1 = tk.Entry(root)
canvas1.create_window(200, 140, window=entry1)


def getSquareRoot():
    x1 = entry1.get()

    label3 = tk.Label(root, text='The final market value of your portfolio is:', font=('helvetica', 10))
    canvas1.create_window(200, 210, window=label3)

    label4 = tk.Label(root, text=str(investment(int(x1))), font=('helvetica', 10, 'bold'))
    canvas1.create_window(200, 230, window=label4)


button1 = tk.Button(text='Calculate your profit', command=getSquareRoot, bg='brown', fg='white',
                    font=('helvetica', 9, 'bold'))
canvas1.create_window(200, 180, window=button1)

root.mainloop()