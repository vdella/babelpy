from src.regex.tree import SyntaxTree, Node
from src.structures.automata.fa import FiniteAutomata, State


def fa_from(regex) -> FiniteAutomata:
    result = FiniteAutomata()

    tree = SyntaxTree(regex)
    tree.root.gen_follow_pos()

    unmarked = [tree.root.first_pos()]
    d_states = [tree.root.first_pos()]

    while unmarked:
        print('Before: ' + str(unmarked))
        first_pos = unmarked.pop(0)
        print('After: ' + str(unmarked))

        for terminal in tree.terminals:
            gatherer = set()

            for node in first_pos:
                if node.symbol == terminal:
                    gatherer |= node.follow_pos

            src_state = __squash_into_state(first_pos)
            dst_state = __squash_into_state(gatherer)

            if gatherer not in d_states:
                d_states.append(gatherer)
                unmarked.append(gatherer)
                result.states |= {src_state} | {dst_state}

            if not result.transitions.get((src_state, terminal)):
                result.transitions[(src_state, terminal)] = {dst_state}

            # TODO needs to reformat automata before return.
    __remove_hashtag_from(result)
    print(len(result.transitions))
    return result


def __remove_hashtag_from(fa: FiniteAutomata):
    cached_transitions = dict(fa.transitions)

    for key in cached_transitions.keys():
        _, symbol = key
        if symbol == '#':
            del fa.transitions[key]


def __squash_into_state(nodes: set) -> State:
    """:param nodes: as the symbols from the first_pos() of a node.
    :returns: a state with all symbols joined by '-' as labels."""
    string = list()
    for node in nodes:
        string.append(node.symbol)
    label = '-'.join(string)
    return State(label)


if __name__ == '__main__':
    fa1 = fa_from('(a|b)*abb#')
    print(fa1)

