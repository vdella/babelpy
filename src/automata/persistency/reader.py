from src.automata.structures.fa import FiniteAutomata
from src.exceptions.MalformedFileError import MalformedFileError
from src.automata.structures.state import State
from src import resource_dir
from src.automata.persistency.writer import write

__state_cache = dict()


def read_fa_from(filepath: str) -> FiniteAutomata:
    with open(resource_dir / filepath) as f:
        raw_fa = list(f)
        cleaned: list = __strip_blank_line(raw_fa)
        __verify(cleaned)

    fa = FiniteAutomata()

    fa.states = {State(s) for s in cleaned[1: cleaned.index('#initial')]}
    fa.initial_state = State(cleaned[cleaned.index('#initial') + 1])
    fa.final_states = {State(s) for s in cleaned[cleaned.index('#final') + 1: cleaned.index('#transitions')]}

    __populate_state_cache_from(fa)

    str_transitions = cleaned[cleaned.index('#transitions') + 1:]
    for raw_line in str_transitions:
        # Raw line as 'src input -> dst'.
        digested_line = raw_line.split()

        # We have to search for references inside the dict cache.
        src = __state_cache[digested_line[0]]
        input_symbol = digested_line[1]
        dst = search_states(digested_line[3:])
        fa.transitions[(src, input_symbol)] = dst

    return fa


def __populate_state_cache_from(fa: FiniteAutomata) -> dict:
    """Saves a record of :param fa: state inside the cache by using its label as key."""
    for state in fa.states:
        __state_cache[state.label] = state

    return __state_cache


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
    if '#states' not in file_lines or '#initial' not in file_lines\
            or '#final' not in file_lines or '#transitions' not in file_lines:
        raise MalformedFileError('File does not have preambles.')

    # The file has to include one, and only one, initial state for the automata.
    initial_states = file_lines[file_lines.index('#initial') + 1: file_lines.index('#final')]

    if len(initial_states) != 1:
        raise MalformedFileError('Incorrect initial state quantity.')


if __name__ == '__main__':
    fa1 = read_fa_from('simple_nfa.txt')
    # print(fa1)
    # print(fa1.is_nfa())

    fa2 = read_fa_from('ab_with_last_equals_first.txt')
    # print(fa2)
    # print(fa2.is_nfa())

    print(fa1 | fa2)
    write(fa1 | fa2)
    print(read_fa_from('generated_fa.txt'))