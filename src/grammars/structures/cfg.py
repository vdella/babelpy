import string
from prettytable import PrettyTable
from src.grammars.decorators import show


class ContextFreeGrammar:
    __MAX_FACTOR = 10
    __VARIABLES = set(string.ascii_uppercase)

    def __init__(self, non_terminals, terminals, productions: dict, start):
        self.non_terminals = non_terminals
        self.terminals = terminals
        self.symbols: set = self.terminals | self.non_terminals
        self.productions: dict = productions
        self.start = start

    def __str__(self):
        gatherer = str()
        for src, dst in self.productions.items():
            if src and dst:
                gatherer += '{} -> '.format(src)
                for i in dst:
                    if i == dst[-1]:
                        gatherer += '{}'.format(' '.join(i))
                    else:
                        gatherer += '{} | '.format(' '.join(i))
                gatherer += '\n'
        return gatherer

    def first(self):
        first = {symbol: set() for symbol in self.symbols}

        # Rules are different for terminals, as they are their own firsts.
        first |= {terminal: {terminal} for terminal in self.terminals}

        nullable = self.nullable()

        def build_for(symbol):
            body = self.productions[symbol]

            for piece in body:
                head = piece[0]

                if head in self.terminals or head == '&':  # Whether starts with a terminal or with &.
                    first[symbol] |= {head}
                else:  # Starts with a non-terminal.
                    while piece:
                        head = piece[0]

                        if not first[head]:
                            build_for(head)  # Executes a depth-first search from the given letter.
                        first[symbol] |= first[head]

                        if not nullable[symbol]:    # & will be added by default if found in other firsts,
                            first[symbol] -= {'&'}  # but it must not be added if the symbol is not itself nullable.

                        if not nullable[head]:
                            break

                        piece = piece[1:]

        for non_terminal in self.non_terminals:
            build_for(non_terminal)

        return first

    @show
    def show_first(self) -> str:
        table = PrettyTable()
        table.field_names = ['Non-terminals', 'First']

        first = self.first()

        for symbol, value in first.items():
            if symbol in self.non_terminals:
                table.add_row([symbol, value])

        return str(table)

    def nullable(self):
        """:returns: a (symbol, bool) dictionary built from the grammar.
        Terminals are not nullable by default. Non-terminals will
        be nullable if there is at least one path from which they can find an &."""
        nullable = {symbol: False for symbol in self.symbols}
        visited = {non_terminal: False for non_terminal in self.non_terminals}

        def check(symbol):
            body = self.productions[symbol]

            for production in body:
                for head in production:
                    if head == '&':
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

    @show
    def show_nullable(self) -> str:
        table = PrettyTable()
        table.field_names = ['Nullables']

        nullables = self.nullable()

        for non_terminal, value in nullables.items():
            if value:
                table.add_row([non_terminal])

        return str(table)

    def follow(self):
        follow = {symbol: set() for symbol in self.symbols}
        follow |= {terminal: {'/'} for terminal in self.terminals}
        follow[self.start] = {'$'}

        first = self.first()
        nullable = self.nullable()

        def search_for(symbol):
            ocurrences = self.find(symbol)

            for head, body in ocurrences.items():
                for line in body:
                    end = -1
                    if line[end] == symbol:  # Last production symbol.
                        while nullable[line[end]]:
                            if not follow[head] and head != symbol:
                                search_for(head)
                            follow[line[end]] |= follow[head]
                            end -= 1
                        follow[symbol] |= follow[head]
                    else:
                        where = line.index(symbol) + 1
                        here = line[where]
                        follow[symbol] |= first[here] - {'&'}

                        while nullable[here]:
                            where += 1

                            if where == len(line):
                                break

                            here = line[where]
                            follow[symbol] |= first[here] - {'&'}

        for non_terminal in self.non_terminals:
            search_for(non_terminal)

        return follow

    def find(self, symbol):
        """Finds all ocurrences of a :param symbol. :returns a dictionary containing the production rule lines
        where it appears."""

        finder = {non_terminal: list() for non_terminal in self.non_terminals}

        for non_terminal, productions in self.productions.items():
            for piece in productions:
                for char in piece:
                    if char == symbol:
                        finder[non_terminal].append(piece)

        for entry in finder.copy().keys():
            if not finder[entry]:
                del finder[entry]

        return finder

    @show
    def show_follow(self) -> str:
        table = PrettyTable()
        table.field_names = ['Non-terminals', 'Follow']

        first = self.follow()

        for symbol, value in first.items():
            if symbol in self.non_terminals:
                table.add_row([symbol, value])

        return str(table)

    def __reversed_nullable_productions(self):
        reversed_productions = {non_terminal: set() for non_terminal in self.non_terminals}

        for non_terminal in self.non_terminals:
            for production in self.productions[non_terminal]:
                if production[-1] in self.non_terminals:  # Checks if the productions ends with a non-terminal.
                    reversed_productions[non_terminal] |= {production[::-1]}

        return reversed_productions

    def get_new_state(self):
        disp = self.__VARIABLES - self.non_terminals
        return min(disp)

    def left_recursion(self):
        return self.eliminate_indirect_recursion()

    def eliminate_direct_recursion(self, non_terminal):
        contem = list()
        nao_contem = list()
        new_state = self.get_new_state()
        for production in self.productions[non_terminal]:
            head = production[0]
            tail = production[1:]
            if head == non_terminal:
                if len(tail) != 0:
                    j = str().join(tail)+new_state
                    if not (j in contem):
                        contem.append(j)
                else:
                    continue
            else:
                i = str().join(production)+new_state
                if not (i in nao_contem):
                    nao_contem.append(i)

        if len(contem) != 0:
            contem.append('&')
            self.non_terminals |= {new_state}
            self.productions[new_state] = contem

            if len(nao_contem) != 0:
                self.productions[non_terminal] = nao_contem
            else:
                nao_contem.append(new_state)
                self.productions[non_terminal] = nao_contem

    def eliminate_indirect_recursion(self):
        non_terminals = list(self.non_terminals)
        i = 0
        stop_condition = True
        new_productions = list()
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
                            new_productions.append(list(prod_ind) + list(new_production))
                        prod_to_remove = production
                for new_prod in list(new_productions):
                    if not (new_prod in self.productions[non_terminals[i]]):
                        self.productions[non_terminals[i]].append(new_prod)
                if prod_to_remove and prod_to_remove in self.productions[non_terminals[i]]:
                    self.productions[non_terminals[i]].remove(prod_to_remove)

            self.eliminate_direct_recursion(non_terminals[i])
            i = i + 1
            if i >= len(non_terminals):
                stop_condition = False

        return ContextFreeGrammar(self.non_terminals, self.terminals, self.productions, self.start)

    def number_derivation(self):
        productions_non_terminals = list()
        for prod in self.productions:
            productions_non_terminals.append(prod[0])
        productions_non_terminals = list(dict.fromkeys(productions_non_terminals))
        return len(productions_non_terminals)

    def factor(self):
        # self.left_recursion()
        iterations = 0
        while iterations < ContextFreeGrammar.__MAX_FACTOR:
            # length = self.number_derivation()
            # for _ in range(1):
            self.eliminate_direct_non_determinism()
            # self.eliminate_indirect_non_determinism()
            iterations += 1

    def eliminate_direct_non_determinism(self):
        variables = list(self.non_terminals)
        for variable in variables:
            derivations = list(self.productions[variable])
            derivation_to_change = {}
            for derivation in derivations:
                head = derivation[0]
                tail = derivation[1:]
                if head not in derivation_to_change:
                    derivation_to_change[head] = []
                derivation_to_change[head].append(list(tail))

            for head, tails in derivation_to_change.items():
                already_added = False
                if len(tails) == 1:
                    continue
                else:
                    productions_new_state = list()
                    new_state = self.get_new_state()
                    self.non_terminals |= {new_state}
                    self.productions[new_state] = {}
                    for tail in tails:
                        if tail == '':
                            productions_new_state.append('&')
                        else:
                            productions_new_state.append(list(tail))
                        if not already_added:
                            self.productions[variable].append(list(head) + list(new_state))
                            already_added = True
                        to_remove = list(tail)
                        to_remove.insert(0, head)
                        print(to_remove)
                        print(variable)
                        print(self.productions[variable])
                        self.productions[variable].remove(to_remove)

                    resultant_list = []
                    for element in productions_new_state:
                        if element not in resultant_list:
                            resultant_list.append(element)

                    self.productions[new_state] = resultant_list

    def eliminate_indirect_non_determinism(self):
        variables = list(self.non_terminals)
        for var in variables:
            productions = self.productions[var].copy()

            for production in productions:
                head, tail = production[0], production[1:]

                already_removed = False

                if head in self.non_terminals and head != var:

                    sub_productions = list(self.productions[head])
                    for sub_production in sub_productions:
                        if not already_removed:
                            self.productions[var].remove(production)
                            already_removed = True
                        # if isinstance(sub_production, list):
                        self.productions[var].append(list(sub_production) + list(tail))
                        # else:
                        #     self.productions[variable].append(sub_production + tail)
