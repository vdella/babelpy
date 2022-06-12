operators = {'*', '.', '|', '+', '?'}
parenthesis = {'(', ')'}
non_terminals = operators | parenthesis


def eat(regex) -> list and set:
    """Eats a non formatted regex and returns its list digested form
    with its terminal symbols."""

    if len(regex) == 1:
        # If a regex is 1 char long, that regex is already digested.
        return [regex], {regex}

    if regex[-1] == '#':  # No need to add # if the regex already has it.
        digest = __trim_blank_spaces(regex)
    else:
        digest = __trim_blank_spaces(regex) + '#'

    digest = __add_missing_concatenations(digest)
    return list(digest), __terminals_from(digest) | {'&'}


def __add_missing_concatenations(regex):
    stripped = list(regex.replace('.', ''))
    concatenated = '.'.join(stripped)  # Join all strings in a list of strings with periods.

    # As we added '.' between every string, we need to trim the wrong additions.
    return concatenated.replace('(.', '(').replace('.)', ')').replace('.|.', '|').replace('.*', '*').replace('.?', '?')


def __non_terminal_surrounded(regex: str, place) -> bool:
    """Checks if a character is surrounded by non-terminals by any of its sides."""
    before = regex[place - 1]

    if place == len(regex) - 1:  # Checks if 'place' is at the regex' final position.
        return False

    after = regex[place + 1]

    return before in non_terminals and after in non_terminals


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


def sides_for(operator, regex):
    """:returns the inner regexes of a :param regex
    at the side of a given :param operator"""

    left_tree, right_tree = str(), str()
    parenthesis_count = 0

    for i in range(len(regex) - 1, -1, -1):  # We'll be looking from right to left.
        if regex[i] == operator and parenthesis_count == 0:
            left_tree = regex[:i]
            return left_tree, right_tree[::-1]

        if regex[i] == ')':
            parenthesis_count += 1
        elif regex[i] == '(':
            parenthesis_count -= 1

        right_tree += regex[i]

    return left_tree, right_tree[::-1]


def __trim_blank_spaces(regex: str) -> str:
    return regex.replace(' ', '')

