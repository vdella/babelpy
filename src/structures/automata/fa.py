from src.structures.state import initial_state, State


class FiniteAutomata:

    def __init__(self):
        self.states = set()
        self.transitions = dict()
        self.initial_state = initial_state()
        self.final_states = set()

    def read(self, sentence: str) -> bool:
        """Iteratively loops over a transition table and
        checks if a final state can be reached from the given input."""

        cached_state = self.initial_state

        for symbol in sentence:
            for state in self.transitions[(cached_state, symbol)]:
                cached_state = state

        return cached_state in self.final_states

    def __or__(self, other):
        # if isinstance(other, FiniteAutomata):
        #     # TODO add decorator.
        #     raise TypeError('Comparison between {} and {}'.format(type(FiniteAutomata), type(other)))

        new_fa = FiniteAutomata()

        new_fa.initial_state = State(0)
        self.__update_ids_from(1)
        other.__update_ids_from(len(self.states) + 1)

        new_fa.states = self.states | other.states

        new_fa.transitions = self.transitions | other.transitions
        new_fa.transitions[(new_fa.initial_state, '&')] = {self.initial_state, other.initial_state}

        return new_fa

    def __update_ids_from(self, seed: int):
        for state in self.states:
            state.identifier += seed
