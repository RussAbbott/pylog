from math import log10
from timeit import default_timer as timer
from typing import Generator, List


def is_safe(placement: List[int], col: int) -> bool:
  """ Given the Placement so far, is it safe to add a queen in the next row at the col position? """

  row = len(placement)

  # (row, col) is the proposed position of the new queen. 
  # Assuming that (rowp, colp) is the position of a previously set queen, (row, col) is a safe placement if:
  # (a) col has not been used previously, i.e., col != colp, and
  # (b) (row, col) is not on the same diagonal as any previous queen, i.e., abs(rowp - row) != abs(colp - col).

  return all([col != colp and abs(rowp - row) != abs(colp - col) for (rowp, colp) in enumerate(placement)])


def layout(placement: [int], board_width: int) -> str:
  """ Format the placement for display. """
  offset = ord('a')
  # Generate the column headers.
  col_hdrs = ' '*(4+int(log10(board_width))) + \
             '  '.join([f'{chr(n+offset)}' for n in range(board_width)]) + '  col#\n'
  display = col_hdrs + '\n'.join([one_row(r, c, board_width) for (r, c) in enumerate(placement)])
  return display


def one_row(row: int, col: int, board_width: int) -> str:
  """ Generate one row of the board. """
  # (row, col) is the queen position expressed in 0-based indices.
  return f'{space_offset(row+1, board_width)}{row+1}) ' + \
         f'{" . "*col} Q {" . "*(board_width-col-1)} {space_offset(col+1, board_width)}({col+1})'


def place_n_queens(board_width: int):
  """
  Generate and display all solutions to the n-queens problem.

  A Placement is a list of n integers. The rth integer indicates where the queen is to be
  placed in the rth row. I.e., Placement[r] is the position of the queen in row r.
  Initially, Placement is an empty list.

  This implementation uses a Python list wrapped in a PyValue for Placement. That's so that we
  can demonstrate how to return the solution through Solution rather than through the parameter
  in the "for _ in place_remaining_queens" statement.
  "for Solution in place_remaining_queens" would work as well as long as place_remaining_queens
  yields the solution rather than unifying it with Solution.
  """
  start = timer()
  placement = []
  solutionNbr = 0
  for solution in place_remaining_queens(placement, board_width):
    solutionNbr += 1
    solution_display = layout(solution, board_width)
    print(f'\n{solutionNbr}.\n{solution_display}')
    end = timer()
    print(f'time: {round(end-start, 3)}')
    inp = input('\nMore? (y, or n)? > ').lower( )
    if inp != 'y':
      break
    start = timer()


def place_remaining_queens(placement: List[int], board_width: int) -> Generator[List[int], None, None]:
  """
  Find a safe spot for a queen in the row after those in the current Placement and continue with the rest of the rows.

  :param placement: A placement is a list of n integers. It indicates the rows, from 0 through len(Placement)-1,
  that have non-conflicting queen column assignments. The rth integer, i.e., Placement[r], indicates the column in
  which the queen is to be placed in the rth row.
  :param board_width: the size of the board: board_width x board_width, generally 8.
  """
  # The following will try all the columns as possible positions for the next queen.
  # It's what makes Prolog look like it's backtracking.
  for col in range(board_width):
    # Note that there is no 'else' for the following if. Whether or not col is a safe position,
    # we go on to the next value after processing col.
    if is_safe(placement, col):
      extended_placement = placement + [col]

      # Have we filled the board?
      if len(extended_placement) == board_width:
        # Found a solution; yield it.
        yield extended_placement

      # More queens to place.
      else:
        # Find columns for the remaining queens.
        yield from place_remaining_queens(extended_placement, board_width)
        # The preceding 'yield from' line is equivalent to the following.
        # for _ in place_remaining_queens(Extended_Placement, board_width, Solution):
        #   yield


def space_offset(n, board_width):
  return " "*( int(log10(board_width) ) - int(log10(n)) )


if __name__ == "__main__":
  # The parameter to place_n_queens is the size of the board, typically 8x8.
  place_n_queens(20)
