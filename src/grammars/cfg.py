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
        pass

    def follow(self):
        pass
