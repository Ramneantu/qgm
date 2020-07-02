from src.block import Block
from src.exceptions import UnmultiplicativeNetwork
from src.value_block import ValueBlock
from src.backtracking import Backtracking

import numpy as np
from ncon import ncon
import copy
from typing import Optional


class QGM:
    """
    Class representing QGM as a tensor network

    Blocks are stored in self.block: list
    (Controlling) ValueBlocks stored separately
    """
    def __init__(self):
        self.block = []
        self.value_block = []

    def add_block(self, block: Block):
        """
        Adds a new block to the network
        :param block: Block to be added
        :return: None
        """
        if isinstance(block, ValueBlock):
            self.value_block.append(block)
        self.block.append(block.get_block())


    def remove_block(self, block: Block):
        """
        Removes a block and all its incoming connections from the QGM

        :param block:
        :return: None
        """
        self.block.remove(block)
        for b in self.block:
            if block in b.adjacent:
                del b.adjacent[block]

    def add_connection(self, block_1: Block, index_1, block_2: Block, index_2):
        """
        Add an edge between index_1 of block_1 and index_2 of block_2

        :param block_1: Block
        :param index_1: int
        :param block_2: Block
        :param index_2: int
        :return: None
        """
        # Since Value Blocks only allow one connection, get_block() always returns a new block for that variable
        block_1 = block_1.get_block()
        if block_1 not in self.block:
            self.block.append(block_1)
        block_2 = block_2.get_block()
        if block_2 not in self.block:
            self.block.append(block_2)
        if block_2 in block_1.adjacent.keys():
            block_1.adjacent[block_2].append((index_1, index_2))
        else:
            block_1.adjacent[block_2] = [(index_1, index_2)]
        if block_1 in block_2.adjacent.keys():
            block_2.adjacent[block_1].append((index_2, index_1))
        else:
            block_2.adjacent[block_1] = [(index_2, index_1)]

    def contract(self, x: Block, y: Block):
        """
        Contract two blocks on the edges between them. Removes both blocks from the network and adds a new block.
        Edges between the blocks x and y and other blocks are carried over to the new block.

        :param x:
        :param y:
        :return: None
        """
        xi = [i[0] for i in x.adjacent[y]]
        yi = [i[0] for i in y.adjacent[x]]

        def construct_index_list(node, start, index_list):
            l = []
            correspondence = {}
            compensation = 0
            for i in range(1, node.get_value().ndim + 1):
                idx = i + start
                if i not in index_list:
                    l.append(-idx + compensation)
                    # correspondence between old and new
                    correspondence[i] = idx - compensation
                else:
                    l.append(0)
                    compensation += 1
            return l, correspondence

        x_links, x_corr = construct_index_list(x, 0, xi)
        y_links, y_corr = construct_index_list(y, abs(min(x_links)), yi)
        common = 1
        for x_out, y_in in x.adjacent[y]:
            # Accounting for zero based indexing
            x_links[x_out - 1] = common
            y_links[y_in  - 1] = common
            common += 1

        val = ncon([x.get_value(), y.get_value()], [x_links, y_links])
        new_block = Block(val)
        self.add_block(new_block)
        # Restoring old connections
        for z in x.adjacent.keys():
            if z == y:
                continue
            for x_out, z_in in x.adjacent[z]:
                self.add_connection(new_block, x_corr[x_out], z, z_in)

        for z in y.adjacent.keys():
            if z == x:
                continue
            for y_out, z_in in y.adjacent[z]:
                self.add_connection(new_block, y_corr[y_out], z, z_in)

        self.remove_block(x)
        self.remove_block(y)

    def contract_all(self):
        """
        Iteratively contracts all neighboring blocks (two blocks at a time).
        QGM is not preserved.
        :return: None
        """
        neigh: Optional[Block] = self.block[0]
        while neigh is not None:
            neigh = None
            for block in self.block:
                if len(block.adjacent) > 0:
                    neigh = next(iter(block.adjacent.keys()))
                    break
            if neigh is not None:
                self.contract(block, neigh)

    def calculate(self):
        """
        Collapses the entire QGM to get a numberical value, if possible.
        Only works is all subgraphs of the QGM collapse to numbers (number of dimensions zero).
        QGM is not modified.
        :return: double: product of all collapsed subgraphs
        """
        clone = copy.deepcopy(self)
        clone.contract_all()
        for block in clone.block:
            if block.value.shape != ():
                raise UnmultiplicativeNetwork()
        product = 1
        for block in clone.block:
            product *= block.value
        return product

    def marginal(self, marginal_blocks):
        """
        Calculate the probability of the assigment of ValueBlocks listed in marginal_blocks

        :param marginal_blocks: a list of ValueBlocks for which we want a probability
        :return: double: the unnormalized probability
        """
        switchable = []
        for var in self.value_block:
            if var not in marginal_blocks:
                switchable.append(var)

        unnormalized_probability = 0
        back = Backtracking(2, len(switchable))
        while back.has_next():
            assignment = back.next()
            for i in range(len(switchable)):
                switchable[i].set(assignment[i])
            unnormalized_probability += self.calculate()

        return unnormalized_probability




