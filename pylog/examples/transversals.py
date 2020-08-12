from inspect import isgeneratorfunction, signature
from typing import Generator, List, Optional, Set, Tuple

from control_structures import fails
from logic_variables import PyValue
from sequence_options.sequences import PyList, PySet, PyTuple
from sequence_options.super_sequence import member


class Trace:

    def __init__(self, f):
        self.param_names = [param.name for param in signature(f).parameters.values()]
        self.f = f
        self.depth = 0

    def __call__(self, *args):
        print(self.trace_line(args))
        self.depth += 1
        if isgeneratorfunction(self.f):
            return self.yield_from(*args)
        else:
            f_return = self.f(*args)
            self.depth -= 1
            return f_return

    def yield_from(self, *args):
        yield from self.f(*args)
        self.depth -= 1

    @staticmethod
    def to_str(xs):
        xs_string = f'[{", ".join(Trace.to_str(x) for x in xs)}]' if isinstance(xs, list) else str(xs)
        return xs_string

    def trace_line(self, args):
        prefix = "  " * self.depth
        params = ", ".join([f'{param_name}: {Trace.to_str(arg)}'
                            for (param_name, arg) in zip(self.param_names, args)])
        # Special case for the transversal functions
        termination = ' <=' if not args[0] else ''
        return prefix + params + termination


def uninstantiated_indices(transversal):
    """ Must return the actual list because the result is used twice.  """
    return [indx for indx in range(len(transversal)) if transversal[indx] is None]


@Trace
def transversal_dfs_first(sets: List[Set[int]], transversal) -> Optional[Tuple]:
    """ Looking for the first solution. """
    remaining_indices = uninstantiated_indices(transversal)
    if not remaining_indices:
        return transversal

    # noinspection PyUnboundLocalVariable
    if propagate and set() in (sets[indx] for indx in remaining_indices):
        return None

    next_index = min(remaining_indices,
                     key=lambda indx: indx if not smallest_first else len(sets[indx]))
    for element in sets[next_index]:
        if element not in transversal:
            new_transversal = transversal[:next_index] + (element, ) + transversal[next_index+1:]
            new_sets = sets if not propagate else [set-{element} for set in sets]
            complete_transversal = transversal_dfs_first(new_sets, new_transversal)
            if complete_transversal is not None:
                return complete_transversal


# Use this for all non-lv tests.
sets = [{1, 2, 3}, {1, 2, 4}, {1}]

if __name__ == '__main__':

    global propagate, smallest_first
    for smallest_first in [False, True]:
        for propagate in [False, True]:
            print(f'\n{"-" * 75}'
                  f'\ntransversal_dfs_first({sets}, (None, None, None)) '
                  f'\npropagate: {propagate}; smallest_first: {smallest_first}\n')
            transversal_dfs_first(sets, (None, None, None))

"""Output

---------------------------------------------------------------------------
transversal_dfs_first([[1, 2, 3], [2, 4], [1]], [])

sets: [[1, 2, 3], [2, 4], [1]], transversal: []
. sets: [[2, 4], [1]], transversal: [1]
. . sets: [[1]], transversal: [1, 2]
. . sets: [[1]], transversal: [1, 4]
. sets: [[2, 4], [1]], transversal: [2]
. . sets: [[1]], transversal: [2, 4]
. . . sets: [], transversal: [2, 4, 1]
. . . => [2, 4, 1]

"""

"""                  transversal_dfs_all                   """


@Trace
def transversal_dfs_all(sets: List[Set[int]], transversal) -> List[Tuple]:
    remaining_indices = uninstantiated_indices(transversal)

    if not remaining_indices:
        return [transversal]

    all_transversals = []

    # noinspection PyUnboundLocalVariable
    if propagate and set() in (sets[indx] for indx in remaining_indices):
        return []

    next_index = min(remaining_indices,
                     key=lambda indx: indx if not smallest_first else len(sets[indx]))
    for element in sets[next_index]:
        if element not in transversal:
            new_transversal = transversal[:next_index] + (element, ) + transversal[next_index+1:]
            new_sets = sets if not propagate else [set-{element} for set in sets]
            all_transversals += transversal_dfs_all(new_sets, new_transversal)
    return all_transversals


if __name__ == '__main__':
    for smallest_first in [False, True]:
        for propagate in [False, True]:
            print(f'\n{"-" * 75}'
                  f'\ntransversal_dfs_all({sets}, (None, None, None)) '
                  f'\npropagate: {propagate}; smallest_first: {smallest_first}\n')
            print(f'\nAll transversals: {transversal_dfs_all(sets, (None, None, None))}')


"""
---------------------------------------------------------------------------
transversal_dfs_all([[1, 2, 3], [2, 4], [1]], [])

sets: [[1, 2, 3], [2, 4], [1]], transversal: []
. sets: [[2, 4], [1]], transversal: [1]
. . sets: [[1]], transversal: [1, 2]
. . sets: [[1]], transversal: [1, 4]
. sets: [[2, 4], [1]], transversal: [2]
. . sets: [[1]], transversal: [2, 4]
. . . sets: [], transversal: [2, 4, 1]
. . . => [2, 4, 1]
. sets: [[2, 4], [1]], transversal: [3]
. . sets: [[1]], transversal: [3, 2]
. . . sets: [], transversal: [3, 2, 1]
. . . => [3, 2, 1]
. . sets: [[1]], transversal: [3, 4]
. . . sets: [], transversal: [3, 4, 1]
. . . => [3, 4, 1]
"""

"""                  transversal_yield                   """


@Trace
def transversal_yield(sets: List[Set[int]], transversal: Tuple = ()) -> Generator[Tuple, None, None]:
    remaining_indices = uninstantiated_indices(transversal)
    if not remaining_indices:
        yield transversal
    else:
        # noinspection PyUnboundLocalVariable
        if propagate and set() in (sets[indx] for indx in remaining_indices):
            return None

        next_index = min(remaining_indices,
                         key=lambda indx: indx if not smallest_first else len(sets[indx]))
        for element in sets[next_index]:
            if element not in transversal:
                new_transversal = transversal[:next_index] + (element, ) + transversal[next_index+1:]
                new_sets = sets if not propagate else [set-{element} for set in sets]
                yield from transversal_yield(new_sets, new_transversal)


if __name__ == '__main__':
    for smallest_first in [False, True]:
        for propagate in [False, True]:
            print(f'\n{"-" * 75}'
                  f'\ntransversal_yield({sets}, (None, None, None)) '
                  f'\npropagate: {propagate}; smallest_first: {smallest_first}\n')
            for Transversal in transversal_yield(sets, (None, None, None)):
                print(f'Transversal: {Transversal}\n')


"""
---------------------------------------------------------------------------
transversal_yield([[1, 2, 3], [2, 4], [1]], [])

[2, 4, 1]
[3, 2, 1]
[3, 4, 1]

"""
"""                  transversal_yield_lv                   """

Sets_lv = [PySet({1, 2, 3}), PySet({1, 2, 4}), PySet({1})]
Sets_lv_string = f'[{", ".join(str(s) for s in Sets_lv)}]'


# This is the original transversal_yield_lv
# @Trace
# def transversal_yield_lv_0(Sets: List[PySet], Transversal: PyTuple, Complete_Transversal: Var):
#   if not Sets:
#     yield from unify(Transversal, Complete_Transversal)
#   else:
#     (S, Ss) = (Sets[0], Sets[1:])
#     if S.is_empty():
#       return None
#     Element = Var()
#     for _ in member(Element, S):
#       for _ in fails(member)(Element, Transversal):
#         yield from transversal_yield_lv_0(Ss, Transversal + PyTuple((Element, )), Complete_Transversal)
#
#
# if __name__ == '__main__':
#   print(f'\n{"-"*75}\ntransversal_yield_lv_0({Sets_lv_string}, ()), Ans)\n')
#   Complete_Transversal = Var()
#   for _ in transversal_yield_lv_0(Sets_lv, PyTuple(()), Complete_Transversal):
#     print(f'{" "*30}  =>  {Complete_Transversal}')
#
#
def uninstantiated_indices_lv(transversal):
    """ Must return the actual list because the result is used twice.  """
    return [indx for indx in range(len(transversal)) if not transversal[indx].is_instantiated()]


@Trace
def transversal_yield_lv(Sets: List[PySet], Transversal: PyTuple):
    """
    Transversal is a tuple of length len(Sets).
    Initially it consists of uninstaniated PyValues.
    When all the PyValues are instantiated, it is yielded as the answer.
    """
    remaining_indices = uninstantiated_indices_lv(Transversal)
    if not remaining_indices:
        yield Transversal
    else:
        if propagate:
            # If we are propagating, we will have removed used values from all the sets.
            # If any of those sets are now empty but are associated with
            # an uninstantiated position in Transversal, fail;
            empty_sets = [Sets[indx].is_empty() for indx in remaining_indices]
            if any(empty_sets):
                return None

        next_index = min(remaining_indices,
                         key=lambda indx: indx if not smallest_first else len(sets[indx]))
        # T_next is the PyValue to be instantiated this time around.
        T_next = Transversal[next_index]
        # Keep PyCharm happy
        assert isinstance(T_next, PyValue)
        used_values = PyList([Transversal[i] for i in range(len(Transversal)) if i not in remaining_indices])
        for _ in member(T_next, Sets[next_index]):
            for _ in fails(member)(T_next, used_values):
                New_sets = Sets if not propagate else [set.discard(T_next) for set in Sets]
                yield from transversal_yield_lv(New_sets, Transversal)


if __name__ == '__main__':
    for smallest_first in [False, True]:
        for propagate in [False, True]:
            print(f'\n{"-" * 75}'
                  f'\ntransversal_yield_lv({Sets_lv_string}, (None, None, None), Ans)'
                  f'\npropagate: {propagate}; smallest_first: {smallest_first}\n')
            Complete_Transversal = PyTuple((None, None, None))
            for _ in transversal_yield_lv(Sets_lv, Complete_Transversal):
                print(Complete_Transversal)

"""
---------------------------------------------------------------------------
transversal_yield_lv([[1, 2, 3], [2, 4], [1]], [], Ans)

[2, 4, 1]
[3, 2, 1]
[3, 4, 1]

"""

"""
transversal_prolog(Sets, Partial_Transversal, _Complete_Transversal) :-
    writeln('Sets': Sets,'  Partial_Transversal': Partial_Transversal), 
    fail.

transversal_prolog([], Complete_Transversal, Complete_Transversal) :-
    format(' => '),
    writeln(Complete_Transversal), nl.

transversal_prolog([S|Ss], Partial_Transversal, Complete_Transversal_X) :-
    member(X, S),
    \+ member(X, Partial_Transversal),
    append(Partial_Transversal, [X], Partial_Transversal_X),
    transversal_prolog(Ss, Partial_Transversal_X, Complete_Transversal_X).


    
    
    
    
    
?- transversal_prolog([[1, 2, 3], [2, 4], [1]], [], Complete_Transversal).

Sets:[[1, 2, 3], [2, 4], [1]]; Partial_Transversal:[]
Sets:[[2, 4], [1]]; Partial_Transversal:[1]
Sets:[[1]]; Partial_Transversal:[1, 2]
Sets:[[1]]; Partial_Transversal:[1, 4]
Sets:[[2, 4], [1]]; Partial_Transversal:[2]
Sets:[[1]]; Partial_Transversal:[2, 4]
Sets:[]; Partial_Transversal:[2, 4, 1]
 => [2, 4, 1]

Sets:[[2, 4], [1]]; Partial_Transversal:[3]
Sets:[[1]]; Partial_Transversal:[3, 2]
Sets:[]; Partial_Transversal:[3, 2, 1]
 => [3, 2, 1]

Sets:[[1]]; Partial_Transversal:[3, 4]
Sets:[]; Partial_Transversal:[3, 4, 1]
 => [3, 4, 1]



"""


# def print_ABCDE(A, B, C, D, E):
#     print(f'A: {A}, B: {B}, C: {C}, D: {D}, E: {E}')
#
#
# (A, B, C, D, E) = (Var(), Var(), Var(), Var(), 'abc')
# print_ABCDE(A, B, C, D, E)
# for _ in unify(A, B):
#   print_ABCDE(A, B, C, D, E)
#   for _ in unify(D, C):
#     print_ABCDE(A, B, C, D, E)
#     for _ in unify(A, C):
#       print_ABCDE(A, B, C, D, E)
#       for _ in unify(E, D):
#         print_ABCDE(A, B, C, D, E)
#       print_ABCDE(A, B, C, D, E)
#     print_ABCDE(A, B, C, D, E)
#   print_ABCDE(A, B, C, D, E)
# print_ABCDE(A, B, C, D, E)
