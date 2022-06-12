operators = {'*', '.', '|', '+', '?'}
parenthesis = {'(', ')'}
non_terminals = operators | parenthesis


def eat(regex) -> list and set:
    """Eats a non formatted regex and returns its list digested form
    with its terminal symbols."""
    if regex[-1] == '#':
        digest = __trim_blank_spaces(regex)
    else:
        digest = __trim_blank_spaces(regex) + '#'
    digest = __add_missing_concatenations(digest)
    return list(digest), __terminals_from(digest)


def __add_missing_concatenations(regex):
    """Gets a simple regex and reads it char-by-char; those that are not accompanied
    by the concatenation operator will have it added."""
    stripped = list(regex)
    for i in range(len(stripped)):
        if stripped[i] not in operators - {'.'} and stripped[i] not in parenthesis \
                and not __non_terminal_surrounded(regex, i) and not __left_parenthesis_surrounded(regex, i):
            stripped[i] = '.' + stripped[i]
    return ''.join(stripped)  # Turns a list of strings into a single string.


def __non_terminal_surrounded(regex: str, place) -> bool:
    """Checks if a character is surrounded by non-terminals by any of its sides."""
    return regex[place - 1] in non_terminals and regex[place + 1] in non_terminals


def __left_parenthesis_surrounded(regex: str, place) -> bool:
    """As the missing concatenations will be added by the left of a symbol,
    we have to avoid adding concatenations at its left if there is a '('."""
    return regex[place - 1] == '(' and regex[place] in __terminals_from(regex)


def __terminals_from(regex) -> set:
    """Scans a regex and gathers its terminals inside a set."""
    terminals = set()

    for symbol in regex:
        if symbol not in operators and symbol not in parenthesis:
            terminals.add(symbol)
    return terminals


def __trim_blank_spaces(regex: str) -> str:
    return regex.replace(' ', '')


if __name__ == '__main__':
    print(__terminals_from('(ab)*abb'))
    print(__left_parenthesis_surrounded('(ab)*abb', 1))
    print(eat('(a|b)*abb'))
