
import time
import paymium
from paymium import Constants

# Get your client id and secret here by creating a new application:
# https://www.paymium.com/page/developers/apps


class Controller(paymium.BaseController):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.btc_limit = 0.002
        self.balance_btc = None

    def buy(self, price):
        amount = self.btc_limit
        print("Buying " + str(amount) + " at: " + str(price))
        self.api.buy_limit(price, amount)

    def sell(self, price):
        amount = self.api.get_user()["balance_btc"]
        print("Selling " + str(amount) + " at: " + str(price))
        self.api.sell_limit(price, amount)

    def update(self):
        ticker = self.api.get_ticker()
        user_info = self.api.get_user()
        self.balance_btc = user_info["balance_btc"]
        bid = ticker["bid"]
        ask = ticker["ask"]
        loss = ask * Constants.TRADING_FEES + bid * Constants.TRADING_FEES
        spread = ask - bid
        potential = spread - loss
        # print(ticker)
        orders = self.api.get_orders()
        if len(orders):
            for order in orders:
                price = order["price"]
                uuid = order["uuid"]
                if order["direction"] == "buy":
                    if price < bid:
                        self.api.cancel_order(uuid)
                else:
                    if price > ask:
                        self.api.cancel_order(uuid)
        else:
            if self.balance_btc == 0:
                print("Potential: " + str(potential))
                if potential < 10:
                    print("potential too low: " + str(potential))
                    return
                self.buy(bid + potential / 2.5)
            else:
                self.sell(ask - potential / 2.5)


def main():
    p = paymium.Api()
    # print(p.get_trades(since=time.time()-1000))
    p.user_auth()
    p.refresh_token()
    print("Refreshed token")
    c = Controller(p)
    c.run()


if __name__ == "__main__":
    main()
