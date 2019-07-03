import paymium
import unittest
import time
from .base_test_case import BaseTestCase


class TestPublicApi(BaseTestCase):
    def test_ticker(self):
        p = paymium.Api()
        ticker = p.get_ticker()
        assert ticker["currency"] == "EUR"
        assert ticker["bid"] < ticker["ask"]
        assert ticker["low"] < ticker["high"]

    def test_trades(self):
        p = paymium.Api()
        trades = p.get_trades()
        assert len(trades) > 0
        first = trades[0]
        assert 'uuid' in first
        assert 'currency' in first
        assert 'traded_btc' in first
        assert 'traded_currency' in first
        assert 'created_at' in first
        assert 'currency' in first
        assert 'side' in first
        assert 'price' in first
        assert 'created_at_int' in first

    def test_depth(self):
        p = paymium.Api()
        depth = p.get_depth()
        asks = depth["asks"]
        bids = depth["bids"]
        assert len(asks) > 0
        assert len(bids) > 0
        first_bid = bids[0]
        first_ask = asks[0]
        assert "timestamp" in first_bid
        assert "amount" in first_bid
        assert "price" in first_bid
        assert "timestamp" in first_ask
        assert "amount" in first_ask
        assert "price" in first_ask
