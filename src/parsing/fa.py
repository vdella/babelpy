from src.structures.automata.fa import FiniteAutomata
from src.exceptions.MalformedFileError import MalformedFileError
from src.structures.automata.state import State
from src import resource_dir
from src.parsing.loader import save

__state_cache = dict()


def parse_fa_from(filepath: str) -> FiniteAutomata:
    with open(filepath) as f:
        raw_fa = list(f)
        cleaned: list = __strip_blank_line(raw_fa)
        __verify(cleaned)

    finite_automata = FiniteAutomata()

    str_states = cleaned[1: cleaned.index('*transitions')]

    for s in str_states:
        if s.__contains__('->'):  # Adds initial state...
            state_ref = State(s)
            finite_automata.initial_state = state_ref
            finite_automata.states = {finite_automata.initial_state}
            __state_cache[s[2:]] = finite_automata.initial_state  # Holds label without arrow.

        elif s.__contains__('*'):  # ... And final states.
            state_ref = State(s)
            finite_automata.final_states |= {state_ref}
            finite_automata.states |= finite_automata.final_states
            __state_cache[s[1:]] = state_ref  # Holds label without star.

        else:  # Add rest of states that are not initial nor final.
            state_ref = State(s)
            finite_automata.states |= {state_ref}
            __state_cache[s] = state_ref  # Cuts nothing from label as it does not have an arrow nor a star.

    str_transitions = cleaned[cleaned.index('*transitions') + 1:]
    for raw_line in str_transitions:
        # Raw line as 'src input -> dst'.
        digested_line = raw_line.split()

        # We have to search for references inside the dict cache.
        src = __state_cache[digested_line[0]]
        input_symbol = digested_line[1]
        dst = search_states(digested_line[3:])
        finite_automata.transitions[(src, input_symbol)] = dst

    # for state in finite_automata.states:
    #     print(str(state))

    return finite_automata


def search_states(label_list) -> set:
    """In case it is NFA, we will have more than one destiny state,
    thus we need to search the cache to gather the wanted ones and put
    them in a set. In case there is no destination, returns a set
    with a string stating that aren’t any destiny states.

    :param label_list as the list of state labels to gather references inside
    the dict state cache.
    :returns a set containing the state references from within the cache."""
    result = set()

    for label in label_list:
        if __state_cache[label]:
            result |= {__state_cache[label]}
    return result if result else {''}


def __strip_blank_line(file_lines: list) -> list:
    cleaned = list()
    for line in file_lines:
        cleaned.append(line.replace('\n', ''))
    return cleaned


def __verify(file_lines: list):
    """Verifies if a given file is organized according
    to the project's artifact standards.

    :param: file_lines: as the lines of an already opened file.
    :return: nothing if the file is in good shape. Else, raises
    an exception to indicate a malformed file."""

    # Needs to check the preambles. The file needs '*states' and '*transitions' preambles.
    if not file_lines.__contains__('*states') or not file_lines.__contains__('*transitions'):
        raise MalformedFileError('File does not have preambles.')

    declared_states = file_lines[1:file_lines.index('*transitions')]

    # The file has to include one, and only one, initial state for the automata.
    initial_states = 0
    for s in declared_states:
        if s.__contains__('->'):
            initial_states += 1

    if initial_states != 1:
        raise MalformedFileError('Incorrect initial state quantity.')


if __name__ == '__main__':
    fa1 = parse_fa_from(resource_dir / 'simple_nfa.txt')
    print(fa1.is_nfa())

    fa2 = parse_fa_from(resource_dir / 'ab_with_last_equals_first.txt')
    print(fa2.is_nfa())

    # print(fa1 | fa2)
    save(fa1 | fa2)
    print(parse_fa_from(resource_dir / 'generated_fa.txt'))
