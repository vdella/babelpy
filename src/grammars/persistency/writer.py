from src.grammars.structures.cfg import ContextFreeGrammar
from src import resource_dir
from src.grammars.persistency.reader import read_grammar_from


def write(cfg: ContextFreeGrammar, filename='generated_grammar.txt'):
    with open(resource_dir / filename, 'w') as f:
        f.write('#start\n')
        f.write('{}\n'.format(cfg.start))

        f.write('#non-terminals\n')
        for non_terminal in cfg.non_terminals:
            f.write('{}\n'.format(non_terminal))

        f.write('#terminals\n')
        for terminal in cfg.terminals:
            f.write('{}\n'.format(terminal))

        f.write('#productions\n')
        f.write(str(cfg))


if __name__ == '__main__':
    grammar = read_grammar_from('simple_grammar_recursion.txt')
    reduced = grammar.left_recursion()
    # print(reduced)
    reduced.factor()
    write(reduced)
