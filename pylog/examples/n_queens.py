from typing import Generator, List, Union
from math import log10, floor

from control_structures import eot
from logic_variables import unify, Var  
from sequence_options.sequences import PyList


# The eot decorator replaces every Var arg with the element at the end of its unification trail.
# The one that we care about is Placement, which append will have created as a Var at the previous level.
# Solution is also a Var, but until unified with an actual solution, it is the end of its unification trail.
@eot
def place_the_remaining_queens(Placement: Union[PyList, Var],
                               board_width: int,
                               Solution: Var)                  -> Generator[List[int], None, None]:
  """
  Find a safe spot for a queen in the row after those in the current Placement and continue with the rest of the rows.
  
  :param Placement: The positions of the queens in the currently set rows.
  A Placement is a list of n integers. The rth integer indicates where the queen is to be
  placed in the rth row. I.e., Placement[r] is the position of the queen in row r.
  :param board_width: the size of the board: board_width x board_width, generally 8.
  :param Solution: the Var that will eventually be unified with the Placement holding an answer. This is how
  answers are generally returned in Prolog.
  """
  # This will eventually try all the columns.
  # It's what makes Prolog look like it's backtracking.
  for col in range(board_width):
    # Note that there is no else for this if. If col is not a safe position, go on to the next one.
    # We will eventually do that anyway even if is_safe is true.
    if is_safe(Placement, col):
      # + is defined for PyLists to be the same as for normal Python lists.
      Extended_Placement = Placement + PyList([col])

      # Have we filled the board?
      if len(Extended_Placement) == board_width:
        # Found a solution. Unify it with Solution and indicate success by yielding.
        yield from unify(Extended_Placement, Solution)
      
      # Still more queens to place.
      else:
        # Find columns for the remaining queens.
        yield from place_the_remaining_queens(Extended_Placement, board_width, Solution)
        # The preceding (yield from) line is equivalent to the following.
        # for _ in place_the_remaining_queens(Extended_Placement, board_width, Solution):
        #   yield


def is_safe(Placement: PyList, col: int) -> bool:
  """ Given the Placement so far, is it safe to add a queen in the next row at the col position? """

  # The elements of a PyList are all Logic Variables of some sort. In this case they are all
  # Ground(<int>) for some integer. To work with the actual values, we convert the PyList to
  # a Python list and then extract the values from their Ground wrappers.

  # Col_Nbr will be a Ground object containing a col number.
  # get_ground_value() extracts the actual integer.

  placement_vector = [Col_Nbr.get_ground_value() for Col_Nbr in Placement.to_python_list()]

  row = len(Placement)

  # (row, col) is the proposed position of the new queen. 
  # Assuming that (rowp, colp) is the position of a previously set queen, this is a safe placement if:
  # (a) col has not been used previously, col != colp, and
  # (b) (row, col) is not on the same diagonal as any previous queen, i.e., abs(rowp - row) != abs(colp - col).

  return all([col != colp and abs(rowp - row) != abs(colp - col)
              for (rowp, colp) in enumerate(placement_vector)])


def gen_n_queens(board_width: int):
  """
  Generate and display all solutions to the n-queens problem.
  """
  # Placement is the current rows that have non-conflicting queen column assignments.
  # Initially, it is an empty list
  Placement = PyList( [] )  
  solutionNbr = 0
  Solution = Var()
  # Traditional Prolog style puts the Arg that will be unified with the answer at the end.
  for _ in place_the_remaining_queens(Placement, board_width, Solution):
    # This is like typical for-loop in Python: for every solution we find, we will reach this point.
    solutionNbr += 1
    # get_ground_value follows Solution's unification trail to the end and then finds the ground value.
    # (In this case, the Solution's trail end is only one step away.)
    solution_display = layout(Solution.get_ground_value(), board_width)
    print(f'\n{solutionNbr}.\n{solution_display}')


def layout(placement_vector: [int], board_width: int) -> str:
  """ Format the placement_vector list for display."""
  offset = ord('a')
  # Generate the column headers
  col_hdrs = ' '*(4+floor(log10(board_width))) + \
             '  '.join([f'{chr(n+offset)}' for n in range(board_width)]) + '  col#\n'
  # The "+1'" in "r+1" converts 0-based computation to 1-based display.
  display = col_hdrs + '\n'.join([one_row(r+1, c, board_width) for (r, c) in enumerate(placement_vector)])
  return display


def one_row(row: int, col: int, board_width: int) -> str:
  return f'{row}){" "*( floor(log10(board_width) ) - floor(log10(row)) )} ' + \
         f'{" . "*col} Q {" . "*(board_width-col-1)} ({col+1})'


if __name__ == "__main__":
  # The parameter to gen_n_queens is the size of the board onto which we want place queens.
  gen_n_queens(8)
