from format import eat
from format import sides_for


class SyntaxTree:

    def __init__(self, regex):
        digest, self.terminals = eat(regex)
        self.root: Node = _tree_from(digest)
        _add_serials_to(self)


def _add_serials_to(tree: SyntaxTree):
    """Adds serial numbers to every terminal, from left to right, in a :param tree:."""
    serial = 1

    def seek_from(node):
        # Ints are immutable, so we need to declare an outer scope variable in order to change it through recursion.
        nonlocal serial

        left, right = node.left, node.right

        if left:
            if left.regex_symbol not in tree.terminals:
                seek_from(left)
            else:
                left.serial_number = serial
                serial += 1

        if right:
            if right.regex_symbol not in tree.terminals:
                seek_from(right)
            else:
                right.serial_number = serial
                serial += 1

    seek_from(tree.root)


def _tree_from(regex):
    left, right = sides_for('|', regex)
    if left:
        return Node('|', _tree_from(left), _tree_from(right))

    left, right = sides_for('.', regex)
    if left:
        return Node('.', _tree_from(left), _tree_from(right))

    left, _ = sides_for('*', regex)
    if left:
        return Node('*', _tree_from(left))

    left, _ = sides_for('?', regex)
    if left:
        return Node('|', _tree_from(left), Node('&'))

    if regex[0] == '(' and regex[-1] == ')':
        return _tree_from(regex[1:-1])

    return Node(regex[0])


class Node:

    def __init__(self, symbol: str, left=None, right=None):
        self.regex_symbol = symbol
        self.serial_number = 0

        self.left: Node = left
        self.right: Node = right

        self.follow_pos = set()

    def __str__(self):
        """Returns a node's regex symbol with its first_pos() and last_pos() by its sides."""
        str_first_pos, str_last_pos = stringfy(self)
        return str_first_pos + ' ' + self.regex_symbol + ' ' + str_last_pos

    def nullable(self) -> bool:
        if self.regex_symbol == '&' or self.regex_symbol == '*':
            return True
        elif self.regex_symbol == ".":
            return self.left.nullable() and self.right.nullable()
        elif self.regex_symbol == "|":
            return self.left.nullable() or self.right.nullable()
        return False

    def first_pos(self) -> set:
        match self.regex_symbol:
            case '&':
                return set()
            case '*':
                return self.left.first_pos()
            case '.':
                if self.left.nullable():
                    return self.left.first_pos() | self.right.first_pos()
                else:
                    return self.left.first_pos()
            case '|':
                return self.left.first_pos() | self.right.first_pos()
            case _:
                return {self}

    def last_pos(self) -> set:
        match self.regex_symbol:
            case '&':
                return set()
            case '*':
                return self.left.last_pos()
            case '.':
                if self.right.nullable():
                    return self.left.last_pos() | self.right.last_pos()
                else:
                    return self.right.last_pos()
            case '|':
                return self.left.last_pos() | self.right.last_pos()
            case _:
                return {self}

    def calculate_follow_pos(self) -> ():
        for children in {self.left, self.right}:
            if children:
                children.calculate_follow_pos()

        if self.regex_symbol == '.':
            for children in self.left.last_pos():
                children.follow_pos |= self.right.first_pos()

        elif self.regex_symbol == '*':
            for children in self.last_pos():
                children.follow_pos |= self.first_pos()


def stringfy(node):
    """:returns the first_pos() and last_pos() of a :param node: as strings
    in order to print them in Node.__str__()."""
    first_pos = [n.serial_number for n in node.first_pos()]
    first_pos.sort()

    last_pos = [n.serial_number for n in node.last_pos()]
    last_pos.sort()

    return str(first_pos), str(last_pos)


def show_tree_from(root, level=0):
    if root:
        show_tree_from(root.right, level + 1)
        print(' ' * 4 * level + '-> ' + str(root))
        show_tree_from(root.left, level + 1)


if __name__ == "__main__":
    a = '(&|b)(ab)*(&|a)'
    t = SyntaxTree(a)
    show_tree_from(t.root)
