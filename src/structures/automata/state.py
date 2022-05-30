class State:

    def __init__(self, identifier: int, label: str = None):
        self.id = identifier
        self.label = label

    def __str__(self):
        return self.label if self.label is not None else 'q{}'.format(self.id)

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return self.id == other.id


if __name__ == '__main__':
    s = set()
    s.add(State(0))
    print(s.pop())
