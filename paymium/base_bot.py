
from abc import abstractmethod, ABC


class BaseBot(ABC):

    def setup(self, api, controller):
        self.api = api
        self.controller = controller

    @abstractmethod
    def update(self):
        pass
