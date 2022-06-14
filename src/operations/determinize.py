from src.parsing.fa import parse_fa_from
from src.structures.automata.fa import FiniteAutomata
from src import resource_dir
from src.structures.automata.state import State


__state_cache = dict()


class Determinator:

    def __init__(self, fa: FiniteAutomata):
        self.fa = fa
        self.epsilon_transition = dict()
        self.epsilon_fecho = dict()
        self.determinate_fa()

    def determinate_fa(self):
        symbols = self.fa_symbols()

        if '&' in symbols:
            self.create_epsilon_fecho()
            self.epsilon_fa()
        else:
            for _ in range(10):
                new_states = set()

                for key, value in self.fa.transitions.items():

                    if len(value) > 1:
                        new_label = ''.join([str(i) for i in value])
                        new_states.add(State(new_label))

                self.create_new_states(new_states)

    def create_new_states(self, new_list):
        for i in new_list:
            new_state = State(i)
            self.fa.states.add(new_state)
            self.add_transitions(new_state)

    def add_transitions(self, new_state: State):
        new_state_label = str(new_state)

        for i in self.fa_symbols():
            new_destiny = None

            for transition, arrival in self.fa.transitions.items():
                src_state, symbol = transition

                for state in new_state_label:
                    if src_state == State(state) and symbol == i and new_destiny is None:
                        new_destiny = arrival
                    elif src_state == State(state) and symbol == i and new_destiny is not None:
                        new_destiny |= arrival

            self.fa.transitions[(new_state, i)] = new_destiny

    def fa_symbols(self):
        symbols = set()

        for key in self.fa.transitions.keys():
            symbols.add(key[1])

        return symbols

    def create_epsilon_fecho(self):
        # cria dicionario com E-fecho de todos os estados do automado
        states = self.fa.states

        for transition, arrival in self.fa.transitions.items():
            gatherer = list()
            src_state, symbol = transition

            if symbol == '&':
                if symbol in arrival:
                    for i in arrival:
                        gatherer.append(i)
                    self.epsilon_transition[src_state] = gatherer
                else:
                    gatherer.append(src_state)

                    for i in arrival:
                        if str(i) != '':
                            gatherer.append(i)
                    self.epsilon_transition[src_state] = gatherer

        for state in states:
            i = 1
            x = self.epsilon_transition[state]
            while i < len(x):
                for j in self.epsilon_transition[x[i]]:
                    x.append(j)
                    x = list(dict.fromkeys(x))
                i = i + 1
            self.epsilon_fecho[state] = x

    # inicia a criação de um proximo automato apenas com transiçoes por E-fecho
    def epsilon_fa(self) -> FiniteAutomata:
        symbols = self.fa_symbols()
        initial_state_fecho = self.epsilon_fecho[self.fa.initial_state]
        label = str()

        for x1 in initial_state_fecho:
            label = label + x1.label

        initial_state = State(label)

        new_fa = FiniteAutomata()
        new_fa.initial_state = initial_state
        new_fa.states = {initial_state}

        self.create_transition_epsilon(initial_state, new_fa)

        # esse range seria a parte recursiva para criar novos estados, esta assim para testes menores
        for irange in range(4):
            new_states = list()
            for key, value in new_fa.transitions.items():
                new_label = ''.join([str(i) for i in value])
                new_states.add(State(new_label))

            new_states = list(dict.fromkeys(new_states))

            print(new_states)

            for i in new_states:
                if not(i is None):
                    i = i.replace('->', '')
                    new_state = State(i)
                    new_fa.states.add(new_state)
                    self.create_transition_epsilon(new_state, new_fa)

        # self.fa = new_fa
        # save(new_fa)

        for h in new_fa.states:
            print(h.label)

        for key, value in new_fa.transitions.items():
            print(str(key[0]))
            print(key[1])
            for v in value:
                print(str(v))

    # em teoria os proximos dois defs deverian transformar uma transição por 0 por exemplo
    # em um estado para saber se ele ja existe
    def transition_to_state_epsilon(self, malformed_state: str, new_fa):
        state = ''.join(sorted(malformed_state))
        state = state.replace('->', '')
        if state.__contains__('*'):
            state = state.replace('*', '')
            state = "*" + state
            if not (self.already_exists_epsilon(state, new_fa)):
                return state
        elif state.__contains__('->'):
            state = state.replace('->', '')
            if not (self.already_exists_epsilon(state, new_fa)):
                return state

    def already_exists_epsilon(self, verify_state: str, new_fa):
        for state in new_fa.states:
            if state.label == verify_state:
                return True
        return False

    # a partir do estado atual cria as transições para o proximo estado por todos os simbolos
    def create_transition_epsilon(self, new_state: State):
        new_state_label: str = new_state.label
        symbols = self.fa_symbols()
        symbols.remove('&')

        for i in symbols:
            new_destiny = None
            new_epsilon_destiny = set()
            for transition, arrival in self.fa.transitions.items():
                src_state, symbol = transition

                if symbol != '&':
                    for state in new_state_label:
                        if src_state == state and symbol == i and new_destiny is None:
                            new_destiny = arrival
                        elif src_state == state and symbol == i and new_destiny:
                            new_destiny |= arrival

            for s in new_destiny:
                if str(s) != '':
                    new_epsilon_destiny.add(self.epsilon_fecho[s])


if __name__ == '__main__':
    fa1 = parse_fa_from(resource_dir / 'simple_nfa.txt')
    print(fa1)
    x = Determinator(fa1)
    print(x.determinate_fa())

