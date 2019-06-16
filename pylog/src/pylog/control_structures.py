# from inspect import getmembers
from typing import Generator

from .logic_variables import euc, PyValue, unify, unify_pairs, Var


class Bool_Yield_Wrapper:
  """
  Objects of this class are created to serve as generators. It takes two steps.
  Suppose gen is a generator, i.e.,

  def gen():
      yield

  Such generators are decorated with @bool_yield_wrapper, which returns a function that will create an
  instance of this class when invoked.

  That function is invoked by calling the original generator, e.g.,

  runnable_gen = bool_yield_wrapper(gen)(...)

  runnable_gen will be an instance of Bool_Yield_Wrapper, this class. It is run through its has_more( ) method. E.g.
    while runnable_gen.has_more( ):
        <do something>

  The original gen function must be such that it returns its value through one of its parameters.
  To use the append function as an example,

  @bool_yield_wrapper
  def append(_Xs: Union[PrList, Var], Ys: Union[PrList, Var], _Zs: Union[PrList, Var]):
      ....

  runnable_append = append(Xs, Ys, Zs) # Presumably one or more of Xs, Ys, and Zs is uninstantiated.

  while runnable_append.has_more( ): ... will instantiate the uninstantiated variables.

    (Xs, Ys, Zs) = (Var(), Var(), PrList( [1, 2, 3] )
    runnable_append = append(Xs, Ys, Zs)
    while runnable_append.has_more( ):
        print(f'Xs = {Xs}\nYs = {Ys}\nZs = {Zs}')
        # Prints the various instantiations of Xs and Ys, which, when concatenated, produce Zs.

  These Bool_Yield_Wrapper objects are used in "with" and "while" statements. The current strategy is to
  have a with-statement and embedded while-statement for each generator. For example:

      with append(Xs, Ys, Zs) as gen:
          while gen.has_more():
              <do something>

  The body of the while-loop will repeat each time the generator succeeds.
  """
  def __init__(self, gen):
    self.done = False
    self.gen = gen
    self.name = gen.__name__

  # __enter__ and __exit__ are required for "with"-statements
  def __enter__(self):
    return self

  def __exit__(self, type, value, traceback):
    """
    The three parameters get values if an Exception occurs inside the "with" block, in which case
    __exit__ is passed those properties of the Exception. If __exit__ returns True, it is assumed the
    Exception has been handled. Otherwise, it is assumed the Exception has not been handled and is
    raised outside the "with" block. If no Exception occurs, the values passed are all None, and
    the __exit__ returned value ignored.
    :param type: of Exception, if any; otherwise None.
    :param value: of Exception, if any; otherwise None.
    :param traceback: of Exception, if any; otherwise None.
    :return: Whether Exception has been handeled or should be re-raised.
    """
    pass

  def __iter__(self):
    return self

  def __next__(self):
    """ Can be called next(runnable_append) as well as runnable_append.has_more() """
    if self.done:
      return False
    else:
      try:
        next(self.gen)
        return True
      except StopIteration:
        self.done = True
        return False

  def has_more(self):
    """
    Called only by a while embedded within a with.
    """
    return self.__next__( )


def bool_yield_wrapper(gen):
  """
  A decorator. Generates the Bool_Yield_Wrapper object. See is_even_3, below
  Can also be used explicitly as a function. See is_even_5, below.
  :param gen: the function (not a call to the function) being decorated.
  """
  def wrapped_func(*args, **kwargs):
    return Bool_Yield_Wrapper(gen(*args, **kwargs))

  return wrapped_func


def bool_to_sf(b: bool) -> Generator[None, None, None]:
  """ 
  Turns a boolean condition into a Generator, which succeeds/fails
  if the boolean condition is True/False
  """
  if b:
    yield


def fails(f):
  """
  Applied to a function so that the resulting function succeeds iff the original fails.
  Note that it is applied to the function itself, not to a function call.
  Similar to a decorator but applied explicitly when used.
  """
  def fails_wrapper(*args, **kwargs):
    for _ in f(*args, **kwargs):
      return  # Fail if f succeeds
    yield     # Succeed if f fails.

  return fails_wrapper


def forall(gens):
  """
  Succeeds if all generators in the gens list succeed. The elements in the gens list
  are embedded in lambda functions to avoid premature evaluation.
  """
  if not gens:
    # They have all succeeded.
    yield
  else:
    # Get gens[0] and evaluate the lambda expression to get a fresh iterator.
    # If it succeeds, run the rest of the generators in the list.
    for _ in gens[0]( ):
      yield from forall(gens[1:])


def forany(gens):
  """
  Succeeds if any of the generators in the gens list succeed. On "back-up," tries them all.
  """
  for gen in gens:
    # Get the gens; evaluate them to extract them from lambda; and run them.
    # Succeed if any of them succeed.
    # Can probably not do the lambda trick here, but keeping it makes it
    # parallel to forall. Succeed if any of them succeed.
    # Try them all even if earlier ones succeed. 
    # for _ in gen( ):
    #   yield
    yield from gen( )


def trace(x, succeed=True, show_trace=True):
  """
  Can be included in a list of generators (as in forall and forany) to see where we are.
  The second argument determines whether it succeeds or fails.
  When included in a list of forall generators, succeed should be set to True so that
  it doesn't provent forall from succeeding.
  When included in a list of forany generators, succeed should be set to False so that forany
  will just go on the the next generator one and won't take this one as an extraneous successes.
  """
  if show_trace:
    print(x)
  if succeed:
    yield


def would_succeed(f):
  """
  Applied to a function so that the resulting function succeeds/fails iff the original succeeds/fails.
  If the original succeeds, this also succeeds but without binding any variables.
  Similar to a decorator but applied explicitly when used.
  """
  def would_succeed_wrapper(*args, **kwargs):
    succeeded = False
    for _ in f(*args, **kwargs):
      succeeded = True
      # Do not yield in the context of f succeeding.
      # So un-unify any unifications that occurred in f.

    if succeeded:
      yield  # Succeed if f succeeded.
    # else:
    #   pass   # Fail if f failed

  return would_succeed_wrapper


def yield_to_bool(f):

  def y_to_b_wrapper(*args, **kwargs):
    for _ in f(*args, **kwargs):
      return True
    return False

  return y_to_b_wrapper


if __name__ == '__main__':

  # The following examples illustrate various ways to call a generator
  # and to pass results back through logic variable arguments.

  # Yields when i is even.
  @euc
  def is_even_1(i: int) -> Generator[None, None, None]:
    for _ in unify(PyValue(True), PyValue(i % 2 == 0)):
        yield

  # If is_even_1(i) fails to unify, for _ in is_even_1(i) fails.
  # It works similarly to an if condition.
  evens_1 = [i for i in range(5) for _ in is_even_1(i)]
  print(f'\n1. evens_1: {evens_1}')    # => 1. evens_1: [0, 2, 4]

  # Same as is_even_1 but includes the range generator.
  def is_even_2(n: int, Res: Var) -> Generator[None, None, None]:
    for i in range(n):
        for _ in unify_pairs([ (PyValue(i % 2 == 0), PyValue(True)),
                               (PyValue(i), Res)
                               ]):
          yield

  # Can reuse this variable in all examples.
  # After each example, it is left uninstantiated.
  Result = Var()

  # This version uses the function directly as a generator.
  evens_2 = [Result.get_py_value() for _ in is_even_2(7, Result)]
  print(f'2. evens_2: {evens_2}')    # => 2. evens_2: [0, 2, 4, 6]

  evens_3 = []
  # Here we apply the decorator function explicitly.
  # bool_yield_wrapper makes it possible to use the generator with .has_more() as a boolean.
  # The has_more() function, defined in the BoolYIeldWrapper class, both calls next() on
  # the generator and returns True or False depending on whether next() has succeeded. If
  # next() succeeds, the next value is unified with Result. The next value is also stored
  # within the BoolYIeldWrapper object as self.next, and can be retrieved that way.
  with bool_yield_wrapper(is_even_2)(9, Result) as is_even_gen_3:
    while is_even_gen_3.has_more( ):
      evens_3.append(Result.get_py_value())
  print(f'3. evens_3: {evens_3}')    # => 3. evens_4: [0, 2, 4, 6, 8]

  @bool_yield_wrapper
  def is_even_2_decorated(n: int, Res: Var) -> Bool_Yield_Wrapper:
    for i in range(n):
        for _ in unify_pairs( [(PyValue(i % 2 == 0), PyValue(True)),
                              (PyValue(i), Res)
                               ]):
          yield

  evens_4 = []
  # Create the generator in a separate step.
  is_even_gen_4 = is_even_2_decorated(11, Result)
  while is_even_gen_4.has_more( ):
    evens_4.append(Result.get_py_value())
  print(f'4. evens_4: {evens_4}')    # => 4. evens_4: [0, 2, 4, 6, 8, 10]

  evens_5 = []
  # Create the generator in a 'with' statement.
  with is_even_2_decorated(13, Result) as is_even_gen_5:
    while is_even_gen_5.has_more( ):
      evens_5.append(Result.get_py_value())
  print(f'5. evens_5: {evens_5}')    # => 5. evens_5: [0, 2, 4, 6, 8, 10, 12]

  print('\nEnd of test')
