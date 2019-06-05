from typing import List, Union

from logic_variables import n_Vars, PyValue, unify, Var


def add_digits(carry_in: int, d1: Union[int, str], d2: Union[int, str], d_sum: Union[int, str], Carry_Out: Var):
  """ Add carry_in, d1, and d2. Succeed if the sum is d_sum with a carry unified with Carry_Out. """

  """ Convert ' ' to 0 when adding. A utility used only by add_digits. """
  b_to_0 = lambda c: 0 if c == ' ' else c

  total = sum([carry_in, b_to_0(d1), b_to_0(d2)])
  (c, d) = divmod(total, 10)
  if d == b_to_0(d_sum):
    yield from unify(Carry_Out, PyValue(c))


def solve(Carries: List[Var], Term1: List[Var], Term2: List[Var], Total: List[Var], Non_Zero_Vars: List[Var]):
  """
  Solve the problem.
  The two embedded functions refer to the lists of Vars in the solve params.
  The lists never change, but their elements are unified with values.
  No point is copying the lists repeatedly.
  """

  def instantiate_all(Vars: List[Var], digits_in: List[int]):
    """
    Vars are the digits we are currently adding. Unify them with digit values.
    digits-in are the digits that have not yet been assigned to a Var.
    Return (through yield) the digits that are not yet used after the new assignments.
    We do this recursively on Vars.
    """
    if not Vars:
      # We're done. Succeed.
      yield digits_in
    elif not digits_in:
      # No more digits. Fail.
      return
    else:
      [V, *Vs] = Vars
      # If V already has a value nothing to do. Go on to the next Vars.
      if isinstance(V.trail_end( ), PyValue):
        yield from instantiate_all(Vs, digits_in)
      else:
        # Give V one of the available digits. Through "backup" all digits will be tried.
        for i in range(len(digits_in)):
          # Make sure we don't assign 0 to one of the leading digits.
          if V not in Non_Zero_Vars or digits_in[i] != 0:
            for _ in unify(V, PyValue(digits_in[i])):
              yield from instantiate_all(Vs, digits_in[:i] + digits_in[i + 1:])

  def solve_aux(index: int, digits_in: List[int]):
    """ Traditional addition. Working from right to left. """

    # print(f'{index}, {digits_in}, {digits(Term1)}, {digits(Term2)}, {digits(Total)}')
    # When we reach 0, we're done. Can't allow a carry to that position.
    if index == 0 and Carries[0].get_py_value() == 0:
      yield
    else:
      for digits_out in instantiate_all([Term1[index], Term2[index], Total[index]], digits_in):
        # Extract the digits from the Vars.
        (carry_in, d1, d2, d_sum) = [d.get_py_value()
                                     for d in [Carries[index], Term1[index], Term2[index], Total[index]] ]
        for _ in add_digits(carry_in, d1, d2, d_sum, Carries[index-1]):
          yield from solve_aux(index-1, digits_out)
    
  yield from solve_aux(len(Carries)-1, list(range(10)))


if __name__ == '__main__':

  def solution_to_string(solution):
    """ Convert a list of digits to a single number represented as a string. """
    return ''.join([str(c) for c in PyValue.get_py_values(solution)])

  """
  SEND    = [ ,  , S, E, N, D]
  MORE    = [ ,  , M, O, R, E]
  MONEY   = [ , M, O, N, E, Y]
  Carries is a list of Vars. The first (rightmost) one is 0.
  Carries = [*list(n_Vars(5)), PyValue(0)]
  Doing it this way makes all the lists--SEND, MORE, MONEY, and Carries--the same length.
  """

  (S, E, N, D, M, O, R, Y) = n_Vars(8)
  Z = PyValue(' ')
  send = [ Z, Z, S, E, N, D]
  more = [ Z, Z, M, O, R, E]
  money = [Z, M, O, N, E, Y]
  carries = [*list(n_Vars(5)), PyValue(0)]
  print(f'\n  SEND\n+ MORE\n{"-" * len(money)}\n MONEY')
  # [S, M] must be constrained not to be 0 since they start numbers.
  for _ in solve(carries, send, more, money, [S, M]):
    # Discard the leading blanks and convert each to a string.
    (send, more, money) = map(solution_to_string, (send[1:], more[1:], money[1:]))
    print(f'\n {send}\n+{more}\n{"-"*(len(money)+1)}\n {money}')
    want_more = input('\nMore? (y/n) > ')
    if want_more.lower() != 'y':
      break
