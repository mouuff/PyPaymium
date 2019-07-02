
from .paymium import Paymium


class Controller:
    def __init__(self, api, bot):
        self.running = False
        self.bot = bot
        self.api = api

    def run(self):
        self.running = True
        while self.running:
            self.bot.update()
