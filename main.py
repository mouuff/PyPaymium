
import time
import paymium
from paymium import Constants

# Get your client id and secret here by creating a new application:
# https://www.paymium.com/page/developers/apps


class Controller(paymium.BaseController):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def update(self):
        ticker = self.api.get_ticker()
        bid = ticker["bid"]
        ask = ticker["ask"]
        loss = ask * Constants.TRADING_FEES + bid * Constants.TRADING_FEES
        spread = ask - bid
        potential = spread - loss
        print(spread)
        print(potential)


def main():
    p = paymium.Api()
    print(p.get_trades(since=time.time()-1000))
    # print(p.get_ticker())
    p.user_auth()
    p.refresh_token()
    print(p._token)
    print("Refreshed token")
    c = Controller(p)
    c.run()


if __name__ == "__main__":
    main()
