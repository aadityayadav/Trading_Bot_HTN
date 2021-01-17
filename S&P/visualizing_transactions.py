import pickle
import matplotlib.pyplot as plt

with open('action/all_buys.pickle', 'rb') as file:
    allBuys = pickle.load(file)

with open('action/all_sells.pickle', 'rb') as file:
    allSells = pickle.load(file)

with open('tickers_info/shortlisted_tickers', 'rb') as file:
    shortlist = pickle.load(file)

allStockBuys = {}   # {stock: [list of buys], ...}
for ticker in shortlist:
    allStockBuys[ticker] = []

    for buy in allBuys:
        if buy['stock'] == ticker:
            allStockBuys[ticker].append(buy)

allStockSells = {}
for ticker in shortlist:
    allStockSells[ticker] = []

    for sell in allSells:
        if sell['stock'] == ticker:
            allStockSells[ticker].append(sell)



stock_price_histories = {}
for ticker in shortlist:
    ticker_value = 0
    stock_price_histories[ticker] = [[], []]
    sum = allStockBuys[ticker] + allStockSells[ticker]
    all_actions = sorted(sum, key=lambda k: k['time'])

    for action in all_actions:

        if action['action'] == 'buy':
            ticker_value += action['volume'] * action['price']
            stock_price_histories[ticker][1].append(ticker_value)

        elif action['action'] == 'sell':
            current_history = stock_price_histories[ticker][1]
            stock_price_histories[ticker][1].append(0)
            ticker_value -= ticker_value

        stock_price_histories[ticker][0].append(action['time'])

print(stock_price_histories['KEYS'][1])

plt.style.use('seaborn-darkgrid')
palette = plt.get_cmap('Set1')

num = 0
for stock in stock_price_histories.keys():
    num += 1

    plt.subplot(3, 3,  num)

    plt.plot(stock_price_histories[stock][0], stock_price_histories[stock][1], marker='', color=palette(num), linewidth=1.9, alpha=0.9, label=stock)

    if num in range(7):
        plt.tick_params(labelbottom='off')
    if num not in [1, 4, 7]:
        plt.tick_params(labelleft='off')

    plt.title(stock, loc='left', fontsize=12, fontweight=0, color=palette(num))

plt.suptitle('Investment value of all shortlisted stocks', fontsize=13, fontweight=0, color=palette(num), style='italic', y=1.02)

plt.text(0.5, 0.02, 'Time', ha='center', va='center')
plt.text(0.06, 0.5, 'Note', ha='center', va='center', rotation='vertical')
plt.show()