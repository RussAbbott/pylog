from pylog.logic_variables import n_Vars, StructureItem, unify

from puzzles import Problem
from pylog.sequence_options.super_sequence import is_contiguous_in, member, members, next_to, SuperSequence

"""
One version of the famous Zebra problem. (All versions are structurally similar, but the names are often different.)

                        ----------------------------------------------------------------

There are 5 houses in a row, each with a unique color. 
Each house is occupied by a family of a unique nationality. 
Each family has a pet, a favorite smoke, and a favorite drink.

1. The English live in the red house.
2. The Spanish have a dog.
3. They drink coffee in the green house.
4. The Ukrainians drink tea.
5. The green house is immediately to the right of the white house.
6. The Old Gold smokers have snails.
7. They smoke Kool in the yellow house.
8. They drink milk in the middle house.
9. The Norwegians live in the first house on the left.
10. The Chesterfield smokers live next to the fox.
11. They smoke Kool in the house next to the horse.
12. The Lucky smokers drink juice.
13. The Japanese smoke Parliament.
14. The Norwegians live next to the blue house.

Who has a zebra and who drinks water?

Houses:
  1. Norwegians(Kool, fox, water, yellow)
  2. Ukrainians(Chesterfield, horse, tea, blue)
  3. English(Old Gold, snails, milk, red)
  4. Spanish(Lucky, dog, juice, white)
  5. Japanese(Parliament, zebra, coffee, green)
  
  The Japanese own a zebra, and the Norwegians drink water.

 
    =================================================================================================================
      This and the scholarship problem are both written so that they can use either LinkedLists or one of the
      PySequence options: PyList or PyTuple. Make a choice at the bottom of the file.
    =================================================================================================================
"""


class House(StructureItem):
  def __init__(self, nationality=None, smoke=None, pet=None, drink=None, color=None, first_arg_as_str_functor=True):
    # Package the properties together and create a StructureItem for this Student.
    super( ).__init__( (nationality, smoke, pet, drink, color), first_arg_as_str_functor)


# noinspection PyMethodMayBeStatic
class ZebraProblem(Problem):

  def additional_answer(self, Houses: SuperSequence):
    (Nat1, Nat2) = n_Vars(2)
    for _ in members([House(nationality=Nat1, pet='zebra'),
                      House(nationality=Nat2, drink='water')], Houses):
      ans = f'\n\tThe {Nat1} both own a zebra and drink water.' if Nat1 == Nat2 else \
            f'\n\tThe {Nat1} own a zebra, and the {Nat2} drink water.'
      print(ans)

  def clue_0(self, _: SuperSequence):
    """
    Problem setup.
      There are 5 houses in a row, each with a unique color: blue, green, red, white, yellow.
      Each house is occupied by a family of a unique nationality: English, Japanese, Norwegians, Spanish, Ukrainians.
      Each family has:
        a pet: dog, fox, horse, snails, zebra,
        a favorite smoke: Chesterfield, Kool, Lucky, Old Gold, Parliament, and
        a favorite drink: coffee, juice, milk, tea, water.
    """
    Houses = self.ListType([House( ) for _ in range(5)])
    self.Items = Houses

    # Check all attributes for distinctness
    self.check_all_for_distinctness(House)

    # self.clues at the Problem level is [self.clue_0]. That ensures that this setup clue will run.
    # We append the actual clues so that the clues will be in their correct list index positions,
    # i.e., clue_i at self.clues[i].
    self.clues += [self.clue_1, self.clue_2, self.clue_3, self.clue_4, self.clue_5,
                   self.clue_6, self.clue_7, self.clue_8, self.clue_9, self.clue_10,
                   self.clue_11, self.clue_12, self.clue_13, self.clue_14, self.clue_15]

    # Show trace only after all clues have succeeded -- and we just need to fill in empty spaces.
    self.show_trace_list = [14]
    yield

  def clue_1(self, Houses: SuperSequence):
    """ 1. The English live in the red house.  """
    yield from member(House(nationality='English', color='red'), Houses)

  def clue_2(self, Houses: SuperSequence):
    """ 2. The Spanish have a dog. """
    yield from member(House(nationality='Spanish', pet='dog'), Houses)

  def clue_3(self, Houses: SuperSequence):
    """ 3. They drink coffee in the green house. """
    yield from member(House(drink='coffee', color='green'), Houses)

  def clue_4(self, Houses: SuperSequence):
    """ 4. The Ukrainians drink tea. """
    yield from member(House(nationality='Ukrainians', drink='tea'), Houses)

  def clue_5(self, Houses: SuperSequence):
    """ 5. The green house is immediately to the right of the white house. """
    yield from is_contiguous_in([House(color='white'), House(color='green')], Houses)

  def clue_6(self, Houses: SuperSequence):
    """ 6. The Old Gold smokers have snails. """
    yield from member(House(smoke='Old Gold', pet='snails'), Houses)

  def clue_7(self, Houses: SuperSequence):
    """ 7. They smoke Kool in the yellow house. """
    yield from member(House(smoke='Kool', color='yellow'), Houses)

  def clue_8(self, Houses: SuperSequence):
    """ 8. They drink milk in the middle house.
        Note the use of a slice. Houses[2] picks the middle house. """
    yield from unify(House(drink='milk'), Houses[2])

  def clue_9(self, Houses: SuperSequence):
    """ 9. The Norwegians live in the first house on the left.
        Instead of Houses.head(), could have written Houses[0]. """
    yield from unify(House(nationality='Norwegians'), Houses.head())

  def clue_10(self, Houses: SuperSequence):
    """ 10. The Chesterfield smokers live next to the fox.
        Saying 'next to' doesn't commit to the right or left. """
    yield from next_to(House(smoke='Chesterfield'), House(pet='fox'), Houses)

  def clue_11(self, Houses: SuperSequence):
    """ 11. They smoke Kool in the house next to the horse. """
    yield from next_to(House(smoke='Kool'), House(pet='horse'), Houses)

  def clue_12(self, Houses: SuperSequence):
    """ 12. The Lucky smokers drink juice. """
    yield from member(House(drink='juice', smoke='Lucky'), Houses)

  def clue_13(self, Houses: SuperSequence):
    """ 13. The Japanese smoke Parliament. """
    yield from member(House(nationality='Japanese', smoke='Parliament'), Houses)

  def clue_14(self, Houses: SuperSequence):
    """ 14. The Norwegians live next to the blue house. """
    yield from next_to(House(nationality='Norwegians'), House(color='blue'), Houses)

  def clue_15(self, Houses: SuperSequence):
    """ 15 (implicit) Fill in unmentioned properties. """
    yield from members([House(pet='zebra'), House(drink='water')], Houses)


if __name__ == '__main__':

  """ Select either LinkedList or a PySequence (PyList or PyTuple) as the ListType. """

  # from pylog.sequence_options.linked_list import LinkedList
  # ListType = LinkedList
  #
  from pylog.sequence_options.sequences import PyList  # or PyTuple
  ListType = PyList  # or PyTuple

  """ Run problem """
  ZebraProblem()(ListType)
