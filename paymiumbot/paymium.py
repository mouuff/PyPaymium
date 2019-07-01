import requests
import json
import sys

authorize_url = "https://www.paymium.com/api/oauth/authorize?client_id=63ad627670dd4d6b25083e2e8454dcaf53202ddf6fcb4e4a4b42aa4e8ccbcc19&redirect_uri=https%3A%2F%2Fwww.paymium.com%2Fpage%2Foauth%2Ftest&response_type=code"
token_url = "https://paymium.com/api/oauth/token"
redirect_uri = "https://www.paymium.com/page/oauth/test"

client_id = '63ad627670dd4d6b25083e2e8454dcaf53202ddf6fcb4e4a4b42aa4e8ccbcc19'
client_secret = '7de4b1015e19590efb7c6abaf4db19170fd9884bc717bf2a8bb18c6c2863d924'


class Paymium:
    def __init__(self):
        pass

    def post(self, url, data, assert_ok=True):
        resp = requests.post(url, data=data, verify=False,
                             allow_redirects=False, auth=(client_id, client_secret))
        if assert_ok and resp.headers["Status"] != "200 OK":
            raise AssertionError(
                'Status != 200 OK : ' + str(resp.headers))
        return resp

    def authorize(self):
        print(authorize_url)
        code = input('code: ')
        data = {
            "client_id": client_id,
            "client_secret": client_secret,
            "grant_type": 'authorization_code',
            "redirect_uri": redirect_uri,
            "code": code
        }
        access_token_response = self.post(token_url, data)

        body = json.loads(access_token_response.text)
        '''
        body = {"access_token": "xxx", "token_type": "bearer", "expires_in": 1800,
        "refresh_token": "xxx", "scope": "basic", "created_at": 1561993742}
        '''
        return body
