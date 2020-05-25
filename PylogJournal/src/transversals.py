from typing import Generator, List, Optional

from control_structures import fails
from logic_variables import unify, Var
from sequence_options.sequences import PyList
from sequence_options.super_sequence import member, reversed

"""
transversal definitions

Kung, J. P., Rota, G. C., & Yan, C. H. (2009). Combinatorics: the Rota way. Cambridge University Press.

Let Y = (SJiel be a family of subsets of a set E. A set K C E is a transversal of the family 9’ if there exists a 
bijection p : K + I such that k E &h) for all k E K. Note that Y may contain the same set more than
once; hence the notation “9 = (S&i’ rather than “9’ = {Si}iEI .” 

Weinberger, D. B. (1974). Sufficient regularity conditions for common transversals. Journal of Combinatorial Theory, 
Series A, 16(3), 380-390.
https://www.sciencedirect.com/science/article/pii/0097316574900612/pdf?md5=2c5a36ee9f7460417ac00d6c8f1ebdbd&isDTMRedir=Y&pid=1-s2.0-0097316574900612-main.pdf&_valck=1
"""








"""                  transversal_dfs_first                   """
def transversal_dfs_first(sets: List[List[int]],
                          so_far: List[int]) \
                                  -> Optional[List[int]]:
  """ Looking for the first solution. """
  print(f'sets/{sets}; so_far_reversed/{so_far[::-1]}')
  if not sets:
    # X[::-1] returns the reverse of X
    return so_far[::-1]
  else:
    # Set s and ss to sets[0] and sets[1:] respectively.
    [s, *ss] = sets
    [x, *s_rest] = s
    t_result = None if x in so_far else \
               transversal_dfs_first(ss, [x] + so_far)
    return t_result if t_result else \
           None if not s_rest else \
           transversal_dfs_first([s_rest] + ss, so_far)


if __name__ == '__main__':
  print(f'\n{"-"*75}\ntransversal_dfs_first([[1, 2, 3], [2, 4], [1]], [])\n')
  print(f'{" "*30}  =>  {transversal_dfs_first([[1, 2, 3], [2, 4], [1]], [])}')

"""Output

---------------------------------------------------------------------------




transversal_dfs_first([[1, 2, 3], [2, 4], [1]], [])

sets/[[1, 2, 3], [2, 4], [1]]; so_far_reversed/[]
sets/[[2, 4], [1]]; so_far_reversed/[1]
sets/[[1]]; so_far_reversed/[1, 2]
sets/[[4], [1]]; so_far_reversed/[1]
sets/[[1]]; so_far_reversed/[1, 4]
sets/[[2, 3], [2, 4], [1]]; so_far_reversed/[]
sets/[[2, 4], [1]]; so_far_reversed/[2]
sets/[[4], [1]]; so_far_reversed/[2]
sets/[[1]]; so_far_reversed/[2, 4]
sets/[]; so_far_reversed/[2, 4, 1]
                                =>  [1, 4, 2]
"""





"""                  transversal_dfs_all                   """
def transversal_dfs_all(sets: List[List[int]], so_far: List[int]) -> List[List[int]]:
  print(f'sets/{sets}; so_far_reversed/{so_far[::-1]}')
  if not sets:
    return [so_far[::-1]]
  else:
    [s, *ss] = sets
    answers = []
    for x in s:
      if x not in so_far:
        answers += transversal_dfs_all(ss, [x] + so_far)
    return answers


if __name__ == '__main__':
  print(f'\n{"-"*75}\ntransversal_dfs_all([[1, 2, 3], [2, 4], [1]], [])\n')
  print(f'{" "*30}  =>  {transversal_dfs_all([[1, 2, 3], [2, 4], [1]], [])[::-1]}')

"""
---------------------------------------------------------------------------

transversal_dfs_all([[1, 2, 3], [2, 4], [1]], [])

sets/[[1, 2, 3], [2, 4], [1]]; so_far_reversed/[]
sets/[[2, 4], [1]]; so_far_reversed/[1]
sets/[[1]]; so_far_reversed/[1, 2]
sets/[[1]]; so_far_reversed/[1, 4]
sets/[[2, 4], [1]]; so_far_reversed/[2]
sets/[[1]]; so_far_reversed/[2, 4]
sets/[]; so_far_reversed/[2, 4, 1]
sets/[[2, 4], [1]]; so_far_reversed/[3]
sets/[[1]]; so_far_reversed/[3, 2]
sets/[]; so_far_reversed/[3, 2, 1]
sets/[[1]]; so_far_reversed/[3, 4]
sets/[]; so_far_reversed/[3, 4, 1]
                                =>  [[1, 4, 2], [1, 2, 3], [1, 4, 3]]
"""



"""                  transversal_yield                   """
def transversal_yield(sets: List[List[int]], so_far: List[int]) -> Generator[List[int], None, None]:
  print(f'sets/{sets}; so_far_reversed/{so_far[::-1]}')
  if not sets:
    yield so_far[::-1]
  else:
    [s, *ss] = sets
    for x in s:
      if x not in so_far:
        for t_result in transversal_yield(ss, [x] + so_far):
          if t_result:
            yield t_result


if __name__ == '__main__':
  print(f'\n{"-"*75}\ntransversal_yield([[1, 2, 3], [2, 4], [1]], [])\n')
  for Ans in transversal_yield([[1, 2, 3], [2, 4], [1]], []):
    print(f'{" "*30}  =>  {Ans}')

"""
---------------------------------------------------------------------------
transversal_yield([[1, 2, 3], [2, 4], [1]], [])

sets/[[1, 2, 3], [2, 4], [1]]; so_far_reversed/[]
sets/[[2, 4], [1]]; so_far_reversed/[1]
sets/[[1]]; so_far_reversed/[1, 2]
sets/[[1]]; so_far_reversed/[1, 4]
sets/[[2, 4], [1]]; so_far_reversed/[2]
sets/[[1]]; so_far_reversed/[2, 4]
sets/[]; so_far_reversed/[2, 4, 1]
                                =>  [1, 4, 2]
sets/[[2, 4], [1]]; so_far_reversed/[3]
sets/[[1]]; so_far_reversed/[3, 2]
sets/[]; so_far_reversed/[3, 2, 1]
                                =>  [1, 2, 3]
sets/[[1]]; so_far_reversed/[3, 4]
sets/[]; so_far_reversed/[3, 4, 1]
                                =>  [1, 4, 3]

"""
"""                  transversal_yield_lv                   """
def transversal_yield_lv(sets: List[PyList], so_far: PyList, Answer: Var):
  print(f'sets/[{", ".join([str(S) for S in sets])}]; so_far_reversed/{reversed(so_far)}')
  if not sets:
    yield from unify(reversed(so_far), Answer)
  else:
    [S, *Ss] = sets
    X = Var( )
    for _ in member(X, S):
      for _ in fails(member)(X, so_far):
        yield from transversal_yield_lv(Ss, PyList([X]) + so_far, Answer)


if __name__ == '__main__':
  print(f'\n{"-"*75}\ntransversal_yield_lv([[1, 2, 3], [2, 4], [1]], [], Ans)\n')
  Ans = Var( )
  for _ in transversal_yield_lv([PyList([1, 2, 3]), PyList([2, 4]), PyList([1])], PyList([]), Ans):
    print(f'{" "*30}  =>  {Ans}')

"""
---------------------------------------------------------------------------
transversal_yield_lv([[1, 2, 3], [2, 4], [1]], [], Ans)

sets/[[1, 2, 3], [2, 4], [1]]; so_far_reversed/[]
sets/[[2, 4], [1]]; so_far_reversed/[1]
sets/[[1]]; so_far_reversed/[1, 2]
sets/[[1]]; so_far_reversed/[1, 4]
sets/[[2, 4], [1]]; so_far_reversed/[2]
sets/[[1]]; so_far_reversed/[2, 4]
sets/[]; so_far_reversed/[2, 4, 1]
                                =>  [1, 4, 2]
sets/[[2, 4], [1]]; so_far_reversed/[3]
sets/[[1]]; so_far_reversed/[3, 2]
sets/[]; so_far_reversed/[3, 2, 1]
                                =>  [1, 2, 3]
sets/[[1]]; so_far_reversed/[3, 4]
sets/[]; so_far_reversed/[3, 4, 1]
                                =>  [1, 4, 3]
"""

"""
transversal_prolog(sets, so_far, _Answer) :-
    reverse(so_far, so_far_reversed),
    writeln('sets'/sets;'  so_far_reversed'/so_far_reversed), 
    fail.

transversal_prolog([], so_far, Answer) :-
    reverse(so_far, Answer),
    format('                                  '),
    writeln('Answer '=Answer), nl.

transversal_prolog([S|Ss], so_far, Answer) :-
    member(X, S),
    \+ member(X, so_far),
    transversal_prolog(Ss, [X|so_far], Answer).
    
    
    
    
    
    
transversal_prolog(Sets, So_Far, _Answer) :-
    reverse(So_Far, So_Far_Reversed),
    writeln('Sets'/Sets;'  So_Far_Reversed'/So_Far_Reversed), 
    fail.

transversal_prolog([], So_Far, Answer) :-
    reverse(So_Far, Answer),
    format('                                  '),
    writeln('Answer '=Answer), nl.

transversal_prolog([S|Ss], So_Far, Answer) :-
    member(X, S),
    \+ member(X, So_Far),
    transversal_prolog(Ss, [X|So_Far], Answer).
    
    
    
    
    
    
?- transversal_prolog([[1, 2, 3], [2], [1]], [], Answer).

Sets/[[1, 2, 3], [2, 4], [1]]; So_Far_Reversed/[]
Sets/[[2, 4], [1]]; So_Far_Reversed/[1]
Sets/[[1]]; So_Far_Reversed/[1, 2]
Sets/[[1]]; So_Far_Reversed/[1, 4]
Sets/[[2, 4], [1]]; So_Far_Reversed/[2]
Sets/[[1]]; So_Far_Reversed/[2, 4]
Sets/[]; So_Far_Reversed/[2, 4, 1]
                                  Answer = [2, 4, 1]

Sets/[[2, 4], [1]]; So_Far_Reversed/[3]
Sets/[[1]]; So_Far_Reversed/[3, 2]
Sets/[]; So_Far_Reversed/[3, 2, 1]
                                  Answer = [3, 2, 1]

Sets/[[1]]; So_Far_Reversed/[3, 4]
Sets/[]; So_Far_Reversed/[3, 4, 1]
                                  Answer = [3, 4, 1]


