from src.main.structures.automata.fa import FiniteAutomata
from src.main.exceptions.MalformedFileError import MalformedFileError
from src.main.structures.state import State
from src.main import resource_dir


def parse_fa_from(filepath: str) -> FiniteAutomata:
    with open(filepath) as f:
        raw_fa = list(f)
        cleaned: list = __strip_blank_line(raw_fa)
        __verify(cleaned)

    finite_automata = FiniteAutomata()  # To be completed.

    str_states = cleaned[1:cleaned.index('*transitions')]

    i = 0
    for s in str_states:
        if s.__contains__('->'):  # Adds initial state...
            finite_automata.initial_state = State(i, s)
            finite_automata.states |= {finite_automata.initial_state}

        elif s.__contains__('*'):  # ... And final states.
            finite_automata.final_states |= {State(i, s)}
            finite_automata.states |= finite_automata.final_states

        else:  # Add rest of states that are not initial nor final.
            finite_automata.states |= {State(i, s)}
        i += 1

    str_transitions = cleaned[cleaned.index('*transitions') + 1:]
    for raw_line in str_transitions:
        # Raw line as 'src input -> dst'.
        digested_line = raw_line.split()
        src_state_label = digested_line[0]
        input_symbol = digested_line[1]
        dst_state_label = digested_line[3]
        finite_automata.transitions[(src_state_label, input_symbol)] = dst_state_label

    return finite_automata


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
    fa1 = parse_fa_from(resource_dir / 'simple_five_states.txt')
    fa2 = parse_fa_from(resource_dir / 'ab_with_last_equals_first.txt')
    print(fa1 | fa2)
