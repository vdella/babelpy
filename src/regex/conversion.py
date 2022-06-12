from src.regex.tree import SyntaxTree, show_tree_from
from src.structures.automata.fa import FiniteAutomata, State


def fa_from(regex) -> FiniteAutomata:
    result = FiniteAutomata()

    tree = SyntaxTree(regex)

    show_tree_from(tree.root)

    tree.root.gen_follow_pos()

    unmarked = [tree.root.first_pos()]
    d_states = [tree.root.first_pos()]

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
                result.states |= {src_state} | {dst_state}

            if not result.transitions.get((src_state, terminal)):
                result.transitions[(src_state, terminal)] = {dst_state}

    __remove_useless_states(result)

    return result


def __remove_useless_states(fa: FiniteAutomata):
    cached_transitions = dict(fa.transitions)

    for key in cached_transitions.keys():
        state, symbol = key

        if state.label == '' or symbol == '#':
            del fa.transitions[key]


def __squash_into_state(nodes: set) -> State:
    """:param nodes: as the symbols from the first_pos() of a node.
    :returns: a state with all symbols joined by '-' as labels."""
    string = [str(node.serial_number) for node in nodes]
    string.sort()

    label = ''.join(string)
    return State(label)


if __name__ == '__main__':
    fa1 = fa_from('(a|b)*abb')
    print(fa1)

