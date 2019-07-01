
import requests
import json
import subprocess
import sys

authorize_url = "https://www.paymium.com/api/oauth/authorize?client_id=63ad627670dd4d6b25083e2e8454dcaf53202ddf6fcb4e4a4b42aa4e8ccbcc19&redirect_uri=https%3A%2F%2Fwww.paymium.com%2Fpage%2Foauth%2Ftest&response_type=code"
token_url = "https://paymium.com/api/oauth/token"
redirect_uri = "https://www.paymium.com/page/oauth/test"

client_id = '63ad627670dd4d6b25083e2e8454dcaf53202ddf6fcb4e4a4b42aa4e8ccbcc19'
client_secret = '7de4b1015e19590efb7c6abaf4db19170fd9884bc717bf2a8bb18c6c2863d924'

print(authorize_url)
authorization_code = input('code: ')

data = {
    "client_id": client_id,
    "client_secret": client_secret,
    "grant_type": 'authorization_code',
    "redirect_uri": redirect_uri,
    "code": authorization_code
}

access_token_response = requests.post(
    token_url, data=data, verify=False, allow_redirects=False, auth=(client_id, client_secret))
tokens = json.loads(access_token_response.text)
'''
tokens = {"access_token": "bf72bde1f7ac9534d149801ffccd438c947c6d30448e0b647814d49557a868d1", "token_type": "bearer", "expires_in": 1800,
"refresh_token": "7685bded00d61275f05835582397d726ac7a2c05990924a66090f4a20c8976b0", "scope": "basic", "created_at": 1561993742}
'''

# print(access_token_response.headers)

'''
# we can now use the access_token as much as we want to access protected resources.
tokens = json.loads(access_token_response.text)
print(tokens)
access_token = tokens['access_token']
print("access token: " + access_token)

api_call_headers = {'Authorization': 'Bearer ' + access_token}


test_api_url = "<<the URL of the API you want to call, along with any parameters, goes here>>"
api_call_response = requests.get(
    test_api_url, headers=api_call_headers, verify=False)

print(api_call_response.text)
'''


def main():
    print("ok")


if __name__ == "__main__":
    main()
