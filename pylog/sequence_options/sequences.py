from __future__ import annotations
from typing import List, Union

from logic_variables import euc, PyValue, n_Vars, unify, unify_pairs, unify_sequences, Var
from sequence_options.super_sequence import SuperSequence


class PySequence(SuperSequence):
  """
  Python treats lists and tuples as essentially the same. This is the common core.
  The self.args are the list/tuple elements. Their length is fixed. (This disallows
  appending elements to a list or extending a list.)
  """
  def __init__(self, pyType, initialElements: Union[list, set, tuple]):
    super().__init__( (pyType, *initialElements) )

  def __add__(self, Other: Union[PySequence, Var]) -> PySequence:
    Other_EoT = Other.unification_chain_end()
    # If not, can't append.
    assert isinstance(Other_EoT, PySequence)
    Result = Var()
    for _ in append(self, Other_EoT, Result):
      Result_EoT = Result.unification_chain_end()
      # To make the PyCharm type checker happy.
      assert isinstance(Result_EoT, PySequence)
      return Result_EoT

  def __getitem__(self, key: Union[int, slice]):
    return self.args[key] if isinstance(key, int) else self.__class__(self.args[key])

  def __len__(self):
    return len(self.args)

  def __str__(self):
    (left, right) = {list: ('[', ']'), set: ('{', '}'), tuple: ('(', ')')}[self.functor]
    values_string = self.values_string(self.args)
    if len(self.args) == 1 and self.functor == tuple:
      values_string = values_string + ", "
    result = f'{left}{values_string}{right}'
    return result

  def get_py_value(self) -> tuple:
    return self.functor(arg.get_py_value() for arg in self.args)

  def has_contiguous_sublist(self, As: List):
    """ Can As be unified with a contiguous segment of this list? """
    (len_As, len_self) = (len(As), len(self))
    if len_As == 0:
      yield  # Succeed
    elif len_As > len_self:
      return  # Fail.
    else:
      for i in range(len_self - len_As + 1):
        # Succeed for each segment of self that can be unified with As.
        # This is the same strategy used in the LinkedList version. Just much more straightforward.
        for _ in unify_sequences(As, self.args[i:i+len_As]):
          yield

  def head(self):
    return self[0]

  def tail(self) -> PySequence:
    return self.__class__(self.args[1:])

  def to_python_list(self) -> list:
    return [*self.args]


class PyList(PySequence):
  def __init__(self, initialElements: list):
    super().__init__( list, initialElements )


class PyTuple(PySequence):
  def __init__(self, initialElements: tuple):
    super( ).__init__( tuple, initialElements )


class PySet(PySequence):
  def __init__(self, initialElements: Union[list, set, tuple]):
    """ Doesn't check to see whether initialElements is really a set. """
    super( ).__init__( set, tuple(initialElements) )

  def discard(self, Other: PyValue) -> PySet:
    Other_EoT = Other.unification_chain_end()
    new_args = [arg for arg in self.args if arg != Other_EoT]
    new_set = PySet(new_args)
    return new_set


@euc
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
      XYs = [*Xs.unification_chain_end().args, *Ys.unification_chain_end().args]
      yield from unify_sequences(XYs, Zs.args)
      # for _ in unify_sequences(XYs, Zs.args):
      #   yield


if __name__ == '__main__':

  print(PyTuple( (1, 2, 3) ))
  print(PyList( [1, 2, 3] ))

  Xs = PyList(['Python'])  # list(map(PyValue, range(3)))
  Ys = PyList([PyValue('Q')])  # [PyValue(i+3) for i in range(3)]
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
  for _ in unify_sequences(Y, tuple(map(PyValue, ['A', 'B', 'C', 'D']))):
    print(f"unify_sequences(Y, tuple(map(PyValue, ['A', 'B', 'C', 'D']))) => X: {PyTuple(X)}, Y: {PyTuple(Y)}")

  B = tuple(n_Vars(8))
  print(f'\nB: {PyTuple(B)}')

  for _ in unify(B[3], PyValue('XYZ')):
    print(f"unify(B[3], PyValue('XYZ')) => B: {PyTuple(B)}")
