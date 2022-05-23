class State:

    def __init__(self, identifier: int):
        self.id = identifier

    def __str__(self):
        return 'q{}'.format(self.id)


def initial_state():
    return State(0)


if __name__ == '__main__':
    s = set()
    s.add(State(0))
