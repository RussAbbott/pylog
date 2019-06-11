from typing import Callable, List, Type

from pylog.control_structures import fails, trace
from pylog.logic_variables import Term


def all_distinct(lst: List[Term]):
  # The following builds a set, not a list: no duplicates.
  values = { x.get_py_value() if x.is_instantiated() else str(x) for x in lst }
  if len(values) == len(lst):
    # Succeed if the number of distinct values is the same as the length of the list.
    yield


def all_all_distinct(lists: List[List[Term]]):
  for lst in lists:
    for _ in fails(all_distinct)(lst):
      # Fail if any of the lists fails all_distinct.
      return
  # Succeed if they all succeed.
  yield


class Problem:
  """ Specific problems will be subclasses of Problem. See scholarship_problem. """

  def __init__(self, Items):
    self.Items = Items
    self.rule_applications = SimpleCounter( )
    # Create these two variables here. The will be set up in the subclass.
    self.all_distinct_lists = None
    self.clues = None
    self.show_trace_list = None

  def __call__(self, ListType: Type, additional_answer: Callable = None):
    """ Run the problem and display the answer. Take and display timing information. """

    inp = None  # needed below at this block level
    from timeit import default_timer as timer
    (start1, end1, start2, end2) = (timer( ), None, None, None)

    last_rule_count = 0

    for _ in trace(f'\n{self.rule_applications.incr( )}) At the start: {self.Items}'):
      for _ in self.run_all_clues(0):
        rule_applications_increment = self.rule_applications.count( ) - last_rule_count
        last_rule_count = self.rule_applications.count( )
        end1 = timer( )
        print(f'\nAfter {rule_applications_increment} rule applications,\nSolution: ')
        for (index, item) in enumerate(self.Items):
          print(f'\t{index + 1}. {item}')
        if additional_answer:
          additional_answer(self.Items)
        inp = input('\nMore? (y, or n)? > ').lower( )
        start2 = timer( )
        if inp != 'y':
          break
      end2 = timer( )
      rule_applications_increment = self.rule_applications.count( ) - last_rule_count
      if inp == 'y':
        print(f'\nAfter {rule_applications_increment} final rule applications, no more solutions.')
      print(f'\nUsing {ListType.__name__}s, the total compute time was: {round(end1 + end2 - start1 - start2, 3)} sec')

  # noinspection SpellCheckingInspection
  def run_clue(self, indx):
    """ Run clue_<indx>, check the all_distinct constraints, and show progress. """
    for _ in self.clues[indx](self.Items):
      for _ in all_all_distinct(self.all_distinct_lists):
        for _ in trace(f'{self.rule_applications.incr( )}) After clue {indx+1}: {self.Items}',
                       show_trace=(indx+1) in self.show_trace_list):
          yield
      
  def run_all_clues(self, clue_number):
    if clue_number >= len(self.clues):
      # Ran all the clues. Succeed.
      yield
    else:
      # Run the current clue and the rest of them.
      for _ in self.run_clue(clue_number):
        yield from self.run_all_clues(clue_number+1)
    
  def set_clues_list(self, clues):
    self.clues = clues

  def set_all_distinct_lists(self, all_distinct_lists):
    self.all_distinct_lists = all_distinct_lists  # {index+1: clue for (index, clue) in enumerate(clue_names)}


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