from __future__ import annotations
from functools import wraps
from inspect import isgeneratorfunction
from typing import Any, Generator, Iterable, List, Optional, Sequence, Sized, Tuple

"""
Developed by Ian Piumarta as the "unify" library (http://www.ritsumei.ac.jp/~piumarta/pl/src/unify.py) for a
course on programming languages (http://www.ritsumei.ac.jp/~piumarta/pl/index.html). 

See discussion on the GitHub page: https://github.com/RussAbbott/pylog
"""

"""
The pylog core (this file) contains the logic variable and data structure classes and the unify function.
"""


def eot(f):
  """ A decorator that takes trail_end() of all Var arguments """

  def get_arg_Vars_trail_ends(args):
    args = (arg.trail_end() if isinstance(arg, Var) else arg for arg in args)
    return args

  @wraps(f)
  def eot_wrapper_gen(*args, **kwargs):
    args = get_arg_Vars_trail_ends(args)
    yield from f(*args, **kwargs)

  @wraps(f)
  def eot_wrapper_non_gen(*args, **kwargs):
    args = get_arg_Vars_trail_ends(args)
    return f(*args, **kwargs)

  return eot_wrapper_gen if isgeneratorfunction(f) else eot_wrapper_non_gen


class Term:
  """

                                                     Term  (An abstract logic variable class)
                                                       |
                               ------------------------------------------------
                               |                       |                      |
                            Ground                    Var                 Structure
                               |                                              |
                   -----------------------                              SuperSequence
                   |                     |                                    |
               Container         (int, float, string}                   -------------------
        (a quasi-logic-variable)                                        |                 |
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
    self == other if either (a) they have the same ground value or (b) are the same variable.
    """
    # return self is other
    (self_eot, other_eot) = (self.trail_end(), other.trail_end())
    return self_eot is other_eot or \
           (self is not self_eot or other is not other_eot) and self_eot == other_eot

  def __lt__(self, other: Term) -> bool:
    return str(self) < str(other)

  def __ne__(self, other: Term) -> bool:
    return not (self == other)

  def __str__(self) -> str:
    """
    The str( ) of a Var is its ground value if is_ground( ) or its term_id otherwise.
    """
    self_eot = self.trail_end( )
    return f'{self_eot}' if self_eot.is_ground( ) or isinstance(self_eot, Structure) else f'_{self_eot.term_id}'

  @staticmethod
  def ensure_is_logic_variable(x: Any) -> Term:
    # Ground anything that is not a Term.
    return x if isinstance(x, Term) else Ground(x)

  def get_ground_value(self) -> Any:
    return None

  def is_ground(self) -> bool:
    return False

  def trail_end(self) -> Term:
    return self


class Ground(Term):

  """ A wrapper class for integers, strings, etc. """

  def __init__(self, ground_value: Optional[Any] = None ):
    self._ground_value = ground_value
    super( ).__init__( )

  def __eq__(self, other: Term) -> bool:
    other_eot = other.trail_end()
    return isinstance(other_eot, Ground) and self.get_ground_value() == other_eot.get_ground_value()

  def __lt__(self, other: Term) -> bool:
    other_eot = other.trail_end()
    return isinstance(other_eot, Ground) and self.get_ground_value() < other_eot.get_ground_value()

  def __str__(self) -> str:
    return f'{self._ground_value}'

  def get_ground_value(self) -> Any:
    return self._ground_value

  def is_ground(self) -> bool:
    return True


class Container(Ground):
  def get_contents(self) -> Any:
    return self._ground_value

  def incr_and_return(self) -> Any:
    self._ground_value += 1
    return self._ground_value

  def set_contents(self, value: Any):
    self._ground_value = value


class Structure(Term):
  """
  self.functor is the functor
  self.args is a tuple of args
  """
  def __init__(self, term: Tuple = ( None, () )):
    self.functor = term[0]
    self.args = tuple(map(self.ensure_is_logic_variable, term[1:]))
    super().__init__()

  def __eq__(self, other: Term) -> bool:
    other_eot = other.trail_end()
    return (isinstance(other_eot, Structure) and
            self.functor == other_eot.functor and
            len(self.args) == len(other_eot.args) and
            all([selfArg == other_eotArg for (selfArg, other_eotArg) in zip(self.args, other_eot.args)]))

  # noinspection PySimplifyBooleanCheck
  def __str__(self):
    args_str = self.values_string(self.args)
    result = f'{self.functor}({args_str})'
    return result

  def get_ground_value(self) -> Tuple:
    ground_args = [arg.get_ground_value() for arg in self.args]
    return (self.functor, *ground_args)

  def is_ground(self) -> bool:
    grounded = all([arg.is_ground() for arg in self.args])
    return grounded

  @staticmethod
  def values_string(values: Iterable):
    result = ', '.join(map(str, values))
    return result


class Var(Term):
  """
  A logic variable
  """

  def __init__(self):
    # self.trail_next points to the next element on the trail, if any.
    self.trail_next = None
    super().__init__()

  def __len__(self):
    self_eot = self.trail_end()
    # To make PyCharm's type checker happy.
    assert isinstance(self_eot, Sized)
    return len(self_eot) if hasattr(self_eot, '__len__') else None

  def _has_trail_next(self) -> bool:
    # Is this the end of the trail?
    return self.trail_next is not None

  @eot
  def get_ground_value(self) -> Optional[Any]:
    Trail_End_Var = self.trail_end( )
    return Trail_End_Var.get_ground_value( ) if Trail_End_Var.is_ground( ) else None

  # Can't use @eot. Generates an infinite recursive loop.
  def is_ground(self) -> bool:
    """ Is ground if its trail end is ground """
    Trail_End_Var = self.trail_end( )
    return not isinstance(Trail_End_Var, Var) and Trail_End_Var.is_ground()

  def trail_end(self):
    """
    return: the Term, whatever it is, at the end of this Var's unification trail.
    """
    return self.trail_next.trail_end( ) if self._has_trail_next( ) else self


def n_Vars(n: int) -> List[Var]:
  """ Generate a list of uninstantiated variables of length n. """
  return [Var( ) for _ in range(n)]


@eot
def unify(Left: Term, Right: Term):
  """
  Unify two logic Terms.

  The strategy is to keep track of the "unification trail" for all variables.

  The unification trail is a linked list of logic variables, which are all unified.

  The final element on the trail is either
  o a non-Var, in which case the value of all preceding variables is the value of that non-Var, or
  o a Var (which is not linked to any further variable), in which case, all variables on the trail
    are unified, but they do not (yet) have a value.
  """

  # If the trail_ends are equal, either because they have the same ground value or
  # because they are the same (unbound) Var, do nothing. They are already unified.
  # yield to indicate unification success.
  if Left == Right:
    yield

  # Since they are not equal, if they are both ground but have different values,
  # they can't be unified. To indicate unification failure, terminate without a yield.
  elif Left.is_ground( ) and Right.is_ground( ):
    pass

  # If at least one is a Var. Make the other an extension of its trail.
  # (If both are Vars, it makes no functional difference which extends which.)
  elif isinstance(Left, Var) or isinstance(Right, Var):
    (pointsFrom, pointsTo) = (Left, Right) if isinstance(Left, Var) else (Right, Left)
    pointsFrom.trail_next = pointsTo
    yield
    # All yields create a context in which more of the program is executed--like
    # the body of a while-loop or a for-loop. A "next()" request asks for alternatives.
    # But there is only one functional way to do unification.
    # So on backup, simply unlink the two and exit without a further yield.
    pointsFrom.trail_next = None

  # If both Left and Right are Structures, they can be unified if
  # (a) they have the same functor and
  # (b) their arguments can be unified.
  elif isinstance(Left, Structure) and isinstance(Right, Structure) and \
       Left.functor == Right.functor:
    yield from unify_sequences(Left.args, Right.args)


def unify_pairs(tuples: List[Tuple[Term, Term]]):
  """ Apply unify to pairs of terms. """
  if not tuples:  # If no more tuples, we are done.
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
  """ Unify simple sequences. e.g., lists or tuples, of Terms. """
  # The two sequences must be the same length.
  if len(seq_1) != len(seq_2):
    return

  # If they are both empty, we are done.
  if len(seq_1) == 0:
    yield

  else:
    # Unify the first element of each sequence. If successful go on to the rest.
    for _ in unify(seq_1[0], seq_2[0]):
      yield from unify_sequences(seq_1[1:], seq_2[1:])


if __name__ == '__main__':

  V = Var()

  print(isgeneratorfunction(V.get_ground_value))

  print(V.get_ground_value())

  print(f'{Structure(  (list, 1, 2, 3) ) }')

  print(Ground(1) == Ground(1))

  A = Ground('abc')
  B = Var( )
  C = Var( )
  D = Ground('def')
  print(f'\na. A: {A}; B: {B}; C: {C}; D: {D}')

  for _ in unify_pairs([(A, B), (B, C), (C, D)]):
    print(f'b. A: {A}; B: {B}; C: {C}; D: {D}')
  print(f'c. A: {A}; B: {B}; C: {C}; D: {D}')
  print('b. should not have printed.')

  A = Var( )
  B = Var( )
  C = Var( )
  D = Ground('def')

  print(f'\n1. A: {A}; B: {B}; C: {C}; D: {D}')  # With while: A: A; B: _12. With if: A: A; B: A.
  for _ in unify(A, B):
    print(f'2a. A: {A}; B: {B}; C: {C}; D: {D}')  # With while: A: A; B: _12. With if: A: A; B: A.
    for _ in unify(A, C):
      print(f'2b. A: {A}; B: {B}; C: {C}; D: {D}')  # With while: A: A; B: _12. With if: A: A; B: A.
      for _ in unify(A, D):
        print(f'2c. A: {A}; B: {B}; C: {C}; D: {D}')  # With while: A: A; B: _12. With if: A: A; B: A.
  print(f'3. A: {A}; B: {B}; C: {C}; D: {D}')  # With while: A: A; B: _12. With if: A: A; B: A.

  print('End first test\n')

  """
  Expected output

  A: A; B: _3
  A: A; B: A
  A: A; B: _3

  1. Y1: [abc, _5], Y2: [_9, _9]
  2. Y1: [abc, abc], Y2: [abc, abc]
  3. Y1: [abc, _5], Y2: [_9, _9]  

  End first test
  """

  A = Var( )
  B = Var( )
  C = Var( )

  print(f'1. A: {A}, B: {B}, C: {C}')
  for _ in unify_pairs([(A, B), (B, C)]):
    print(f'2. A: {A}, B: {B}, C: {C}')
    print(f'3. A.eot: {A.trail_end( )}, '
          f'B.eot: {B.trail_end( )}, '
          f'C.eot: {C.trail_end( )}')  # => A.eot: _6, B.eot: _6, C.eot: _6

    D = Ground('xyz')
    for _ in unify(D, B):
      print(
        f'4. A: {A}, A.eot: {A.trail_end( )}, '
        f'B: {B}, B.eot: {B.trail_end( )}, '
        f'C: {C}, C.eot: {C.trail_end( )}, '
        f'D: {D}, D.eot: {D.trail_end( )}'  # => A.eot: xyz, B.eot: xyz, C.eot: xyz, D.eot: xyz
      )

    print(f'\n5. No longer unified with D. A: {A}, B: {B}, C: {C}')  # => A: xyz, B: xyz, C: xyz, D: xyz
  print(f'6. No longer unified with each other. A: {A}, B: {B}, C: {C}')  # => A: xyz, B: xyz, C: xyz, D: xyz
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

  def is_even(i: int) -> Generator[None, None, None]:
    is_even = Var( )
    # Can serve as a guard. But unlike an if-statement, when it succeeds,
    # will go on to the rest of the program on the next "next()" call.
    # To prevent that put return after yield. Try it with and without the return.
    # Note that "After yield" is printed before the next i. The program doesn't
    # Stop after yield. It continues on until the program either terminates or
    # encounters another yield.
    # Note also that in all cases, wf backs out of its unification with i % 2
    # Before getting to the Rest of the Program.
    print(f'\nBefore unify with ({i} % 2). is_even: {is_even}')
    for _ in (unify(is_even, Ground(not bool(i % 2)))):
      print(f'Before unify with 0. is_even: {is_even}')
      for _ in (unify(is_even, Ground(True))):
        print("Before yield.")
        yield is_even
        print("After yield. Stops here if return is uncommented.")
        # return
      print(f'Outside unify with 0. is_even: {is_even}')
    print(f'Outside unify with i % 2. is_even: {is_even}')


  evens = [(i, isEvn, isEvn.trail_end( ).get_ground_value( )) for i in range(3) for isEvn in is_even(i)]
  evens_str = [(a, f'{type(b).__name__}({b.trail_end( ).get_ground_value( )})', c) for (a, b, c) in evens]
  print(f'\nevens: {evens_str}\n')
  print('End of fourth test')

  """
  Expected output:

  Before unify with (0 % 2). is_even: _20
  Before unify with 0. is_even: True
  Before yield.
  After yield. Stops here if return is uncommented.
  Outside unify with 0. is_even: True
  Outside unify with i % 2. is_even: _20

  Before unify with (1 % 2). is_even: _23
  Before unify with 0. is_even: False
  Outside unify with 0. is_even: False
  Outside unify with i % 2. is_even: _23

  Before unify with (2 % 2). is_even: _26
  Before unify with 0. is_even: True
  Before yield.
  After yield. Stops here if return is uncommented.
  Outside unify with 0. is_even: True
  Outside unify with i % 2. is_even: _26

  evens: [(0, 'Var(None)', True), (2, 'Var(None)', True)]

  print('End fourth test\n')
  """

  # Simple unification examples.
  X = Ground(1)
  Y = Ground(2)
  print(f'\na. X: {X}, Ys: {Y}')
  for _ in unify(X, Y):
    print(f'\nb. X: {X}, Ys: {Y}')
  print('Output b. should not have printed. \nDone 1')
  print(f'c. X: {X}, Ys: {Y}')

  print(f'd. {Var()}, {Var()}')
  X = Var( )
  for _ in unify(Ground('abc'), X):
    Y = Var( )
    Z = Var( )
    print(f'\n1. X: {X}, Y: {Y}, Z: {Z}')  # => abc
    for _ in unify(X, Y):
      print(f'2. X: {X}, Y: {Y}, Z: {Z}')  # => abc
      for _ in unify(Z, Y):
        print(f'3. X: {X}, Y: {Y}, Z: {Z}')  # => abc
      print(f'4. X: {X}, Y: {Y}, Z: {Z}')  # => abc
    print(f'5. X: {X}, Y: {Y}, Z: {Z}')  # => abc

    print(f'\nAgain')
    print(f'6. X: {X}, Y: {Y}, Z: {Z}')  # => _2
    for _ in unify(Y, X):
      print(f'7. X: {X}, Y: {Y}, Z: {Z}')  # => abc
      for _ in unify(Y, Z):
        print(f'8. X: {X}, Y: {Y}, Z: {Z}')  # => abc


"""
Expected output:

a. X: 1, Ys: 2
Done 1

c. X: 1, Ys: _5
d. X: 1, Ys: 1
e. X: 1, Ys: _5
f. _6, _7

1. X: abc, Y: _10, Z: _11
2. X: abc, Y: abc, Z: _11
3. X: abc, Y: abc, Z: abc
4. X: abc, Y: abc, Z: _11
5. X: abc, Y: _10, Z: _11

Again
6. X: abc, Y: _10, Z: _11
7. X: abc, Y: abc, Z: _11
8. X: abc, Y: abc, Z: abc

9. Y1: [abc, _12], Y2: [_17, _17]
10. Y1: [abc, abc], Y2: [abc, abc]
11. Y1: [abc, _12], Y2: [_17, _17]

End test
"""
