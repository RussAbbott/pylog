from typing import Iterable, List, Union

from logic_variables import n_Vars, PyValue, unify, unify_pairs, Var


def complete_column(carry_out: int, Carry_Out_Dig: Var,
                    sum_dig: int, Sum_Dig: Var,
                    digits_in: List[int], Leading_Digits):
  """
  If Sum_Dig (the digit in the sum for this column) is not yet instantiated, instantiate it to sum_dig
  (if that digit is available). If Sum_Dig is already instantiated, ensure it is consistent with the sum_dig.
  Instantiate Carry_Out_Dig to carry_out.
  """
  # Is Sum_Dig uninstantiated? If so, instantiate it to sum_digit if possible.
  # Instantiate Carry_Out_Dig, and return (yield) digits_in with sum_digit removed.
  if not Sum_Dig.has_py_value():
    try:
      # digits_in.index(sum_dig) throws a ValueError if sum_dig is not in digits_in
      i = digits_in.index(sum_dig)
      # Ensure not to instantiate any of the Leading_Digits to 0.
      if digits_in[i] != 0 or Sum_Dig not in Leading_Digits:
        for _ in unify_pairs([(Carry_Out_Dig, carry_out), (Sum_Dig, sum_dig)]):
          yield digits_in[:i] + digits_in[i + 1:]
    # sum_dig is not available in digits_in. Fail.
    except ValueError:
      return

  # If Sum_Dig is instantiated, is it equal to sum_digit?
  # If so, instantiate Carry_Out_Dig and return the current digits_in.
  elif sum_dig == Sum_Dig.get_py_value( ):
    for _ in unify(Carry_Out_Dig, carry_out):
      yield digits_in

  # Sum_Dig is instantiated but not to sum_digit. Fail.
  else:
    return


def solve(Carries: List[Var],
          Term1: List[Union[Var, PyValue]],
          Term2: List[Union[Var, PyValue]],
          Sum: List[Union[Var, PyValue]],
          Leading_Digits: List[Var]):
  """
  Solve the problem.
  The two embedded functions below refer to the lists in solve's params.
  The lists never change, but their elements are unified with values.
  No point is copying the lists repeatedly. So embed the functions that refer to them.
  """

  def b_to_0(c):
    """ Convert ' ' to 0 when adding. Used only by fill_column. """
    return 0 if c == ' ' else c

  def fill_column(Vars: List[Var], index: int, digits_in: List[int]):
    """
    Vars are the digits in the current column to be added together, one from each term.
    digits-in are the digits that have not yet been assigned to a Var.
    Find digits in digits_in that make the column add up properly.
    Return (through yield) the digits that are not yet used after the new assignments.
    We do this recursively on Vars--even though we are currently assuming only two terms.
    """
    if not Vars:
      # We have instantiated the term digits.
      # Instantiate Sum_Dig (if possible) and Carries[index - 1]
      # Completing the column is a bit more work than it might seem.
      (carry_in, digit_1, digit_2) = (b_to_0(d.get_py_value( )) for d in [Carries[index], Term1[index], Term2[index]])
      (carry_out, sum_dig) = divmod(sum([carry_in, digit_1, digit_2]), 10)
      yield from complete_column(carry_out, Carries[index-1], sum_dig, Sum[index], digits_in, Leading_Digits)

    else:
      # Get head and tail of Vars.
      [V, *Vs] = Vars
      # If V already has a value, nothing to do. Go on to the remaining Vars.
      if V.has_py_value():
        yield from fill_column(Vs, index, digits_in)
      else:
        # Give V one of the available digits. Through "backup" all digits will be tried.
        for i in range(len(digits_in)):
          # Make sure we don't assign 0 to one of the leading digits.
          if digits_in[i] != 0 or V not in Leading_Digits:
            for _ in unify(V, digits_in[i]):
              yield from fill_column(Vs, index, digits_in[:i] + digits_in[i + 1:])

  def solve_aux(index: int, digits_in: List[int]):
    """ Traditional addition: work from right to left. """
    # When we reach 0, we're done.
    if index == 0:
      # Can't allow a carry to that position.
      if Carries[0].get_py_value() == 0:
        yield
      else:
        # If we reach index == 0 but have a carry into the last column, fail.
        # Won't have such a carry with only two terms. But it might happen with many terms,.
        return
    else:
      for digits_out in fill_column([Term1[index], Term2[index]], index, digits_in):
          yield from solve_aux(index-1, digits_out)
    
  yield from solve_aux(len(Carries)-1, list(range(10)))


def solution_to_string(solution):
  """ Convert a list of digits to a single number represented as a string. """
  return ''.join([str(c) for c in PyValue.get_py_values(solution)])


def letters_to_vars(st: Iterable, d: dict) -> List:
  return [d[s] for s in st]


def set_up_puzzle(t1, t2, sum):
  var_letters = sorted(list(set(t1 + t2 + sum)))
  if len(var_letters) > 10:
    print(f'Too many variables: {var_letters}')
    return
  vars_dict = dict(zip(var_letters, n_Vars(len(var_letters))))
  Z = PyValue(' ')
  length = len(sum) + 1
  T1 = [Z for _ in range((length - len(t1)))] + letters_to_vars(t1, vars_dict)
  T2 = [Z for _ in range((length - len(t2)))] + letters_to_vars(t2, vars_dict)
  Tot = [Z for _ in range((length - len(sum)))] + letters_to_vars(sum, vars_dict)
  non_zero_vars = letters_to_vars({t1[0], t2[0], sum[0]}, vars_dict)
  carries = [*list(n_Vars(length - 1)), PyValue(0)]
  return (T1, T2, Tot, non_zero_vars, carries)


def solve_crypto(t1: str, t2: str, sum: str):
  (T1, T2, Tot, non_zero_vars, carries) = set_up_puzzle(t1, t2, sum)
  want_more = None
  for _ in solve(carries, T1, T2, Tot, non_zero_vars):
    # Discard the leading blanks and convert number each to a string.
    (t1_out, t2_out, tot_out) = map(solution_to_string, (T1[1:], T2[1:], Tot[1:]))
    print()
    print(f'  {t1}  -> {t1_out}')
    print(f'+ {t2}  -> {t2_out}')
    print(f'{"-" * (len(sum)+1)}     {"-" * len(sum)}')
    print(f' {sum}  -> {tot_out}')
    ans = input('\nLook for more solutions? (y/n) > ').lower( )
    want_more = ans[0] if len(ans) > 0 else 'n'
    if want_more != 'y':
      break
  if want_more == 'y':
    print('No more solutions.')


if __name__ == '__main__':

  # See http://bach.istc.kobe-u.ac.jp/llp/crypt.html (and links) for many(!) others.
  for puzzle in [('SEND', 'MORE', 'MONEY'),
                 ('BASE', 'BALL', 'GAMES'),
                 ('SATURN', 'URANUS', 'PLANETS'),
                 ('POTATO', 'TOMATO', 'PUMPKIN')
                 ]:
    solve_crypto(*puzzle)
