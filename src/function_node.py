import numpy as np
from src.factor_node import FactorNode
from src.qgm import QGM
from src.hadamard import Hadamard
from src.diag import Diag
from src.block import Block

class FunctionNode(FactorNode):

    def __init__(self, index, a, b, c, node1, node2):
        super(FunctionNode, self).__init__(index)
        self.a = a
        self.b = b
        self.c = c
        self.node1 = node1
        self.node2 = node2

    def get_value(self):
        x1 = self.node1.get_value()
        x2 = self.node2.get_value()
        return np.exp(self.a*x1*x2 + self.b*x1 + self.c*x2)

    def augment_qgm(self, qgm: QGM, node_to_block):
        x1 = node_to_block[self.node1]
        x2 = node_to_block[self.node2]
        d1 = Diag(1, np.sqrt(np.exp(self.b + self.a/2)))
        qgm.add_block(d1)
        d1c = Diag(1, np.sqrt(np.exp(self.b + self.a/2)))
        qgm.add_block(d1c)
        d2 = Diag(1, np.sqrt(np.exp(self.c + self.a/2)))
        qgm.add_block(d2)
        d2c = Diag(1, np.sqrt(np.exp(self.c + self.a/2)))
        qgm.add_block(d2c)
        l1 = 2
        l2 = 2*np.exp(-self.a/2)
        m = Block(np.array([[.5*(l1 + l2), .5*(l1 - l2)], [.5*(l1 - l2), .5*(l1 + l2)]]))
        qgm.add_block(m)
        trileg = []
        for i in range(2):
            trileg.append(Block(np.array([[[1, 0], [0, 0]], [[0, 0], [0, 1]]])))
            qgm.add_block(trileg[i])
        hadamard = []
        for i in range(4):
            hadamard.append(Hadamard())
            qgm.add_block(hadamard[i])
        qgm.add_connection(d1c, 1, hadamard[0], 1)
        qgm.add_connection(hadamard[0], 2, trileg[0], 1)
        qgm.add_connection(trileg[0], 2, m, 1)
        qgm.add_connection(trileg[0], 3, hadamard[1], 1)
        qgm.add_connection(hadamard[1], 2, d2c, 1)
        qgm.add_connection(d1c, 2, x1, 1)
        qgm.add_connection(x1, 1, d1, 1)
        qgm.add_connection(d1, 2, hadamard[2], 1)
        qgm.add_connection(hadamard[2], 2, trileg[1], 1)
        qgm.add_connection(m, 2, trileg[1], 2)
        qgm.add_connection(trileg[1], 3, hadamard[3], 1)
        qgm.add_connection(d2c, 2, x2, 1)
        qgm.add_connection(x2, 1, d2, 1)
        qgm.add_connection(d2, 2, hadamard[3], 2)
