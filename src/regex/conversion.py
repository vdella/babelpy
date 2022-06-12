from src.regex.tree import SyntaxTree
from src.structures.automata.fa import FiniteAutomata, State


def fa_from(regex) -> FiniteAutomata:
    result = FiniteAutomata()

    tree = SyntaxTree(regex)
    final_states_id = str(tree.root.right.serial_number)

    tree.root.calculate_follow_pos()

    unmarked = [tree.root.first_pos()]
    d_states = [tree.root.first_pos()]

    initial_state_not_set = True

    while unmarked:
        first_pos = unmarked.pop(0)

        for terminal in tree.terminals:
            gatherer = set()

            for node in first_pos:
                if node.regex_symbol == terminal:
                    gatherer |= node.follow_pos

            src_state = __squash_into_state(first_pos)
            dst_state = __squash_into_state(gatherer)

            if gatherer not in d_states:
                d_states.append(gatherer)
                unmarked.append(gatherer)

                if initial_state_not_set:
                    result.initial_state = src_state
                    initial_state_not_set = False

                result.states |= {src_state} | {dst_state}

                if final_states_id in src_state.label:
                    result.final_states |= {src_state}
                if final_states_id in dst_state.label:
                    result.final_states |= {dst_state}

            if not result.transitions.get((src_state, terminal)):
                result.transitions[(src_state, terminal)] = {dst_state}

    __remove_useless_states(result)

    return result


def __remove_useless_states(fa: FiniteAutomata):
    cached_transitions = dict(fa.transitions)  # Copy as we will change the size of fa.transactions during iteration.

    for key in cached_transitions.keys():
        state, symbol = key

        # The resulting automata will always be deterministic. Thus, the destiny set of states contains only one.
        # If that said destiny state has an empty string as a label, it's useless and needs to be removed.
        arrival = list(cached_transitions[key])[0]

        if state.label == '' or symbol == '#' or arrival.label == '':
            del fa.transitions[key]


def __squash_into_state(nodes: set) -> State:
    """:param nodes: as the symbols from the first_pos() of a node.
    :returns: a state with all symbols joined by '-' as labels."""
    string = [str(node.serial_number) for node in nodes]
    string.sort()

    label = ''.join(string)
    return State(label)


if __name__ == '__main__':
    fa2 = fa_from('b?(ab)*a?')
    print(fa2)
