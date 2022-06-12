from src.structures.automata.state import State
from prettytable import PrettyTable


class FiniteAutomata:

    def __init__(self):
        self.initial_state = State()
        self.states = {}
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

    def is_nfa(self):
        """Checks for non-determinism in an automata. It's non-deterministic
        if it has an '&' as an input in a transition or if one of its transitions has more
        than one, or none, destiny states."""
        for transition in self.transitions:
            symbol = transition[1]
            if symbol == '&' or len(self.transitions[transition]) != 1:
                return True
        return False

    def __or__(self, other):
        new_fa = FiniteAutomata()

        # As the previous start states have arrows, we have to take them out
        # before showing the results to the user.
        self.initial_state.label = self.initial_state.label[2:]
        other.initial_state.label = other.initial_state.label[2:]

        new_fa.states = self.states | other.states | {new_fa.initial_state}
        new_fa.transitions = self.transitions | other.transitions
        new_fa.transitions[(new_fa.initial_state, '&')] = {self.initial_state, other.initial_state}

        return new_fa

    def __str__(self):
        """Shows a Finite Automata as its transition table."""
        table = PrettyTable()
        table.field_names = ['Transition', 'Arrival']

        for key, value in self.transitions.items():

            state = str(key[0])
            symbol = key[1]
            transition = (state, symbol)

            # Gathers all possible destiny state labels, as we can have more than one.
            arrival = {str(s) for s in value}

            table.add_row([transition, arrival])
        return str(table)
