from functools import reduce
from typing import List, Tuple, Union

from control_structures import forall
from logic_variables import PyValue, n_Vars, Term, unify, unify_pairs, Var

from sequence_options.sequences import PyTuple


lines = {
  "Biwako": ["Takatsuki", "Kyoto", "Yamashina", "Otsu", "Ishiyama", "Kusatsu"],
  "Kosei": ["Kyoto", "Yamashina", "Otsukyo", "Karasaki", "Sakamoto", "Ogoto-onsen"],
  "Keihan": ["Ishiyamadera", "Zeze", "Hamaotsu", "Ano", "Sakamoto"]
}


def best_route(Start: PyValue, Route: Var, End: PyValue):
  """
  A Route will be: [Station, (Line, Dist), Station, (Line, Dist), ..., Station].
  Ignoring Dist, this will be the sequence of stations and lines to take from Start to End.
  The Dist components are the number of intermediate stations on the associated line.

  The best route uses the fewest lines, and of routes using the same number of lines, the fewest total Dist values.
  """
  # Look for routes that use the fewest lines.
  for i in range(len(lines)):
    # The middle sequence is the intermediate lines and stations.
    legs = (Start, *n_Vars(2*i+1), End)
    # If route(*legs) succeeds, route will instantiate legs to
    #         [Station, (Line, int), Station, (Line, int), ... , Station]
    # Once legs is instantiated, must take the py_values so that the collection
    # of routes remains instantiated after the list comprehension terminates.
    route_options = [ [elt.get_py_value() for elt in legs] for _ in route(*legs) ]
    # Once we find at least one route from Start to End, find the best of them and quit.
    if route_options:
      routes_with_totals = map(sum_distances, route_options)
      best_option = min(routes_with_totals, key=lambda routeDist: routeDist[1])
      # best_option will be a simple list. Make it a PyValue object so that it can be unified with Route.
      yield from unify(Route, PyValue(best_option))
      # break or return prevents backtracking, i.e., looking for alternative (and possibly longer) routes.
      # Has an effect similar to a cut (!) in Prolog.
      break
      # return


def connected(S1: Union[PyValue, Var], Line_Dist: Union[Var, PyTuple], S2: Union[PyValue, Var]):
  """
  Are stations S1 and S2 connected on the same train line?
  If so, which line is it, and how many stations are between them?
  Line_Dist will be unified with (Line, count_of_stations)
  """
  # print(f'-> connected({S1}, {Line_Dist}, {S2})?')
  if S1 != S2:
    Line = Var()
    for _ in forall([lambda: has_station(Line, S1),
                     lambda: has_station(Line, S2)]):
      # Test again since S1 or S2 may have started as Var's
      if S1 != S2:
        stations = lines[Line.get_py_value()]
        pos1 = stations.index(S1.get_py_value())
        pos2 = stations.index(S2.get_py_value())
        yield from unify(Line_Dist, PyTuple( (Line, PyValue(abs(pos1 - pos2))) ) )
  # print(f'XX connected({S1}, {Line_Dist}, {S2})?')


def has_station(L: Union[PyValue, Var], S: Union[PyValue, Var]):
  # print(f'-> has_station({L}, {S})?')
  for line in lines:
    for station in lines[line]:
      for _ in unify_pairs([(L, PyValue(line)),
                            (S, PyValue(station))]):
        # print(f'<- has_station({L}, {S})')
        yield
  # print(f'XX has_station({L}, {S})')


def route(*legs: Tuple[Term]):
  """
  Can we get from the first station to the last? If so, which lines and
  which intermediate stations should we use?
  :param legs: a sequence of: station, line, station, line, ... station.
         All but the first and last may be variables.
  :return:
  """
  # print(f'-> route({[str(leg) for leg in legs]})?')
  if len(legs) == 0 or len(legs) == 2:
    # fail
    # print(f'XX route({[str(leg) for leg in legs]}?')
    pass
  elif len(legs) == 1:  # Have arrived at our destination
    # succeed
    # print(f'<- route({[str(leg) for leg in legs]}?')
    yield
  else:  # len(legs) >= 3. Take the next leg.
    for _ in connected(*legs[:3]):
      # Drop the first two elements, i.e., [Station, Line], and recurse.
      # for _ in route(*legs[2:]):
        # print(f'<- route({[str(leg) for leg in legs]}?')
        # yield
      yield from route(*legs[2:])


def sum_distances(legs: [Union[str, Tuple[str, int]]]) -> ([str], int):
  """
  For a given route of legs, sum the distances along each line.
  :param legs: Each leg is either a station or a (line, dist) tuple.
  :return: (legs, total_dist), where legs drops the internal distances along each line
  """

  def split_elts(routeDist: Tuple[tuple, int], elt: Union[str, Tuple[str, int]]) -> Tuple[tuple, int]:
    """
    This is the reduce function.

    If elt is a station, add it to the existing list of stations and lines.
    If it a (line, dist) tuple, add the line to the existing list of stations and lines and
    add the dist to the existing dist.
    """
    (route, dist) = routeDist
    new_route = route + ( (elt[0] if isinstance(elt, tuple) else elt), )
    new_dist = dist + elt[1] if isinstance(elt, tuple) else dist
    return (new_route, new_dist)

  # print(f'-> sum_distances({[str(leg) for leg in legs]})?')
  (new_route, total_dist) = reduce( split_elts, legs, ((), 0) )
  # print(f'<- sum_distances: {(new_route, total_dist)}')

  return (new_route, total_dist)


if __name__ == '__main__':

  def s(nbr):
    return '' if nbr == 1 else 's'

  def print_route(stations_and_lines: List[str], stations_passed: int):
    nbr_lines = len(stations_and_lines) // 2
    for i in range(nbr_lines):
      (station, line, next_station) = stations_and_lines[2*i:2*i+3]
      print(f'\tFrom {station} take the {line} line to {next_station}.')

    transfer_stns_insert = f', including {nbr_lines -1} transfer station{s(nbr_lines -1)}' if nbr_lines > 1 else ''
    print(f'This route uses {nbr_lines} line{s(nbr_lines)} and ', end='')
    print(f'passes {stations_passed - 1} intermediate station{s(stations_passed - 1)}{transfer_stns_insert}.')


  for (s1, s2) in [("Takatsuki", "Yamashina"),  # Direct
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

    (S1, S2) = (PyValue(s1), PyValue(s2))
    # Use Route in Prolog style to pass back the route.
    # In this case it's simply a basket in which the best route is conveyed.
    Route = Var( )
    for _ in best_route(S1, Route, S2):
      print(f'\nA route from {S1} to {S2} that uses fewest lines ', end='')
      print(f'and of those that passes fewest intermediate stations:')
      print_route( *Route.trail_end().get_py_value() )
