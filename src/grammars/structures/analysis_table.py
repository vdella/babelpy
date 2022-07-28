import copy

from src.automata.structures.state import State
# from prettytable import PrettyTable
#from src.grammars.persistency.reader import read_grammar_from
from src.grammars.persistency.reader import read_grammar_from
from src.grammars.structures.cfg import ContextFreeGrammar

class AnalysisTableContrcutor:

    def __init__(self, grammar: ContextFreeGrammar):
        self.grammar = grammar
        self.productions = grammar.productions
        self.terminals = grammar.terminals
        self.start_state = grammar.start
        self.non_terminals = grammar.non_terminals
        self.split_productions = set()
        self.table = ''
        #self.split_productions = dict()

    def set_to_list(self, i: int):

        my_list = dict()

        if i == 1:
            for key, value in self.grammar.first().items():
                my_list[key] = list(value)
        if i == 2:
            for key, value in self.grammar.follow().items():
                my_list[key] = list(value)
        if i == 3:
            for key, value in self.grammar.productions.items():
                my_list[key] = list(value)
        return my_list

    def generate_table(self):

        first = self.set_to_list(1)
        follows = self.set_to_list(2)
        productions = self.set_to_list(3)

        print(follows)

        non_terminals = list(self.non_terminals)
        terminals = (list(self.terminals) + ['$'])
        table = {nt: {t: str() for t in terminals} for nt in non_terminals}


        i = 1

        split_productions = dict()
        aux_dict = dict()


        for p in self.productions:
            for c in range(len(self.productions[p])):
                split_productions[i] = ((productions[p])[c-1])
                aux_dict[i] = p
                i = i+1
        self.split_productions = split_productions


        #for key,value in first.items():
            #print(type(value))


        for non_terminal in self.non_terminals:
            firsts = first[non_terminal]
            for derivation in split_productions:
                if (split_productions[derivation])[0] in self.terminals:
                    if table[non_terminal][(split_productions[derivation])[0]] == '' and aux_dict[derivation] == non_terminal:
                        if split_productions[derivation] == '&':
                            for follow in follows[non_terminal]:
                                table[non_terminal][follow] = derivation
                            table[non_terminal][('$')[0]] = derivation
                        else:
                            table[non_terminal][(split_productions[derivation])[0]] = derivation
                else:
                    for key in firsts:
                        if table[non_terminal][key] == '' and aux_dict[derivation] == non_terminal:
                            table[non_terminal][key] = derivation

        self.table = table

    def run_analysis(self, sentence):
        stacktrace = []
        stack = ['$']
        stack.append(self.start_state)
        entry = sentence + '$'
        accepted = False

        variables = self.non_terminals


        while entry != '' and stack != '':
            history = {"stack": stack, "entry": entry}
            stacktrace.append(copy.deepcopy(history))
            symbol = stack.pop()

            if symbol in variables:
                if symbol in self.table and entry[0] in self.table[symbol]:
                    derivation = self.table[symbol][entry[0]]
                    if derivation == '':
                        accepted = False
                        break

                    derivation = list(self.split_productions[derivation])
                    i = 0
                    for var in derivation:
                        if var == "'":
                            derivation[i - 1] = derivation[i - 1] + "'"
                            del derivation[i]
                        i = i + 1
                    derivation.reverse()
                    if derivation[0] == "&":
                        continue
                    stack += derivation
                else:
                    accepted = False
                    break
            elif symbol == entry[0]:
                if symbol == "$":
                    accepted = True
                    break
                else:
                    entry = entry[1:]
            else:
                accepted = False
                break
        print(accepted)
        return stacktrace, accepted


# analysisTable = AnalysisTableContrcutor()
# analysisTable.read()
#
#
# table = PrettyTable()
#
# header = ['NonTerminal']
# for terminal in analysisTable.terminals:
#     header.append(terminal)
# header.append('$')
#
# table.field_names = header
#
# analysisTable.generate_table()
# analysisTable.run_analysis('ivi^i')

#for column in analysisTable.table:
   # lista = []
    #for line in analysisTable.table[column]:
       # print("teste: " ,(analysisTable.table[column])[line])

    #print((analysisTable.table[column])['i'])


if __name__ == '__main__':
    read_grammar = read_grammar_from('grammar.txt')
    analysisTable = AnalysisTableContrcutor(read_grammar)
    analysisTable.generate_table()
    analysisTable.run_analysis("ivi^i")

    table = PrettyTable()

    header = ['NonTerminal']
    for terminal in analysisTable.terminals:
        header.append(terminal)
    header.append('$')

    table.field_names = header

    for nt in analysisTable.non_terminals:
        entry = []
        entry.append(nt)
        mydict = analysisTable.table[nt]
        for t in analysisTable.terminals:
            entry.append(mydict[t])
        entry.append(mydict['$'])
        table.add_row(entry)

    print(table)




