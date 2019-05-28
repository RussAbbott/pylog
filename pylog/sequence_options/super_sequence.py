from __future__ import annotations
from typing import List, Union

from control_structures import forany, forall
from logic_variables import Structure, unify, Term


class SuperSequence(Structure):
  """
  A subclass of Structure that can serve as a superclass for both PySequence and LinkedList
  Declares a number of abstract methods.
  """

  def __getitem__(self, key: Union[int, slice]) -> Union[SuperSequence, Term]:
      pass

  def __len__(self):
    pass

  def head(self) -> Term:
    pass

  def tail(self) -> SuperSequence:
    pass


def is_subsequence(As: List, Zs: SuperSequence):
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
                     # Match As[0] and Zs[0]; go on to is_subsequence(As[1:], Zs[1:])
                     lambda: forall([lambda: unify(As[0], Zs[0]),
                                     lambda: is_subsequence(As[1:], Zs[1:])]),
                     # Whether or not we matched As[0] and Zs[0] above,
                     # try is_subsequence(As, Zs[1:]), either to match the rest of the As or as an alternative.
                     lambda: is_subsequence(As, Zs[1:])
                     ]):
      yield
