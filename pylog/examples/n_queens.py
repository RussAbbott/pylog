from logic_variables import Container
from typing import Generator, List


def add_a_row(placement_container: Container, board_width: int) -> Generator[List[int], None, None]:
  """
  Find a safe spot for a queen in the next row and continue with the rest of the rows.

  :param placement_container:  The placement is the positions of the queens in earlier rows.
  A placement is a list of n integers. The rth integer indicates where the queen is to be
  placed in the rth row. I.e., placement[r] is the position of the queen in row r.
  placement_container is used to pass placement lists up and down the recursion.
  :param board_width: the size of the board: board_width x board_width, generally 8.
  """
  placement = placement_container.get_ground_value()
  for col in range(board_width):
    if is_safe(placement, col):
      extended_placement = placement+[col]
      placement_container.set_contents(extended_placement)
      if len(extended_placement) == board_width:
        # Found a solution. It is stored in the placement_container Container rather than being "yielded."
        # This function should be called with an empty container as the placement_container argument.
        # placement_container.setContents(extended_placement)
        yield
      else:
        # Find a column for the next row -- and beyond.
        yield from add_a_row(placement_container, board_width)
        # Preceding line is equivalent to the following.
        # for _ in add_a_row(extended_placement, board_width, placement_container):
        #   yield


def is_safe(placement: [int], col: int) -> bool:
  """ Given the placement so far, is it safe to add a queen in the next row at col? """
  row = len(placement)
  return all([col != colp and abs(rowp - row) != abs(colp - col)
              for (rowp, colp) in enumerate(placement)])


def gen_n_queens(board_width: int):
  """
  Generate and display all solutions to the n-queens problem.
  Uses yield and backtracking but not logic variables.
  The "container" is something like a poor-man's logic variable.
  """
  placement_container = Container( [ ] )
  solutionNbr = 0
  for _ in add_a_row(placement_container, board_width):
    solutionNbr += 1
    print(f'\n{solutionNbr}.\n{layout(placement_container.get_contents( ), board_width)}')


def layout(placement: [int], board_width: int) -> str:
  """ Format the placement list for display."""
  offset = ord('a')
  # Generate the column headers
  col_hdrs = ' '*4 + '  '.join([f'{chr(n+offset)}' for n in range(board_width)]) + '  col#\n'
  display = col_hdrs + '\n'.join([one_row(r, c, board_width) for (r, c) in enumerate(placement)])
  return display


def one_row(row: int, col: int, board_width: int) -> str:
  # The "+1's" convert 0-based computation to 1-based display.
  return f'{row+1}. {" . "*col} Q {" . "*(board_width-col-1)} ({col+1})'


if __name__ == "__main__":
  gen_n_queens(8)
