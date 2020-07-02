from abc import ABC, abstractmethod


class FactorNode(ABC):

    def __init__(self, index):
        self.index = index

    @abstractmethod
    def get_value(self):
        pass
