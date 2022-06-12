from src.regex.format import eat


class SyntaxTree:

    def __init__(self, regex):
        digest, self.terminals = eat(regex)
        self.root: Node = _tree_from(digest)
        _attach_serial_to(self)


def _attach_serial_to(tree: SyntaxTree):

    serial = 1

    def seek_from(node):

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
        self.regex_symbol = symbol
        self.serial_number = 0

        self.left: Node = left
        self.right: Node = right

        self.follow_pos = set()

    def __str__(self):
        return self.regex_symbol

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

    def gen_follow_pos(self) -> ():
        # TODO test.
        for children in {self.left, self.right}:
            if children:
                children.gen_follow_pos()

        if self.regex_symbol == '.':
            for children in self.left.last_pos():
                children.follow_pos |= self.right.first_pos()

        elif self.regex_symbol == '*':
            for children in self.last_pos():
                children.follow_pos |= self.first_pos()


def stringfy(node):
    first_pos = [n.serial_number for n in node.first_pos()]
    first_pos.sort()

    last_pos = [n.serial_number for n in node.last_pos()]
    last_pos.sort()

    return str(first_pos), str(last_pos)


def show_tree_from(root, level=0):
    if root:
        str_first_pos, str_last_pos = stringfy(root)

        show_tree_from(root.right, level + 1)
        print(' ' * 4 * level + '-> ' + str_first_pos + ' ' + root.regex_symbol + ' ' + str_last_pos)
        show_tree_from(root.left, level + 1)


if __name__ == "__main__":
    a = 'a(a | b)*a'
    t = SyntaxTree(a)
    show_tree_from(t.root)
    print(stringfy(t.root))
