from src.grammars.structures.cfg import ContextFreeGrammar
from src import resource_dir
from src.grammars.persistency.reader import read_grammar_from


def write(cfg: ContextFreeGrammar, filename='generated_grammar.txt'):
    with open(resource_dir / filename, 'w') as f:
        f.write(str(cfg))


if __name__ == '__main__':
    grammar = read_grammar_from('a_even_b_even.txt')
    print(grammar)
    write(grammar)
