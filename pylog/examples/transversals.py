from typing import Generator, List, Optional

from control_structures import fails
from logic_variables import unify, Var
from sequence_options.sequences import PyList
from sequence_options.super_sequence import member






"""                  transversal_dfs_first                   """
def transversal_dfs_first(sets: List[List[int]],
                          partial_transversal: List[int]) \
                                  -> Optional[List[int]]:
  """ Looking for the first solution. """
  print(f'sets/{sets}; '
        f'partial_transversal/{partial_transversal}')
  if not sets:
    return partial_transversal
  else:
    (s, ss) = (sets[0], sets[1:])
    for element in s:
      if element not in partial_transversal:
        complete_transversal = \
          transversal_dfs_first(ss,
                                partial_transversal
                                + [element])
        if complete_transversal is not None:
          return complete_transversal


if __name__ == '__main__':
  print(f'\n{"-"*75}\ntransversal_dfs_first([[1, 2, 3], [2, 4], [1]], [])\n')
  print(f'{" "*30}  =>  {transversal_dfs_first([[1, 2, 3], [2, 4], [1]], [])}')

"""Output

---------------------------------------------------------------------------




transversal_dfs_first([[1, 2, 3], [2, 4], [1]], [])

sets/[[1, 2, 3], [2, 4], [1]]; partial_transversal_reversed/[]
sets/[[2, 4], [1]]; partial_transversal_reversed/[1]
sets/[[1]]; partial_transversal_reversed/[1, 2]
sets/[[4], [1]]; partial_transversal_reversed/[1]
sets/[[1]]; partial_transversal_reversed/[1, 4]
sets/[[2, 3], [2, 4], [1]]; partial_transversal_reversed/[]
sets/[[2, 4], [1]]; partial_transversal_reversed/[2]
sets/[[4], [1]]; partial_transversal_reversed/[2]
sets/[[1]]; partial_transversal_reversed/[2, 4]
sets/[]; partial_transversal_reversed/[2, 4, 1]
                                =>  [1, 4, 2]
"""



"""                  transversal_dfs_all                   """
def transversal_dfs_all(sets: List[List[int]], partial_transversal: List[int]) \
                                                                     -> List[List[int]]:
  print(f'sets/{sets}; partial_transversal/{list(partial_transversal)}')
  if not sets:
    return [partial_transversal]
  else:
    (s, ss) = (sets[0], sets[1:])
    all_transversals = []
    for element in s:
      if element not in partial_transversal:
        all_transversals += \
          transversal_dfs_all(ss,
                              partial_transversal + [element])
    return all_transversals


if __name__ == '__main__':
  print(f'\n{"-"*75}\ntransversal_dfs_all([[1, 2, 3], [2, 4], [1]], [])\n')
  print(f'{" "*30}  =>  {transversal_dfs_all([[1, 2, 3], [2, 4], [1]], [])}')

"""
---------------------------------------------------------------------------

transversal_dfs_all([[1, 2, 3], [2, 4], [1]], [])

sets/[[1, 2, 3], [2, 4], [1]]; partial_transversal_reversed/[]
sets/[[2, 4], [1]]; partial_transversal_reversed/[1]
sets/[[1]]; partial_transversal_reversed/[1, 2]
sets/[[1]]; partial_transversal_reversed/[1, 4]
sets/[[2, 4], [1]]; partial_transversal_reversed/[2]
sets/[[1]]; partial_transversal_reversed/[2, 4]
sets/[]; partial_transversal_reversed/[2, 4, 1]
sets/[[2, 4], [1]]; partial_transversal_reversed/[3]
sets/[[1]]; partial_transversal_reversed/[3, 2]
sets/[]; partial_transversal_reversed/[3, 2, 1]
sets/[[1]]; partial_transversal_reversed/[3, 4]
sets/[]; partial_transversal_reversed/[3, 4, 1]
                                =>  [[1, 4, 2], [1, 2, 3], [1, 4, 3]]
"""



"""                  transversal_yield                   """
def transversal_yield(sets: List[List[int]], partial_transversal: List[int]) -> Generator[List[int], None, None]:
  print(f'sets/{sets}; '
        f'partial_transversal/{partial_transversal}')
  if not sets:
    yield partial_transversal
  else:
    (s, ss) = (sets[0], sets[1:])
    for element in s:
      if element not in partial_transversal:
        yield from transversal_yield(ss, partial_transversal + [element])


if __name__ == '__main__':
  print(f'\n{"-"*75}\ntransversal_yield([[1, 2, 3], [2, 4], [1]], [])\n')
  for Ans in transversal_yield([[1, 2, 3], [2, 4], [1]], []):
    print(f'{" "*30}  =>  {Ans}')

"""
---------------------------------------------------------------------------
transversal_yield([[1, 2, 3], [2, 4], [1]], [])

sets/[[1, 2, 3], [2, 4], [1]]; partial_transversal_reversed/[]
sets/[[2, 4], [1]]; partial_transversal_reversed/[1]
sets/[[1]]; partial_transversal_reversed/[1, 2]
sets/[[1]]; partial_transversal_reversed/[1, 4]
sets/[[2, 4], [1]]; partial_transversal_reversed/[2]
sets/[[1]]; partial_transversal_reversed/[2, 4]
sets/[]; partial_transversal_reversed/[2, 4, 1]
                                =>  [1, 4, 2]
sets/[[2, 4], [1]]; partial_transversal_reversed/[3]
sets/[[1]]; partial_transversal_reversed/[3, 2]
sets/[]; partial_transversal_reversed/[3, 2, 1]
                                =>  [1, 2, 3]
sets/[[1]]; partial_transversal_reversed/[3, 4]
sets/[]; partial_transversal_reversed/[3, 4, 1]
                                =>  [1, 4, 3]

"""
"""                  transversal_yield_lv                   """
def transversal_yield_lv(Sets: List[PyList], Partial_Transversal: PyList, Complete_Transversal: Var):
  print(f'Sets/[{", ".join([str(S) for S in Sets])}]; Partial_Transversal/{Partial_Transversal}')
  if not Sets:
    yield from unify(Partial_Transversal, Complete_Transversal)
  else:
    (S, Ss) = (Sets[0], Sets[1:])
    Element = Var( )
    for _ in member(Element, S):
      for _ in fails(member)(Element, Partial_Transversal):
        yield from transversal_yield_lv(Ss, Partial_Transversal + PyList([Element]), Complete_Transversal)


if __name__ == '__main__':
  print(f'\n{"-"*75}\ntransversal_yield_lv([[1, 2, 3], [2, 4], [1]], [], Ans)\n')
  Complete_Transversal = Var( )
  for _ in transversal_yield_lv([PyList([1, 2, 3]), PyList([2, 4]), PyList([1])], PyList([]), Complete_Transversal):
    print(f'{" "*30}  =>  {Complete_Transversal}')

"""
---------------------------------------------------------------------------
transversal_yield_lv([[1, 2, 3], [2, 4], [1]], [], Ans)

Sets/[[1, 2, 3], [2, 4], [1]]; Partial_Transversal/[]
Sets/[[2, 4], [1]]; Partial_Transversal/[1]
Sets/[[1]]; Partial_Transversal/[1, 2]
Sets/[[1]]; Partial_Transversal/[1, 4]
Sets/[[2, 4], [1]]; Partial_Transversal/[2]
Sets/[[1]]; Partial_Transversal/[2, 4]
Sets/[]; Partial_Transversal/[2, 4, 1]
                                =>  [1, 4, 2]
Sets/[[2, 4], [1]]; Partial_Transversal/[3]
Sets/[[1]]; Partial_Transversal/[3, 2]
Sets/[]; Partial_Transversal/[3, 2, 1]
                                =>  [1, 2, 3]
Sets/[[1]]; Partial_Transversal/[3, 4]
Sets/[]; Partial_Transversal/[3, 4, 1]
                                =>  [1, 4, 3]
"""

"""
transversal_prolog(Sets, Partial_Transversal, _Complete_Transversal) :-
    writeln('Sets'/Sets;'  Partial_Transversal'/Partial_Transversal), 
    fail.

transversal_prolog([], Complete_Transversal, Complete_Transversal) :-
    format('                                  '),
    writeln('Partial_Transversal '=Complete_Transversal), nl.

transversal_prolog([S|Ss], Partial_Transversal, Complete_Transversal_X) :-
    member(X, S),
    \+ member(X, Partial_Transversal),
    append(Partial_Transversal, [X], Partial_Transversal_X),
    transversal_prolog(Ss, Partial_Transversal_X, Complete_Transversal_X).


    
    
    
    
    
?- transversal_prolog([[1, 2, 3], [2], [1]], [], Complete_Transversal).

Sets/[[1, 2, 3], [2, 4], [1]]; Partial_Transversal/[]
Sets/[[2, 4], [1]]; Partial_Transversal/[1]
Sets/[[1]]; Partial_Transversal/[1, 2]
Sets/[[1]]; Partial_Transversal/[1, 4]
Sets/[[2, 4], [1]]; Partial_Transversal/[2]
Sets/[[1]]; Partial_Transversal/[2, 4]
Sets/[]; Partial_Transversal/[2, 4, 1]
                                  Complete_Transversal = [2, 4, 1]

Sets/[[2, 4], [1]]; Partial_Transversal/[3]
Sets/[[1]]; Partial_Transversal/[3, 2]
Sets/[]; Partial_Transversal/[3, 2, 1]
                                  Complete_Transversal = [3, 2, 1]

Sets/[[1]]; Partial_Transversal/[3, 4]
Sets/[]; Partial_Transversal/[3, 4, 1]
                                  Answer = [3, 4, 1]


"""