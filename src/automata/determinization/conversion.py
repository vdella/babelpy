from src.automata.structures.fa import FiniteAutomata
from src.automata.parsing.parser import parse_fa_from
from src import resource_dir
from src.automata.structures.state import State
from src.automata.parsing.loader import save


def determinize(nfa) -> FiniteAutomata:
    result = FiniteAutomata()

    closured_states = closure_states_for(nfa)

    result.initial_state = closured_states[nfa.initial_state]
    result.states = {result.initial_state}

    stack = {closured_states[nfa.initial_state]}

    while stack:
        top = stack.pop()

        for pair, arrival in transitions_for(nfa, top).items():
            if pair not in result.transitions.keys():
                result.transitions[pair] = {arrival}
                result.states |= {arrival}
                stack.add(arrival)

    result.final_states = finals(nfa.final_states, result.states)
    remove_useless_states_from(result)
    return result


def finals(old_finals: set, all_states: set) -> set:
    final_states = set()

    for oldie in old_finals:
        for newly in all_states:
            if oldie.label in newly.label:
                final_states |= {newly}

    return final_states


def remove_useless_states_from(automata: FiniteAutomata):
    """Removes empty transitions and states without labels
    from the :param automata."""
    copy = dict(automata.transitions)

    for transition, arrrival in copy.items():
        state, symbol = transition

        for destiny in arrrival:
            if symbol == '&' or destiny.label == '':
                del automata.transitions[transition]

        if state.label == '':
            automata.states.discard(state)


def closure_states_for(nfa: FiniteAutomata) -> dict:
    closure_states = dict()
    epsilon_closure: dict = epsilon_closure_from(nfa)

    for src, dst in epsilon_closure.items():
        state = squash(dst)
        closure_states[src] = state

    return closure_states


def squash(states: set) -> State:
    """Digests a :param state set: into a single :return state."""
    label = sorted([state.label for state in states])
    squashed = ''.join(label)
    return State(squashed)


def epsilon_closure_from(nfa: FiniteAutomata) -> dict:
    stack = [s for s in nfa.states]

    epsilon_closure = {state: {state} for state in nfa.states}
    empty_transitions = empty_transitions_from(nfa)

    while stack:
        top = stack.pop()

        for state in empty_transitions[top]:
            if state not in epsilon_closure[top]:
                epsilon_closure[top] |= {state}
                stack.append(state)

    return epsilon_closure


def empty_transitions_from(nfa):
    empty_transitions = {state: set() for state in nfa.states}

    for transition, arrival in nfa.transitions.items():
        src_state, symbol = transition

        if symbol == '&':
            empty_transitions[src_state] |= arrival

    return empty_transitions


def transitions_for(nfa, state: State) -> dict:
    """Gathers every possible transition from a :param state
    in the given :param nfa."""
    transitions = dict()

    for s in nfa.symbols():
        new_destiny = set()

        for transition, arrival in nfa.transitions.items():
            src_state, symbol = transition

            for label in state.label:
                if src_state == State(label) and symbol == s:
                    new_destiny |= arrival

        transitions[(state, s)] = squash(new_destiny)

    return transitions


if __name__ == '__main__':
    fa = parse_fa_from(resource_dir / 'simple_nfa.txt')

    fa = determinize(fa)
    print(fa)

    save(fa)
