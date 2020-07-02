from src.factor_node import FactorNode
from typing import Optional
from src.exceptions import NotDefined

class ValueNode(FactorNode):

    def __init__(self, index, value = None):
        super(ValueNode, self).__init__(index)
        self.value: Optional[float] = value

    def set_value(self, x):
        self.value = x

    def get_value(self):
        if self.value is not None:
            return self.value
        raise NotDefined("Value node " + str(self.index) + " was not initialized")

    def get_index(self):
        return self.index
