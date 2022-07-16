from ordered_set import OrderedSet


class ContextFreeGrammar:

    def __init__(self, non_terminals, terminals, productions: dict, start='S'):
        self.non_terminals = non_terminals
        self.terminals = terminals
        self.symbols: set = self.terminals | self.non_terminals
        self.productions = productions
        self.start = start

    def __str__(self):
        string = str()
        for src, dst in self.productions.items():
            string += '{} -> {}\n'.format(src, ' | '.join(dst))
        return string

    def first(self):
        first = {symbol: set() for symbol in self.symbols}

        # Rules are different for terminals, as they are their own firsts.
        first |= {terminal: {terminal} for terminal in self.terminals}

        nullable = self.nullable()

        def build_for(symbol):
            productions = self.productions[symbol]

            gatherer = str()
            for piece in productions:
                head = piece[0]
                piece_iterator = iter(piece)

                if head in self.terminals or head == '&':  # Whether starts with a terminal or with &.
                    first[symbol] |= {head}
                elif head not in self.symbols:
                    while piece_iterator:
                        gatherer += next(piece_iterator)
                    else:
                        raise Exception('Incorrect grammr found. Please fix.')
                else:  # Starts with a non-terminal.
                    for letter in piece:
                        if letter in self.non_terminals and not first[letter]:
                            build_for(letter)  # Executes a depth-first search from the given letter.
                        first[symbol] |= first[letter]

                        if not nullable[symbol]:
                            # & will be added by default if found in other firsts, but it must not
                            # be added if the symbol is not itself nullable.
                            first[symbol] -= {'&'}

        # for non_terminal in self.non_terminals:
        build_for(self.start)

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
        reversed_productions = {non_terminal: OrderedSet() for non_terminal in self.non_terminals}

        for non_terminal in self.non_terminals:
            for production in self.productions[non_terminal]:
                if production[-1] in self.non_terminals:  # Checks if the productions ends with a non-terminal.
                    reversed_productions[non_terminal] |= {production[::-1]}

        return reversed_productions

    def left_recursion(self):
        self.eliminate_direct_recursion(self.start)
        self.eliminate_indirect_recursion()

    def eliminate_direct_recursion(self, non_terminal):
        contem = set()
        contem_ = set()
        nao_contem = set()
        nao_contem_ = set()
        for production in self.productions[non_terminal]:
            if production[0] == non_terminal:
                contem.add(production)
            else:
                nao_contem.add(production)

        if len(contem) != 0:
            new_non_terminal = non_terminal + '\''
            self.non_terminals |= {new_non_terminal}
            for production in contem:
                production = production.replace(non_terminal, '')
                contem_.add(production + new_non_terminal)
            contem_.add('&')
            self.productions[new_non_terminal] = contem_

            if len(nao_contem) != 0:
                for production in nao_contem:
                    nao_contem_.add(production + new_non_terminal)
                self.productions[non_terminal] = nao_contem_
            else:
                nao_contem_.add(new_non_terminal)
                self.productions[non_terminal] = nao_contem_

    def eliminate_indirect_recursion(self):
        non_terminals = list(self.non_terminals)
        i = 0
        stop_condition = True

        new_productions = set()
        prod_to_remove = str()

        while stop_condition:
            for j in range(i):
                for production in self.productions[non_terminals[i]]:
                    if production[0] == non_terminals[j]:
                        new_productions = set()
                        new_production = production.replace(production[0], str())
                        # nao pode ser o prod[0] pq pode ter simbolo repetido ex: SSa
                        for prod_ind in self.productions[non_terminals[j]]:
                            new_productions.add(prod_ind + new_production)

                        prod_to_remove = production

                for new_prod in new_productions:
                    self.productions[non_terminals[i]].add(new_prod)
                print(prod_to_remove)
                if prod_to_remove and prod_to_remove in self.productions[non_terminals[i]]:
                    self.productions[non_terminals[i]].remove(prod_to_remove)
                print(self.productions[non_terminals[i]])

            self.eliminate_direct_recursion(non_terminals[i])
            i = i + 1
            if i >= len(non_terminals):
                stop_condition = False
