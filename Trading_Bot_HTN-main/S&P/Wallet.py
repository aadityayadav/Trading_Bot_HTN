class Wallet:

    total_money = None
    stocks_owned = {}    # {name: number of stocks}
    invested_money = None
    hourly_limit = 0.1

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


wallet = Wallet(10000)
wallet.buy('AAPL', 10, 100)
print(wallet.get_owned_stocks())