from regex.format import eat


class SyntaxTree:

    __digest = list()

    def __init__(self, regex: str):
        self.__digest, self.terminals = eat(regex)

        self.root = Node('.')
        actual = self.root

        while self.__digest:
            # print(self.__digest)
            actual.right = Node(self.__digest.pop(-1))
            # print(actual.right)
            actual.left = Node(self.__digest.pop(-1))
            # print(actual.left)
            actual = actual.left

    @staticmethod
    def parenthesis_contents(regex):
        """Generates parenthesized contents in string as (level, contents)."""
        stack = list()  # As a parenthesis index stack.
        for i, c in enumerate(regex):
            if c == '(':
                stack.append(i)
            elif c == ')' and stack:
                start = stack.pop()
                yield len(stack), regex[start + 1: i]


class Node:

    def __init__(self, symbol: str, left=None, right=None):
        self.symbol = symbol

        self.left: Node = left
        self.right: Node = right

    def __nullable(self):
        if self.symbol == '&' or self.symbol == '*':
            return True
        elif self.symbol == ".":
            return self.left.__nullable() and self.right.__nullable()
        elif self.symbol == "|":
            return self.left.__nullable() or self.right.__nullable()
        return False

    def __first_pos(self):
        if self.symbol == '&':
            return set()
        elif self.symbol == '*':
            return self.left.__first_pos()
        elif self.symbol == '.':
            return self.left.__first_pos() | self.right.__first_pos() \
                if self.left.__nullable() else self.left.__first_pos()
        elif self.symbol == '|':
            return self.left.__first_pos() | self.right.__first_pos()
        return {self.symbol}

    def __last_pos(self):
        if self.symbol == '&':
            return set()
        elif self.symbol == '*':
            return self.left.__last_pos()
        elif self.symbol == '.':
            return self.left.__last_pos() | self.right.__last_pos() \
                if self.right.__nullable() else self.right.__last_pos()
        elif self.symbol == '|':
            return self.right.__last_pos()


def show(node, level=0):
    if node is not None:
        show(node.left, level + 1)
        print(' ' * 4 * level + '-> ' + node.symbol)
        show(node.right, level + 1)


if __name__ == "__main__":
    regex = '(a | b)*abb'
    print(regex)
    root = SyntaxTree(regex).root
    print(show(root))
