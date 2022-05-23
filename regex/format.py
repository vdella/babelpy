def eat(regex):
    """Eats a non formatted regex and returns its digested form
    with its terminal symbols."""
    digest = __trim_blank_spaces(regex)
    return digest, __terminals_from(digest)


def __terminals_from(regex: str) -> set:
    terminals = set()

    operators = {'*', '.', '+', '|'}
    parenthesis = {'(', ')'}

    for symbol in regex:
        if symbol not in operators and symbol not in parenthesis:
            terminals.add(symbol)
    return terminals


def __trim_blank_spaces(regex: str) -> str:
    return regex.replace(' ', '')


if __name__ == '__main__':
    print(eat('(a | b)*abb'))
