from typing import Callable, List, Type

from control_structures import fails
from logic_variables import Term
from sequence_options.super_sequence import SuperSequence


def all_distinct(lst: List[Term]):
  # The following builds a set, not a list. So no duplicates.
  values = { x.get_py_value() if x.is_instantiated() else str(x) for x in lst }
  if len(values) == len(lst):
    # Succeed if the number of distinct values is the same as the length of the list.
    yield


def all_all_distinct(lists: List[List[Term]]) -> bool:
  for lst in lists:
    for _ in fails(all_distinct)(lst):
      # Fail if any of the lists fails all_distinct.
      return
  # Succeed if they all succeed.
  yield


class SimpleCounter:
  def __init__(self, init_value=0):
    self._count = init_value

  def __str__(self):
    return str(self._count)

  def count(self):
    return self._count

  def incr(self, amount=1):
    self._count += amount
    return self


def run_puzzle(Problem: Callable, ListType: Type, Answer_List: SuperSequence, additional_answer: Callable = None):
  """ Runs the problem and displays the answer. Takes and displays timing information. """

  inp = None  # needed below at this block level
  from timeit import default_timer as timer
  (start1, end1, start2, end2) = (timer( ), None, None, None)

  last_rule_count = 0
  problem = Problem(Answer_List)

  for _ in problem():
    rule_applications_increment = problem.rule_applications.count() - last_rule_count
    last_rule_count = problem.rule_applications.count()
    end1 = timer( )
    print(f'\nAfter {rule_applications_increment} rule applications,\nSolution: ')
    for (index, item) in enumerate(Answer_List):
      print(f'\t{index + 1}. {item}')
    if additional_answer:
      additional_answer(Answer_List)
    inp = input('\nMore? (y, or n)? > ').lower( )
    start2 = timer( )
    if inp != 'y':
      break
  end2 = timer( )
  rule_applications_increment = problem.rule_applications.count( ) - last_rule_count
  if inp == 'y':
    print(f'\nAfter {rule_applications_increment} final rule applications, no more solutions.')
  print(f'\nUsing {ListType.__name__}s, the total compute time was: {round(end1 + end2 - start1 - start2, 3)} sec')
