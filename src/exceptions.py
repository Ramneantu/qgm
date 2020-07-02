class NotDefined(Exception):

    def __init__(self, message):
        self.message = message

class UnmultiplicativeNetwork(Exception):

    def __init__(self, message):
        self.message = message
        self.generic = "The blocks of the network do not collapse to 1x1 tensors"