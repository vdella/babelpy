from src import resource_dir
from src.grammars.structures.cfg import ContextFreeGrammar
from ordered_set import OrderedSet
from collections import OrderedDict


def read_grammar_from(filepath) -> ContextFreeGrammar:
    with open(resource_dir / filepath, 'r') as f:
        lines = f.readlines()

    trimmed = __trim(lines)

    productions = OrderedDict()
    for production in trimmed:
        non_terminal = production[0]  # Expected to always be non-terminal.
        productions[non_terminal] = set(production[1:])  # Without '->', only productions are left in the line.

    terminals = set()
    non_terminals = OrderedSet([non_terminal for non_terminal in productions.keys()])
    for _, arrival in productions.items():
        unified = ''.join(arrival)  # In order to avoid O(n^3), turns the list into a single string...

        for symbol in unified:  # And searches its insides, symbol by symbol.
            if symbol.islower():
                terminals |= {symbol}
            elif symbol.isupper():
                non_terminals |= {symbol}

    return ContextFreeGrammar(non_terminals, terminals, productions)


def __trim(lines) -> list:
    """Removes arrows and slashes from :param lines."""
    trimmed = list()

    for line in lines:
        correted = line.replace('->', '').replace('|', '').split()
        trimmed.append(correted)

    return trimmed


if __name__ == '__main__':
    grammar = read_grammar_from('reduced_grammar2.txt')
    print(grammar)

    for key, value in grammar.first().items():
        if key.isupper():
            print(key, value)

    print()

    for key, value in grammar.follow().items():
        print(key, value)

    # grammar2 = read_grammar_from('reduced_grammar2.txt')
    # print(grammar2)
