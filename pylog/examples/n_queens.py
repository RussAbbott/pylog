from typing import Generator, List

from logic_variables import unify, Var  
from sequence_options.sequences import PyList


def add_a_row(Placement: PyList, board_width: int, Solution: Var) -> Generator[List[int], None, None]:
  """
  Find a safe spot for a queen in the next row and continue with the rest of the rows.
  
  The actual checking for safety is done at the Python level rather than at the Prolog level.
  So the values in the current Placement are extracted and processed directly.
  An extended placement_vector is then wrapped in a PyList wrapper.

  :param Placement: The placement_vector is the positions of the queens in earlier rows.
  A placement_vector is a list of n integers. The rth integer indicates where the queen is to be
  placed in the rth row. I.e., placement_vector[r] is the position of the queen in row r.
  Placement is used to pass placement_vector lists up and down the recursion.
  :param board_width: the size of the board: board_width x board_width, generally 8.
  :param Solution: the Var that will eventually be unified with the container holding an answer
  """
  # The elements of a PyList are all Logic Variables of some sort. In this case they are all
  # Ground(<int>) for some integer. To work with the actual values, we extract the list
  # and then extract the values from their Ground wrappers.
  placement_vector = [col.get_ground_value() for col in Placement.to_python_list()]
  for col in range(board_width):
    if is_safe(placement_vector, col):
      extended_placement = placement_vector+[col]
      # The PyList constructor wraps elements of the list it is given in Ground wrappers.
      Extended_Placement = PyList(extended_placement)
      if len(extended_placement) == board_width:
        # Found a solution. Unify it with the Solution Var.
        for _ in unify(Extended_Placement, Solution):
          yield
      else:
        # Find a column for the next row -- and beyond.
        yield from add_a_row(Extended_Placement, board_width, Solution)
        # Preceding line is equivalent to the following.
        # for _ in add_a_row(extended_placement, board_width, Placement):
        #   yield


def is_safe(placement_vector: [int], col: int) -> bool:
  """ Given the placement_vector so far, is it safe to add a queen in the next row at col? """
  row = len(placement_vector)
  return all([col != colp and abs(rowp - row) != abs(colp - col)
              for (rowp, colp) in enumerate(placement_vector)])


def gen_n_queens(board_width: int):
  """
  Generate and display all solutions to the n-queens problem.
  Uses yield and backtracking but not logic variables.
  The "container" is something like a poor-man's logic variable.
  """
  # Placement is the current rows that have non-conflicting column assignments.
  # Initially, it's an empty list
  Placement = PyList( [] )  
  solutionNbr = 0
  Solution = Var()
  # Traditional Prolog style puts Solution, the Arg that will be unified with the answer, at the end.
  for _ in add_a_row(Placement, board_width, Solution):
    solutionNbr += 1
    # get_ground_value follows Solution's unification trail to the end and then finds the ground value.
    # (In this case, the Solution's trail end is only one step away.)
    print(f'\n{solutionNbr}.\n{layout(Solution.get_ground_value(), board_width)}')


def layout(placement_vector: [int], board_width: int) -> str:
  """ Format the placement_vector list for display."""
  offset = ord('a')
  # Generate the column headers
  col_hdrs = ' '*4 + '  '.join([f'{chr(n+offset)}' for n in range(board_width)]) + '  col#\n'
  display = col_hdrs + '\n'.join([one_row(r, c, board_width) for (r, c) in enumerate(placement_vector)])
  return display


def one_row(row: int, col: int, board_width: int) -> str:
  # The "+1's" convert 0-based computation to 1-based display.
  return f'{row+1}. {" . "*col} Q {" . "*(board_width-col-1)} ({col+1})'


if __name__ == "__main__":
  gen_n_queens(8)
