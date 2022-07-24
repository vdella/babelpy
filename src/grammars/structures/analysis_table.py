import copy

from src.automata.structures.state import State
from prettytable import PrettyTable
#from src.grammars.persistency.reader import read_grammar_from
from src.grammars.structures.cfg import ContextFreeGrammar

class AnalysisTableContrcutor:

    def __init__(self):
        self.firsts = ''
        self.follows = ''
        self.productions = ''
        self.terminals = ''
        self.start_state = ''
        self.non_terminals = ''
        self.split_productions = ''
        self.table = ''
        self.split_productions = dict()

    def read(self):

        entry_file = open('grammar.txt', 'r')
        lines = entry_file.readlines()


        trimmed = [line.rstrip() for line in lines]

        start = trimmed[trimmed.index('#start') + 1]
        non_terminals = {symbol for symbol in trimmed[trimmed.index('#non-terminals') + 1: trimmed.index('#terminals')]}
        terminals = {symbol for symbol in trimmed[trimmed.index('#terminals') + 1: trimmed.index('#productions')]}

        productions = dict()
        for production in trimmed[trimmed.index('#productions') + 1: trimmed.index('#firsts')]:
            line_without_arrow = production.replace(' ', '').split('->')
            non_terminal = line_without_arrow[0]  # Expected to always be non-terminal.
            digested_line = ''.join(line_without_arrow[1:]).split('|')
            productions[non_terminal] = digested_line

        firsts = dict()
        for first in trimmed[trimmed.index('#firsts') + 1: trimmed.index('#follows')]:
            line_without_arrows = first[:-1].replace(' ', '').split('{')
            non_terminal = line_without_arrows[0]  # Expected to always be non-terminal.
            digested_lines = ''.join(line_without_arrows[1:]).split(',')
            firsts[non_terminal] = digested_lines

        follows = dict()
        for follow in trimmed[trimmed.index('#follows') + 1:]:
            line_without_arrows = follow[:-1].replace(' ', '').split('{')
            non_terminal = line_without_arrows[0]  # Expected to always be non-terminal.
            digested_lines = ''.join(line_without_arrows[1:]).split(',')
            follows[non_terminal] = digested_lines

        self.non_terminals = non_terminals
        self.terminals = terminals
        self.productions = productions
        self.start_state = start
        self.firsts = firsts
        self.follows = follows

    def generate_table(self):
        non_terminals = list(self.non_terminals)
        terminals = (list(self.terminals) + ['$'])
        table = {nt: {t: str() for t in terminals} for nt in non_terminals}

        i = 1

        split_productions = dict()
        aux_dict = dict()
        for p in self.productions:
            for c in range(len(self.productions[p])):
                split_productions[i] = ((self.productions[p])[c-1])
                aux_dict[i] = p
                i = i+1
        self.split_productions = split_productions

        for non_terminal in self.non_terminals:
            firsts = self.firsts[non_terminal]
            for derivation in split_productions:
                if (split_productions[derivation])[0] in self.terminals:
                    if table[non_terminal][(split_productions[derivation])[0]] == '' and aux_dict[derivation] == non_terminal:
                        if split_productions[derivation] == '&':
                            for follow in self.follows[non_terminal]:
                                table[non_terminal][follow] = derivation
                            table[non_terminal][('$')[0]] = derivation
                        else:
                            table[non_terminal][(split_productions[derivation])[0]] = derivation
                else:
                    for first in firsts:
                        if table[non_terminal][first] == '' and aux_dict[derivation] == non_terminal:
                            table[non_terminal][first] = derivation

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
            print(stack)

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
                    print(stack)
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
                print('2')
                break
        print(accepted)
        return stacktrace, accepted


analysisTable = AnalysisTableContrcutor()
analysisTable.read()


table = PrettyTable()

header = ['NonTerminal']
for terminal in analysisTable.terminals:
    header.append(terminal)
header.append('$')

table.field_names = header

analysisTable.generate_table()
analysisTable.run_analysis('ivi^i')

#for column in analysisTable.table:
   # lista = []
    #for line in analysisTable.table[column]:
       # print("teste: " ,(analysisTable.table[column])[line])

    #print((analysisTable.table[column])['i'])






