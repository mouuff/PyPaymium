
from paymiumbot import Paymium


def main():
    p = Paymium('63ad627670dd4d6b25083e2e8454dcaf53202ddf6fcb4e4a4b42aa4e8ccbcc19',
                '7de4b1015e19590efb7c6abaf4db19170fd9884bc717bf2a8bb18c6c2863d924')
    # print(p.get_trades())
    # print(p.get_ticker())
    p.user_auth()
    p.refresh_token()
    print(p.get_user())
    p.buy(40, 1)


if __name__ == "__main__":
    main()
