
import time
import paymium

# Get your client id and secret here by creating a new application:
# https://www.paymium.com/page/developers/apps


class Controller(paymium.BaseController):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def update(self):
        print(self.api.get_ticker())


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
