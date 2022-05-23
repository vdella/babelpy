class State:

    def __init__(self, identifier: int):
        self.id = identifier

    def __str__(self):
        return 'q{}'.format(self.id)

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        if isinstance(other, State):
            return self.id == other.id


if __name__ == '__main__':
    s = set()
    s.add(State(0))
