from functools import reduce
from typing import Iterator, List, Tuple, Union

#from pylog.control_structures import forall
from pylog.logic_variables import PyValue, Term, unify


lines = {
  "Biwako": ["Takatsuki", "Kyoto", "Yamashina", "Otsu", "Ishiyama", "Kusatsu"],
  "Kosei": ["Kyoto", "Yamashina", "Otsukyo", "Karasaki", "Sakamoto", "Ogoto-onsen"],
  "Keihan": ["Ishiyamadera", "Zeze", "Hamaotsu", "Ano", "Sakamoto"]
}


def best_route(Start: PyValue, End: PyValue):
  """
  A Route will be: [Station, (Line, Dist), Station, (Line, Dist), ..., Station].
  Ignoring Dist, this will be the sequence of stations and lines to take from Start to End.
  The Dist components are the number of intermediate stations on the associated line.

  The best route uses the fewest lines, and of routes using the same number of lines, the fewest total Dist values.
  """
  # Look for routes that use the fewest lines.
  for i in range(1, len(lines)+1):
    # i is the number of lines used.
    # The middle sequence is the intermediate lines and stations.
    # One line involves one intermediate element, the line used.
    # Two lines involves 3 intermediate elements, the two lines used and the transfer station.
    # Etc.
    # The "+1" above allows i to take on the value len(lines), in which case we are using all the lines.
    intermediate = (PyValue() for _ in range(2*i-1))
    legs = [Start, *intermediate, End]
    # If route(*legs) succeeds, route will instantiate legs to
    #         [Station, (Line, int), Station, (Line, int), ... , Station]
    # Once legs is instantiated, must extract the py_values so that the collection
    # of routes remains instantiated after the list comprehension terminates.
    route_options = [ [elt.get_py_value() for elt in legs] for _ in route(*legs) ]
    # Once we find an i so that there is at least one route from Start to End using i lines,
    # find the best of them and quit--by using return at the bottom.
    # No point in looking for routes that use more lines.
    if route_options:
      routes_with_totals: Iterator[Tuple[List[str], int]] = map(sum_distances, route_options)
      best_option: Tuple[List[str], int] = min(routes_with_totals, key=lambda routeDist: routeDist[1])
      yield best_option
      # return prevents backtracking, i.e., looking for longer routes.
      # Has an effect similar to a cut (!) at the end of a clause in Prolog.
      # break would work as well since it jumps out of the for-loop and returns.
      return


def connected(S1: PyValue, Line_Dist: PyValue, S2: PyValue):
  # S1: Union[PyValue, Var], Line_Dist: Var, S2: Union[PyValue, Var
  """
  Are stations S1 and S2 connected on the same train line?
  If so, which line is it, and how many stations are between them?
  Line_Dist will be unified with (line, count_of_stations)
  """
  # print(f'-> connected({S1}, {Line_Dist}, {S2})?')
  Line = PyValue()
  # Can use either forall or nested for _ in has_station's
  # for _ in forall([lambda: has_station(Line, S1),
  #                  lambda: has_station(Line, S2)]):
  for _ in has_station(Line, S1):
    for _ in has_station(Line, S2):
      # Ensure that S1 != S2
      if S1 != S2:
        line = Line.get_py_value()
        stations = lines[line]
        pos1 = stations.index(S1.get_py_value())
        pos2 = stations.index(S2.get_py_value())
        yield from unify(Line_Dist, (line, abs(pos1 - pos2)))
  # print(f'XX connected({S1}, {Line_Dist}, {S2})?')


def has_station(L: PyValue, S: PyValue):
  # print(f'-> has_station({L}, {S})?')
  for line in lines:
    # If L is instantiated, find out whether it is line before looking at all the stations.
    for _ in unify(L, line):
      for station in lines[line]:
        for _ in unify(S, station):
          # print(f'<- has_station({L}, {S})')
          yield
  # print(f'XX has_station({L}, {S})')


def route(*legs: List[Term]):
  """
  Can we get from the first station to the last? If so, which lines and
  which intermediate stations should we use?
  :param legs: a sequence of: station, line, station, line, ... station.
  :return: Find a route and instantiate the intermediate PyValues.
  """
  # print(f'-> route({[str(leg) for leg in legs]})?')
  if len(legs) == 1:
    # We have arrived at our destination. succeed
    # print(f'<- route({[str(leg) for leg in legs]}?')
    yield

  # len(legs) should never be 0 or 2.
  elif len(legs) >= 3:
    # Take the next leg.
    for _ in connected(*legs[:3]):
      # Drop the first two elements, i.e., [Station, Line], and recurse.
      yield from route(*legs[2:])


def sum_distances(legs: List[Union[str, Tuple[str, int]]]) -> Tuple[List[str], int]:
  """
  For a given route of legs, sum the distances along each line.
  :param legs: Each leg is either a station or a (line, dist) tuple.
  :return: (legs, total_dist), where legs drops the internal distances along each line
  """

  def split_elts(routeDist: Tuple[List[str], int], elt: Union[str, Tuple[str, int]]) -> Tuple[List[str], int]:
    """
    This is the reduce function.

    If elt is a station, add it to the existing list of stations and lines.
    If it a (line, dist) tuple, add the line to the existing list of stations and lines and
    add the dist to the existing dist.
    """
    (route, dist) = routeDist
    assert isinstance(route, List) and isinstance(dist, int)
    new_route: List[str] = route + [elt[0] if isinstance(elt, tuple) else elt]
    new_dist = dist + elt[1] if isinstance(elt, tuple) else dist
    return (new_route, new_dist)

  # print(f'-> sum_distances({[str(leg) for leg in legs]})?')
  (new_route, total_dist) = reduce( split_elts, legs, ([], 0) )
  # print(f'<- sum_distances: {(new_route, total_dist)}')

  return (new_route, total_dist)


if __name__ == '__main__':

  def add_plural_s(nbr):
    return '' if nbr == 1 else 's'

  def print_route(stations_and_lines: List[str], stations_passed: int):
    nbr_lines = len(stations_and_lines) // 2
    for i in range(nbr_lines):
      (station, line, next_station) = stations_and_lines[2*i:2*i+3]
      print(f'\tFrom {station} take the {line} line to {next_station}.')

    transfer_stns = f', including {nbr_lines -1} transfer station{add_plural_s(nbr_lines -1)}' if nbr_lines > 1 else ''
    print(f'This route uses {nbr_lines} line{add_plural_s(nbr_lines)} and passes {stations_passed - 1} ', end='')
    print(f'intermediate station{add_plural_s(stations_passed - 1)}{transfer_stns}.')


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
    # Route = Var( )
    for Route in best_route(S1, S2):
      print(f'\nA route from {S1} to {S2} that uses fewest lines, ', end='')
      print(f'and of those the one that passes the fewest intermediate stations:')
      print_route( *Route )
