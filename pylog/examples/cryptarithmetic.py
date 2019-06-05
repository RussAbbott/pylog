from typing import List

from logic_variables import PyValue, n_Vars, unify, Var


def b_to_0(c):
  return 0 if c == ' ' else c


def add_digits(carry_in: int, d1: int, d2: int, d_sum: int, Carry_Out: Var):
  total = sum([carry_in, b_to_0(d1), b_to_0(d2)])
  (c, d) = divmod(total, 10)
  if d == b_to_0(d_sum):
    yield from unify(Carry_Out, PyValue(c))


def get_py_values(Vars: List[Var]):
  return [v.get_py_value() for v in Vars]


def instantiate_all(Vars: List[Var], digits_in: List[int], Non_Zero_Vars: List[Var]):
  if not Vars:
    # We're done. Succeed.
    yield digits_in
  elif not digits_in:
    # No more digits. Fail.
    return
  else:
    [V, *Vs] = Vars
    if isinstance(V.trail_end( ), PyValue):
      yield from instantiate_all(Vs, digits_in, Non_Zero_Vars)
    else:
      for i in range(len(digits_in)):
        if V not in Non_Zero_Vars or digits_in[i] != 0:
          for _ in unify(V, PyValue(digits_in[i])):
            yield from instantiate_all(Vs, digits_in[:i] + digits_in[i+1:], Non_Zero_Vars)


def solve(Carries: List[Var], Term1: List[Var], Term2: List[Var], Total: List[Var], Non_Zero_Vars: List[Var]):

  def solve_aux(index: int, digits_in: List[int]):
    # print(f'{index}, {digits_in}, {digits(Term1)}, {digits(Term2)}, {digits(Total)}')
    if index == 0 and Carries[0].get_py_value() == 0:
      yield
    else:
      for digits_out in instantiate_all([Term1[index], Term2[index], Total[index]], digits_in, Non_Zero_Vars):
        (carry_in, d1, d2, d_sum) = [d.get_py_value()
                                     for d in [Carries[index], Term1[index], Term2[index], Total[index]] ]
        for _ in add_digits(carry_in, d1, d2, d_sum, Carries[index-1]):
          yield from solve_aux(index-1, digits_out)
    
  yield from solve_aux(len(Carries)-1, list(range(10)))


if __name__ == '__main__':

  def sol_to_string(sol):
    return ''.join([str(c) for c in get_py_values(sol)])

  """
  SEND    = [ ,  , S, E, N, D]
  MORE    = [ ,  , M, O, R, E]
  MONEY   = [ , M, O, N, E, Y]
  Carries = list(n_Vars(6))
  """

  (S, E, N, D, M, O, R, Y) = n_Vars(8)
  Z = PyValue(' ')
  send = [ Z, Z, S, E, N, D]
  more = [ Z, Z, M, O, R, E]
  money = [Z, M, O, N, E, Y]
  carries = [*list(n_Vars(5)), PyValue(0)]
  print(f'\n   SEND\n+  MORE\n{"-" * (len(money) + 1)}\n  MONEY')
  for _ in solve(carries, send, more, money, [S, M]):
    send1  = sol_to_string(send)
    more1  = sol_to_string(more)
    money1 = sol_to_string(money)
    print(f'\n {send1}\n+{more1}\n{"-"*(len(money)+1)}\n {money1}')
    want_more = input('\nMore? (y/n) > ')
    if want_more.lower() != 'y':
      break
