# babelpy
A JFlap-like software for analysing regex and generating their finite automata.

## First steps

For using `babelpy`, you will need `Python3.10`
and a package named `PrettyTable.`

1. `Python3.10`

`sudo apt update && sudo apt upgrade -y`\
`sudo apt install software-properties-common -y`\
`sudo add-apt-repository ppa:deadsnakes/ppa`\
`sudo apt install python3.10`

2. `PrettyTable`

For `PrettyTable` installation, you will need a `pip` compatible
version with `Python3.10`.

`sudo apt install python3.10-distutils`\
`python3.10 -m pip install -U prettytable`

## How does it work?

The code will, indeed, look a lot more like
a lib than an application. Due to the fact
there is no `main` module at the time
being, users may be confused at the beggining, thus
it is worth mentioning that every project module works
as a `main` in its own way.

There are 3 big topics from the field of
Formal Languages implemented here:

1. Finite Automata (FA);
2. Grammars;
3. Regular Expressions (regex).
    
### Finite Automata (FA)

There is no explicit distinction between those
that are deterministic and their counterpart.
Every FA will have:

    1. A set containing all of its states;
    2. An initial state;
    3. A set of all its final states; and
    4. A transition dictionary, indexed by
    tuples of (State, Symbol).

There is no need to keep the alphabet in a variable.
Its only usage in the project is at the process
of `determinization`, but, if one does need it,
there is `FiniteAutomata.symbols()` to retrieve
an alphabet from a FA.

The `FiniteAutomata` class overrides the `__or__()`
and the `__str__()` as the user is able to get
the union of 2 automata like this:

> `fa3 = fa1 | fa2`

To see the result, `PrettyTable` package helps us
to show the FA in user-friendly table-looking way
by using `print(fa3)`.

Along with the automata, there are modules to
deal with data persistency. `parser` comes
with `parse_fa_from(filepath: str)` to read
an automata from a file; `loader`, responsible
for saving FA into `.txt` files, does so with
its `save(FiniteAutomata)` function.

#### File formatting

An automata can be retrived from a file with
contents like this:

> #states\
q0\
q1\
q2\
q3\
q4\
#initial\
q0\
#final\
q1\
q2\
#transitions\
q0 0 -> q1 q2\
q0 1 -> q2\
q1 0 -> q1\
q1 1 -> q3\
q2 0 -> q4\
q2 1 -> q1\
q3 0 -> q1\
q3 1 -> q3\
q4 0 -> q4\
q4 1 -> q3

It **must** have its contents divided in 4 sections:

    1. states;
    2. initial;
    3. final;
    4. transitions.

Every section **has** to begin with "#".

### Grammars

WIP

### Regular Expressions (regex)

A regex can be turned into a FA from a hard-coded
string, as functions for retrieving single
strings from files would make things harder
to understand. The conversion process
from regex to FA is done by following the
Dragon Book algorithm for Lexical Analysis.

The `format` module is used only to prepare
the regexes to be scanned, e.g. adds missing
concatenations between operators. The crowl
jewelry are the `conversion` and `tree` modules.

The `tree` module is responsible for building
a `SyntaxTree` from a given regex. The said tree
works as a binary tree, with every node being
a symbol from the regex, that is scanned from
*right to left*. If wanted, it can be viewed
by using `show_tree_from(root: Node)` function.
From `(&|b)(ab)*(&|a)`, the following tree
can be obtained.

![Tree from (&|b)(ab)*(&|a)](images/regex.png "Tree from (&|b)(ab)*(&|a)")

The `conversion` module will create a
`SyntaxTree` from a given regex and build
its FA equivalent. Using `fa_from(regex: str)`,
one can retrieve its automata.

![Fa from (&|b)(ab)*(&|a)](images/fa_from_regex.png "Fa from (&|b)(ab)*(&|a)")