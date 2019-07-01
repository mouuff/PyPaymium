
from paymiumbot import Paymium
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
    p = Paymium()
    # print(p.get_trades())
    print(p.get_ticker())
    p.user_auth()
    p.refresh_token()
    print(p.get_user())


if __name__ == "__main__":
    main()
