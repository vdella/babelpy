from prettytable import PrettyTable

class Env:

    def __init__(self):
        self.st = {}
        self.tl = []
        # self.prev = p

    def putST(self, s: str):
        if s not in self.st:
            self.st[s] = len(self.st)
            st.add_row([len(self.st),s])
        return self.st.get(s)

    def putTL(self, s):
        if s not in self.tl:
           tl.add_row([s])
           self.tl.append(s)


rw_file = open('reserved_words.txt', 'r')
rw_read = rw_file.readlines()
reservedTerms = []
for line in rw_read:
    reservedTerms.append(line[:-1])

entry_file = open('entry.txt', 'r')

entry_read = entry_file.readlines()
entry = []
for word in entry_read:
    entry.append(word[:-1])

tables = Env()

st = PrettyTable()
st.field_names = ["index", "id"]
tl = PrettyTable()
tl.field_names = ["Token List"]

for word in entry:
    if (word not in reservedTerms):
        index = tables.putST(word)
        tables.putTL(["id", index])
    else:
        tables.putTL(word)

print(st)
print(tl)




