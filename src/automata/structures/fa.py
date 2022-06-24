from src.automata.structures.state import State
from prettytable import PrettyTable


class FiniteAutomata:

    def __init__(self):
        self.initial_state = State()
        self.states = {self.initial_state}
        self.transitions = dict()
        self.final_states = set()
        self.symbol_table = []

    def read(self, sentence: str) -> bool:
        """Iteratively loops over a transition table and
        checks if a final state can be reached from the given input."""

        cached_state = self.initial_state

        for symbol in sentence:
            for s in self.transitions[(cached_state, symbol)]:
                cached_state = s

        return cached_state in self.final_states

    def gen_st(self, identifier: str) -> int:

        if not (identifier in self.symbol_table):
            self.symbol_table.append(identifier)
        return self.symbol_table.index(identifier)

    def is_nfa(self):
        """Checks for non-determinism in an automata. It's non-deterministic
        if it has an '&' as an input in a transition or if one of its transitions has more
        than one, or none, destiny states."""
        for transition, arrival in self.transitions.items():
            _, symbol = transition
            if symbol == '&' or len(arrival) != 1:
                return True
        return False

    def __or__(self, other):
        new_fa = FiniteAutomata()

        new_fa.states = self.states | other.states | {new_fa.initial_state}
        new_fa.final_states = self.final_states | other.final_states
        new_fa.transitions = self.transitions | other.transitions
        new_fa.transitions[(new_fa.initial_state, '&')] = {self.initial_state, other.initial_state}

        return new_fa

    def __str__(self):
        """Shows a Finite Automata as its transition table."""
        table = PrettyTable()
        table.field_names = ['Transition', 'Arrival']

        for key, value in self.transitions.items():
            state = str(key[0])

            if key[0] in self.final_states:
                state = '*{}'.format(str(state))
            if key[0] == self.initial_state:
                state = '->{}'.format(str(state))

            symbol = key[1]
            transition = (state, symbol)

            # Gathers all possible destiny state labels, as we can have more than one.
            arrival = {str(s) for s in value}

            table.add_row([transition, arrival])
        return str(table)
