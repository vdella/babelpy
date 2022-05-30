from src.regex.format import eat


class SyntaxTree:
    def __init__(self, regex):
        digest, _ = eat(regex)
        self.root = _tree_from(digest)


def _tree_from(regex):

    def __sides_for(operator):
        left_tree, right_tree = str(), str()
        parenthesis = 0

        for i in range(len(regex) - 1, -1, -1):
            if regex[i] == operator and parenthesis == 0:
                left_tree = regex[:i]
                return left_tree, right_tree[::-1]

            if regex[i] == ')':
                parenthesis += 1
            elif regex[i] == '(':
                parenthesis -= 1

            right_tree += regex[i]

        return left_tree, right_tree[::-1]

    left, right = __sides_for('|')
    if left:
        return Node('|', _tree_from(left), _tree_from(right))

    left, right = __sides_for('.')
    if left:
        return Node('.', _tree_from(left), _tree_from(right))

    left, _ = __sides_for('*')
    if left:
        return Node('*', _tree_from(left))

    if regex[0] == '(' and regex[-1] == ')':
        return _tree_from(regex[1:-1])

    return Node(regex[0])


class Node:

    def __init__(self, symbol: str, left=None, right=None):
        self.symbol = symbol

        self.left: Node = left
        self.right: Node = right

    def __str__(self):
        return self.symbol

    def nullable(self):
        if self.symbol == '&' or self.symbol == '*':
            return True
        elif self.symbol == ".":
            return self.left.nullable() and self.right.nullable()
        elif self.symbol == "|":
            return self.left.nullable() or self.right.nullable()
        return False

    def first_pos(self):
        if self.symbol == '&':
            return set()
        elif self.symbol == '*':
            return self.left.first_pos()
        elif self.symbol == '.':
            return self.left.first_pos() | self.right.first_pos() \
                if self.left.nullable() else self.left.first_pos()
        elif self.symbol == '|':
            return self.left.first_pos() | self.right.first_pos()
        return {self.symbol}

    def last_pos(self):
        if self.symbol == '&':
            return set()
        elif self.symbol == '*':
            return self.left.last_pos()
        elif self.symbol == '.':
            return self.left.last_pos() | self.right.last_pos() \
                if self.right.nullable() else self.right.last_pos()
        elif self.symbol == '|':
            return self.right.last_pos()


def show_tree_from(root, level=0):
    if root is not None:
        show_tree_from(root.right, level + 1)
        print(' ' * 4 * level + '-> ' + root.symbol)
        show_tree_from(root.left, level + 1)


if __name__ == "__main__":
    a = '(a | b)*abb'
    tree = SyntaxTree(a)
    show_tree_from(tree.root)
