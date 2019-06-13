from math import log10
from timeit import default_timer as timer
from typing import List

from logic_variables import PyValue, unify


# noinspection SpellCheckingInspection
def is_safe(placement: List[PyValue]) -> bool:
  """ Given the Placement so far, is it safe to add a queen in the next row at the col position? """

  placement_vector = [c.get_py_value() for c in placement if c.is_instantiated()]
  row = len(placement_vector)-1
  col = placement_vector[-1]
  # (row, col) is the proposed position of the new queen.
  # Assuming that (rowp, colp) is the position of a previously set queen, (row, col) is a safe placement if:
  # (a) col has not been used previously, i.e., col != colp, and
  # (b) (row, col) is not on the same diagonal as any previous queen, i.e., abs(rowp - row) != abs(colp - col).

  return all([col != colp and abs(rowp - row) != abs(colp - col) for (rowp, colp) in enumerate(placement_vector[:-1])])


def layout(placement_vector: [int], board_width: int) -> str:
  """ Format the placement for display. """
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


def place_n_queens(board_width: int):
  """
  Generate and display all solutions to the n-queens problem.

  A Placement is a list of n PyValue integers. The rth integer indicates where the queen is to be
  placed in the rth row. I.e., Placement[r] is the position of the queen in row r.

  """
  start = timer()
  # Create the entire list of PyValue variables.
  placement = [PyValue() for _ in range(board_width)]
  solutionNbr = 0
  # place_remaining_queens will instantiate the PyValue variables one by one.
  for _ in place_remaining_queens(placement):
    solutionNbr += 1
    solution_display = layout([c.get_py_value() for c in placement], board_width)
    print(f'\n{solutionNbr}.\n{solution_display}')
    end = timer()
    print(f'time: {round(end-start, 3)}')
    inp = input('\nMore? (y, or n)? > ').lower( )
    if inp != 'y':
      break
    start = timer()


def place_remaining_queens(placement: List[PyValue]):
  """
  Find a safe spot for the next queen and eithe quit if it's the last position or call this recursively.
  """
  # next_col is the next column to be instantiated
  next_col = len([c for c in placement if c.is_instantiated()])
  for d in range(len(placement)):
    for _ in unify(placement[next_col], d):
      # Note that there is no 'else' for if is_safe(placement). Whether or not d is a safe position,
      # we go on to the next value after processing it.
      if is_safe(placement):
        # Have we filled the board? If so, next_col will be, e.g., 7, and len(placement) will be 8.
        last_col = len(placement)-1
        if next_col == last_col:
          # Found a solution; yield.
          yield

        # More queens to place.
        else:
          # Find columns for the remaining queens.
          yield from place_remaining_queens(placement)


def space_offset(n, board_width):
  return " "*( int(log10(board_width) ) - int(log10(n)) )


if __name__ == "__main__":
  # The parameter to place_n_queens is the size of the board, typically 8x8.
  place_n_queens(20)
