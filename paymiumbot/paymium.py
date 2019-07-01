import requests
import json
import sys

authorize_url = "https://www.paymium.com/api/oauth/authorize?client_id=63ad627670dd4d6b25083e2e8454dcaf53202ddf6fcb4e4a4b42aa4e8ccbcc19&redirect_uri=https%3A%2F%2Fwww.paymium.com%2Fpage%2Foauth%2Ftest&response_type=code"
token_url = "https://paymium.com/api/oauth/token"
redirect_uri = "https://www.paymium.com/page/oauth/test"

client_id = '63ad627670dd4d6b25083e2e8454dcaf53202ddf6fcb4e4a4b42aa4e8ccbcc19'
client_secret = '7de4b1015e19590efb7c6abaf4db19170fd9884bc717bf2a8bb18c6c2863d924'


def _assert_headers_ok(resp):
    if resp.headers["Status"] != "200 OK":
        raise AssertionError('Status != 200 OK : ' + str(resp.headers))


class Paymium:
    def __init__(self):
        self.token = None

    def post(self, url, data, assert_ok=True):
        resp = requests.post(url, data=data, verify=False,
                             allow_redirects=False, auth=(client_id, client_secret))
        if assert_ok:
            _assert_headers_ok(resp)
        return resp

    def get_token(self, code):
        data = {
            "grant_type": 'authorization_code',
            "redirect_uri": redirect_uri,
            "code": code
        }
        access_token_response = self.post(token_url, data)

        self.token = json.loads(access_token_response.text)
        '''body = {"access_token": "xxx", "token_type": "bearer", "expires_in": 1800,
           "refresh_token": "xxx", "scope": "basic", "created_at": 1561993742}
        '''

    def refresh_token(self):
        data = {
            "grant_type": 'refresh_token',
            "redirect_uri": redirect_uri,
            "refresh_token": self.token["refresh_token"]
        }
        refresh_token_response = self.post(token_url, data)
        self.token = json.loads(refresh_token_response.text)

    def user_auth(self):
        print(authorize_url)
        code = input('code: ')
        self.get_token(code)
        print("Auth successful")

    def get_trades(self):
        resp = requests.get(
            "https://paymium.com/api/v1/data/eur/trades", verify=False)
        _assert_headers_ok(resp)
        return json.loads(resp.text)

    def get_user(self):
        headers = {
            "Authorization": "Bearer " + self.token["access_token"]
        }
        resp = requests.get(
            "https://paymium.com/api/v1/user", verify=False, headers=headers)
        _assert_headers_ok(resp)
        return json.loads(resp.text)
