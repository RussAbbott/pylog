from __future__ import annotations
from typing import List, Union

from control_structures import forany, forall
from logic_variables import eot, Structure, unify, Term


class SuperSequence(Structure):
  """
  A subclass of Structure that can serve as a superclass for both PySequence and LinkedList
  Declares a number of abstract methods.
  """

  def __getitem__(self, key: Union[int, slice]) -> Union[SuperSequence, Term]:
      pass

  def __len__(self):
    pass

  # def has_adjacent_members(self, E1, E2):
  #   pass
  #
  def has_contiguous_sublist(self, As):
    pass

  def has_member(self, E: Term):
    pass

  # def has_members(self, Es: List[Term]):
  #   pass
  #
  def head(self) -> Term:
    pass

  def tail(self) -> SuperSequence:
    pass


@eot
def is_contiguous_in(As: List, Zs: SuperSequence):
  """ Can As be unified with a segment of Zs? """
  yield from Zs.has_contiguous_sublist(As)


@eot
def is_a_subsequence_of(As: List, Zs: SuperSequence):
  """
  As may be spread out in Zs but must be in the same order as in Zs.
  """
  if not As:
    # If no more As to match, we're done. Succeed.
    yield

  elif not Zs:
    # If no more Zs to match the remaining As, fail.
    pass

  else:
    for _ in forany([
                     # Match As[0] and Zs[0]; go on to is_a_subsequence_of(As[1:], Zs[1:])
                     lambda: forall([lambda: unify(As[0], Zs[0]),
                                     lambda: is_a_subsequence_of(As[1:], Zs[1:])]),
                     # Whether or not we matched As[0] and Zs[0] above,
                     # try is_a_subsequence_of(As, Zs[1:]), either to match the rest of the As or as an alternative.
                     lambda: is_a_subsequence_of(As, Zs[1:])
                     ]):
      yield


@eot
def member(E: Term, A_List: SuperSequence):
  """ Is E in A_List? """
  yield from A_List.has_member(E)


@eot
def members(Es: List, A_List: SuperSequence):
  """ Do all elements of es appear in A_List (in any order). """
  # yield from A_List.has_members(Es)
  # No more to look up. We're done.
  if not Es:
    yield
  else:
    for _ in member(Es[0], A_List):
      yield from members(Es[1:], A_List)


def next_to_in(E1: Term, E2: Term, Es: SuperSequence):
  """ Are E1 and E2 are next to each other in Es. """
  # yield from Es.has_adjacent_members(E1, E2)
  for _ in forany([
                   lambda: is_contiguous_in([E1, E2], Es),
                   lambda: is_contiguous_in([E2, E1], Es),
                   ]):
    yield
