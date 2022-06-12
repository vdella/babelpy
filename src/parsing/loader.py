from src.structures.automata.fa import FiniteAutomata
from src import resource_dir


def save(fa: FiniteAutomata, filename='generated.txt'):
    with open(resource_dir / filename, 'w') as f:
        f.write('*states\n')

        for state in fa.states:
            if state == fa.initial_state:
                f.write('{}\n'.format(str(state)))
            elif state in fa.final_states:
                f.write('{}\n'.format(str(state)))
            else:
                f.write(str(state) + '\n')

        f.write('*transitions\n')

        for transition in fa.transitions:
            src = __strip_arrows_and_star_from(transition[0])
            f.write('{} {} -> '.format(src, transition[1]))

            destinies = list(fa.transitions[transition])
            for destiny in destinies:
                dst = __strip_arrows_and_star_from(destiny)
                if destiny == destinies[-1]:
                    f.write('{}\n'.format(dst))
                else:
                    f.write('{} '.format(dst))


def __strip_arrows_and_star_from(state):
    written_state = str(state)
    return written_state.replace('->', '').replace('*', '')
