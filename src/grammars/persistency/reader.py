from src import resource_dir
from src.grammars.cfg import ContextFreeGrammar


def read_grammar_from(filepath) -> ContextFreeGrammar:
    with open(resource_dir / filepath, 'r') as f:
        lines = f.readlines()

    trimmed = __trim(lines)

    productions = dict()
    for production in trimmed:
        non_terminal = production[0]  # Expected to always be non-terminal.
        productions[non_terminal] = set(production[1:])  # Without '->', only productions are left in the line.

    terminals = set()
    non_terminals = set()
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


def verify(grammar):
    # TODO implement.
    pass


if __name__ == '__main__':
    grammar = read_grammar_from('a_even_b_even.txt')
    print(grammar.terminals)
    print(grammar.non_terminals)
    print(grammar.symbols)
    print(grammar)
