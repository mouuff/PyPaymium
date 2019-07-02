
from .paymium import Paymium
import time


class Controller:
    def __init__(self, api, bot):
        self.running = False
        self.bot = bot
        self.api = api
        self.average_xrate = 0  # average xrate usage
        self.loop_count = 0

    def run(self):
        self.running = True
        while self.running:
            pre_xrate = self.api.xrate
            self.bot.update()
            post_xrate = self.api.xrate
            used_xrate = post_xrate - pre_xrate
            self.average_xrate = (
                self.average_xrate * self.loop_count + used_xrate) / (self.loop_count + 1)
            self.loop_count += 1
            time.sleep(1)
