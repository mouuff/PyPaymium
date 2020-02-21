
from paymium import Constants
import paymium
import time
import logging

logging.basicConfig(level=logging.INFO)


logger = logging.getLogger(__file__)


# Get your client id and secret here by creating a new application:
# https://www.paymium.com/page/developers/apps


class Controller(paymium.BaseController):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.trading_btc = 0.01  # btc to trade
        # offer in EUR compared to highest bid or lowest ask price (used for buy_all / sell_all)
        self.offer = 0.1
        self.ticker = None
        self.user_info = None

    @property
    def bid(self):
        return float(self.ticker["bid"])

    @property
    def ask(self):
        return float(self.ticker["ask"])

    @property
    def balance_btc(self):
        return self.api.get_user()["balance_btc"]

    def buy_all(self, price):
        self.api.buy_limit(price, self.trading_btc)

    def sell_all(self, price):
        self.api.sell_limit(price, self.trading_btc)

    def sell_all_max(self):
        should_make_order = False
        orders = self.api.get_orders()
        for order in orders:
            order_price = float(order["price"])
            if order["direction"] == "sell":
                if order_price > self.ask or order_price < self.ask - self.offer:
                    self.api.cancel_order(order["uuid"])
                    should_make_order = True
        else:
            should_make_order = True
        if should_make_order:
            self.sell_all(self.ask - self.offer)

    def buy_all_max(self):
        should_make_order = False
        orders = self.api.get_orders()
        for order in orders:
            order_price = float(order["price"])
            if order["direction"] == "buy":
                if order_price < self.bid or order_price > self.bid + self.offer:
                    self.api.cancel_order(order["uuid"])
                    should_make_order = True
        else:
            should_make_order = True
        if should_make_order:
            self.buy_all(self.bid + self.offer)

    def update(self):
        self.ticker = self.api.get_ticker()
        self.user_info = self.api.get_user()
        # do whatever you want down here


def main():
    p = paymium.Api(client_id="YOUR_ID",
                    client_secret="YOUR_SECRET")
    p.user_auth()
    p.refresh_token()
    print("Refreshed token")
    c = Controller(p)
    c.run()


if __name__ == "__main__":
    main()
