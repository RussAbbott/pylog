from math import log10
from random import choice
from timeit import default_timer as timer
from typing import Dict


class Placement(Dict):
  """
  This is a dictionary that stores the column placements.
  The keys are rows. For each row, store a tuple(value, available_values):
  (a) If a col has been assigned for that row, value is that col and available_values is frozenset({}).
  (b) If no col hsa yet been assigned for that row, value is None and the available_values are those that don't
      conflict with any of the assigned rows.
  """
  def __init__(self, board_size=8):
    self.board_size = board_size
    for row in range(board_size):
      # Initially every row is uninstantiated, and all values are available.
      self[row] = (None, frozenset(range(board_size)))
    super().__init__()
    
  def uninstantiated_rows(self):
    """ Return the uninstantiated rows. """
    return [row for row in self if self.value_for(row) is None]

  def values_available_for(self, row):
    """ Return the values available for this row. """
    return self[row][1]

  def value_for(self, row):
    """ Return the value assigned to this row. """
    return self[row][0]
  
  
##### Computations ##### 


def new_placement_val(next_row, col, r, c, avail):
  """
  If next_row gets a col value of col, what is the dictionary value for row r?
  next_row: The row being assigned a value
  col: The value being assigned to next_row
  r: some row in the current placement
  c: the current value of r
  avail: the values currently available for r
  """
  diff = abs(next_row - r)
  # If next_row == r: the tuple is (col, frozenset())
  # If r already has an assigned value. Keep it
  # If r is unassigned, keep it unassigned, but remove {col, col+diff, col-diff}) from its available_values.
  return (col, frozenset()) if next_row == r else \
         (c, avail) if c is not None else \
         (None, avail - {col, col+diff, col-diff})


# Timing and counting
limit = 0
start = 0
total_time_start = 0


def place_n_queens(board_size: int):
  """
  The main function.
  
  Generate and display solutions to the n-queens problem.
  """
  global limit, start, total_time_start
  starts = 0
  total_time_start = timer( )
  i = 0
  while True:
    i += 1
    limit = i/4
    starts += 1
    start = timer()
    placement = Placement(board_size)
    solutionNbr = 0
    for solution in place_remaining_queens(placement):
      solutionNbr += 1
      display_solution(board_size, solution, solutionNbr, start, starts, total_time_start)
      inp = input('\nMore? (y, or n)? > ').lower( )
      if inp != 'y':
        return
      starts = 1
      total_time_start = start = timer()
      i = 1


def place_remaining_queens(placement: Placement):
  """
  Find a safe spot for the next queen and either quit if it's the last unfilled row or call this recursively.
  """
  uninstantiated_rows = placement.uninstantiated_rows()
  # Select the row with the fewest available possibilities as the next_row to be instantiated.
  most_constrained_row = min( uninstantiated_rows, key=lambda row: len(placement.values_available_for(row)) )
  avail_size = len(placement.values_available_for(most_constrained_row))
  most_constrained_rows = [k for k in uninstantiated_rows if len(placement.values_available_for(k)) == avail_size]
  # Pick a random most_constrained_row as the next one to instantiate.
  next_row = choice(most_constrained_rows)
  for col in placement.values_available_for(next_row):
    # Quit and restart if we've taken too long.
    if timer( ) - start > limit:
      return
    # Build the next placement.
    next_placement = Placement(placement.board_size)
    for (r, (c, avail)) in placement.items( ):
      next_placement[r] = new_placement_val(next_row, col, r, c, avail)
    # Have we just instantiated our last column?
    # if len(uninstantiated_rows) was 1, we have just instantiated the final row.
    if len(uninstantiated_rows) == 1:
      yield next_placement

    # If some column now has no options left, fail and try the next col for next_row.
    elif frozenset() in [next_placement.values_available_for(row) for row in next_placement.uninstantiated_rows()]:
      # This must be pass rather than return. We want to continue on to the next col, not jump out of the loop.
      pass

    # More queens to place.
    else:
      # Find columns for the remaining queens.
      yield from place_remaining_queens(next_placement)
      
      
#############  Display functions  #############


def display_solution(board_size, solution, solutionNbr, start, starts, total_time_start):
  end = timer( )
  sol = sorted([(r, c) for (r, (c, _)) in solution.items( )])
  placement_vector = [c for (_, c) in sol]
  solution_display = layout(placement_vector, board_size)
  print(f'\n{solutionNbr}.\n{solution_display}')
  print(f'After {starts} start{"" if starts == 1 else "s"}, time: {round(end - start, 3)} sec '
        f'on the final run out of {round(end - total_time_start, 3)} total seconds.')


def layout(placement_vector: [int], board_size: int) -> str:
  """ Format the placement for display. """
  offset = ord('a')
  # Generate the column headers.
  col_hdrs = ' '*(4+int(log10(board_size))) + \
             '  '.join([f'{chr(n+offset)}' for n in range(board_size)]) + '  col#\n'
  display = col_hdrs + '\n'.join([one_row(r, c, board_size) for (r, c) in enumerate(placement_vector)])
  return display


def one_row(row: int, col: int, board_size: int) -> str:
  """ Generate one row of the board. """
  # (row, col) is the queen position expressed in 0-based indices.
  return f'{space_offset(row+1, board_size)}{row+1}) ' + \
         f'{" . "*col} Q {" . "*(board_size-col-1)} {space_offset(col+1, board_size)}({col+1})'


def space_offset(n, board_size):
  return " "*( int(log10(board_size) ) - int(log10(n)) )


if __name__ == "__main__":
  # The parameter to place_n_queens is the size of the board, typically 8x8.
  place_n_queens(235)
