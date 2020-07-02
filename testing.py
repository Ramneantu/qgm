"""
Testing file
"""
from src.qgm import QGM, Block
from src.hadamard import Hadamard
from src.value_block import ValueBlock
from src.diag import Diag
from src.backtracking import Backtracking
from src.factor_graph import FactorGraph
import numpy as np
from ncon import ncon

# qgm = QGM()
# H = Hadamard()
# plus = Block(np.sqrt(2) * np.array([1, 1]))
# trileg = Block(np.array([[[1, 0], [0, 0]], [[0, 0], [0, 1]]]))
# x = ValueBlock(1)
# y = ValueBlock(1)
# diag1 = Diag(3, 4)
# diag2 = Diag(3, 4)

# qgm.add_block(plus)
# qgm.add_block(trileg)
# qgm.add_connection(plus, 1, trileg, 2)
# qgm.contract(plus, trileg)

# qgm.add_block(x)
# qgm.add_block(y)
# qgm.add_block(diag1)
# qgm.add_block(diag2)
# qgm.add_connection(x, 1, diag1, 1)
# qgm.add_connection(diag1, 2, diag2, 1)
# qgm.add_connection(y, 1, diag2, 2)
#
# qgm.contract_all()
#
# print(qgm.block[0].value)

# x = np.array([1, 1])
# y = np.array([1, 1])
# z = ncon([x, y], [[1],[1]])
# print(z * 2)

fc = FactorGraph()
x1 = fc.add_value_node()
x2 = fc.add_value_node()
x3 = fc.add_value_node()
x4 = fc.add_value_node()
x1.set_value(1)
x2.set_value(1)
x3.set_value(0)
x4.set_value(1)
fc.add_function_node(0.7, 1.3, -2, x1, x2)
fc.add_function_node(1.2, -0.9, -2, x3, x4)
resf = fc.marginal_distribution([x2, x3])
qgm = fc.to_qgm()
resq = qgm.marginal([qgm.value_block[1], qgm.value_block[2]])
print("Result from factor graph: " + str(resf))
print("Result from QGM:          " + str(resq))