class Backtracking:
    """
    Computes all tuples from [n] x [n] x [n] x ... x [n] (k times)
    where:
     x is the cross product
     [n] is the set of natural numbers smaller than n (self.diff_values)
     k = len(self.list)
    """
    def __init__(self, diff_values, length):
        self.diff_values = diff_values
        self.list = [0] * length
        self.index = length
        self.first = True

    def set_length(self, length):
        self.list = [0] * length
        self.index = length
        self.first = True

    def has_next(self):
        return self.list != [self.diff_values - 1] * len(self.list)

    def next(self):
        if self.first:
            self.first = False
            return self.list
        if self.index >= len(self.list):
            self.index = len(self.list) - 1
            while self.list[self.index] >= self.diff_values - 1:
                self.list[self.index] = 0
                self.index -= 1
            self.list[self.index] += 1
            self.index = len(self.list)
        else:
            self.list[self.index] += 1
            self.index += 1
        return self.list

