from typing import Generator, List
from math import log10

from logic_variables import unify, Var
from sequence_options.sequences import PyList


def place_the_remaining_queens(Placement: PyList, board_width: int, Solution: Var) -> Generator[List[int], None, None]:
  """
  Find a safe spot for a queen in the row after those in the current Placement and continue with the rest of the rows.
  
  :param Placement: A Placement is a list of n integers. It indicates the rows, from 0 through len(Placement)-1,
  that have non-conflicting queen column assignments. The rth integer, i.e., Placement[r], indicates the column in
  which the queen is to be placed in the rth row.
  :param board_width: the size of the board: board_width x board_width, generally 8.
  :param Solution: the Var that will eventually be unified with the Placement holding an answer. This is how
  answers are generally returned in Prolog.
  """
  # The following will try all the columns as possible positions for the next queen.
  # It's what makes Prolog look like it's backtracking.
  for col in range(board_width):
    # Note that there is no 'else' for the following if. Whether or not col is not a safe position,
    # we go on to the next one after processing col.
    if is_safe(Placement, col):
      # + is defined for PyLists to mirror + for normal Python lists.
      Extended_Placement: PyList = Placement + PyList([col])

      # Have we filled the board?
      if len(Extended_Placement) == board_width:
        # Found a solution. Unify it with Solution and indicate success by yielding.
        yield from unify(Extended_Placement, Solution)
        # The preceding 'yield from' line is equivalent to the following.
        # for _ in unify(Extended_Placement, Solution):
        #   yield

      # Still more queens to place.
      else:
        # Find columns for the remaining queens.
        yield from place_the_remaining_queens(Extended_Placement, board_width, Solution)
        # The preceding 'yield from' line is equivalent to the following.
        # for _ in place_the_remaining_queens(Extended_Placement, board_width, Solution):
        #   yield


def is_safe(Placement: PyList, col: int) -> bool:
  """ Given the Placement so far, is it safe to add a queen in the next row at the col position? """

  # The elements of a PyList are all Logic Variables of some sort. In this case they are all
  # Ground(<int>) for some integer. To work with the actual integer values, we convert the PyList to
  # a Python list and then extract the values from their Ground wrappers.

  # Ground_Col_Nbr will be a Ground object containing a col number.
  # get_ground_value() extracts the actual integer.

  placement_vector: [int] = [Ground_Col_Nbr.get_ground_value() for Ground_Col_Nbr in Placement.to_python_list()]

  row = len(Placement)  # the same as len(placement_vector)

  # (row, col) is the proposed position of the new queen. 
  # Assuming that (rowp, colp) is the position of a previously set queen, (row, col) is a safe placement if:
  # (a) col has not been used previously, i.e., col != colp, and
  # (b) (row, col) is not on the same diagonal as any previous queen, i.e., abs(rowp - row) != abs(colp - col).

  return all([col != colp and abs(rowp - row) != abs(colp - col) for (rowp, colp) in enumerate(placement_vector)])


def gen_n_queens(board_width: int):
  """
  Generate and display all solutions to the n-queens problem.

  A Placement is a list of n integers. The rth integer indicates where the queen is to be
  placed in the rth row. I.e., Placement[r] is the position of the queen in row r.
  Initially, it is an empty list.
  """
  Placement = PyList( [] )
  solutionNbr = 0
  Solution = Var()
  # Traditional Prolog style puts the arg that will be unified with the answer (in this case Solution) at the end.
  for _ in place_the_remaining_queens(Placement, board_width, Solution):
    # This is a typical Python for-loop: we reach this point for every solution found.
    # The difference is that the solution is returned in the Solution argument
    # rather than in a variable in the fol-loop between 'for' and 'in'.
    solutionNbr += 1
    # get_ground_value follows Solution's unification trail to the end and then finds the ground value.
    # (In this case, Solution's unification trail is only one step.)
    solution_display = layout(Solution.get_ground_value(), board_width)
    print(f'\n{solutionNbr}.\n{solution_display}')


def layout(placement_vector: [int], board_width: int) -> str:
  """ Format the placement_vector for display. """
  offset = ord('a')
  # Generate the column headers.
  col_hdrs = ' '*(4+int(log10(board_width))) + \
             '  '.join([f'{chr(n+offset)}' for n in range(board_width)]) + '  col#\n'
  display = col_hdrs + '\n'.join([one_row(r, c, board_width) for (r, c) in enumerate(placement_vector)])
  return display


def one_row(row: int, col: int, board_width: int) -> str:
  """ Generate one row of the board. """
  # (row, col) is the queen position expressed in 0-based indices.
  return f'{space_offset(row+1, board_width)}{row+1}) ' + \
         f'{" . "*col} Q {" . "*(board_width-col-1)} {space_offset(col+1, board_width)}({col+1})'


def space_offset(n, board_width):
  return " "*( int(log10(board_width) ) - int(log10(n)) )


if __name__ == "__main__":
  # The parameter to gen_n_queens is the size of the board, typically 8x8.
  gen_n_queens(10)
