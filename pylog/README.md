## Abstract (outline from [The Programming Journal](https://programming-journal.org/cfp/))

<dl><dt>Context: What is the broad context of the work? What is the importance of the general research area?</dt>
<dd>Pylog inhabits three programming contexts.<br/><br/>
 
**a)** Pylog explores the integration of two distinct programming language paradigms: (i) the modern general purpose programming paradigm, which often includes features of procedural programming, object-oriented programming, functional programming, and meta-programming, here represented by Python, and (ii) logic programming, whose primary features are logic variables (and unification) and built-in depth-first search, here represented by Prolog. These logic programming feature are generally missing from modern general purpose languages. Pylog illustrates how these two features can be implemented in and integated into Python. 

**b)** Pylog demonstrates the breadth and broad applicability of Python. Although Python is now the most widely used programming language for teaching introductory programming, it has also become very widely used for sophisticated programming tasks. One of the reasons for its popularity is the range of capabilities it offers—most of which are not used in elementary programming classes or for the sort of scripting applications with which Python is often associated. Pylog makes effective use of many of those capabilities.  

**c)** Pylog examplifies programming at its best. Pylog is first-of-all a programming exercise: How can the primary features of logic programming be integrated with Python? Secondly, Pylog uses features of Python in ways that aere both intended and innovative. The overall result is software worth studying. From the perspective of [The Programming Journal](https://programming-journal.org/cfp/), it would fit into its Art-of-Programming category.
</dd>

<dt>Inquiry: What problem or question does the paper address? How has this problem or question been addressed by others (if at all)?</dt>
<dd>The primary issue addressed in the paper—and in Pylog itself—is how logic variables and backtracking can be integrated cleanly into a Python framework. A fair amount of work has been done in this area: see <i>Related Work</i>. Although well done, most of it has been incomplete in one way or another. Pylog is the first complete system (as far as we know) to achieve the goal of integration.</dd>

<dt>Approach: What was done that unveiled new knowledge?</dt>
<dd>Pylog, exhibits the integration mentined above. The paper discusses—and Pylog demonstrates—how logic variables and backtracking can be interwoven with standard Python data structures and control structures.</dd>

<dt>Knowledge: What new facts were uncovered? If the research was not results oriented, what new capabilities are enabled by the work?</dt>
<dd>Pylog  is available as a logic programming library for use in Python software.</dd>

<dt>Grounding: What argument, feasibility proof, artifacts, or results and evaluation support this work?</dt>
<dd>Pylog demonstrates by its existence and functionality that the goal of integrating logic variables and backtracking with Python can be achieved.</dd>

<dt>Importance: Why does this work matter?</dt>
<dd>Python is known to be compatible with functional programming. This work shows that it is also (and simultaneously) compatible with logic programming. This work also demonstrates the power and elegance of well-designed software. 
<dd>
</dl>

## Introduction

Prolog, a programming language derived from logic, was developed in the 1970s. It became very popular during the 1980s as an AI language, especially in Japan as part of their [5th generation project](https://www.nytimes.com/1992/06/05/business/fifth-generation-became-japan-s-lost-generation.html). 

Prolog went out of favor because [it was difficult to trace the execution of Prolog programs](https://synthese.wordpress.com/2010/08/21/prologs-death/)—which made debugging very challenging.

Structurally, Prolog is both one of the simplest of all programming languages—you can learn it very quickly—and one of the most interesting. It is quite different from virtually all other programming languages. In Prolog you make assertions of facts and then pose questions about those facts. Answers are *unified* with (rather than assigned to) variables.  Prolog is seductively elegant and powerful. 

We can look a few examples [here](https://swish.swi-prolog.org/p/kb_rja.pl).

## SWI-Prolog

[SWI-Prolog](http://www.swi-prolog.org/) has kept the Prolog flame burning and seems to have developed a successful community of Prolog users.

<dl>
<dt>From the <a href="http://www.swi-prolog.org/features.html">SWI-Prolog website</a></dt>
<dd> SWI-Prolog is a versatile implementation of the <a href="https://en.wikipedia.org/wiki/Prolog">Prolog language</a>. Although SWI-Prolog gained its popularity primarily in education, its development is mostly driven by the needs for application development. This is facilitated by a rich interface to other IT components by supporting many document types and (network) protocols as well as a comprehensive low-level interface to C that is the basis for high-level interfaces to C++, Java (bundled), C#, Python, etc (externally available). Data type extensions such as dicts and strings as well as full support for Unicode and unbounded integers simplify smooth exchange of data with other components.<br /><br />
SWI-Prolog aims at scalability. Its robust support for multi-threading exploits multi-core hardware efficiently and simplifies embedding in concurrent applications. Its Just In Time Indexing (JITI) provides transparent and efficient support for predicates with millions of clauses.</dd>
</dl>

## Prolog tutorials

* Blackburn, Patrick, Johan Bos, and Kristina Striegnitz (2012) [*Learn Prolog Now!*](http://lpn.swi-prolog.org/lpnpage.php?pageid=online) (This version of the book is embedded in SWI Prolog’s [SWI SH](http://swish.swi-prolog.org/) ([SWI-Prolog](http://www.swi-prolog.org/) for SHaring), an online Prolog interpreter similar to Jupyter.)

* Wilson, Bill, ["Introduction to Prolog Programming,"](http://www.cse.unsw.edu.au/~billw/cs9414/notes/prolog/intro.html) for the course COMP9414/9814 "Artificial Intelligence." Consists mostly of extracts from the first five chapters of 

  * Bratko, I. (2011) [*Programming in Prolog for Artificial Intelligence*](https://www.amazon.com/gp/product/0321417461/ref=dbs_a_def_rwt_hsch_vapi_taft_p1_i0), 4th Edition, Addison-Wesley.
 
* Piumarta, Ian (2017) ["Programming-language-paradigms"](http://www.ritsumei.ac.jp/~piumarta/pl/) (a course).  “Logic programming and Prolog” is explored in week 5 ([slides-5](http://www.ritsumei.ac.jp/~piumarta/pl/slides/PL-05.pdf), [exercises-5](http://www.ritsumei.ac.jp/~piumarta/pl/ex/PL-05-ex.pdf)), week 6 ([slides-6](http://www.ritsumei.ac.jp/~piumarta/pl/slides/PL-06.pdf), [exercises-6](http://www.ritsumei.ac.jp/~piumarta/pl/ex/PL-06-ex.pdf)), and week 7 ([slides-7](http://www.ritsumei.ac.jp/~piumarta/pl/slides/PL-07.pdf), [exercises-7](http://www.ritsumei.ac.jp/~piumarta/pl/ex/PL-07-ex.pdf)). Week 7 is a Prolog tutorial. You should be able to understand it without first reading weeks 5 and 6. But those weeks are important. They show how to  implement many Prolog features in Python.

## Pylog: prolog in Python
This repository is a Python implementation of many Prolog features. It is a fork of Piumarta’s [`unify.py`](http://www.ritsumei.ac.jp/~piumarta/pl/src/unify.py).

As an introductory example, consider the following (Python) code—adapted from [Piumarta's week 5 exercises](http://www.ritsumei.ac.jp/~piumarta/pl/ex/PL-05-ex.py). (You can run it [here](https://colab.research.google.com/drive/1BkWBGY0GpOYqHLpyylzbPU9OLdyqxSmk).) (The type annotations are not required, but they are useful to understand what's going on.) 

```python
from typing import Generator

def isEven(i: int) -> Generator[None, None, None]:
    if i % 2 == 0:
        print(f'{i}-even', end = ', ')
        yield 
    else:
        print(f'{i}-odd', end = ', ')
        
evens = [i for i in range(10) for _ in isEven(i)]

print(f'\n{evens}')
        
```
Can you figure out how the preceding produces these results? 
```python
0-even, 1-odd, 2-even, 3-odd, 4-even, 5-odd, 6-even, 7-odd, 8-even, 9-odd,
[0, 2, 4, 6, 8] 
```
In particular, what does 

```python 
for _ in isEven(i)
``` 

do in the list comprehension?

In Prolog, program components are understood as predicates. They may *succeed* or *fail*. To succeed/fail means that the system was/was not able to establish that the predicate holds given the information available. 

Success or failure is implemented in Python through generators. A generator that **yield**s a result (at the Python level) is said to succeed (at the Prolog level); one that does not **yield** a result, fails (at the Prolog level).

In this case, `isEven(i)` succeeds/fails when `i` is even/odd. (In either case it produces an output line.) When

```python
for _ in isEven(i)
```

succeeds/fails for a given `i`, the list comprehension completes/fails to complete the iteration for that `i` and includes/does not include `i` in the generated list.  

## Implementing logic variables and unification in Python

*To be written*

## Implementing Prolog backtracking in Python 

*To be written*

## File organization (not recently updated)

```
pylog                            -- Root directory
    examples                     -- A directory of example pylog programs
        n_queens.py              -- The traditional n-queens problem. Uses minimal pylog features but illustrates the pylog style.
        puzzles.py               -- A file containing information common to the scholarship_problem and the zebra_problem
        scholarship_problem.py   -- A traditional Prolog logic puzzle—less complex than the zebra problem
        trains.py                -- A revised version of the train example from Piumarta
        zebra_problem.py         -- The well-known logic puzzle often solved with Prolog
    sequence_options             -- A directory of options for lists and sequences
        linked_list.py           -- A traditional head/tail list structure. Allows a variable tail, which Python does not
        sequences.py             -- Implementations of Python lists and tuples
        super_sequence.py        -- A class that serves as a superclass for all the sequences
    control_structures.py        -- Implementation of the Prolog control structures
    logic_variables.py           -- Implementation of Prolog's logic variables
```

## File dependencies/`imports from` relations (not recently updated)

```
logic_variables: none
control_structures: logic_variables

super_sequence: control_structures, logic_variables
linked_list and sequences: logic_variables, super_sequence

n_queens: logic_variables, sequences
trains: control_structures, logic_variables, sequences
puzzle: super_sequence
scholarship_problem and zebra_problem: control_structures, logic_variables, puzzles, super_sequence

```
## Naming conventions

For the most part, Python identifier names follow PEP 8 conventions: all lower case, with underscores between words; no camel case except for class names.

However, since Prolog uses identifiers that begin with an upper case letter for Prolog variables, Python identifiers used as Prolog variables begin with upper case letters.

## Previous work

* Berger, Shai (2004) [Pythologic](http://code.activestate.com/recipes/303057-pythologic-prolog-syntax-in-python/)

* Bolz, Carl Friedrich (2007) [A Prolog Interpreter in Python](http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.121.8625&rep=rep1&type=pdf)

* Delord, Christophe (2009) [PyLog](http://cdsoft.fr/pylog/index.html)

* Frederiksen, Bruce Frederiksen (2011) [Pyke](http://pyke.sourceforge.net/)

* Kopec, David (2019) [Constraint-Satisfaction Problems in Python](https://freecontent.manning.com/constraint-satisfaction-problems-in-python/) from _[Classic Computer Science Problems in Python](https://www.manning.com/books/classic-computer-science-problems-in-python)_, Manning ([GitHub code repository](https://github.com/davecom/ClassicComputerScienceProblemsInPython/tree/master/Chapter3))

* Maxime, Istasse (2016) [Prology: Logic programming for Python3](https://github.com/mistasse/Prology)

* Meyers, Chris (2015) [Prolog in Python](http://www.openbookproject.net/py4fun/countClick.php?dest=prolog/intro.html)

* Niemeyer, Gustavo and Sébastien Celles (2019). [python-constraint](https://github.com/python-constraint/python-constraint). Pypi page: [python-constraint](https://pypi.org/project/python-constraint/) (Also discussed in Popović, Olivera (2019) [Constraint Programming with python-constraint](https://stackabuse.com/constraint-programming-with-python-constraint/#listofbuiltinconstraints))

* Orsini, Francesc, Paolo Frasconi, Luc De Raedt (2017) [kProbLog: an algebraic Prolog for machine learning](https://link.springer.com/article/10.1007/s10994-017-5668-y) (This seems more like a theoretical discussion of kProbLog, which was implementated in Python, rather than an integraton of Python and Prolog. It's a worthwhile distinction to make. One can implement Prolog in any general purpose language. Pylog is notable because it integrates Python and Prolog.)

* Python Foundation [re: Regular expression operations](https://docs.python.org/3/library/re.html)

* Rocklin, Matthew (2015) [Unification](https://github.com/mrocklin/unification)

* Rocklin, Matthew (2019) [kanren: Logic Programming in Python](https://github.com/logpy/logpy/) (The author of [toolz](https://toolz.readthedocs.io/en/latest/index.html))

* Santini, Claudio (2018) [Pampy: The Pattern Matching for Python you always dreamed of](https://github.com/santinic/pampy)  

* Stack Overflow questions.
  * [Implementing the Prolog Unification algorithm in Python? Backtracking](https://stackoverflow.com/questions/49101342/implementing-the-prolog-unification-algorithm-in-python-backtracking)
  * [Relational/Logic Programming in Python?](https://stackoverflow.com/questions/1917607/relational-logic-programming-in-python)

* Thompson, Jeff (2017) [Yield Prolog](http://yieldprolog.sourceforge.net/)

* Triska, Markus [CLP(FD): Constraint Logic Programming over Finite Domains](http://www.swi-prolog.org/man/clpfd.html) (also [CLP(FD): Constraint Logic Programming over Finite Domains](http://www.swi-prolog.org/pldoc/man?section=clpfd) (Repo of [examples](https://github.com/triska/clpz))

