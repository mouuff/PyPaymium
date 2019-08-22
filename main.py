
import time
import paymium
from paymium import Constants

# Get your client id and secret here by creating a new application:
# https://www.paymium.com/page/developers/apps


class Controller(paymium.BaseController):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.btc_limit = 0.002
        self.buying = True

    def buy(self, price):
        amount = self.btc_limit
        print("Buying " + str(amount) + " at: " + str(price))
        self.api.buy_limit(price, amount)

    def sell(self, price):
        amount = self.api.get_user()["balance_btc"]
        print("Buying " + str(amount) + " at: " + str(price))
        self.api.buy_limit(price, amount)

    def update(self):
        ticker = self.api.get_ticker()
        bid = ticker["bid"]
        ask = ticker["ask"]
        loss = ask * Constants.TRADING_FEES + bid * Constants.TRADING_FEES
        spread = ask - bid
        potential = spread - loss
        # print(potential)
        print(ticker)
        orders = self.api.get_orders()
        if len(orders):
            print(orders)
        else:
            if self.buying:
                if potential < 10:
                    print("potential too low: " + str(potential))
                    return
                self.buy(bid + potential / 3)
                self.buying = False
            else:
                self.api.sell_limit(ask - potential / 3)
                self.buying = True


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
