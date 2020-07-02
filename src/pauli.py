from src.block import Block
import numpy as np

class Pauli(Block):

    def __init__(self, t):
        if t == 'x':
            self.value = np.array([[0, 1], [1, 0]])
        elif t == 'z':
            self.value = np.array([[1, 0], [0, -1]])
        self.adjacent = {}

