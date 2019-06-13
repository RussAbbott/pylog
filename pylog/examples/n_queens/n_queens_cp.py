from math import log10
from timeit import default_timer as timer
from typing import Dict

# from logic_variables import PyValue, unify


class Placement(Dict):
  def __init__(self, board_size=8):
    self.board_size = board_size
    for c in range(board_size):
      self.__setitem__(c, (None, frozenset(range(board_size))))
    super().__init__()
    
  def __len__(self):
    return self.board_size

  def get_available(self, c):
    return self[c][1]

  def get_value(self, c):
    return self[c][0]

  def is_instantiated(self, c):
    return self.get_value(c) is not None

  def uninstantiated_rows(self):
    return [c for c in self if self.get_value(c) is None]


def layout(placement_vector: [int], board_size: int) -> str:
  """ Format the placement for display. """
  offset = ord('a')
  # Generate the column headers.
  col_hdrs = ' '*(4+int(log10(board_size))) + \
             '  '.join([f'{chr(n+offset)}' for n in range(board_size)]) + '  col#\n'
  display = col_hdrs + '\n'.join([one_row(r, c, board_size) for (r, c) in enumerate(placement_vector)])
  return display


def new_placement_val(next_row, col, r, c, avail):
  """ If next_row gets a col value of c, what is the dictionary value for row r? """
  diff = abs(next_row - r)
  return (col, frozenset()) if next_row == r else \
         (c, avail) if c is not None else \
         (None, avail - {col, col+diff, col-diff})


def one_row(row: int, col: int, board_size: int) -> str:
  """ Generate one row of the board. """
  # (row, col) is the queen position expressed in 0-based indices.
  return f'{space_offset(row+1, board_size)}{row+1}) ' + \
         f'{" . "*col} Q {" . "*(board_size-col-1)} {space_offset(col+1, board_size)}({col+1})'


def place_n_queens(board_size: int):
  """
  Generate and display all solutions to the n-queens problem.

  A Placement is a list of n PyValue integers. The rth integer indicates where the queen is to be
  placed in the rth row. I.e., Placement[r] is the position of the queen in row r.

  """
  start = timer()
  # Create the entire list of PyValue variables along with, for each, the possible
  # values still available for it.
  placement = Placement(board_size)
  solutionNbr = 0
  # place_remaining_queens will instantiate the PyValue variables one by one.
  for solution in place_remaining_queens(placement):
    solutionNbr += 1
    sol = sorted([(r, c) for (r, (c, _)) in solution.items()])
    stripped_sol = [c for (_, c) in sol]
    solution_display = layout(stripped_sol, board_size)
    print(f'\n{solutionNbr}.\n{solution_display}')
    end = timer()
    print(f'time: {round(end-start, 3)}')
    inp = input('\nMore? (y, or n)? > ').lower( )
    if inp != 'y':
      break
    start = timer()


def place_remaining_queens(placement: Placement):
  """
  Find a safe spot for the next queen and either quit if it's the last position or call this recursively.
  """
  uninstantiated_rows = placement.uninstantiated_rows()
  # Select the col with the fewest available possibilities as the next_row to be instantiated.
  next_row = min( uninstantiated_rows, key=lambda row: len(placement.get_available(row)) )
  for col in placement.get_available(next_row):
    next_placement = Placement(placement.board_size)
    # The value for col is None, since it's uninstantiated.
    for (r, (c, avail)) in placement.items( ):
      next_placement[r] = new_placement_val(next_row, col, r, c, avail)
    # Have we just instantiated our last column?
    if len(uninstantiated_rows) == 1:
      yield next_placement

    # If some column has no options left, fail and try the next col, rathet than jumping out of the loop.
    elif frozenset() in [next_placement.get_available(row) for row in next_placement.uninstantiated_rows()]:
      # This must be pass rather than return. We want to continue on to the next col, not jump out of the loop.
      pass

    # More queens to place.
    else:
      # Find columns for the remaining queens.
      yield from place_remaining_queens(next_placement)


def space_offset(n, board_size):
  return " "*( int(log10(board_size) ) - int(log10(n)) )


if __name__ == "__main__":
  # The parameter to place_n_queens is the size of the board, typically 8x8.
  place_n_queens(20)
