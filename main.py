
import time
import paymium

# Get your client id and secret here by creating a new application:
# https://www.paymium.com/page/developers/apps


def main():
    p = paymium.Api()
    print(p.get_trades(since=time.time()-1000))
    # print(p.get_ticker())
    p.user_auth()
    p.refresh_token()
    print("Refreshed token")
    # print(p.get_user())
    #p.buy_at(40, 1)
    print(p.get_ticker())
    print(p.xrate)


if __name__ == "__main__":
    main()
