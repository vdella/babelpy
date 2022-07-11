class ContextFreeGrammar:

    def __init__(self, non_terminals: set, terminals: set, productions: dict):
        self.non_terminals = non_terminals
        self.terminals = terminals
        self.symbols: set = self.terminals | self.non_terminals
        self.productions = productions
        self.start = 'S'

    def __str__(self):
        string = str()
        for src, dst in self.productions.items():
            string += '{} -> {}\n'.format(src, ' | '.join(dst))
        return string

    def first(self):
        first = {symbol: set() for symbol in self.symbols}

        for symbol in self.symbols:
            if symbol in self.terminals:
                first[symbol] = {symbol}
            else:
                production = self.productions[symbol]

                for piece in production:
                    head = piece[0]

                    if head == '&' or head in self.terminals:
                        first[symbol] |= {head}
                    else:  # Starts with a non-terminal.
                        for letter in piece:
                            after = piece[1:]
                            first[symbol] |= first[letter]

        return first

    def follow(self):
        pass
