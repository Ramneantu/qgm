from src.block import Block
import numpy as np


class Diag(Block):

    def __init__(self, d1, d2):
        self.value = np.diag([d1, d2])
        self.adjacent = {}
