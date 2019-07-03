import paymium
import unittest
import time
from .base_test_case import BaseTestCase


class TestPublicApi(BaseTestCase):
    def test_1(self):
        p = paymium.Api()
        print(p.get_trades(since=time.time()-10000))
