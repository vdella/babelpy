from time import process_time_ns


class State:

    def __init__(self, label: str = None):
        self.id = process_time_ns()
        self.label = label

    def __str__(self):
        return self.label if self.label is not None else 'q{}'.format(self.id)

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return self.id == other.id


if __name__ == '__main__':
    s = set()
    s.add(State())
    print(s.pop())
