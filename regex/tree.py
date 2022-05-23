from src.structures.automata.fa import FiniteAutomata


class SyntaxTree:

    def __init__(self):
        self.root = Node('.', None, None)


class Node:

    def __init__(self, symbol: str, left=None, right=None):
        self.symbol = symbol
        self.left = left
        self.right = right
