from src.grammars.persistency.reader import read_grammar_from, ContextFreeGrammar


def organize(grammar):
    incorrects = unknown_symbols_for(grammar)
    productions = production_lists_from(grammar)

    for entry in incorrects:
        key, outer, body, inner, element = entry

        inc, previous = 0, str()
        while previous not in grammar.symbols:
            inc += 1
            print(body[inner - inc: inner + inc])
            previous = str().join(body[inner - inc: inner + inc])

        print(productions[key][outer])
        to_be_removed = body[inner - inc: inner + inc]
        print(inner)
        print(to_be_removed)
        print()
        # productions[key][outer].remove(to_be_removed)
        # productions[key][outer] += previous

    # print(productions)


def unknown_symbols_for(grammar):
    incorrects = list()

    for key, value in production_lists_from(grammar).items():
        for i, symbols in enumerate(value):
            for j, symbol in enumerate(symbols):
                if symbol not in grammar.symbols:
                    incorrects.append((key, i, symbols, j, symbol))

    return incorrects


def production_lists_from(grammar: ContextFreeGrammar):
    productions = {non_terminal: list() for non_terminal in grammar.non_terminals}

    for key, value in grammar.productions.items():
        stripped = list()
        for i, body in enumerate(value):
            stripped.append(list(body))
            productions[key] += stripped

    return productions


if __name__ == '__main__':
    grammar1 = read_grammar_from('ll1.txt')
    print(grammar1)
    # print(grammar1.productions)
    # print(production_lists_from(grammar1))
    # print(unknown_symbols_for(grammar1))
    organize(grammar1)
