from __future__ import annotations
from typing import Any, List, Optional, Tuple, Union

from logic_variables import ensure_is_logic_variable, euc, PyValue, n_Vars, Term, unify, unify_pairs, Var
from sequence_options.super_sequence import is_a_subsequence_of,  member, SuperSequence


class LinkedList(SuperSequence):
  """
  A special Structure for Prolog (Linked) Lists.
  self.functor = 'linkedList'
  self.args is in general a tuple of args. In this case,
  self.args[0] = head(list)
  self.args[1] = LinkedList(tail(list))

  When used as a constructor, the argument must be either a Python list or a (Head, Tail) tuple.
  In the second case, Tail must be a LinkedList or a Var.
  """
  def __init__(self, list_or_tuple: Union[list, str, Term, tuple], tail: Optional[Term] = None ):
    # args will either have two elements or none -- if we are creating an empty list.
    if tail is None:
      args = self.args_from_pyList(list_or_tuple) if isinstance(list_or_tuple, list) else \
             list_or_tuple if isinstance(list_or_tuple, tuple) else \
             self.args_from_pyList(list(list_or_tuple))  # Run list_or_tuple to get a list if it's a generator.
    else:
      args = (list_or_tuple, tail)
    super().__init__( ('linkedList', *args) )

  def __getitem__(self, key: Union[int, slice]):
    (prefix, tail) = self.prefix_and_tail( )
    stop = key if isinstance(key, int) else \
           key.stop if isinstance(key.stop, int) else \
           len(self) if key.stop is None else \
           None
    if len(prefix) >= stop:
      slice_elements = prefix[key]
      if isinstance(key, int):
        return slice_elements
      else:
        return LinkedList(slice_elements)
    if not isinstance(tail, Var):
      return None
    template = LinkedList(n_Vars(stop))
    for _ in unify(self, template):
      (prefix, _) = template.prefix_and_tail()
      return LinkedList(prefix[key])

  def __len__(self):
    return len(self.to_python_list())

  def __str__(self):
    (prefix, tail) = self.prefix_and_tail( )
    valuesString = self.values_string(prefix)
    result = f'[{valuesString}' + (f' | {tail}]' if isinstance(tail, Var) else ']' )
    return result

  @staticmethod
  # pyList is a standard Python list.
  def args_from_pyList(pyList: list):
    """
    Converts a standard Python list into the appropriate args, i.e., (head, tail), for a LinkedList
    :param pyList: a standard Python list
    :return: (nested) args for a LinkedList, i.e, (head, tail) of pylist.
    """
    # return ( ) if not pyList else ( Term.ensure_is_logic_variable(pyList[0]), LinkedList(pyList[1:]) )
    return ( ) if not pyList else ( ensure_is_logic_variable(pyList[0]), LinkedList(pyList[1:]) )

  def get_py_value(self):
    args_list = self.to_python_list()
    py_value_args = [arg.get_py_value() for arg in args_list]
    return py_value_args

  def has_contiguous_sublist(self, As: List):
    """ Can As be unified with a segment of this list? """
    # Initially, As is a standard Python list. Make it a LinkedList.
    As = LinkedList(As)
    (len_As, len_self) = (len(As), len(self))
    if len_As == 0:
      yield  # Succeed once.
    elif len_As > len_self:
      return  # Fail.
    else:
      (Xs, Ys) = n_Vars(2)
      # Succeed if we can find a way to divide self into Xs and Ys so that As is an initial sublist of Ys.
      # for _ in forall([lambda: append(Xs, Ys, self),
      #                  lambda: append(As, Var( ), Ys)
      #                  ]):
      #   yield
      for _ in append(Xs, Ys, self):
        yield from append(As, Var( ), Ys)

  def head(self) -> Term:
    return self.args[0]

  def prefix_and_tail(self) -> Tuple[List[Term], Any]:
    """ Get the initial list of objects and either the tail if it is a Var or [] if it is not a Var. """
    if self.is_empty():
      return ([], [])
    else:
      Tail_EoT = self.tail().unification_chain_end()
      if isinstance(Tail_EoT, LinkedList):
        (tail_prefix, Tail_Tail) = Tail_EoT.prefix_and_tail( )
        return ([self.head()] + tail_prefix, Tail_Tail)
      else:
        return ([self.head()], Tail_EoT)

  def tail(self) -> Union[LinkedList, Var]:
    return self.args[1]

  def to_python_list(self) -> Union[list, Tuple[list, Var]]:
    (prefix, tail) = self.prefix_and_tail()
    return (prefix, tail) if isinstance(tail, Var) else prefix


emptyLinkedList = LinkedList([])


@euc
def append(Xs: Union[LinkedList, Var], Ys: Union[LinkedList, Var], Zs: Union[LinkedList, Var]):
  """
    append([], Ys, Ys).
    append([X|Xs], Ys, [X|Zs]) :- append(Xs, Ys, Zs).

  Note that this could just have well have been written:
    append([Z|Xs], Ys, [Z|Zs]) :- append(Xs, Ys, Zs).
  or
    append([W|Xs], Ys, [W|Zs]) :- append(Xs, Ys, Zs).

  We don't have to implicitly favor the Xs.

  No matter what the variable is called, this is really unifying Xs_head and Zs_head.

  append/3 converts between: Xs + Ys <--> Zs

  It does this by moving elements between the Xs and the Zs.
  If we are moving from Zs to Xs + Ys, there will be multiple answers depending on
  how much of Zs is shifted before we let Ys be the rest.

  The function consists of two "clauses" (see prolog definition above), which are tried in sequence.
  
  Clause 1
  This is the step in which we set Xs to [] and set Ys to Zs. No recursive call.
  At this point, earlier recursion calls will have shifted elements between Xs and Zs.
  But those are not visible at this level.

  Clause 2. The recursive step.
  Move an element between Xs and Zs and call append recursively with Xs_Tail and Zs_Tail.
  Since an empty list cannot unify with a LinkedList that has a head and a tail, if either
  Xs or Zs is empty, unify_pairs will fail.

  The actual code is quite short. It's very similar to the prolog code.
  """

  # Corresponds to append([], Ys, Ys).
  yield from unify_pairs([(Xs, emptyLinkedList), (Ys, Zs)])

  # Corresponds to append([X | Xs], Ys, [X | Zs]): - append(Xs, Ys, Zs).
  (XZ_Head, Xs_Tail, Zs_Tail) = n_Vars(3)
  for _ in unify_pairs([(Xs, LinkedList(XZ_Head, Xs_Tail)),
                        (Zs, LinkedList(XZ_Head, Zs_Tail))]):
    yield from append(Xs_Tail, Ys, Zs_Tail)


if __name__ == '__main__':

  print( LinkedList([]) == LinkedList(()))

  print(emptyLinkedList)
  E = PyValue(3)
  for _ in member(E, emptyLinkedList):
    print(f'Error: should not get here.')

  A = LinkedList(Var( ), Var( ))
  A112 = A[4:11:2]
  A37 = A[3:7]
  print(f'\nA: {A}\nA[3:7]: {A37}\nA[4:11:2]: {A112}')
  for _ in unify(A37, LinkedList('ABCD')):
    print(f'\nA: {A}\nA[3:7]: {A37}\nA[4:11:2]: {A112}')
    print( )

  print(f'A[:4]: {A[:4]}')
  A_tail = A.tail()
  print(f'A.tail()[:3]: {A_tail[:3]}')
  print(f'A.tail().tail()[:2]: {A.tail().tail()[:2]}')

  print(f'\nemptyLinkedList: {emptyLinkedList}')

  Xs = LinkedList([*range(10)])
  print(f'\nSlices: Xs: {Xs}')
  print(f'\tXs[2:-1:2]: {Xs[2:-1:2]}')
  print(f'\tXs[-1:2:-2]: {Xs[-1:2:-2]}')
  print(f'\tXs[5]: {Xs[5]}')
  """
  Slices: Xs: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    tXs[2, -1, 2]: [2, 4, 6, 8]
    Xs[-1, 3, -1]: [9, 7, 5, 3]
    Xs[5]: 5
  """
  Xs = list(map(PyValue, range(9)))
  Sub_Xs = [PyValue(1), Var( ), PyValue(4), Var( ), PyValue(8)]
  print(f'\nLinkedList(Sub_Xs): {LinkedList(Sub_Xs)}, LinkedList(Xs): {LinkedList(Xs)}')
  for _ in is_a_subsequence_of(Sub_Xs, LinkedList(Xs)):
    print(f'\tLinkedList(Sub_Xs): {LinkedList(Sub_Xs)}')
  Sub_Xs = [PyValue(1), Var( ), PyValue(8), Var( ), PyValue(7)]
  print(f'\nLinkedList(Sub_Xs): {LinkedList(Sub_Xs)}, LinkedList(Xs): {LinkedList(Xs)}')
  for _ in is_a_subsequence_of(Sub_Xs, LinkedList(Xs)):
    print(f'\tLinkedList(Sub_Xs): {LinkedList(Sub_Xs)}')

  (Start, Pivot, End) = n_Vars(3)
  Zs = LinkedList( list(range(10)) )

  L = LinkedList( n_Vars(3) )
  print(f'\nGiven: L = LinkedList( n_Vars(3) ): {L}' )
  E = Var( )
  for _ in unify(L, LinkedList([1, 2, 3])):
    print(f'Given: E: {E}, L: {L}')

    print(f'?- LinkedList.member(E, L)')
    for _ in member(E, L):
      print(f'E = {E}')

  A_List = LinkedList( [*map(PyValue, [1, 2, 3, 2, 1])] )
  E_Sub = [PyValue(2), Var( )]
  linkedlistE_Sub = LinkedList(E_Sub)
  print(linkedlistE_Sub)
  print(f'\nE_Sub: {linkedlistE_Sub}\n?- is_contiguous_in(E_Sub, {A_List})')
  for _ in A_List.has_contiguous_sublist(E_Sub):
    print(f'E_Sub: {linkedlistE_Sub}')

  E_Sub = [Var( ), PyValue(2)]
  linkedlistE_Sub = LinkedList(E_Sub)
  print(f'\nE_Sub: {linkedlistE_Sub}\n?- is_contiguous_in(E_Sub, {A_List})')
  for _ in A_List.has_contiguous_sublist(E_Sub):
    print(f'E_Sub: {linkedlistE_Sub}')

  X = PyValue('abc')
  Z1 = Var( )
  Y1 = LinkedList([X, Z1])

  Z2 = Var( )
  Z3 = Var( )
  Y2 = LinkedList([Z2, Z3])

  print(f'\n1. Y1: {Y1}, Y2: {Y2}')
  for _ in unify_pairs([(Y1, Y2), (Z2, Z3)]):
    print(f'2. Y1: {Y1}, Y2: {Y2}')
  print(f'3. Y1: {Y1}, Y2: {Y2}')

  print('\nAgain, switching the order of the unifications')
  print(f'4. Y1: {Y1}, Y2: {Y2}')
  for _ in unify_pairs([(Y1, Y2), (Z2, Z3)]):
    print(f'5. Y1: {Y1}, Y2: {Y2}')
  print(f'6. Y1: {Y1}, Y2: {Y2}')
  print('End test')

  """
  Expected output
  
  emptyLinkedList: []
  LinkedList([1, 2, 3]): [1, 2, 3]
  
  1. Y1: [abc, _13], Y2: [_17, _17]
  2. Y1: [abc, abc], Y2: [abc, abc]
  3. Y1: [abc, _13], Y2: [_17, _17]
  
  End test
  """

  # Append examples
  # Run "forward:" Xs + Ys --> Zs
  # Only one way to do this.
  (Xs, Ys, Zs) = (LinkedList([0, 1]), LinkedList([2, 3, 4]), Var())
  print(f'\nGiven: Zs: {Zs}\n?- append({Xs}, {Ys}, Zs)')
  for _ in append(Xs, Ys, Zs):
    print(f'Zs = {Zs}')

  # Run "backward:" Zs --> Xs + Ys
  # Multiple ways to split up Zs between Xs and Ys
  (Xs, Ys, Zs) = (Var(), Var(), LinkedList([1, 2, 3]))
  print(f'\nGiven: Xs: {Xs}, Ys: {Ys}, Zs: {Zs}\n?-  append(Xs, Ys, {Zs};')
  for _ in append(Xs, Ys, Zs):
    print(f'Xs = {Xs}\nYs = {Ys}\nZs = {Zs}\n')

  (Xs, Ys, Zs) = (LinkedList([1, 2, 3]), Var(), Var())
  print(f'\nGiven: Xs: {Xs}, Ys: {Ys}, Zs: {Zs}')
  print(f'?- append({Xs}, Ys, Zs); ')
  for _ in append(Xs, Ys, Zs):
    print(f'nlXs = {Xs}')
    print(f'Ys = {Ys}')

  """
  Expected output:
  
  > append([0, 1], [2, 3, 4], Zs); (Zs: _14)
  Zs = [0, 1, 2, 3, 4]
  Zs = _14
  """

  (Xs, Ys, Zs) = (Var(), Var(), LinkedList([1, 2, 3, 4]))
  print(f'\nGiven: Ys: {Ys}, Zs: {Zs}\n?- append({Xs}, Ys, Zs); ')
  for _ in append(Xs, Ys, Zs):
    print(f'Ys = {Ys}')
    print(f'Zs = {Zs}')

  """
  
  > append(Xs, Ys, [0, 1, 2, 3, 4]); (Xs: _36, Ys: _37)
  Xs = []
  Ys = [0, 1, 2, 3, 4]
  
  Xs = [0]
  Ys = [1, 2, 3, 4]
  
  Xs = [0, 1]
  Ys = [2, 3, 4]
  
  Xs = [0, 1, 2]
  Ys = [3, 4]
  
  Xs = [0, 1, 2, 3]
  Ys = [4]
  
  Xs = [0, 1, 2, 3, 4]
  Ys = []
  
  
  > append([1, 2, 3], Ys, Zs); (Ys: _122, Zs: _123)
  Ys = _139;
  Zs = ([], 1, ([], 2, ([], 3, _139)))
  
  """

  print(f'\n?- LinkedList([Var()]).is_instantiated(): {LinkedList([Var( )]).is_instantiated( )}')
  A = LinkedList([1, 2, 3])
  B_Head = Var( )
  B_Tail = Var( )
  B = LinkedList(B_Head, B_Tail)

  print(f'1. A: {A}, B: {B}')
  for _ in unify(A, B):
    print(f'2. A: {A}, B: {B}')

    B_Tail_TrailEnd = B_Tail.unification_chain_end( )
    C = LinkedList([0, *B_Tail_TrailEnd.get_py_value( )])
    print(f'3. C: {C}')

    D2 = Var( )
    D3 = Var( )
    D = LinkedList([D3, D2, D3])

    print(f'4a. B: {B}, D: {D}')
    for _ in unify(D.tail(), B.tail()):
      print(f'4b. unify(D.tail(), B.tail() => B: {B}, D: {D}')
    for _ in unify(D.head(), B):
      print(f'4c. unify(D.head(), B) => B: {B}, D: {D}')
    E = Var( )
    print(f'5a. B: {B}, E: {E}')
    for _ in unify(E, B):
      # Since E is a Var, must take its unification_chain_end to get something that has a head and tail.
      E_EoC = E.unification_chain_end( )
      assert isinstance(E_EoC, LinkedList)
      print(f'5b. unify(E, B) => E: {E}, E_EoT.head(): {E_EoC.head( )}, E_EoT.tail(): {E_EoC.tail( )}\n')

  # The empty LinkedList is a LinkedList ith no arguments.
  head = PyValue('head')
  Unclosed_List1 = LinkedList(head, Var( ))
  print(f'6. Unclosed_List1: {Unclosed_List1}, len(Unclosed_List1): {len(Unclosed_List1)}')
  Unclosed_List2 = LinkedList(Var( ), Var( ))
  print(f'7. Unclosed_List2: {Unclosed_List2}, len(Unclosed_List2): {len(Unclosed_List2)}')
  for _ in unify(LinkedList([*range(5)]), Unclosed_List2):
    print(f'8. unify(LinkedList([*range(5)]), Unclosed_List2) => ' 
          f'Unclosed_List2: {Unclosed_List2}; len(Unclosed_List2): {len(Unclosed_List2)}')

  Unclosed_List3 = LinkedList(Var( ), Var( ))
  print('\nStarting to call member on an open-ended list.')
  limit1 = 4
  for _ in member(PyValue(5), Unclosed_List3):
    if limit1 <= 0:
      break
    limit1 -= 1
    print(Unclosed_List3)
    limit2 = 2
    for _ in member(PyValue(9), Unclosed_List3):
      if limit2 <= 0:
        break
      limit2 -= 1
      print(Unclosed_List3)

  print('\nEnd fifth test\n')

  """
  Expected output
  
  LinkedList([Var()]).is_instantiated(): False
  1. A: [1, 2, 3], B: ('[]', '_46', '_47')
  2. A: [1, 2, 3], B: [1, 2, 3]
  3. C: [0, 2, 3]
  4. D3: 3, D2: 2, D: [3, 2, 3]
  5. E: [1, 2, 3], E_EoT.head(): 1, E_EoT.tail(): [2, 3]
  
  6. Unclosed_List1: ('[]', 'head', '_64')
  7. Unclosed_List2: ('[]', '_66', '_67')
  8. Unclosed_List2: [1, 2, 3]
  
  End fifth test
  """
