
from .paymium import Paymium
from .base_bot import BaseBot
import time


class Controller:
    def __init__(self, api, bot):
        assert issubclass(type(bot), BaseBot)
        self.bot = bot
        self.api = api
        self._running = False
        self._average_xrate = 0  # average xrate usage
        self._loop_count = 0
        self._saved_xrate = None
        self.bot.setup(api, self)

    @property
    def average_xrate(self):
        return self._average_xrate

    def _calc_average_xrate(self):
        '''This function should only be called once per bot.update()'''
        if self._saved_xrate is None:
            used_xrate = self._saved_xrate - self.api.xrate
            self._average_xrate = (
                self._average_xrate * self._loop_count + used_xrate
            ) / (self._loop_count + 1)
        self._saved_xrate = self.api.xrate

    def run(self):
        self._running = True
        while self._running:
            self.bot.update()
            self._calc_average_xrate()
            self._loop_count += 1
            time.sleep(1)
