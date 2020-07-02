from __future__ import annotations
from abc import ABC, abstractmethod


class Block:

    def __init__(self, value):
        self.value = value
        self.adjacent = {}

    def get_value(self):
        return self.value

    def get_block(self):
        return self
