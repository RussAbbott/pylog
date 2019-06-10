from __future__ import annotations
from functools import wraps
from inspect import isgeneratorfunction
from numbers import Number
from typing import Any, Iterable, List, Optional, Sequence, Sized, Tuple, Union

"""
Developed by Ian Piumarta as the "unify" library (http://www.ritsumei.ac.jp/~piumarta/pl/src/unify.py) for a
course on programming languages (http://www.ritsumei.ac.jp/~piumarta/pl/index.html). 

See discussion on the GitHub page: https://github.com/RussAbbott/pylog
"""

"""
The pylog core, this file contains the logic variable and data structure classes and the unify function.
"""


def eot(f):
  """ A decorator that takes trail_end() of all Var arguments """

  def var_trail_end(v):
    return v.trail_end() if isinstance(v, Var) else v

  def arg_Vars_trail_ends(args):
    args_trail_ends = (var_trail_end(arg) for arg in args)
    return args_trail_ends

  def dict_Vars_trail_ends(dic):
    dic_trail_ends = {k: var_trail_end(v) for (k, v) in dic.items()}
    return dic_trail_ends

  @wraps(f)
  def eot_wrapper_gen(*args, **kwargs):
    args_trail_ends = arg_Vars_trail_ends(args)
    kwargs_trail_ends = dict_Vars_trail_ends(kwargs)
    yield from f(*args_trail_ends, **kwargs_trail_ends)

  @wraps(f)
  def eot_wrapper_non_gen(*args, **kwargs):
    args = arg_Vars_trail_ends(args)
    kwargs_trail_ends = dict_Vars_trail_ends(kwargs)
    return f(*args, **kwargs_trail_ends)

  return eot_wrapper_gen if isgeneratorfunction(f) else eot_wrapper_non_gen


class Term:
  """

                                                     Term  (An abstract logic variable superclass)
                                                       |
                               ------------------------------------------------
                               |                       |                      |
                            PyValue                   Var                 Structure
                               |                                              |
                   --------------------------                            SuperSequence
                    int, float, string, etc.                                  |
                   Any immutable Python value                        -------------------
                                                                     |                 |
                                                                 LinkedList       PySequence
                                                                                       |
                                                                                 -------------
                                                                                 |           |
                                                                               PyList      PyTuple
  """

  term_count = 0

  def __init__(self):
    Term.term_count += 1
    self.term_id = self.term_count

  # @eot Can't use decorators on dunder methods without doing this:
  # (https://stackoverflow.com/questions/55550300/python-how-to-decorate-a-special-dunder-method).
  # Not sure I understand it. Not sure it's worth the trouble.
  def __eq__(self, other: Term) -> bool:
    """
    self == other if either (a) they have the same py_value or (b) are the same variable.
    """
    (self_eot, other_eot) = (self.trail_end(), other.trail_end())
    return self_eot is other_eot or \
           (self is not self_eot or other is not other_eot) and self_eot == other_eot

  def __lt__(self, other: Term) -> bool:
    return str(self) < str(other)

  def __ne__(self, other: Term) -> bool:
    return not (self == other)

  def __str__(self) -> str:
    """
    The str( ) of a Var is (a) the str of its py_value if is_instantiated( ) or (b) its term_id otherwise.
    """
    self_eot = self.trail_end( )
    return f'{self_eot}' if self_eot.is_instantiated( ) or isinstance(self_eot, Structure) else \
           f'_{self_eot.term_id}'

  def get_py_value(self) -> Any:
    return None

  @eot
  def is_instantiated(self) -> bool:
    """ Should never get here since no trail-end is a Term. """
    return False

  def trail_end(self) -> Term:
    return self


def is_immutable(x):
  return (isinstance(x, (Number, str, bool, type(None))) or
          isinstance(x, (frozenset, tuple)) and all(is_immutable(c) for c in x))


class PyValue(Term):

  """ A wrapper class for integers, strings, and other immutable Python value. """

  def __init__(self, py_value: Optional[str, Number] = None ):
    assert is_immutable(py_value), f"Only immutable values are allowed as PyValues. {py_value} is mutable."
    self._py_value = py_value
    super( ).__init__( )

  def __eq__(self, other: Term) -> bool:
    other_eot = other.trail_end()
    return (isinstance(other_eot, PyValue) and
            self.get_py_value() == other_eot.get_py_value() and
            # Don't need to test both.
            self.is_instantiated() and other.is_instantiated)

  def __lt__(self, other: Term) -> bool:
    other_eot = other.trail_end()
    return isinstance(other_eot, PyValue) and self.get_py_value() < other_eot.get_py_value()

  def __str__(self) -> str:
    return f'{self._py_value}'

  # This instantiates a PyValue, which had been None. This is dangerous since it mutates this object.
  def _set_py_value(self, py_value):
    assert is_immutable(py_value), f"Only immutable values are allowed as PyValues. {py_value} is mutable."
    self._py_value = py_value

  def get_py_value(self) -> Any:
    return self._py_value

  @staticmethod
  def get_py_values(Vars: List[Var]):
    return [v.get_py_value( ) for v in Vars]

  def is_instantiated(self) -> bool:
    return self.get_py_value() is not None


class Structure(Term):
  """
  self.functor is the functor
  self.args is a tuple of args
  """
  def __init__(self, term: Tuple = ( None, () ) ):
    self.functor = term[0]
    self.args = tuple(map(ensure_is_logic_variable, term[1:]))
    super().__init__()

  def __eq__(self, other: Term) -> bool:
    other_eot = other.trail_end()
    return (other_eot is self or
            isinstance(other_eot, Structure) and
            self.functor == other_eot.functor and
            len(self.args) == len(other_eot.args) and
            all([selfArg == other_eotArg for (selfArg, other_eotArg) in zip(self.args, other_eot.args)]))

  def __getitem__(self, key: Union[int, slice]):
    return self.args[key]

  # noinspection PySimplifyBooleanCheck
  def __str__(self):
    args_str = self.values_string(self.args)
    result = f'{self.functor}({args_str})'
    return result

  def get_py_value(self) -> Structure:
    py_value_args = [arg.get_py_value() for arg in self.args]
    return Structure( (self.functor, *py_value_args) )

  def is_instantiated(self) -> bool:
    """ A Structure is instantiated if all its args are. """
    args_are_instantiated = all(arg.is_instantiated() for arg in self.args)
    return args_are_instantiated

  @staticmethod
  def values_string(values: Iterable):
    result = ', '.join(map(str, values))
    return result


class StructureItem(Structure):
  """
  A utility class for building and displaying Structure-based items.
  """

  def __init__(self, args, first_arg_as_str_functor=False):
    self.first_arg_as_str_functor = first_arg_as_str_functor
    functor = type(self).__name__.lower( )
    super().__init__( (functor, *map(make_property, args)) )

  def __str__(self):
    all_args_uninstantiated = all(isinstance(arg.trail_end(), Var) for arg in self.args)
    if all_args_uninstantiated:
      # If all the args are uninstantiated, print a simple underscore.
      return '_'
    elif self.first_arg_as_str_functor:
      # If first_arg_as_str_functor, use the first arg as the functor for printing.
      args_str = ', '.join(map(str, self.args[1:]))
      result = f'{self.args[0]}({args_str})'
      return result
    else:
      # Use default Structure __str__( )
      return super().__str__( )


class Var(Term):
  """
  A logic variable
  """

  def __init__(self):
    # self.trail_next points to the next element on the trail, if any.
    self.trail_next = None
    super().__init__()

  def __getattr__(self, item):
    self_eot = self.trail_end()
    if self is not self_eot:
      return self_eot.__getattribute__(item)

  # Apparently __getattr__ is not called for calls to __getitem__ when __getitem__ is missing
  def __getitem__(self, key: Union[int, slice]):
    self_eot = self.trail_end()
    if self is not self_eot and hasattr(self_eot, '__getitem__'):
      return self_eot.__getitem__(key)

  def __len__(self):
    self_eot = self.trail_end()
    # To make PyCharm's type checker happy.
    assert isinstance(self_eot, Sized)
    return None if not hasattr(self_eot, '__len__') or self == self_eot else len(self_eot)

  def _has_trail_next(self) -> bool:
    # Is this the end of the trail?
    return self.trail_next is not None

  @eot
  def get_py_value(self) -> Optional[Any]:
    return self.get_py_value( ) if self.is_instantiated( ) else None

  # Can't use @eot. Generates an infinite recursive loop.
  def is_instantiated(self) -> bool:
    """ A Var is_instantiated if its trail end is_instantiated """
    Trail_End_Var = self.trail_end( )
    return not isinstance(Trail_End_Var, Var) and Trail_End_Var.is_instantiated()

  def trail_end(self):
    """
    return: the Term, whatever it is, at the end of this Var's unification trail.
    """
    return self.trail_next.trail_end( ) if self._has_trail_next( ) else self


# @staticmethod
def ensure_is_logic_variable(x: Any) -> Term:
  # PyValue anything that is not a Term.
  return x if isinstance(x, Term) else PyValue(x)


# @staticmethod
def make_property(prop):
  """
    Applied to each argument in a term.
    Applies PyValue to those that are not already Terms.
    If a property is None, create a Var for it.
  """
  return Var( ) if prop is None else ensure_is_logic_variable(prop)  # \
  # prop if isinstance(prop, Term) else \
  # PyValue(prop)


def n_Vars(n: int) -> List[Var]:
  """ Generate a list of uninstantiated variables of length n. """
  return [Var( ) for _ in range(n)]


# noinspection PyProtectedMember
@eot
def unify(Left: Any, Right: Any):
  """
  Unify two logic Terms.

  The strategy is to keep track of the "unification trail" for all variables.

  The unification trail is a linked list of logic variables, which are all unified.

  The final element on the trail is either
  o a non-Var, in which case the value of all preceding variables is the value of that non-Var, or
  o a Var (which is not linked to any further element), in which case, all variables on the trail
    are unified but do not (yet) have a value.
  """

  # Make sure both Left and Right are logic variables. This allows us to call, e.g, unify(X, 'abc').
  # ensure_is_logic_variable will wrap 'abc' in a PyValue.
  (Left, Right) = map(ensure_is_logic_variable, (Left, Right))

  # If the trail_ends are equal, either because they have the same py_value or Structure or
  # because they are the same (unbound) Var, do nothing. They are already unified.
  # yield to indicate unification success. If Left and Right are both
  # uninstantiated PyValues, Left != Right. (See PyValue.__eq__.)
  if Left == Right:
    yield

  # The rest consists of special cases: both PyValues, both Structures, at least one Var.

  # Case 1. Both PyValues and exactly one is instantiated.
  # "Assign" it's value to the other. This is similar to (but simpler than)
  # how we handle two Var's. But instead of building a trail, we "assign"
  # one value to the other.
  elif isinstance(Left, PyValue) and isinstance(Right, PyValue) and \
       (not Left.is_instantiated( ) or not Right.is_instantiated( )) and \
       (Left.is_instantiated( ) or Right.is_instantiated( )):
    (assignedTo, assignedFrom) = (Left, Right) if Right.is_instantiated( ) else (Right, Left)
    assignedTo._set_py_value(assignedFrom.get_py_value( ))
    yield
    # See discussion in unify below for why we do this.
    assignedTo._set_py_value(None)
    # :
    # # If they are both PyValues, treat specially.
    # yield from unify_PyValues(Left, Right)
    
  # Case 2. Both  Structures. They can be unified if
  # (a) they have the same functor and
  # (b) their arguments can be unified.
  elif isinstance(Left, Structure) and isinstance(Right, Structure) and Left.functor == Right.functor:
    yield from unify_sequences(Left.args, Right.args)

  # Case 3. At least one is a Var. Since we use @eot, it's the end of its trail.
  # Make the other an extension of its trail.
  # (If both are Vars, it makes no functional difference which extends which.)
  elif isinstance(Left, Var) or isinstance(Right, Var):
    (pointsFrom, pointsTo) = (Left, Right) if isinstance(Left, Var) else (Right, Left)
    pointsFrom.trail_next = pointsTo
    yield
    # All yields create a context in which more of the program is executed--like
    # the body of a while-loop or a for-loop. A "next()" request asks for alternatives.
    # But there is only one functional way to do unification. So on "backup," unlink the
    # two and exit without a further yield, i.e., fail.

    # This is fundamental! It's what makes it possible for a Var to become un-unified outside
    # the context in which it was unified, e.g., unifying a Var with (successive) members
    # of a list. The first successful unification must be undone before the second can occur.
    pointsFrom.trail_next = None

    
def unify_pairs(tuples: List[Tuple[Any, Any]]):
  """ Apply unify to pairs of terms. """
  # If no more tuples, we are done.
  if not tuples:
    yield
  else:
    # Get the first tuple from the tuples list.
    [(Left, Right), *restOfTuples] = tuples
    # If they unify, go on to the rest of the tuples list.
    for _ in unify(Left, Right):
      yield from unify_pairs(restOfTuples)
    # The preceding is equivalent to the following.
    # for _ in forall([lambda: unify(Left, Right),
    #                  lambda: unify_pairs(restOfTuples)]):
    #   yield


def unify_sequences(seq_1: Sequence, seq_2: Sequence):
  """ Unify simple sequences, e.g., lists or tuples, of Terms. """
  # The two sequences must be the same length.
  if len(seq_1) != len(seq_2):
    return

  # If they are both empty, we are done.
  if len(seq_1) == 0:
    yield

  else:
    # Unify the two first elements. If successful go on to the rest.
    # Note that slice notation is supported.
    for _ in unify(seq_1[0], seq_2[0]):
      yield from unify_sequences(seq_1[1:], seq_2[1:])


if __name__ == '__main__':

  A = 'abc'
  B = Var( )
  C = Var( )
  D = 'def'
  print(f'\nA: {A}; B: {B}; C: {C}; D: {D}')
  print(f'Attempting: unify_pairs([(A, B), (B, C), (C, D)]).  A, B, C, D will all be the same if it succeeds.')
  for _ in unify_pairs([(A, B), (B, C), (C, D)]):
    print(f'b. A: {A}; B: {B}; C: {C}; D: {D}')
  print('As expected, unify_pairs fails -- because A and D have distinct PyValue values.')

  PV1 = PyValue()
  PV2 = PyValue()
  print(f'\nTrying unify({PV1}, {PV2}). '
        f"Should fail because we explicitly don't allow two uninstantiated PV's to unify.")
  for _ in unify(PV1, PV2):
    print("Shouldn't have succeeded.")
  print("Failed, as expected, if nothing before this.")
  print(f'Trying unify({PV1}, 1). Should succeed.')
  for _ in unify(PV1, 1):
    print(f"PV1.is_instantiated(): {PV1.is_instantiated()}: {PV1}")
  print(f"PV1.is_instantiated(): {PV1.is_instantiated()}: {PV1}")

  A = Var( )
  # B, C, and D are the same as above.

  print(f'\n1. A: {A}; B: {B}; C: {C}; D: {D}')
  for _ in unify(A, B):
    print(f'2a. After unify(A, B).  A: {A}; B: {B}; C: {C}; D: {D}')
    for _ in unify(A, C):
      print(f'2b. After unify(A, C). A: {A}; B: {B}; C: {C}; D: {D}')
      for _ in unify(A, D):
        print(f'2c. After unify(A, D). A: {A}; B: {B}; C: {C}; D: {D}')
  print(f'3. Outside the scope of all unifies. A: {A}; B: {B}; C: {C}; D: {D}')

  print('End first test\n')

  """
  A: abc; B: _2; C: _3; D: def
  Attempting: unify_pairs([(A, B), (B, C), (C, D)]).  A, B, C, D will all be the same if it succeeds.
  As expected, unify_pairs fails.
  
  1. A: _5; B: _6; C: _7; D: def
  2a. After unify(A, B).  A: _6; B: _6; C: _7; D: def
  2b. After unify(A, C). A: _7; B: _7; C: _7; D: def
  2c. After unify(A, D). A: def; B: def; C: def; D: def
  3. Outside the scope of all unifies. A: _5; B: _6; C: _7; D: def
  End first test
  """

  A = Var( )
  B = Var( )
  C = Var( )
  D = 'xyz'

  print(f'1. A: {A}, B: {B}, C: {C}, D: {D}')
  for _ in unify_pairs([(A, B), (B, C)]):
    print(f'2. After unify_pairs([(A, B), (B, C)]):. A: {A}, B: {B}, C: {C}, D: {D}')

    for _ in unify(D, B):
      print('3. After unify(D, B): A: {A}, B: {B}, C: {C}, D: {D}'  # => A.eot: xyz, B.eot: xyz, C.eot: xyz, D.eot: xyz
            )

    print(f'\n4. No longer unified with D. A: {A}, B: {B}, C: {C}')  # => A: xyz, B: xyz, C: xyz, D: xyz
  print(f'5. No longer unified with each other. A: {A}, B: {B}, C: {C}')  # => A: xyz, B: xyz, C: xyz, D: xyz
  print('\nEnd second test\n')

  """
  Expected output

  1. A: _13, B: _14, C: _15
  2. A: _15, B: _15, C: _15
  3. A.eot: _15, B.eot: _15, C.eot: _15
  4. A.eot: xyz, B.eot: xyz, C.eot: xyz, D.eot: xyz

  5. A: _15, B: _15, C: _15
  6. A: _13, B: _14, C: _15

  End second test
  """

  X = Var( )
  Y = Var( )
  Z = Var( )
  print(f'X: {X}, Y: {Y}, Z: {Z}')
  for _ in unify('abc', X):
    print(f'After unify("abc", X): X: {X}, Y: {Y}, Z: {Z}')  # => abc
    for _ in unify(X, Y):
      print(f'After unify(X, Y): X: {X}, Y: {Y}, Z: {Z}')  # => abc
      for _ in unify(Z, Y):
        print(f'After unify(Z, Y): X: {X}, Y: {Y}, Z: {Z}')  # => abc
      print(f'Outside unify(Z, Y): X: {X}, Y: {Y}, Z: {Z}')  # => abc
    print(f'Outside unify(X, Y): X: {X}, Y: {Y}, Z: {Z}')  # => abc
  print('\nEnd third test\n')

  V1 = Var()
  T1 = Structure( ('t', 1, V1, V1))
  V2 = Var()
  V3 = Var()
  T2 = Structure( ('t', V2, V2, V3))

  print(f'V1: {V1}, V2: {V2}, V3: {V3}, ')
  print(f'T1: t(1, V1, V1), T2: t(V2, V2, V3)')
  for _ in unify(T1, T2):
    print('After unify(T1, T2):')
    print(f'V1: {V1}, V2: {V2}, V3: {V3}, ')
    print(f'T1: {T1}, T2: {T2}')
    print('End of fourth test.')

  """
  Expected output
  
  T1: t(1, 1, 1), T2: t(1, 1, 1)
  V1: 1, V2: 1, V3: 1, 
  End of fourth test.

  """

  V4 = Var()
  T4 = Structure( ('t', 1, V4))
  print(f'\nV4: {V4}')
  print(f'T4: t(1, V4)')
  for _ in unify(T4, V4):
    print('After unify(T4, V4):')
    print(f'V4[0]: {V4[0]}')
    print(f'V4[1] is T4: {V4[1] is T4}')
    print(f'V4[1] == T4: {V4[1] == T4}, because: V4[1].trail_end() is T4: {V4[1].trail_end() is T4}')
    print('An attempt to print T4 or V4 will produce "RecursionError: maximum recursion depth exceeded"')
    print('\nEnd of fifth test.')

  """
  Expected output

  V4: _23
  T4: t(1, V4)
  After unify(T4, V4):
  V4[0]: 1
  V4[1] is T4: False
  V4[1] == T4: True, because: V4[1].trail_end() is T4: True
  An attempt to print T4 or V4 will produce "RecursionError: maximum recursion depth exceeded"
  
  End of fifth test.

  """

  T5 = Structure( ('g', 1, 2, 3) )
  print(f'\nT5 = Structure( ("g", 1, 2, 3) ): {T5}')
  T6 = Structure( ('t', *range(4), T5, *range(5, 9)) )
  print(f'T6 = Structure( ("t", *range(4), T5, *range(5, 9) ): {T6}')
  print(f'(", ".join(map(str, T6[3:8]))): ({", ".join(map(str, T6[3:8]))})')
  print(f'tuple(x.get_py_value( ) for x in T6[4][1:3]): { tuple(x.get_py_value() for x in T6[4][1:3]) }')
  print('\nEnd of sixth test.')

  """
  Expected output
  
  T5 = Structure( ("g", 1, 2, 3) ): g(1, 2, 3)
  T6 = Structure( ("t", *range(4), T5, *range(5, 9) ): t(0, 1, 2, 3, g(1, 2, 3), 5, 6, 7, 8)
  (", ".join(map(str, T6[3:8]))): (3, g(1, 2, 3), 5, 6, 7)
  tuple(x.get_py_value( ) for x in T6[4][1:3]): (2, 3)
  
  End of sixth test.
  """
