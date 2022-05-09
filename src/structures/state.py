class State:

    def __init__(self, identifier: int, label: str = ''):
        self.identifier = identifier
        self.label = label

    def __str__(self):
        return 'q' + str(self.identifier)

    def __eq__(self, other):
        # TODO needs to change. Check for input and output states
        #  for measuring equality. If both have same input and output,
        #  they are both equal states.
        if other is State:
            return self.identifier == other.identifier
        return False


def initial_state():
    return State(0, 'Initial state')
