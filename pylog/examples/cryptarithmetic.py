from typing import Iterable, List

from logic_variables import PyValue, unify, unify_pairs


def complete_column(carry_out: int, Carry_Out_Dig: PyValue,
                    sum_dig: int, Sum_Dig: PyValue,
                    digits_in: List[int], Leading_Digits):
  """
  If Sum_Dig (the digit in the sum for this column) is not yet instantiated, instantiate it to sum_dig
  (if that digit is available). If Sum_Dig is already instantiated, ensure it is consistent with the sum_dig.
  Instantiate Carry_Out_Dig to carry_out.
  """
  # Is Sum_Dig uninstantiated? If so, instantiate it to sum_digit if possible.
  # Then instantiate Carry_Out_Dig, and return (yield) digits_in with sum_digit removed.
  if not Sum_Dig.has_py_value():
    try:
      # digits_in.index(sum_dig) throws a ValueError if sum_dig is not in digits_in
      i = digits_in.index(sum_dig)
      # Ensure not to instantiate any of the Leading_Digits to 0.
      if digits_in[i] != 0 or all(Sum_Dig is not LV for LV in Leading_Digits):
        for _ in unify_pairs([(Carry_Out_Dig, carry_out), (Sum_Dig, sum_dig)]):
          yield digits_in[:i] + digits_in[i + 1:]
    # sum_dig is not available in digits_in. Fail, i.e., return instead of yield.
    except ValueError:
      return

  # If Sum_Dig is instantiated, is it equal to sum_digit?
  # If so, instantiate Carry_Out_Dig and return the current digits_in.
  elif sum_dig == Sum_Dig.get_py_value( ):
    for _ in unify(Carry_Out_Dig, carry_out):
      yield digits_in

  # Sum_Dig is instantiated, but it is not sum_digit. Fail.
  # This branch is not necessary. If we get to this point, we return by running off the end of the function.
  else:
    return


def solve(Carries: List[PyValue],
          Term1: List[PyValue],
          Term2: List[PyValue],
          Sum: List[PyValue],
          Leading_Digits: List[PyValue]):
  """
  Solve the problem.
  The two embedded functions below refer to the lists in solve's params.
  The lists never change, but their elements are unified with values.
  No point is copying the lists repeatedly. So embed the functions that refer to them.
  """

  def fill_column(PVs: List[PyValue], index: int, digits_in: List[int]):
    """
    PVs are the digits in the current column to be added together, one from each term.
    digits-in are the digits that have not yet been assigned to a Var.
    Find digits in digits_in that make the column add up properly.
    Return (through yield) the digits that are not yet used after the new assignments.
    We do this recursively on PVs--even though we are currently assuming only two terms.
    """
    if not PVs:
      # We have instantiated the digits to be added.
      # Instantiate Sum_Dig (if possible) and Carries[index - 1] to the total.
      # Completing the column is a bit more work than it might seem.
      (carry_in, digit_1, digit_2) = (D.get_py_value( ) for D in [Carries[index], Term1[index], Term2[index]])
      total = sum([carry_in, digit_1, digit_2])
      (carry_out, sum_dig) = divmod(total, 10)
      yield from complete_column(carry_out, Carries[index-1], sum_dig, Sum[index], digits_in, Leading_Digits)

    else:
      # Get head and tail of PVs.
      [V, *Vs] = PVs
      # If V already has a value, nothing to do. Go on to the remaining PVs.
      if V.has_py_value( ):
        yield from fill_column(Vs, index, digits_in)
      else:
        # Give V one of the available digits. Through "backup" all digits will be tried.
        for i in range(len(digits_in)):
          if digits_in[i] != 0 or all(V is not LV for LV in Leading_Digits):
            for _ in unify(V, digits_in[i]):
              yield from fill_column(Vs, index, digits_in[:i] + digits_in[i + 1:])

  def solve_aux(index: int, digits_in: List[int]):
    """ Traditional addition: work from right to left. """
    # When we reach 0, we're done.
    if index == 0:
      # Can't allow a carry to this position.
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


def letters_to_vars(st: Iterable, d: dict) -> List:
  return [d[s] for s in st]


def set_up_puzzle(t1, t2, sum, _Z):
  Var_Letters = sorted(list(set(t1 + t2 + sum)))
  if len(Var_Letters) > 10:
    print(f'Too many variables: {Var_Letters}')
    return
  Vars_Dict = {V: PyValue() for V in Var_Letters}  #dict(zip(var_letters, n_Vars(len(var_letters))))
  length = len(sum) + 1
  T1 = [_Z for _ in range((length - len(t1)))] + letters_to_vars(t1, Vars_Dict)
  T2 = [_Z for _ in range((length - len(t2)))] + letters_to_vars(t2, Vars_Dict)
  Tot = [_Z for _ in range((length - len(sum)))] + letters_to_vars(sum, Vars_Dict)
  non_zero_vars = letters_to_vars({t1[0], t2[0], sum[0]}, Vars_Dict)
  carries = [PyValue() for _ in range(length - 1)] + [PyValue(0)]  # [*list(n_Vars(length - 1)), PyValue(0)]
  return (T1, T2, Tot, non_zero_vars, carries)


def solution_to_string(Term, _Z=PyValue('a'), Blank=PyValue('b')):
  """
  Convert a list of PyValue digits to a single number represented as a string.
  Replace _Z with Blank.
  """
  PyDigits = PyValue.get_py_values([(Blank if PV is _Z else PV) for PV in Term])
  return ''.join(map(str, PyDigits))


def solve_crypto(t1: str, t2: str, sum: str):
  _Z = PyValue(0)
  (T1, T2, Tot, non_zero_vars, carries) = set_up_puzzle(t1, t2, sum, _Z)
  want_more = None
  Blank = PyValue(' ')
  for _ in solve(carries, T1, T2, Tot, non_zero_vars):
    # Discard the leading blanks and convert each number to a string.
    # map(solution_to_string, (T1[1:], T2[1:], Tot[1:]))
    (t1_out, t2_out, tot_out) = (solution_to_string(T, _Z, Blank) for T in [T1[1:], T2[1:], Tot[1:]])
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

  # See http://bach.istc.kobe-u.ac.jp/llp/crypt.html (and links) for these and many(!) more.
  for puzzle in [
                 ('SEND', 'MORE', 'MONEY'),
                 ('BASE', 'BALL', 'GAMES'),
                 ('SATURN', 'URANUS', 'PLANETS'),
                 ('POTATO', 'TOMATO', 'PUMPKIN')
                 ]:
    solve_crypto(*puzzle)
