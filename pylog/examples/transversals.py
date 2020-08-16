from inspect import isgeneratorfunction, signature
from typing import Generator, List, Optional, Set, Tuple

from control_structures import fails, Trace
from logic_variables import PyValue, Var
from sequence_options.sequences import PyList, PySet, PyTuple
from sequence_options.super_sequence import member


# Use this for all non-lv tests.
# Is there a better example?
sets = [{1, 2, 3}, {1, 2, 4}, {1}]


unassigned = '_'
def uninstantiated_indices(transversal):
    """ Must return the actual list because the result is used twice.  """
    return [indx for indx in range(len(transversal)) if transversal[indx] is unassigned]


@Trace
def tnvsl_dfs(sets, tnvsl):
  remaining_indices = uninstantiated_indices(tnvsl)
  if not remaining_indices: return tnvsl

  nxt_indx = remaining_indices[0]
  for elmt in sets[nxt_indx]:
    if elmt not in tnvsl:
      new_tnvsl = tnvsl[:nxt_indx] \
                  + (elmt, ) \
                  + tnvsl[nxt_indx+1:]
      full_tnvsl = tnvsl_dfs(sets, new_tnvsl)
      if full_tnvsl is not None: return full_tnvsl


if __name__ == '__main__':
    print(f'\n{"-" * 75}'
          f'\ntnvsl_dfs({sets}, (_, _, _))\n')
    print(f"\nFirst transversal: {tnvsl_dfs(sets, (unassigned, unassigned, unassigned))}")


@Trace
def tnvsl_dfs_prop(sets, tnvsl):
  remaining_indices = uninstantiated_indices(tnvsl)
  if not remaining_indices: return tnvsl

  if any(not sets[indx] for indx in remaining_indices):
    return None

  nxt_indx = min(remaining_indices)
  for elmt in sets[nxt_indx]:
    if elmt not in tnvsl:
      new_tnvsl = tnvsl[:nxt_indx] \
                  + (elmt, ) \
                  + tnvsl[nxt_indx+1:]
      new_sets = [set - {elmt} for set in sets]
      full_tnvsl = tnvsl_dfs_prop(new_sets, new_tnvsl)
      if full_tnvsl is not None: return full_tnvsl


if __name__ == '__main__':
    print(f'\n{"-" * 75}'
          f'\ntnvsl_dfs_prop({sets}, (_, _, _))\n')
    print(f"\nFirst transversal: {tnvsl_dfs_prop(sets, (unassigned, unassigned, unassigned))}")


@Trace
def tnvsl_dfs_smallest(sets, tnvsl):
  remaining_indices = uninstantiated_indices(tnvsl)
  if not remaining_indices: return tnvsl

  nxt_indx = min(remaining_indices,
                 key=lambda indx: len(sets[indx]))
  for elmt in sets[nxt_indx]:
    if elmt not in tnvsl:
      new_tnvsl = tnvsl[:nxt_indx] \
                  + (elmt, ) \
                  + tnvsl[nxt_indx+1:]
      full_tnvsl = tnvsl_dfs_smallest(sets, new_tnvsl)
      if full_tnvsl is not None: return full_tnvsl


if __name__ == '__main__':
    print(f'\n{"-" * 75}'
          f'\ntnvsl_dfs_smallest({sets}, (_, _, _))\n')
    print(f"\nFirst transversal: {tnvsl_dfs_smallest(sets, (unassigned, unassigned, unassigned))}")


@Trace
def tnvsl_dfs_both(sets, tnvsl):
  remaining_indices = uninstantiated_indices(tnvsl)
  if not remaining_indices: return tnvsl

  if any(not sets[indx] for indx in remaining_indices):
    return None

  nxt_indx = min(remaining_indices,
                 key=lambda indx: len(sets[indx]))
  for elmt in sets[nxt_indx]:
    if elmt not in tnvsl:
      new_tnvsl = tnvsl[:nxt_indx] \
                  + (elmt, ) \
                  + tnvsl[nxt_indx+1:]
      new_sets = [set - {elmt} for set in sets]
      full_tnvsl = tnvsl_dfs_both(new_sets, new_tnvsl)
      if full_tnvsl is not None: return full_tnvsl


if __name__ == '__main__':
    print(f'\n{"-" * 75}'
          f'\ntnvsl_dfs_both({sets}, (_, _, _))\n')
    print(f"\nFirst transversal: {tnvsl_dfs_both(sets, (unassigned, unassigned, unassigned))}")


@Trace
def tnvsl_dfs_gen(sets, tnvsl):
    remaining_indices = uninstantiated_indices(tnvsl)
    if not remaining_indices:
        yield tnvsl
    else:
        if any(not sets[i] for i in remaining_indices):
            return None

        nxt_indx = min(remaining_indices,
                       key=lambda indx: len(sets[indx]))
        for elmt in sets[nxt_indx]:
            if elmt not in tnvsl:
                new_tnvsl = tnvsl[:nxt_indx] \
                            + (elmt,) \
                            + tnvsl[nxt_indx + 1:]
                new_sets = [set - {elmt} for set in sets]
                yield from tnvsl_dfs_gen(new_sets, new_tnvsl)


if __name__ == '__main__':
    print(f'\n{"-" * 75}'
          f'\ntnvsl_dfs_gen({sets}, (_, _, _))\n')
    for tnvsl in tnvsl_dfs_gen(sets, (unassigned, unassigned, unassigned)):
        print('=> ', tnvsl)

    Trace.trace = False
    for tnvsl in tnvsl_dfs_gen(sets, (unassigned, unassigned, unassigned)):
        sum_string = ' + '.join(str(i) for i in tnvsl)
        equals = '==' if sum(tnvsl) == 6 else '!='
        print(f'{sum_string} {equals} 6')
        if sum(tnvsl) == 6: break


def uninstan_indices_lv(tnvsl):
  return [indx for indx in range(len(tnvsl))
               if not tnvsl[indx].is_instantiated()]


@Trace
def tnvsl_dfs_gen_lv(sets, tnvsl):
    var_indxs = uninstan_indices_lv(tnvsl)

    if not var_indxs: yield tnvsl
    else:
        empty_sets = [sets[indx].is_empty()
                      for indx in var_indxs]
        if any(empty_sets): return None

        nxt_indx = min(var_indxs,
                       key=lambda indx: len(sets[indx]))
        used_values = PyList([tnvsl[i]
                              for i in range(len(tnvsl))
                              if i not in var_indxs])
        T_Var = tnvsl[nxt_indx]
        for _ in member(T_Var, sets[nxt_indx]):
            for _ in fails(member)(T_Var, used_values):
                new_sets = [set.discard(T_Var)
                            for set in sets]
                yield from tnvsl_dfs_gen_lv(new_sets,
                                            tnvsl)


if __name__ == '__main__':
    print('\n\n latest')
    Trace.trace = True
    print(f'\n{"=" * 15}')
    (A, B, C) = (Var(), Var(), Var())
    Py_Sets = [PySet(set) for set in sets]
    N = PyValue(6)
    for _ in tnvsl_dfs_gen_lv(Py_Sets, (A, B, C)):
        sum_string = ' + '.join(str(i) for i in (A, B, C))
        equals = '==' if A + B + C == N else '!='
        print(f'{sum_string} {equals} 6')
        if A + B + C == N: break
    print(f'{"=" * 15}')


# propagate = True
# smallest_first = True
# def find_transversal_with_sum_n(py_sets: List[PySet], n: PyValue):
#     (A, B, C) = (Var(), Var(), Var())
#     for _ in tnvsl_dfs_gen_lv(py_sets, (A, B, C)):
#         if A + B + C == n:
#             return (A, B, C)
#         else:
#             print(f'{A} + {B} + {C} != {n}')
#     print(f'No more transversals')
#     # This is the default even without the following statement
#     return None
#

# if __name__ == '__main__':
#     for smallest_first in [False, True]:
#         for propagate in [False, True]:
#             print(f'\n{"-" * 75}'
#                   f'\ntransversal_yield_lv({sets_lv_string}, (PyValue(None), PyValue(None), PyValue(None)))'
#                   f'\n  propagate: {propagate}; smallest_first: {smallest_first}\n')
#             transversal = (PyValue(None), PyValue(None), PyValue(None))
#             for _ in transversal_yield_lv(sets_lv, transversal):
#                 print(f'Yielded logic-variable traversal: {Trace.to_str(transversal)}\n')
#
# """
# ---------------------------------------------------------------------------
# transversal_yield_lv([{1, 2, 3}, {1, 2, 4}, {1}], (PyValue(None), PyValue(None), PyValue(None)))
#   propagate: False; smallest_first: False
#
# sets: [{1, 2, 3}, {1, 2, 4}, {1}], transversal: (_, _, _)
#   sets: [{1, 2, 3}, {1, 2, 4}, {1}], transversal: (1, _, _)
#     sets: [{1, 2, 3}, {1, 2, 4}, {1}], transversal: (1, 2, _)
#     sets: [{1, 2, 3}, {1, 2, 4}, {1}], transversal: (1, 4, _)
#   sets: [{1, 2, 3}, {1, 2, 4}, {1}], transversal: (2, _, _)
#     sets: [{1, 2, 3}, {1, 2, 4}, {1}], transversal: (2, 1, _)
#     sets: [{1, 2, 3}, {1, 2, 4}, {1}], transversal: (2, 4, _)
#       sets: [{1, 2, 3}, {1, 2, 4}, {1}], transversal: (2, 4, 1)
# Yielded logic-variable traversal: (2, 4, 1)
#
#   sets: [{1, 2, 3}, {1, 2, 4}, {1}], transversal: (3, _, _)
#     sets: [{1, 2, 3}, {1, 2, 4}, {1}], transversal: (3, 1, _)
#     sets: [{1, 2, 3}, {1, 2, 4}, {1}], transversal: (3, 2, _)
#       sets: [{1, 2, 3}, {1, 2, 4}, {1}], transversal: (3, 2, 1)
# Yielded logic-variable traversal: (3, 2, 1)
#
#     sets: [{1, 2, 3}, {1, 2, 4}, {1}], transversal: (3, 4, _)
#       sets: [{1, 2, 3}, {1, 2, 4}, {1}], transversal: (3, 4, 1)
# Yielded logic-variable traversal: (3, 4, 1)
#
#
# """
#
# """
# transversal_prolog(Sets, Partial_Transversal, _Complete_Transversal) :-
#     writeln('Sets': Sets,'  Partial_Transversal': Partial_Transversal),
#     fail.
#
# transversal_prolog([], Complete_Transversal, Complete_Transversal) :-
#     format(' => '),
#     writeln(Complete_Transversal), nl.
#
# transversal_prolog([S|Ss], Partial_Transversal, Complete_Transversal_X) :-
#     member(X, S),
#     \+ member(X, Partial_Transversal),
#     append(Partial_Transversal, [X], Partial_Transversal_X),
#     transversal_prolog(Ss, Partial_Transversal_X, Complete_Transversal_X).
#
#
#
#
#
#
#
# ?- transversal_prolog([[1, 2, 3], [2, 4], [1]], [], Complete_Transversal).
#
# Sets:[[1, 2, 3], [2, 4], [1]]; Partial_Transversal:[]
# Sets:[[2, 4], [1]]; Partial_Transversal:[1]
# Sets:[[1]]; Partial_Transversal:[1, 2]
# Sets:[[1]]; Partial_Transversal:[1, 4]
# Sets:[[2, 4], [1]]; Partial_Transversal:[2]
# Sets:[[1]]; Partial_Transversal:[2, 4]
# Sets:[]; Partial_Transversal:[2, 4, 1]
#  => [2, 4, 1]
#
# Sets:[[2, 4], [1]]; Partial_Transversal:[3]
# Sets:[[1]]; Partial_Transversal:[3, 2]
# Sets:[]; Partial_Transversal:[3, 2, 1]
#  => [3, 2, 1]
#
# Sets:[[1]]; Partial_Transversal:[3, 4]
# Sets:[]; Partial_Transversal:[3, 4, 1]
#  => [3, 4, 1]
#
#
#
# """
