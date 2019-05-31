from typing import Callable, Type

from logic_variables import Ground, Structure, Term, Var
from sequence_options.super_sequence import SuperSequence


class Puzzle_Item(Structure):
  """
  A utility superclass for logic puzzles.
  An item in a puzzle list.
  """

  def __str__(self):
    """
    A default way to print out a structure. Use the first arg as the term name.
    """
    allArgs = all(isinstance(arg.trail_end(), Var) for arg in self.args)
    if allArgs:
      # If all the args are uninstantiated, print a simple underscore.
      return '_'
    else:
      args_str = ', '.join(map(str, self.args[1:]))
      result = f'{self.args[0]}({args_str})'
      return result

  @staticmethod
  def make_property(prop):
    """
      Applied to each argument in a term.
      Applies Ground to those that are not already Terms.
      If the property is None, create a Var for it.
    """
    return Var() if prop is None else \
                    prop if isinstance(prop, Term) else \
                    Ground(prop)


def run_puzzle(problem: Callable, ListType: Type, Answer_List: SuperSequence, additional_answer: Callable = None):
  """ Runs the problem and displays the answer. Takes and displays timing information. """

  inp = None  # needed below at this block level
  from timeit import default_timer as timer
  (start1, end1, start2, end2) = (timer( ), None, None, None)
  for _ in problem(Answer_List, ListType):
    end1 = timer( )
    print('\nSolution: ')
    for (index, student) in enumerate(Answer_List):
      print(f'\t{index + 1}. {student}')
    if additional_answer:
      additional_answer(Answer_List)
    inp = input('\nMore? (y, or n)? > ').lower( )
    start2 = timer( )
    if inp != 'y':
      break
  end2 = timer( )
  if inp == 'y':
    print('No more solutions.')
  print(f'\nUsing {ListType.__name__}s, the total compute time was: {round(end1 + end2 - start1 - start2, 3)} sec')
