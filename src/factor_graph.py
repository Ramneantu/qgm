from src.function_node import FunctionNode
from src.value_node import ValueNode
from src.qgm import QGM
from src.value_block import ValueBlock
from src.backtracking import Backtracking


class FactorGraph:

    def __init__(self):
        self.value_nodes = []
        self.function_nodes = []
        pass

    def add_value_node(self):
        """
        Adds a new variable
        :return:
        """
        n = len(self.value_nodes)
        new_node = ValueNode(n)
        self.value_nodes.append(new_node)
        return new_node

    def add_function_node_by_index(self, a, b, c, value_node1_index, value_node2_index):
        """
        Adds a new function node that represents the correlation between two variables x1 and x2 as:
            exp(a*x1*x2 + b*x1 + c*x2)
        :param a: param of function node
        :param b: param of function node
        :param c: param of function node
        :param value_node1_index: index of first var in self.value_nodes
        :param value_node2_index: index of second var
        :return: a new function node
        """
        value_node1 = self.value_nodes[value_node1_index]
        value_node2 = self.value_nodes[value_node2_index]
        return self.add_function_node(a, b, c, value_node1, value_node2)

    def add_function_node(self, a, b, c, value_node1, value_node2):
        """
        Adds a new function node that represents the correlation between two variables x1 and x2 as:
            exp(a*x1*x2 + b*x1 + c*x2)
        :param a: param of function node
        :param b: param of function node
        :param c: param of function node
        :param value_node1: first ValueNode
        :param value_node2: second ValueNode
        :return: a new function node
        """
        n = len(self.function_nodes)
        new_node = FunctionNode(n, a, b, c, value_node1, value_node2)
        self.function_nodes.append(new_node)
        return new_node

    def get_value_node_by_index(self, index):
        return self.value_nodes[index]

    def compute_unnormalized_probability(self):
        """
        Calculates the unnormalized probability of the current variable assignment
        :return: double: unnormalized probability
        """
        res = 1
        for f in self.function_nodes:
            res *= f.get_value()
        return res

    def marginal_distribution(self, marginal_variables):
        """
        Calculate the probability of the assigment of ValueNodes listed in marginal_blocks

        :param marginal_variables: a list of ValueNodes for which we want a probability
        :return: double: the unnormalized probability
        """
        switchable = []
        for var in self.value_nodes:
            if var not in marginal_variables:
                switchable.append(var)

        unnormalized_probability = 0
        back = Backtracking(2, len(switchable))
        while back.has_next():
            assignment = back.next()
            for i in range(len(switchable)):
                switchable[i].set_value(assignment[i])
            unnormalized_probability += self.compute_unnormalized_probability()

        return unnormalized_probability

    def to_qgm(self):
        """
        Transforms the factor graph in an equivalent QGM
        :return: equivalent QGM
        """
        qgm = QGM()
        node_to_block = {}
        for node in self.value_nodes:
            value_block = ValueBlock(node.get_value())
            node_to_block[node] = value_block
            qgm.add_block(value_block)
        for f in self.function_nodes:
            f.augment_qgm(qgm, node_to_block)
        return qgm
