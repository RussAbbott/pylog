# pylog: Prolog in Python

Prolog, a programming language derived from logic, was developed in the 1970s. It became very popular during the 1980s as an AI language, especially in Japan as part of their [5th generation project](https://www.nytimes.com/1992/06/05/business/fifth-generation-became-japan-s-lost-generation.html). 

Prolog went out of favor because [it was difficult to understand and trace the execution of Prolog programs](https://synthese.wordpress.com/2010/08/21/prologs-death/)—which made debugging very challenging.

Structurally, Prolog is both one of the simplest of all programming languages—you can learn it very quickly—and one of the most interesting. It is quite different from virtually all other programming languages. In Prolog you make assertions of facts and then pose questions about those facts. Answers are *unified* with variables.  It is seductively elegant and powerful. 

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
 
* Piumarta, Ian (2017) ["Programming-language-paradigms"](http://www.ritsumei.ac.jp/~piumarta/pl/) (a course).  “Logic programming and Prolog” is explored in weeks 5 ([slides-5](http://www.ritsumei.ac.jp/~piumarta/pl/slides/PL-05.pdf), [exercises-5](http://www.ritsumei.ac.jp/~piumarta/pl/ex/PL-05-ex.pdf)), 6 ([slides-6](http://www.ritsumei.ac.jp/~piumarta/pl/slides/PL-06.pdf), [exercises-6](http://www.ritsumei.ac.jp/~piumarta/pl/ex/PL-06-ex.pdf)), and 7 ([slides-7](http://www.ritsumei.ac.jp/~piumarta/pl/slides/PL-07.pdf), [exercises-7](http://www.ritsumei.ac.jp/~piumarta/pl/ex/PL-07-ex.pdf)). Week 7 is a Prolog tutorial. You should be able to understand it without first reading weeks 5 and 6. But those weeks are important. They show how to  implement many Prolog features in Python.

## Pylog: prolog in Python
This repository is a Python implementation of many Prolog features. It is based on Piumarta’s [`unify.py`](http://www.ritsumei.ac.jp/~piumarta/pl/src/unify.py).

As an introductory example, consider the following (Python) code. (You can run it [here](https://colab.research.google.com/drive/1BkWBGY0GpOYqHLpyylzbPU9OLdyqxSmk).) (The type annotations are not required, but they are useful to understand what's going on.)

```python
from typing import Generator

def isEven(i: int) -> Generator[None, None, None]:
    if i % 2 == 0:
        print(f'{i}-even', end = ', ')
        yield 
    else:
        print(f'{i}-odd', end = ', ')
```
Can you figure out how it produces the following results? 
```python
>>> evens = [i for i in range(10) for _ in isEven(i)] 
0-even, 1-odd, 2-even, 3-odd, 4-even, 5-odd, 6-even, 7-odd, 8-even, 9-odd,

>>> print(evens)
[0, 2, 4, 6, 8] 
```
In particular, what does `for _ in isEven(i)` do in the list comprehension?

In Prolog, program components are understood as predicates. They may *succeed* or *fail*. To succeed/fail means that the system was/was not able to establish that the predicate holds given the information available. 

Success or failure is implemented in Python through generators. A generator that `yield`s a result (at the Python level) is said to succeed (at the Prolog level); one that does not `yield` a result, fails (at the Prolog level).

In this case, `isEven(i)` succeeds/fails when `i` is/is not even. (In either case it produces an output line.) When<br />`for _ in isEven(i)` succeeds/fails for a given `i`, the list comprehension completes/fails to complete the iteration for that `i` and includes (does not include) `i` in the generated list.  

## File organization 

```
pylog
    examples
        n_queens.py
        puzzles.py
        scholarship_problem.py
        trains.py
        zebra_problem.py
    sequence_options
        linked_list.py
        sequences.py
        super_sequence.py
    control_structures.py
    logic_variables.py
```

## File dependencies (Circular dependencies are not allowed.)

```
logic_variables (this file): none
control_structures: logic_variables

super_sequence: control_structures, logic_variables
linked_list and sequences: control_structures, logic_variables, super_sequence

n_queens: logic_variables
trains: control_structures, logic_variables, 
puzzle: logic_variables, super_sequence
zebra_problem: control_structures, logic_variables, puzzles
scholarship_problem: control_structures, logic_variables, puzzles, super_sequence

```
