from src.block import Block
import numpy as np


class ValueBlock(Block):
    """
    Master class for one variable. Not part of QGM tensor network. Never contracted.

    As a QGM contains  multiple copies of the same variable which need to be administered, in the case of value update.
    """
    class ActualValueBlock(Block):
        """
        Block being added to QGM
        """
        def __init__(self, value):
            if value == 0:
                self.value = np.array([1, 0])
            elif value == 1:
                self.value = np.array([0, 1])
            self.adjacent = {}

        def set(self, value):
            if value == 0:
                self.value = np.array([1, 0])
            elif value == 1:
                self.value = np.array([0, 1])

    def __init__(self, value):
        self.value = value
        self.block = [self.ActualValueBlock(value)]

    # Thread carefully with this method. It always returns a Block with no connections. It CREATES NEW BLOCKS!
    def get_block(self):
        """

        :return: new block to be added to QGM, with degree zero. Connections of other copies are not carried over
        """
        last = self.block[-1]
        if len(last.adjacent) == 0:
            return last
        new = self.ActualValueBlock(self.value)
        self.block.append(new)
        return new

    def set(self, value):
        """
        Updates all blocks corresponding to this variable
        :param value: New value
        :return: None
        """
        for block in self.block:
            block.set(value)
