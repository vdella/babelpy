from src.grammars.structures.cfg import ContextFreeGrammar


class ParsingTable:

    def __init__(self, grammar: ContextFreeGrammar):
        self.grammar = grammar

    def __str__(self):
        pass

    @staticmethod
    def digest(grammar):
        pass

    def is_ll1(self):
        self.digest(self.grammar)
        first = self.grammar.first()
        follow = self.grammar.follow()
        nullable = self.grammar.nullable()

        for non_terminal in self.grammar.non_terminals:
            if first[non_terminal] & follow[non_terminal] and nullable[non_terminal]:
                return False
        return True

    def instance(self):
        pass
