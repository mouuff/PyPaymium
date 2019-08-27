
import time
import paymium
from paymium import Constants

# Get your client id and secret here by creating a new application:
# https://www.paymium.com/page/developers/apps


class Controller(paymium.BaseController):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.btc_limit = 0.01  # btc to trade
        self.offer = 0.1  # EUR
        self.min_potential = 0.05/100  # min potential to start trading
        self.balance_btc = None

    def buy_all(self, price):
        amount = self.btc_limit
        print("Buying " + str(amount) + " at: " + str(price))
        self.api.buy_limit(price, amount)

    def sell_all(self, price):
        amount = self.api.get_user()["balance_btc"]
        print("Selling " + str(amount) + " at: " + str(price))
        self.api.sell_limit(price, amount)

    def update(self):
        ticker = self.api.get_ticker()
        user_info = self.api.get_user()
        balance_btc = user_info["balance_btc"]
        bid = ticker["bid"]
        ask = ticker["ask"]
        ticker_price = ticker["price"]
        spread = ask - bid
        potential = ((ask / bid) - 1) - Constants.TRADING_FEES * 2
        # print(ticker)
        orders = self.api.get_orders()
        if len(orders):
            for order in orders:
                order_price = order["price"]
                uuid = order["uuid"]
                if order["direction"] == "buy":
                    if order_price < bid or order_price > bid + self.offer:
                        self.api.cancel_order(uuid)
                        print("Cancelled buy order")
                else:
                    if order_price > ask or order_price < ask - self.offer:
                        self.api.cancel_order(uuid)
                        print("Cancelled sell order")
        else:
            if potential < self.min_potential:
                print("potential too low: " + str(potential))
                return
            print("Potential: " + str(potential))
            if balance_btc == 0:
                price = bid + self.offer
                self.buy_all(price)
            else:
                price = ask - self.offer
                self.sell_all(price)


def main():
    p = paymium.Api()
    p.user_auth()
    p.refresh_token()
    print("Refreshed token")
    c = Controller(p)
    c.run()


if __name__ == "__main__":
    main()
