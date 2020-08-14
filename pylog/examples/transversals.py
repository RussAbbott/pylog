from inspect import isgeneratorfunction, signature
from typing import Generator, List, Optional, Set, Tuple

from control_structures import fails
from logic_variables import PyValue
from sequence_options.sequences import PyList, PySet, PyTuple
from sequence_options.super_sequence import member


trace = True

class Trace:

    def __init__(self, f):
        self.param_names = [param.name for param in signature(f).parameters.values()]
        self.f = f
        self.depth = 0

    def __call__(self, *args):
        if trace:
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
        if type(xs) in [list, tuple]:
            (left, right) = ('[', ']') if isinstance(xs, list) else ('(', ')')
            xs_string = f'{left}{", ".join(Trace.to_str(x) for x in xs)}{right}'
        else:
            xs_string = str(xs)
        return xs_string

    def trace_line(self, args):
        prefix = "  " * self.depth
        params = ", ".join([f'{param_name}: {Trace.to_str(arg)}'
                            for (param_name, arg) in zip(self.param_names, args)])
        # Special case for the transversal functions
        termination = ' <=' if not args[0] else ''
        return prefix + params + termination


unassigned = '_'
def uninstantiated_indices(transversal):
    """ Must return the actual list because the result is used twice.  """
    return [indx for indx in range(len(transversal)) if transversal[indx] is unassigned]


@Trace
def transversal_dfs_first(sets: List[Set[int]], transversal) -> Optional[Tuple]:
    """ Looking for the first solution. """
    remaining_indices = uninstantiated_indices(transversal)
    if not remaining_indices:
        return transversal

    # If the empty set is associated with one of the remaining indices, fail.
    # This can only happen if we are propagating and removing elements from sets.
    if propagate and set() in (sets[indx] for indx in remaining_indices):
        return None

    # Go through the remaining indices either in numerical order or smallest remainging set first.
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
# Is there a better example?
sets = [{1, 2, 3}, {1, 2, 4}, {1}]

if __name__ == '__main__':

    global propagate, smallest_first
    for smallest_first in [False, True]:
        for propagate in [False, True]:
            print(f'\n{"-" * 75}'
                  f'\ntransversal_dfs_first({sets}, (unassigned, unassigned, unassigned) '
                  f'\n  propagate: {propagate}; smallest_first: {smallest_first}\n')
            print(f'\nFirst transversal: {transversal_dfs_first(sets, (unassigned, unassigned, unassigned))}')

"""Output

---------------------------------------------------------------------------
transversal_dfs_first([{1, 2, 3}, {1, 2, 4}, {1}], (unassigned, unassigned, unassigned) 
propagate: False; smallest_first: False

sets: [{1, 2, 3}, {1, 2, 4}, {1}], transversal: (_, _, _)
  sets: [{1, 2, 3}, {1, 2, 4}, {1}], transversal: (1, _, _)
    sets: [{1, 2, 3}, {1, 2, 4}, {1}], transversal: (1, 2, _)
    sets: [{1, 2, 3}, {1, 2, 4}, {1}], transversal: (1, 4, _)
  sets: [{1, 2, 3}, {1, 2, 4}, {1}], transversal: (2, _, _)
    sets: [{1, 2, 3}, {1, 2, 4}, {1}], transversal: (2, 1, _)
    sets: [{1, 2, 3}, {1, 2, 4}, {1}], transversal: (2, 4, _)
      sets: [{1, 2, 3}, {1, 2, 4}, {1}], transversal: (2, 4, 1)
(2, 4, 1)

"""

"""                  transversal_dfs_all                   """


@Trace
def transversal_dfs_all(sets: List[Set[int]], transversal) -> List[Tuple]:
    remaining_indices = uninstantiated_indices(transversal)

    if not remaining_indices:
        return [transversal]

    all_transversals = []

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
                  f'\ntransversal_dfs_all({sets}, (unassigned, unassigned, unassigned)) '
                  f'\n  propagate: {propagate}; smallest_first: {smallest_first}\n')
            print(f'\nAll transversals: {transversal_dfs_all(sets, (unassigned, unassigned, unassigned))}')


"""
---------------------------------------------------------------------------
transversal_dfs_all([{1, 2, 3}, {1, 2, 4}, {1}], (unassigned, unassigned, unassigned)) 
propagate: False; smallest_first: False

sets: [{1, 2, 3}, {1, 2, 4}, {1}], transversal: (_, _, _)
  sets: [{1, 2, 3}, {1, 2, 4}, {1}], transversal: (1, _, _)
    sets: [{1, 2, 3}, {1, 2, 4}, {1}], transversal: (1, 2, _)
    sets: [{1, 2, 3}, {1, 2, 4}, {1}], transversal: (1, 4, _)
  sets: [{1, 2, 3}, {1, 2, 4}, {1}], transversal: (2, _, _)
    sets: [{1, 2, 3}, {1, 2, 4}, {1}], transversal: (2, 1, _)
    sets: [{1, 2, 3}, {1, 2, 4}, {1}], transversal: (2, 4, _)
      sets: [{1, 2, 3}, {1, 2, 4}, {1}], transversal: (2, 4, 1)
  sets: [{1, 2, 3}, {1, 2, 4}, {1}], transversal: (3, _, _)
    sets: [{1, 2, 3}, {1, 2, 4}, {1}], transversal: (3, 1, _)
    sets: [{1, 2, 3}, {1, 2, 4}, {1}], transversal: (3, 2, _)
      sets: [{1, 2, 3}, {1, 2, 4}, {1}], transversal: (3, 2, 1)
    sets: [{1, 2, 3}, {1, 2, 4}, {1}], transversal: (3, 4, _)
      sets: [{1, 2, 3}, {1, 2, 4}, {1}], transversal: (3, 4, 1)

All transversals: [(2, 4, 1), (3, 2, 1), (3, 4, 1)]
"""

"""                  transversal_yield                   """


@Trace
def transversal_yield(sets: List[Set[int]], transversal: Tuple = ()) -> Generator[Tuple, None, None]:
    remaining_indices = uninstantiated_indices(transversal)
    if not remaining_indices:
        yield transversal
    else:

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
                  f'\ntransversal_yield({sets}, (unassigned, unassigned, unassigned)) '
                  f'\n  propagate: {propagate}; smallest_first: {smallest_first}\n')
            for Transversal in transversal_yield(sets, (unassigned, unassigned, unassigned)):
                print(f'Yielded transversal: {Transversal}\n')


"""
---------------------------------------------------------------------------
transversal_yield([[1, 2, 3], [2, 4], [1]], [])

[2, 4, 1]
[3, 2, 1]
[3, 4, 1]

"""
"""                  transversal_yield_lv                   """

sets_lv = [PySet({1, 2, 3}), PySet({1, 2, 4}), PySet({1})]
sets_lv_string = f'[{", ".join(str(s) for s in sets_lv)}]'

def uninstantiated_indices_lv(transversal):
    """ Must return the actual list because the result is used twice.  """
    return [indx for indx in range(len(transversal)) if not transversal[indx].is_instantiated()]


@Trace
def transversal_yield_lv(sets: List[PySet], transversal: Tuple[PyValue]):
    """
    transversal is a tuple of length len(sets).
    Initially it consists of uninstaniated PyValues.
    When all the PyValues are instantiated, it is yielded as the answer.
    """
    remaining_indices = uninstantiated_indices_lv(transversal)
    if not remaining_indices:
        yield transversal
    else:
        if propagate:
            # If we are propagating, we will have removed used values from all the sets.
            # If any of those sets are now empty but are associated with
            # an uninstantiated position in transversal, fail;
            empty_sets = [sets[indx].is_empty() for indx in remaining_indices]
            if any(empty_sets):
                return None

        next_index = min(remaining_indices,
                         key=lambda indx: indx if not smallest_first else len(sets[indx]))
        # T_next is the PyValue to be instantiated this time around.
        T_next = transversal[next_index]
        used_values = PyList([transversal[i] for i in range(len(transversal)) if i not in remaining_indices])
        for _ in member(T_next, sets[next_index]):
            for _ in fails(member)(T_next, used_values):
                new_sets = sets if not propagate else [set.discard(T_next) for set in sets]
                yield from transversal_yield_lv(new_sets, transversal)


if __name__ == '__main__':
    for smallest_first in [False, True]:
        for propagate in [False, True]:
            print(f'\n{"-" * 75}'
                  f'\ntransversal_yield_lv({sets_lv_string}, (PyValue(None), PyValue(None), PyValue(None)))'
                  f'\n  propagate: {propagate}; smallest_first: {smallest_first}\n')
            transversal = (PyValue(None), PyValue(None), PyValue(None))
            for _ in transversal_yield_lv(sets_lv, transversal):
                print(f'Yielded logic-variable traversal: {Trace.to_str(transversal)}\n')

"""
---------------------------------------------------------------------------
transversal_yield_lv([{1, 2, 3}, {1, 2, 4}, {1}], (PyValue(None), PyValue(None), PyValue(None)))
  propagate: False; smallest_first: False

sets: [{1, 2, 3}, {1, 2, 4}, {1}], transversal: (_, _, _)
  sets: [{1, 2, 3}, {1, 2, 4}, {1}], transversal: (1, _, _)
    sets: [{1, 2, 3}, {1, 2, 4}, {1}], transversal: (1, 2, _)
    sets: [{1, 2, 3}, {1, 2, 4}, {1}], transversal: (1, 4, _)
  sets: [{1, 2, 3}, {1, 2, 4}, {1}], transversal: (2, _, _)
    sets: [{1, 2, 3}, {1, 2, 4}, {1}], transversal: (2, 1, _)
    sets: [{1, 2, 3}, {1, 2, 4}, {1}], transversal: (2, 4, _)
      sets: [{1, 2, 3}, {1, 2, 4}, {1}], transversal: (2, 4, 1)
Yielded logic-variable traversal: (2, 4, 1)

  sets: [{1, 2, 3}, {1, 2, 4}, {1}], transversal: (3, _, _)
    sets: [{1, 2, 3}, {1, 2, 4}, {1}], transversal: (3, 1, _)
    sets: [{1, 2, 3}, {1, 2, 4}, {1}], transversal: (3, 2, _)
      sets: [{1, 2, 3}, {1, 2, 4}, {1}], transversal: (3, 2, 1)
Yielded logic-variable traversal: (3, 2, 1)

    sets: [{1, 2, 3}, {1, 2, 4}, {1}], transversal: (3, 4, _)
      sets: [{1, 2, 3}, {1, 2, 4}, {1}], transversal: (3, 4, 1)
Yielded logic-variable traversal: (3, 4, 1)


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

def find_transversal_with_sum_n(sets: List[Set[int]], n: int):
    global trace
    trace = False
    (A, B, C) = (PyValue(), PyValue(), PyValue())
    for _ in transversal_yield_lv(sets, (A, B, C)):
        if A + B + C == PyValue(n):
            return (A.get_py_value(), B.get_py_value(), C.get_py_value())
        else:
            print(f'{A} + {B} + {C} != {n}')


if __name__ == '__main__':
    n = 8
    print(f'{"=" * 15}')
    (a, b, c) = find_transversal_with_sum_n(sets_lv, n)
    print(f'{a} + {b} + {c} == {n}')
    print(f'{"=" * 15}')
