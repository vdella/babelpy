from src.parsing.fa import parse_fa_from
from src.structures.automata.fa import FiniteAutomata
from src import resource_dir
from src.structures.automata.state import State
from src.parsing.loader import save


__state_cache = dict()


class Determinization:
    def __int__(self, fa: FiniteAutomata):
        self.fa = fa
        self.epsilon_transition = dict()
        self.epsilon_fecho = dict()
        self.determinize_automata()

    def determinize_automata(self):
        symbols = self.get_symbols()
        if '&' in symbols:
            self.create_epsilon_fecho()
            self.new_epsilon_autamata()

        else:
            for irange in range(10):
                new_states = list()
                for key, value in self.fa.transitions.items():
                    if len(value) > 1:
                        novo_estado = ''
                        for i in value:
                            novo_estado += str(i)
                        novo_estado = novo_estado.replace('->', '')
                        novo_estado = self.transition_to_state(novo_estado)
                        if not (novo_estado is None):
                            new_states.append(novo_estado)

                new_states = list(dict.fromkeys(new_states))
                self.create_new_states(new_states)

    def create_new_states(self, new_list: list()):
        for i in new_list:
            i = i.replace('->', '')
            new_state = State(i)
            self.fa.states.add(new_state)
            self.add_transactions(new_state)

    def add_transactions(self, new_state: State):
        new_state_label = self.__strip_arrows_and_star_from(new_state)
        new_state_label = sorted(new_state_label)

        for i in self.get_symbols():
            new_destiny = None
            for key, value in self.fa.transitions.items():
                triste = str(key[0]).replace('->', '').replace('*', '')
                for state in new_state_label:
                    if triste == state and key[1] == i and new_destiny is None:
                        new_destiny = value
                    elif triste == state and key[1] == i and not(new_destiny is None):
                        new_destiny = set.union(new_destiny, value)
            self.fa.transitions[(new_state, i)] = new_destiny

    def transition_to_state(self, malformed_state: str):
        state = ''.join(sorted(malformed_state))
        if '*' in state:
            state = state.replace('*', '')
            state = "*" + state
            if not (self.already_exists(state)):
                return state
        elif '->' in state:
            state = state.replace('->', '')
            if not (self.already_exists(state)):
                return state

    def already_exists(self, verify_state: str):
        for state in self.fa.states:
            if state.label == verify_state:
                return True
        return False

    def __strip_arrows_and_star_from(self, state: State):
        written_state = str(state)
        return written_state.replace('->', '').replace('*', '')

    def get_symbols(self):
        symbols = list()
        for key in self.fa.transitions.keys():
            symbols.append(key[1])

        symbols = list(dict.fromkeys(symbols))
        return symbols

    # cria dicionario com E-fecho de todos os estados do automado
    def create_epsilon_fecho(self):
        states = self.fa.states
        for key, value in self.fa.transitions.items():
            lista = list()

            if key[1] == '&':
                if key[0] in value:
                    for i in value:
                        lista.append(i)
                    self.epsilon_transition[key[0]] = lista
                else:
                    lista.append(key[0])
                    for i in value:
                        if not(str(i) == ''):
                            lista.append(i)
                    self.epsilon_transition[key[0]] = lista

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
    def new_epsilon_autamata(self):
        symbols = self.get_symbols()
        initial_state_fecho = (self.epsilon_fecho[self.fa.initial_state])
        label = ''
        for x1 in initial_state_fecho:
            label = label + x1.label
        label = sorted(label)
        label = ''.join(label)
        initial_state = State(label)
        new_fa = FiniteAutomata()
        new_fa.initial_state = initial_state
        new_fa.states = {initial_state}
        self.create_transition_epsilon(initial_state, new_fa)

        # esse range seria a parte recursiva para criar novos estados, esta assim para testes menores
        for irange in range(4):
            new_states = list()
            for key, value in new_fa.transitions.items():
                novo_estado = ''
                for i in value:
                    novo_estado += str(i)
                novo_estado = self.transition_to_state_epsilon(novo_estado, new_fa)
                new_states.append(novo_estado)

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
        if '*' in state:
            state = state.replace('*', '')
            state = "*" + state
            if not (self.already_exists_epsilon(state, new_fa)):
                return state
        elif '->' in state:
            state = state.replace('->', '')
            if not (self.already_exists_epsilon(state, new_fa)):
                return state

    @staticmethod
    def already_exists_epsilon(verify_state: str, new_fa):
        for state in new_fa.states:
            if state.label == verify_state:
                return True
        return False

    # a partir do estado atual cria as transições para o proximo estado por todos os simbolos
    def create_transition_epsilon(self, new_state: State(), new_fa):
        new_state_label = self.__strip_arrows_and_star_from(new_state)
        new_state_label = sorted(new_state_label)
        symbols = self.get_symbols()
        symbols.remove('&')

        for i in symbols:
            new_destiny = None
            new_epsilon_destiny = list()
            for key, value in self.fa.transitions.items():
                if not(key[1] == '&'):
                    triste = str(key[0]).replace('->', '').replace('*', '')
                    for state in new_state_label:
                        if triste == state and key[1] == i and new_destiny is None:
                            new_destiny = value
                        elif triste == state and key[1] == i and not (new_destiny is None):
                            new_destiny = set.union(new_destiny, value)

            for s in new_destiny:
                if not((str(s)) == ''):
                    new_epsilon_destiny.append(self.epsilon_fecho[s])

            flat_list = [x for xs in new_epsilon_destiny for x in xs]
            flat_list = list(dict.fromkeys(flat_list))
            new_fa.transitions[(new_state, i)] = flat_list


if __name__ == '__main__':
    fa1 = parse_fa_from(resource_dir / 'simple_nfa.txt')
    x = Determinization()
    x.__int__(fa1)
    save(fa1)

