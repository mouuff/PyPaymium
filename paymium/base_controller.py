
import time
import sys
from abc import abstractmethod, ABC
from .api import Api
from .constants import Constants


class BaseController(ABC):
    def __init__(self, api):
        self.api = api
        self._running = False
        self._average_xrate = 0  # average xrate usage
        self._loop_count = 0
        self._saved_xrate = None

    @property
    def average_xrate(self):
        """Average xrate usage every loop
        reminder: xrate = API calls remaining for the current day
        """
        return self._average_xrate

    def _calc_average_xrate(self):
        '''This function should only be called once per bot.update()'''
        if self._saved_xrate is not None:
            used_xrate = self._saved_xrate - self.api.xrate
            self._average_xrate = (
                self._average_xrate * self._loop_count + used_xrate
            ) / (self._loop_count + 1)
        self._saved_xrate = self.api.xrate

    def run(self):
        self._running = True
        while self._running:
            self.update()
            if self.api.token_expires_in < Constants.TOKEN_REFRESH_BEFORE:
                self.api.refresh_token()
                print("Refreshed token", file=sys.stderr)
            self._calc_average_xrate()
            self._loop_count += 1
            time.sleep(0.5)

    @abstractmethod
    def update(self):
        pass
