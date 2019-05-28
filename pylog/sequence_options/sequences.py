from __future__ import annotations
from typing import List, Union

from control_structures import forany
from logic_variables import eot, Ground, n_Vars, Term, unify, unify_pairs, unify_sequences, Var
from sequence_options.super_sequence import SuperSequence


class PySequence(SuperSequence):
  def __init__(self, pyType, initialElements: Union[list, tuple]):
    super().__init__( (pyType, *initialElements) )

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

  def head(self):
    return self[0]

  @staticmethod
  def is_contiguous_in(As: List, Zs: PySequence):
    """ Can As be unified with a segment of Zs? """
    (lenAs, lenZs) = (len(As), len(Zs))
    if lenAs == 0:
      yield  # Succeed
    elif lenAs > lenZs:
      return  # Fail.
    else:
      for i in range(lenZs - lenAs + 1):
        # Succeed for each Zs segment that can be unified with As.
        for _ in unify_sequences(As, Zs.args[i:i + lenAs]):
          yield

  @staticmethod
  def member(e: Term, aList):
    """ Is e in aList? """
    if len(aList) > 0:
      for _ in forany([lambda: unify(e, aList.head( )),
                       lambda: PySequence.member(e, aList.tail( ))]):
        yield

  @staticmethod
  def members(es: List, self):
    """ Do all elements of es appear in aList (in any order). """
    if not es:
      yield
    elif len(self) > 0:
      for _ in PySequence.member(es[0], self):
        yield from PySequence.members(es[1:], self)

  @staticmethod
  def next_to(E1, E2, Es):
    """ E1 and E2 are next to each other in Es. """
    for _ in forany([
      lambda: PySequence.is_contiguous_in([E1, E2], Es),
      lambda: PySequence.is_contiguous_in([E2, E1], Es),
    ]):
      yield

  def tail(self):
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
    seq_type = type(Xs)
    # Make Zs a list of Var's of length len(Xs) + len(Ys)
    # After this unification, Zs will still be a Var, but
    # by the time we reach this point again, Zs will refer
    # to its trail end, which is not a Var.
    for _ in unify(Zs, seq_type(n_Vars(len(Xs) + len(Ys)))):
      yield from append(Xs, Ys, Zs)
    return

  # We now know that: Zs is not a Var -- although it may be a sequence of Vars.
  # Divide up its length among Xs and Ys
  seq_type = type(Zs)
  lenZs = len(Zs)
  for i in range(lenZs+1):
    # If Xs or Ys are already instantiated to some fixed length Sequence, unify will fail when given the wrong length.
    for _ in unify_pairs([ (Xs, seq_type(n_Vars(i))),
                           (Ys, seq_type(n_Vars(lenZs - i)))  ]):
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
