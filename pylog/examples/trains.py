from functools import reduce
from typing import List, Tuple, Union

from control_structures import forall
from logic_variables import Container, Ground, n_Vars, Term, unify, unify_pairs, Var

from sequence_options.sequences import PyTuple


lines = {
  "Biwako": ["Takatsuki", "Kyoto", "Yamashina", "Otsu", "Ishiyama", "Kusatsu"],
  "Kosei": ["Kyoto", "Yamashina", "Otsukyo", "Karasaki", "Sakamoto", "Ogoto-onsen"],
  "Keihan": ["Ishiyamadera", "Zeze", "Hamaotsu", "Ano", "Sakamoto"]
}


def best_route(Start: Union[Ground, Var], Route: Container, End: Union[Ground, Var]):
  """
  The best route is defined to be the one that passes the fewest intermediate stations.
  """
  for i in range(len(lines)):
    legs = [Start, *n_Vars(2*i+1), End]
    # If it succeeds, chain will instantiate legs to
    #         [Station, (Line, int), Station, (Line, int), ... , Station]
    # Once legs is instantiated, must take the ground values so that the
    # collection of legs can be processed in the next step.
    # If the ground values aren't taken, the legs variables will lose
    # their values when backtracking through chain.
    route_options = [[elt.get_ground_value() for elt in legs] for _ in chain(*legs)]
    # Once we find at least one chain from Start to End, find the best of them and quit.
    if route_options:
      routes_with_totals = map(sum_distances, route_options)
      best_option = min(routes_with_totals, key=lambda optDist: optDist[1])
      Route.set_contents(best_option)
      yield
      # break or return prevents backtracking, i.e., jumps out of the for-loop
      break
      # return


def chain(*legs: List[Term]):
  """
  Can we get from the first station to the last? If so, which lines and
  which intermediate stations should we use?
  :param legs: a sequence of: station, line, station, line, ... station.
         All but the first and last may be variables.
  :return:
  """
  if len(legs) == 0 or len(legs) == 2:
    # fail
    pass
  elif len(legs) == 1:  # Have arrived at our destination
    # succeed
    yield
  else:  # len(legs) >= 3. Take the next leg.
    for _ in connected(*legs[:3]):
      # Drop the first two elements, i.e., [Station, Line], and recurse.
      yield from chain(*legs[2:])


def connected(S1: Union[Ground, Var], Line_Dist: Union[Var, PyTuple], S2: Union[Ground, Var]):
  """
  Are stations S1 and S2 connected on the same train line?
  If so, which line is it, and how many stations are between them?
  Line_Dist will be unified with (Line, count_of_stations)
  """
  # print(f'-> connected({A}, {LD}, {B})?')
  if S1 != S2:
    Line = Var()
    for _ in forall([lambda: has_station(Line, S1),
                     lambda: has_station(Line, S2)]):
      # Test again since A or B may have started as Var's
      if S1 != S2:
        stations = lines[Line.get_ground_value()]
        pos1 = stations.index(S1.get_ground_value())
        pos2 = stations.index(S2.get_ground_value())
        for _ in unify(Line_Dist, PyTuple((Line, Ground(abs(pos1 - pos2))))):
          # print(f'<- connected({A}, {Line_Dist}, {B})?')
          yield
  # print(f'XX connected({A}, {LD}, {B})?')


def has_station(L: Union[Ground, Var], S: Union[Ground, Var]):
  # print(f'-> has_station({L}, {S})?')
  for line in lines:
    for station in lines[line]:
      for _ in unify_pairs([(L, Ground(line)),
                            (S, Ground(station))]):
        # print(f'<- has_station({L}, {S})')
        yield
  # print(f'XX has_station({L}, {S})')


def sum_distances(legs: [Union[str, Tuple[str, int]]]) -> ([str], int):
  """
  For a given chain of legs, sum the distances along each line.
  :param legs: Each leg is either a station or a (line, dist) tuple.
  :return: (legs, total_dist), where legs drops the internal distances along each line
  """

  def split_elts(chnDist, elt):
    """
    This is the reduce function.

    If elt is a station, add it to the existing list of stations and lines.
    If it a (line, dist) tuple, add the line to the existing list of stations and lines and
    add the dist to the existing dist.
    """
    (chn, dist) = chnDist
    new_chn = chn + [(elt[0] if isinstance(elt, tuple) else elt)]
    new_dist = dist + (elt[1] if isinstance(elt, tuple) else 0)
    return (new_chn, new_dist)

  (new_chain, total_dist) = reduce( split_elts, legs, ([], 0) )
  return (new_chain, total_dist)


if __name__ == '__main__':

  def print_route(stations_and_lines, stations_passed):
    for i in range(len(stations_and_lines) // 2):
      (station, line, next_station) = stations_and_lines[2 * i:2 * i + 3]
      print(f'\tFrom {station} take the {line} line to {next_station}.')
    print(f'  Including transfer stations, if any, you will pass {stations_passed - 1} intermediate stations')


  for (_A, _B) in [("Takatsuki", "Yamashina"),  # Direct
                   ("Takatsuki", "Kyoto"),      # Direct
                   ("Yamashina", "Sakamoto"),   # Direct
                   ("Yamashina", "Ishiyama"),   # Direct
                   ("Otsukyo", "Sakamoto"),     # Direct

                   ("Otsukyo", "Hamaotsu"),     # One-change
                   ("Otsukyo", "Ano"),          # One-change
                   ("Takatsuki", "Otsukyo"),    # One-change
                   ("Yamashina", "Ano"),        # One-change

                   ("Takatsuki", "Ano"),        # Two-changes
                   ("Hamaotsu", "Otsu"),        # Two-changes
                   ("Zeze", "Takatsuki"),       # Two-changes
                   ("Zeze", "Kusatsu"),         # Two-changes
                   ]:

    (A, B) = (Ground(_A), Ground(_B))
    Route = Container( )

    # Use Route as a container to pass back the route.
    # (Yielding it would be equivalent but not in keeping with the Prolog-style of the example.)
    for _ in best_route(A, Route, B):
      print(f'\nFind a best route (passing the fewest intermediate stations) from {A} to {B}: ')
      print_route( *Route.get_contents() )
