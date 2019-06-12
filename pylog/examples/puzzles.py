from timeit import default_timer as timer
from typing import List, Type

from control_structures import fails, trace
from logic_variables import Term


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


# noinspection PyMethodMayBeStatic
class Problem:
  """ Specific problems will be subclasses of Problem. See scholarship_problem. """

  def __init__(self):
    self.all_distinct_lists = None
    self.clues = [self.clue_0]
    self.Items = None
    self.ListType = None
    self.printing_time = 0
    self.rule_applications = SimpleCounter( )
    self.show_trace_list = None

  def __call__(self, ListType: Type):
    """ Run the problem and display the answer. Take and display timing information. """

    self.ListType = ListType
    inp = None  # needed below at this block level
    start = timer( )

    last_rule_count = 0

    for _ in self.run_all_clues( ):
      rule_applications_increment = self.rule_applications.count( ) - last_rule_count
      last_rule_count = self.rule_applications.count( )
      pause_timer = timer( )
      print(f'\nAfter {rule_applications_increment} rule applications,\nSolution: ')
      for (index, item) in enumerate(self.Items):
        print(f'\t{index + 1}. {item}')
      self.additional_answer(self.Items)
      inp = input('\nMore? (y, or n)? > ').lower( )
      self.printing_time += timer( )-pause_timer
      if inp != 'y':
        break
    end = timer( )
    rule_applications_increment = self.rule_applications.count( ) - last_rule_count
    if inp == 'y':
      print(f'\nAfter {rule_applications_increment} final rule applications, no more solutions.')
    print(f'\nUsing {ListType.__name__}s, the total compute time was: '
          f'{round(end - start - self.printing_time, 3)} sec')

  def additional_answer(self, _):
    yield

  def check_all_for_distinctness(self, Class):
    """ Sets up to check all attributes for distinctness """
    nbr_attributes = len(Class( ).args)
    vars_lists = [[item.args[i] for item in self.Items] for i in range(nbr_attributes)]
    self.all_distinct_lists = vars_lists

  def clue_0(self, _):
    """ Override in subclass """
    yield

  # noinspection SpellCheckingInspection
  def run_clue(self, clue_nbr):
    """ Run clue_<clue_nbr>, check the all_distinct constraints, and show progress. """
    for _ in self.clues[clue_nbr](self.Items):
      for _ in all_all_distinct(self.all_distinct_lists):
        pause_timer = timer()
        for _ in trace(f'{self.rule_applications.incr( )}) '
                       f'After {"initial setup" if clue_nbr == 0 else ("clue " + str(clue_nbr))}: {self.Items}',
                       show_trace=(clue_nbr) in self.show_trace_list):
          self.printing_time += timer() - pause_timer
          yield
      
  def run_all_clues(self, clue_number=0):
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
