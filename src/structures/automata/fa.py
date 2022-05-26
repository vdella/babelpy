from src.structures.automata.state import State
from prettytable import PrettyTable


class FiniteAutomata:

    def __init__(self):
        start = State(0)

        self.initial_state = start
        self.states = {self.initial_state}
        self.transitions = dict()
        self.final_states = set()

    def read(self, sentence: str) -> bool:
        """Iteratively loops over a transition table and
        checks if a final state can be reached from the given input."""

        cached_state = self.initial_state

        for symbol in sentence:
            for s in self.transitions[(cached_state, symbol)]:
                cached_state = s

        return cached_state in self.final_states

    def __or__(self, other):
        new_fa = FiniteAutomata()

        new_fa.initial_state = State(0)
        self.__update_ids_from(1)
        other.__update_ids_from(len(self.states) + 1)

        new_fa.states = self.states | other.states

        new_fa.transitions = self.transitions | other.transitions
        new_fa.transitions[(new_fa.initial_state, '&')] = {self.initial_state, other.initial_state}

        return new_fa

    def __update_ids_from(self, seed: int):
        # TODO replace by summing both automata.state length.
        for s in self.states:
            # print(s.id)
            s.id += seed
            print(s.id)

    def __str__(self):
        table = PrettyTable()
        table.field_names = ['Transition', 'Arrival']

        for key, value in self.transitions.items():
            table.add_row([key, value])
        return str(table)


if __name__ == '__main__':
    fa = FiniteAutomata()

    print(fa)

