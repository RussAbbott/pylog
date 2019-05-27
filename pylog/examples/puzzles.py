from logic_variables import Ground, Structure, Term, Var

"""
A utility superclass for logic puzzles.
"""


class Puzzle(Structure):

  def __str__(self):
    """
    A default way to print out a structure. Use the first arg as the term name.
    """
    allArgs = all(isinstance(arg.trail_end(), Var) for arg in self.args)
    if allArgs:
      # If all the args are uninstantiated, print a simple underscore.
      return '_'
    else:
      argsStr = ', '.join(map(str, self.args[1:]))
      result = f'{self.args[0]}({argsStr})'
      return result

  @staticmethod
  def make_property(prop):
    """
    Used for creating terms. This is applied to each argument. It
    applies Ground to those that are not already Terms.
    If the property is None, create a Var for it.
    """
    return Var() if prop is None else \
                    prop if isinstance(prop, Term) else \
                    Ground(prop)
