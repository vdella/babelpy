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

        def build_for(symbol):
            production = self.productions[symbol]

            for piece in production:
                head = piece[0]

                if head in self.terminals or head == '&':  # Whether starts with a terminal or with &.
                    first[symbol] |= {head}
                else:  # Starts with a non-terminal.
                    for letter in piece:
                        if letter in self.non_terminals:
                            build_for(letter)  # Executes a depth-first search from the given letter.
                        first[symbol] |= first[letter]

                        if not self.nullable()[symbol]:
                            # & will be added by default if found in other firsts, but it must not
                            # be added if the symbol is not itself nullable.
                            first[symbol] -= {'&'}

        build_for(self.start)
        return first

    def nullable(self):
        """:returns: a (symbol, bool) dictionary built from the grammar.
        Terminals are not nullable by default. Non-terminals will
        be nullable if there is at least one path from which they can find an &."""
        nullable = {symbol: False for symbol in self.symbols}

        def check(symbol):
            if symbol in self.non_terminals:
                if '&' in self.productions[symbol]:  # &-production.
                    nullable[symbol] = True
                else:  # Didn't find &. Executes depth-first search.
                    for production in self.productions[symbol]:
                        for letter in production:
                            check(letter)

                        if all([nullable[letter] for letter in production]):  # Nullable production found.
                            nullable[symbol] = True

        for non_terminal in self.non_terminals:
            check(non_terminal)

        return nullable

    def follow(self):
        pass
