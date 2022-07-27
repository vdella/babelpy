from src import resource_dir
from src.grammars.structures.cfg import ContextFreeGrammar
# from src.grammars.pattern_matching import find_terminal


def read_grammar_from(filepath) -> ContextFreeGrammar:
    with open(resource_dir / filepath, 'r') as f:
        lines = f.readlines()

    trimmed = [line.rstrip() for line in lines]

    start = __start_symbol_from(trimmed)
    non_terminals = __non_terminals_from(trimmed)
    terminals = __terminals_from(trimmed)
    productions = __digest_productions_from(trimmed)

    return ContextFreeGrammar(non_terminals, terminals, productions, start)


def __start_symbol_from(lines):
    return lines[lines.index('#start') + 1]


def __non_terminals_from(lines):
    return {symbol for symbol in lines[lines.index('#non-terminals') + 1: lines.index('#terminals')]}


def __terminals_from(lines):
    return {symbol for symbol in lines[lines.index('#terminals') + 1: lines.index('#productions')]}


def __digest_productions_from(lines):
    productions = dict()

    for production in lines[lines.index('#productions') + 1:]:
        line_without_arrow = production.replace(' ', '').split('->')
        non_terminal = line_without_arrow[0]  # Expected to always be non-terminal.
        digested_line = ''.join(line_without_arrow[1:]).split('|')
        productions[non_terminal] = list(digested_line)

    return productions


def __show_first_from(cfg):
    for key, value in cfg.first().items():
        if key.isupper():
            print(key, value)
    print()


def __show_follow_from(cfg):
    for key, value in cfg.follow().items():
        if key.isupper():
            print(key, value)
    print()


if __name__ == '__main__':
    grammar = read_grammar_from('simple_grammar_recursion.txt')
    print(grammar)

    reduced = grammar.left_recursion()
    print(reduced.non_terminals)
    print(reduced)

    reduced.factor()
    print(reduced)
    print(reduced.non_terminals)

    __show_first_from(reduced)
