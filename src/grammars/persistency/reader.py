from src import resource_dir
from src.grammars.structures.cfg import ContextFreeGrammar


def read_grammar_from(filepath) -> ContextFreeGrammar:
    with open(resource_dir / filepath, 'r') as f:
        lines = f.readlines()

    trimmed = [line.rstrip() for line in lines]

    start = trimmed[trimmed.index('#start') + 1]
    non_terminals = {symbol for symbol in trimmed[trimmed.index('#non-terminals') + 1: trimmed.index('#terminals')]}
    terminals = {symbol for symbol in trimmed[trimmed.index('#terminals') + 1: trimmed.index('#productions')]}

    productions = dict()
    for production in trimmed[trimmed.index('#productions') + 1:]:
        line_without_arrow = production.replace(' ', '').split('->')
        non_terminal = line_without_arrow[0]  # Expected to always be non-terminal.
        digested_line = ''.join(line_without_arrow[1:]).split('|')
        productions[non_terminal] = set(digested_line)

    return ContextFreeGrammar(non_terminals, terminals, productions, start)


def __show_first_from(cfg):
    for key, value in cfg.first().items():
        if key.isupper():
            print(key, value)
    print()


if __name__ == '__main__':
    # grammar1 = read_grammar_from('a_even_b_even.txt')
    # print(grammar1)
    # __show_first_from(grammar1)

    # grammar2 = read_grammar_from('reduced_grammar2.txt')
    # print(grammar2)
    # print(grammar2.nullable())
    # __show_first_from(grammar2)

    grammar3 = read_grammar_from('ll1.txt')
    print(grammar3)
    __show_first_from(grammar3)
