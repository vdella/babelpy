from src.automata.structures.fa import FiniteAutomata
from src import resource_dir


def write(fa: FiniteAutomata, filename='generated_fa.txt'):
    with open(resource_dir / filename, 'w') as f:
        f.write('#states\n')
        for state in fa.states:
            f.write('{}\n'.format(state))

        f.write('#initial\n')
        f.write('{}\n'.format(fa.initial_state))

        f.write('#final\n')
        for final in fa.final_states:
            f.write('{}\n'.format(final))

        f.write('#transitions\n')
        for transition, arrival in fa.transitions.items():
            src_state, symbol = transition
            f.write('{} {} -> '.format(src_state, symbol))

            destinies = list(arrival)
            for destiny in destinies:
                if destiny == destinies[-1]:
                    f.write('{}\n'.format(destiny))
                else:
                    f.write('{} '.format(destiny))
