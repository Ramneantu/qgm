from src.block import Block
import numpy as np


class Hadamard(Block):

    def __init__(self):
        self.value = np.array([[1, 1], [1, -1]]) / np.sqrt(2)
        self.adjacent = {}






