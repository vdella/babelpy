import copy
import string

#from ordered_set import OrderedSet


class ContextFreeGrammar:
    MAX_FACTOR = 10
    VARIABLES = set(string.ascii_uppercase)

    def __init__(self, non_terminals, terminals, productions: dict, start='S'):
        self.non_terminals = non_terminals
        self.terminals = terminals
        self.symbols: set = self.terminals | self.non_terminals
        self.productions = productions
        self.start = start

    def __str__(self):
        gatherer = str()
        for src, dst in self.productions.items():
            gatherer += '{} -> {}\n'.format(src, ' | '.join(dst))
        return gatherer

    def first(self):
        first = {symbol: set() for symbol in self.symbols}

        # Rules are different for terminals, as they are their own firsts.
        first |= {terminal: {terminal} for terminal in self.terminals}

        nullable = self.nullable()

        def build_for(symbol):
            productions = self.productions[symbol]

            for piece in productions:
                head = piece[0]

                if head in self.terminals or head == '&':  # Whether starts with a terminal or with &.
                    first[symbol] |= {head}
                else:  # Starts with a non-terminal.
                    for letter in piece:
                        if letter in self.non_terminals and not first[letter]:
                            build_for(letter)  # Executes a depth-first search from the given letter.
                        first[symbol] |= first[letter]

                        if not nullable[symbol]:    # & will be added by default if found in other firsts,
                            first[symbol] -= {'&'}  # but it must not be added if the symbol is not itself nullable.
                            break

        # for non_terminal in self.non_terminals:
        for non_terminal in self.non_terminals:
            build_for(non_terminal)

        return first

    def nullable(self):
        """:returns: a (symbol, bool) dictionary built from the grammar.
        Terminals are not nullable by default. Non-terminals will
        be nullable if there is at least one path from which they can find an &."""
        nullable = {symbol: False for symbol in self.symbols}
        visited = {non_terminal: False for non_terminal in self.non_terminals}

        def check(symbol):
            productions = self.productions[symbol]

            for production in productions:
                if production == '&':
                    nullable[symbol] = True
                else:
                    for letter in production:
                        if letter in self.non_terminals and not visited[letter]:
                            visited[letter] = True
                            check(letter)

                    if all([nullable.get(letter) for letter in production]):
                        nullable[symbol] = True

        check(self.start)
        return nullable

    def follow(self):
        follow = {non_terminal: set() for non_terminal in self.non_terminals}
        first = self.first()

        for symbol in self.non_terminals:  # Gathers results from start until end.
            if symbol == self.start:
                follow[symbol] = {'$'}  # The start's follow() is fixed in $ by default.

            productions = self.productions[symbol]

            for production in productions:
                for letter in production:
                    if letter in self.non_terminals:
                        if letter == production[-1]:
                            follow[letter] |= follow[symbol]
                        else:
                            next_pos = production.index(letter) + 1
                            next_letters = production[next_pos:]

                            for next_letter in next_letters:
                                follow[letter] |= first[next_letter] - {'&'}

                                # As there are nullable non-terminals, they are passible of
                                # not happening. In such cases, the actual letter will
                                # receive its next letters follow()s until it find a non-nullable non-terminal.
                                if '&' not in first[next_letter]:
                                    break

        # As we checked every body in normal order, a last checking is needed
        # in order to identify which nullable productions will need its head's set of follow productions.
        nullable = self.nullable()
        for head, body in self.__reversed_nullable_productions().items():
            for piece in body:
                for letter in piece:
                    if letter in self.non_terminals:
                        next_pos = piece.index(letter) + 1
                        next_letter = piece[next_pos: next_pos + 1]

                        if next_letter not in self.terminals and next_letter != piece[-1]:
                            if nullable[letter] and next_letter:
                                if follow.get(next_letter):
                                    # If the actual letter is nullable, its next letter will receive its follow() set.
                                    follow[next_letter] |= follow[head]

        return follow

    def __reversed_nullable_productions(self):
        reversed_productions = {non_terminal: set() for non_terminal in self.non_terminals}

        for non_terminal in self.non_terminals:
            for production in self.productions[non_terminal]:
                if production[-1] in self.non_terminals:  # Checks if the productions ends with a non-terminal.
                    reversed_productions[non_terminal] |= {production[::-1]}

        return reversed_productions

    def get_new_state(self):
        disp = self.VARIABLES - self.non_terminals
        return min(disp)

    def left_recursion(self):
        self.get_new_state()
        # self.eliminate_direct_recursion(self.start)
        self.eliminate_indirect_recursion()

    def eliminate_direct_recursion(self, non_terminal):
        contem = set()
        nao_contem = set()
        new_state = self.get_new_state()
        for production in self.productions[non_terminal]:
            head = production[0]
            tail = production[1:]
            if head == non_terminal:
                contem.add(tail+new_state)
            else:
                nao_contem.add(production+new_state)

        if len(contem) != 0:
            contem.add('&')
            self.non_terminals |= {new_state}
            self.productions[new_state] = contem

            if len(nao_contem) != 0:
                self.productions[non_terminal] = nao_contem
            else:
                nao_contem.add(new_state)
                self.productions[non_terminal] = nao_contem

    def eliminate_indirect_recursion(self):
        non_terminals = list(self.non_terminals)
        i = 0
        stop_condition = True
        new_productions = set()
        prod_to_remove = str()

        while stop_condition:
            for j in range(i):
                for production in list(self.productions[non_terminals[i]]):
                    head = production[0]
                    tail = production[1:]
                    if head == non_terminals[j]:
                        new_productions.clear()
                        new_production = tail
                        for prod_ind in list(self.productions[non_terminals[j]]):
                            new_productions.add(prod_ind + new_production)
                        prod_to_remove = production
                for new_prod in list(new_productions):
                    self.productions[non_terminals[i]].add(new_prod)
                if prod_to_remove and prod_to_remove in self.productions[non_terminals[i]]:
                    self.productions[non_terminals[i]].remove(prod_to_remove)

            self.eliminate_direct_recursion(non_terminals[i])
            i = i + 1
            if i >= len(non_terminals):
                stop_condition = False

    def number_derivation(self):
        productions_non_terminals = set()
        for prod in self.productions:
            productions_non_terminals.add(prod[0])
        productions_non_terminals = list(dict.fromkeys(productions_non_terminals))
        return len(productions_non_terminals)

    def factor(self):
        self.left_recursion()
        iterations = 0
        while iterations < ContextFreeGrammar.MAX_FACTOR:
            # length = self.number_derivation()
            # for _ in range(1):
            self.eliminate_direct_non_determinism()
            self.eliminate_indirect_non_determinism()
            iterations += 1

    def eliminate_direct_non_determinism(self):
        variables = list(self.non_terminals)
        for variable in variables:
            derivations = list(self.productions[variable])
            derivation_to_change = {}
            for derivation in derivations:
                # print(variable)
                # print(derivations)
                head = derivation[0]
                tail = derivation[1:]
                if head not in derivation_to_change:
                    derivation_to_change[head] = []
                derivation_to_change[head].append(tail)
            # print(derivation_to_change)
            for head, tails in derivation_to_change.items():
                already_added = False
                if len(tails) == 1:
                    continue

                productions_new_state = set()
                new_state = self.get_new_state()
                self.productions[new_state] = {}
                for tail in tails:
                    if not already_added:
                        self.productions[variable].add(head + new_state)
                        already_added = True
                    self.non_terminals |= {new_state}
                    self.productions[variable].remove(head + tail)
                    if tail == '':
                        productions_new_state.add('&')
                    else:
                        productions_new_state.add(tail)
                self.productions[new_state] = productions_new_state

        # for variable in self.non_terminals:
        #     print(variable)
        #     print(self.productions[variable])

    def eliminate_indirect_non_determinism(self):
        variables = list(self.non_terminals)
        # print(variables)
        for variable in variables:
            productions = copy.deepcopy(self.productions[variable])
            # print(productions)
            for production in productions:
                # print('VARIABLE: '+ variable)
                # print(production)
                head = production[0]
                tail = production[1:]
                # print(head, tail)
                if head in self.non_terminals:
                    sub_productions = list(self.productions[head])
                    self.productions[variable].remove(production)
                    for sub_production in sub_productions:
                        self.productions[variable].add(sub_production+tail)
