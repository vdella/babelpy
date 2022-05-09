class State:

    def __init__(self, identifier: int, label: str = ''):
        self.identifier = identifier
        self.label = label

    def __str__(self):
        return 'q' + str(self.identifier)

    def __eq__(self, other):
        if other is State:
            return self.identifier == other.identifier
        return False

    def __hash__(self) -> int:
        return 31 * self.identifier * self.label.__hash__()


def initial_state():
    return State(0, 'Initial state')
