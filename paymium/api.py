
import webbrowser
import requests
import json
import sys
import os
import urllib3
import time
import logging

from .constants import Constants
from . import helper


logger = logging.getLogger(__file__)

urllib3.disable_warnings()

token_path = helper.get_script_path("paymium_token.json")


def _write_token(token):
    with open(token_path, 'w') as f:
        json.dump(token, f)


def _read_token():
    if not os.path.isfile(token_path):
        return None
    with open(token_path, 'r') as f:
        token = json.load(f)
    expires_at = token["created_at"] + token["expires_in"] - 30
    now = int(time.time())
    if expires_at <= now:
        print("Token expired: " + str(expires_at) + " >= " + str(now))
        return None
    return token


class Api:
    def __init__(self,
                 client_id=None,
                 client_secret=None,
                 use_saved_token=True):
        if client_id is None:
            client_id = helper.my_getenv(Constants.ENV_CLIENT_ID)
        if client_secret is None:
            client_secret = helper.my_getenv(Constants.ENV_CLIENT_SECRET)
        self._token = None
        if use_saved_token:
            self._token = _read_token()
        self.client_id = client_id
        self.client_secret = client_secret
        self._xrate = None

    def _set_token(self, token):
        assert token != None
        self._token = token
        self._token["created_at"] = time.time()
        _write_token(token)

    @property
    def token_expires_in(self):
        """Time before token expires"""
        if self._token is None:
            print("Warning: time_before_expiration: no token", file=sys.stderr)
            return 0
        expires_at = self._token["created_at"] + self._token["expires_in"]
        return expires_at - time.time()

    @property
    def token(self):
        """Current oauth token
        """
        if not self._token:
            return self._token
        return self._token.copy()

    @property
    def xrate(self):
        """API calls remaining for the current day
        This can be found in resp headers
        """
        return int(self._xrate)

    @property
    def _bearer_headers(self):
        return {"Authorization": "Bearer " + self.token["access_token"]}

    def _update_xrate(self, resp):
        if "X-Ratelimit-Remaining" in resp.headers:
            self._xrate = resp.headers["X-Ratelimit-Remaining"]
        else:
            print("Warning: X-Ratelimit-Remaining not found in header",
                  file=sys.stderr)
            if self._xrate:
                self._xrate -= 1

    def _process_resp(self, resp):
        self._update_xrate(resp)
        helper.assert_status_ok(resp)

    def post_auth(self, url, **kwargs):
        """ HTTP POST with auth info filled
        """
        resp = requests.post(url, verify=False,
                             allow_redirects=False, auth=(self.client_id, self.client_secret),
                             **kwargs)
        self._process_resp(resp)
        return resp

    def post(self, path, url_prefix=Constants.URL_API, **kwargs):
        """ HTTP POST to api with oauth token filled
        """
        resp = requests.post(url_prefix + path, headers=self._bearer_headers, verify=False,
                             allow_redirects=False, **kwargs)
        self._process_resp(resp)

    def public_get(self, path, url_prefix=Constants.URL_API, **kwargs):
        """ HTTP GET WITHOUT oauth token filled
        """
        resp = requests.get(
            url_prefix + path, verify=False, **kwargs)
        self._process_resp(resp)
        return json.loads(resp.text)

    def delete(self, path, url_prefix=Constants.URL_API, **kwargs):
        """ HTTP DELETE with oauth token filled
        """
        requests.delete(url_prefix + path, verify=False,
                        headers=self._bearer_headers, **kwargs)

    def get(self, path, url_prefix=Constants.URL_API, **kwargs):
        """ HTTP GET with oauth token filled
        """
        resp = requests.get(url_prefix + path, verify=False,
                            headers=self._bearer_headers, **kwargs)
        self._process_resp(resp)
        return json.loads(resp.text)

    def new_token(self, code, redirect=Constants.URL_REDIRECT):
        data = {
            "grant_type": 'authorization_code',
            "redirect_uri": redirect,
            "code": code
        }
        access_token_response = self.post_auth(Constants.URL_TOKEN, data=data)
        self._set_token(json.loads(access_token_response.text))

    def refresh_token(self, redirect=Constants.URL_REDIRECT):
        data = {
            "grant_type": 'refresh_token',
            "redirect_uri": redirect,
            "refresh_token": self.token["refresh_token"]
        }
        refresh_token_response = self.post_auth(Constants.URL_TOKEN, data=data)
        self._set_token(json.loads(refresh_token_response.text))

    def user_auth(self):
        if self.token:
            print("Using saved token")
            return
        url = "https://www.paymium.com/api/oauth/authorize?client_id=" + self.client_id + \
            "&redirect_uri=https%3A%2F%2Fwww.paymium.com%2Fpage%2Foauth%2Ftest&response_type=code&scope=basic+activity+trade"
        try:
            webbrowser.open_new_tab(url)
        except webbrowser.Error:
            print("Open this url:")
            print(url)
        code = input('Enter code: ')
        self.new_token(code)
        print("Auth successful")

    def get_trades(self, since=None):
        """ Read the latest executed trades.
        """
        data = {}
        if since:
            data["since"] = int(since)
        return self.public_get("/api/v1/data/eur/trades", data=data)

    def get_ticker(self):
        """ Read the latest ticker data.
        """
        return self.public_get("/api/v1/data/eur/ticker")

    def get_depth(self):
        """ Read the market depth. Bids and asks are grouped by price.
        """
        return self.public_get("/api/v1/data/eur/depth")

    def get_user(self):
        """ Read the latest user info.
        """
        return self.get("/api/v1/user")

    def post_order(self, data):
        return self.post("/api/v1/user/orders", data=data)

    def post_limit_order(self, direction, price, amount):
        price = round(price, 2)  # paymium doesnt allow unrounded numbers
        data = {
            "type": "LimitOrder",
            "currency": "EUR",
            "direction": direction,
            "price": price,
            "amount": amount,
        }
        return self.post_order(data)

    def buy_limit(self, price, btc_amount):
        """ Buy bitcoin at given price limit
        """
        logger.info("Buying " + str(btc_amount) + " at: " + str(price))
        return self.post_limit_order("buy", price, btc_amount)

    def sell_limit(self, price, btc_amount):
        """ Sell bitcoin at given price limit
        """
        logger.info("Selling " + str(btc_amount) + " at: " + str(price))
        return self.post_limit_order("sell", price, btc_amount)

    def post_market_order(self, direction, btc_amount=None, eur_amount=None):
        assert btc_amount is not None or eur_amount is not None
        assert not (btc_amount is None and eur_amount is None)
        data = {
            "type": "MarketOrder",
            "currency": "EUR",
            "direction": direction,
        }
        if btc_amount:
            data["amount"] = btc_amount
        if eur_amount:
            data["currency_amount"] = eur_amount
        return self.post_order(data)

    def get_orders(self, active=True):
        """ Read user's orders.
        """
        data = {}
        if active:
            data["active"] = True
        # TODO: add params https://github.com/Paymium/api-documentation#parameters-1
        return self.get("/api/v1/user/orders", data=data)

    def cancel_order(self, uuid):
        logger.info("Cancelling order: " + str(uuid))
        return self.delete("/api/v1/user/orders/%s/cancel" % uuid)
