from __future__ import annotations
from typing import List, Union

from control_structures import forany
from logic_variables import eot, Ground, n_Vars, Term, unify, unify_pairs, unify_sequences, Var
from sequence_options.super_sequence import SuperSequence


class PySequence(SuperSequence):
  """
  Python treats lists and tuples as essentially the same. This is the common core.
  The self.args are the list/tuple elements. Their length is fixed. (This disallows
  appending elements to a list or extending a list.)
  """
  def __init__(self, pyType, initialElements: Union[list, tuple]):
    super().__init__( (pyType, *initialElements) )

  def __add__(self, Other: Union[PySequence, Var]) -> PySequence:
    Other_EoT = Other.trail_end()
    # If not, can't append.
    assert isinstance(Other_EoT, PySequence)
    Result = Var()
    for _ in append(self, Other_EoT, Result):
      Result_EoT = Result.trail_end()
      # To make the PyCharm type checker happy.
      assert isinstance(Result_EoT, PySequence)
      return Result_EoT

  def __getitem__(self, key: Union[int, slice]):
    return self.args[key] if isinstance(key, int) else self.__class__(self.args[key])

  def __len__(self):
    return len(self.args)

  def __str__(self):
    (left, right) = {list: ('[', ']'), tuple: ('(', ')')}[self.functor]
    values_string = self.values_string(self.args)
    result = f'{left}{values_string}{right}'
    return result

  def get_ground_value(self) -> tuple:
    return self.functor(arg.get_ground_value() for arg in self.args)

  def has_adjacent_members(self, E1, E2):
    """ Are E1 and E2 are next to each other in Es. """
    # yield from self.next_to(E1, E2, self)
    for _ in forany([
      lambda: self.has_contiguous_sublist([E1, E2]),
      lambda: self.has_contiguous_sublist([E2, E1]),
    ]):
      yield

  def has_contiguous_sublist(self, As: List):
    """ Can As be unified with a contiguous segment of this list? """
    # yield from self.is_contiguous_in(As, self)
    (len_As, len_self) = (len(As), len(self))
    if len_As == 0:
      yield  # Succeed
    elif len_As > len_self:
      return  # Fail.
    else:
      for i in range(len_self - len_As + 1):
        # Succeed for each self segment that can be unified with As.
        for _ in unify_sequences(As, self.args[i:i+len_As]):
          yield

  def has_member(self, E: Term):
    """ Is E in A_List? """
    # yield from self.member(E, self)
    if len(self) > 0:
      for _ in forany([lambda: unify(E, self.head( )),
                       lambda: self.tail( ).has_member(E)]):
        yield

  def has_members(self, Es: List):
    """ Do all elements of Es appear in this list (in any order). """
    # yield from self.members(Es, self)
    if not Es:
      yield
    elif len(self) > 0:
      for _ in self.has_member(Es[0]):
        yield from self.has_members(Es[1:])

  def head(self):
    return self[0]

  # @staticmethod
  # def is_contiguous_in(As: List, Zs: PySequence):
  #   """ Can As be unified with a contiguous segment of Zs? """
  #   (lenAs, len_Zs) = (len(As), len(Zs))
  #   if lenAs == 0:
  #     yield  # Succeed
  #   elif lenAs > len_Zs:
  #     return  # Fail.
  #   else:
  #     for i in range(len_Zs - lenAs + 1):
  #       # Succeed for each Zs segment that can be unified with As.
  #       for _ in unify_sequences(As, Zs.args[i:i+lenAs]):
  #         yield

  # @staticmethod
  # def member(E: Term, A_List):
  #   """ Is E in A_List? """
  #   if len(A_List) > 0:
  #     for _ in forany([lambda: unify(E, A_List.head( )),
  #                      lambda: PySequence.member(E, A_List.tail( ))]):
  #       yield
  #
  # @staticmethod
  # def members(Es: List, A_List: PySequence):
  #   """ Do all elements of Es appear in A_List (in any order). """
  #   if not Es:
  #     yield
  #   else:  # len(A_List) > 0:
  #     for _ in A_List.has_member(Es[0]):
  #       yield from PySequence.members(Es[1:], A_List)
  #
  # @staticmethod
  # def next_to(E1: Term, E2: Term, Es: PySequence):
  #   """ Are E1 and E2 are next to each other in Es. """
  #   for _ in forany([
  #     lambda: PySequence.is_contiguous_in([E1, E2], Es),
  #     lambda: PySequence.is_contiguous_in([E2, E1], Es),
  #   ]):
  #     yield
  #
  def tail(self) -> PySequence:
    return self.__class__(self.args[1:])

  def to_python_list(self):
    return [*self.args]


class PyList(PySequence):
  def __init__(self, initialElements: list):
    super().__init__( list, initialElements )


class PyTuple(PySequence):
  def __init__(self, initialElements: tuple):
    super( ).__init__( tuple, initialElements )


@eot
def append(Xs: Union[PySequence, Var], Ys: Union[PySequence, Var], Zs: Union[PySequence, Var]):
  """
    append([], Ys, Zs).
    append([X|Xs], Ys, [X|Zs]) :- append(Xs, Ys, Zs).

    See discussion in linked_list version.

    This version assumes we are working with Python lists or tuples, i.e., no uninstantiated tails.
  """

  if isinstance(Zs, Var) and ( isinstance(Xs, Var) or isinstance(Ys, Var) ):
      # Can't have Xs or Ys Var if Zs is Var.
      return

  if isinstance(Zs, Var):
    ListType = type(Xs)
    # Make Zs a list of Var's of length len(Xs) + len(Ys)
    # After this unification, Zs will still be a Var, but
    # by the time we reach this point again, Zs will refer
    # to its trail end, which is not a Var.
    for _ in unify(Zs, ListType(n_Vars(len(Xs) + len(Ys)))):
      yield from append(Xs, Ys, Zs)
    return

  # We now know that: Zs is not a Var -- although it may be a sequence of Vars.
  # Divide up its length among Xs and Ys
  ListType = type(Zs)
  len_Zs = len(Zs)
  for i in range(len_Zs + 1):
    # If Xs or Ys are already instantiated to some fixed length Sequence, unify will fail when given the wrong length.
    for _ in unify_pairs([ (Xs, ListType(n_Vars(i))),
                           (Ys, ListType(n_Vars(len_Zs - i)))  ]):
      # Although the lengths of Xs and Ys vary with i,
      # Xs, Ys, and Zs are all of fixed lengths in which len(Xs) + len(Ys) = len(Zs).
      # Concatenate Xs and Ys and then unify the concatenation with Zs.
      XYs = [*Xs.trail_end().args, *Ys.trail_end().args]
      for _ in unify_sequences(XYs, Zs.args):
        yield


if __name__ == '__main__':

  print(PyTuple( (1, 2, 3) ))
  print(PyList( [1, 2, 3] ))

  Xs = PyList(['Python'])  # list(map(Ground, range(3)))
  Ys = PyList([Ground('Q')])  # [Ground(i+3) for i in range(3)]
  Zs = Var()

  print(f'\nappend({Xs}, {Ys}, {Zs})')
  for _ in append(Xs, Ys, Zs):
    print(f'\tXs: {Xs}, Ys: {Ys}, Zs: {Zs}')

  Xs = Var( )
  Ys = Var( )
  Zs = PyList(list(range(5)))

  print(f'\nappend({Xs}, {Ys}, {Zs})')
  for _ in append(Xs, Ys, Zs):
    print(f'\tXs: {Xs}, Ys: {Ys}, Zs: {Zs}')

  Xs = Var( )
  Ys = Var( )
  Zs = PyTuple(tuple(range(5)))

  print(f'\nappend({Xs}, {Ys}, {Zs})')
  for _ in append(Xs, Ys, Zs):
    print(f'\tXs: {Xs}, Ys: {Ys}, Zs: {Zs}')

  X = tuple(n_Vars(15))
  Y = X[4:8]
  print(f'\nX: {PyTuple(X)}, Y: {PyTuple(Y)}')
  for _ in unify_sequences(Y, tuple(map(Ground, ['A', 'B', 'C', 'D']))):
    print(f"unify_sequences(Y, tuple(map(Ground, ['A', 'B', 'C', 'D']))) => X: {PyTuple(X)}, Y: {PyTuple(Y)}")

  B = tuple(n_Vars(8))
  print(f'\nB: {PyTuple(B)}')

  for _ in unify(B[3], Ground('XYZ')):
    print(f"unify(B[3], Ground('XYZ')) => B: {PyTuple(B)}")
