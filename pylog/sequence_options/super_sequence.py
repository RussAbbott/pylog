from __future__ import annotations
from typing import List, Union

from control_structures import forany, forall
from logic_variables import euc, Structure, unify, Term, Var


class SuperSequence(Structure):
  """
  A subclass of Structure that can serve as a superclass for both PySequence and LinkedList
  Declares a number of abstract methods.
  """

  def __getitem__(self, key: Union[int, slice]) -> Union[SuperSequence, Term]:
      pass

  def __len__(self):
    pass

  def has_contiguous_sublist(self, As):
    pass

  def head(self) -> Term:
    pass

  def is_empty(self) -> bool:
    # An empty list has no args, i.e., no head or tail.
    # A linked list with a variable tail will also have a head, which itself may be a Var.
    # There is no way to represent a LinkedList is nothing but a variable tail. It is just a simple Var.
    return not self.args

  def to_python_list(self) -> list:
    return []

  def tail(self) -> SuperSequence:
    pass


@euc
def is_contiguous_in(As: List, Zs: SuperSequence):
  """ Can As be unified with a segment of Zs? """
  yield from Zs.has_contiguous_sublist(As)


@euc
def is_a_subsequence_of(As: List, Zs: SuperSequence):
  """
  As may be spread out in Zs but must be in the same order as in Zs.
  """
  if not As:
    # If no more As to match, we're done. Succeed.
    yield

  elif not Zs:
    # If no more Zs to match the remaining As, fail.
    return

  else:
    for _ in forany([
                     # Match As[0] and Zs[0]; go on to is_a_subsequence_of(As[1:], Zs[1:])
                     lambda: forall([lambda: unify(As[0], Zs[0]),
                                     lambda: is_a_subsequence_of(As[1:], Zs[1:])]),
                     # Whether or not we matched As[0] and Zs[0] above, try is_a_subsequence_of(As, Zs[1:])
                     lambda: is_a_subsequence_of(As, Zs[1:])
                     ]):
      yield


@euc
def member(E: Term, A_List: Union[List, SuperSequence, Var]):
  """
  Is E in A_List?
  """
  # if isinstance(A_List, list):
  #   yield from member_python_list(E, A_List)
  #
  # # If A_List is empty, it can't have a member. So fail.
  if A_List.is_empty():
    return

  # The following is an implicit 'or'. Either unify E with A_List.head() or call member(E, A_List.tail()).

  # The first case is easy.
  # for _ in unify(E, A_List.head( )):
  #   yield
  yield from unify(E, A_List.head( ))

  # The second case--member(E, A_List.tail())--is trickier.
  # Since A_List may be an open-ended LinkedList, A_List.tail() may be a Var.
  # In that case, we must first instantiate A_List.tail() to LinkedList( (Var, Var) ).
  A_List_Tail = A_List.tail()
  # Create A_List_New_Tail to be unified with A_List_Tail.
  # A_List_New_Tail will be A_List_Tail in most cases.
  # But if isinstance(A_List_Tail, Var), make A_List_New_Tail = LinkedList( (Var( ), Var( )) ).
  # In either case, unify A_List_Tail with A_List_New_Tail and call member(E, A_List_New_Tail).
  # An issue is that we can't import LinkedList since that would create an import cycle.
  # Instead use type(A_List), which will be LinkedList if A_List_Tail is a Var.
  A_List_New_Tail = type(A_List)((Var( ), Var( ))) if isinstance(A_List_Tail, Var) else A_List_Tail
  # If A_List_New_Tail is A_List_Tail, this unify does nothing.
  for _ in unify(A_List_New_Tail, A_List_Tail):
    yield from member(E, A_List_New_Tail)


@euc
def members(Es: List, A_List: SuperSequence):
  """ Do all elements of es appear in A_List (in any order). """
  # No more to look up. We're done.
  if not Es:
    yield
  else:
    for _ in member(Es[0], A_List):
      yield from members(Es[1:], A_List)


def next_to(E1: Term, E2: Term, Es: SuperSequence):
  """ Are E1 and E2 are next to each other in Es. """
  for _ in forany([
                   lambda: is_contiguous_in([E1, E2], Es),
                   lambda: is_contiguous_in([E2, E1], Es),
                   ]):
    yield


def reversed(A_List: SuperSequence) -> SuperSequence:
  A_List_to_python_list = A_List.to_python_list()
  reversed_A_List = A_List_to_python_list[::-1]
  return type(A_List)(reversed_A_List)