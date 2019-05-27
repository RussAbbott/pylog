from logic_variables import Container
from typing import Generator, List


def add_a_row(placementContainer: Container, boardWidth: int) -> Generator[List[int], None, None]:
  """
  Find a safe spot for a queen in the next row and continue with the rest of the rows.

  :param placementContainer:  The placement is the positions of the queens in earlier rows.
  A placement is a list of n integers. The rth integer indicates where the queen is to be
  placed in the rth row. I.e., placement[r] is the position of the queen in row r.
  placementContainer is used to pass placement lists up and down the recursion.
  :param boardWidth: the size of the board: boardWidth x boardWidth, generally 8.
  """
  placement = placementContainer.get_ground_value()
  for col in range(boardWidth):
    if is_safe(placement, col):
      extendedPlacement = placement+[col]
      placementContainer.set_contents(extendedPlacement)
      if len(extendedPlacement) == boardWidth:
        # Found a solution. It is stored in the placementContainer Container rather than being "yielded."
        # This function should be called with an empty container as the placementContainer argument.
        # placementContainer.setContents(extendedPlacement)
        yield
      else:
        # Find a column for the next row -- and beyond.
        yield from add_a_row(placementContainer, boardWidth)
        # Preceding line is equivalent to the following.
        # for _ in add_a_row(extendedPlacement, boardWidth, placementContainer):
        #   yield


def is_safe(placement: [int], col: int) -> bool:
  """ Given the placement so far, is it safe to add a queen in the next row at col? """
  row = len(placement)
  return all([col != colp and abs(rowp - row) != abs(colp - col)
              for (rowp, colp) in enumerate(placement)])


def gen_n_queens(boardWidth: int):
  """
  Generate and display all solutions to the n-queens problem.
  Uses yield and backtracking but not logic variables.
  The "container" is something like a poor-man's logic variable.
  """
  placementContainer = Container( [ ] )
  solutionNbr = 0
  for _ in add_a_row(placementContainer, boardWidth):
    solutionNbr += 1
    print(f'\n{solutionNbr}.\n{layout(placementContainer.get_contents( ), boardWidth)}')


def layout(placement: [int], boardWidth: int) -> str:
  """ Format the placement list for display."""
  offset = ord('a')
  # Generate the column headers
  colHdrs = ' '*4 + '  '.join([f'{chr(n+offset)}' for n in range(boardWidth)]) + '  col#\n'
  display = colHdrs + '\n'.join([one_row(r, c, boardWidth) for (r, c) in enumerate(placement)])
  return display


def one_row(row: int, col: int, boardWidth: int) -> str:
  # The "+1's" convert 0-based computation to 1-based display.
  return f'{row+1}. {" . "*col} Q {" . "*(boardWidth-col-1)} ({col+1})'


if __name__ == "__main__":
  gen_n_queens(8)
