from control_structures import forall, print_sf
from logic_variables import n_Vars, unify

from examples.puzzles import Puzzle_Item, run_puzzle

""" 
    =================================================================================================================
      This and the scholarship problem are both written so that they can use either LinkedLists or one of the
      PySequence options: PyList or PyTuple.
    =================================================================================================================
"""

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

Solution:

  1. Norwegians(Kool, fox, water, yellow)
  2. Ukrainians(Chesterfield, horse, tea, blue)
  3. English(Old Gold, snails, milk, red)
  4. Spanish(Lucky, dog, juice, white)
  5. Japanese(Parliament, zebra, coffee, green)
  
  The Japanese own a zebra, and the Norwegians drink water.

"""


class House(Puzzle_Item):
  def __init__(self, nationality=None, smoke=None, pet=None, drink=None, color=None):
    functor = type(self).__name__.lower()
    nationality = self.make_property(nationality)
    smoke = self.make_property(smoke)
    pet = self.make_property(pet)
    drink = self.make_property(drink)
    color = self.make_property(color)
    super( ).__init__( (functor, nationality, smoke, pet, drink, color) )


def zebra_problem(Houses):

  for _ in forall([
    # 1. The English live in the red house.
    lambda: Houses.has_member(House(nationality='English', color='red')),
    # lambda: print_sf(f'After 1: {Houses}', 'Succeed'),
    
    # 2. The Spanish have a dog.
    lambda: Houses.has_member(House(nationality='Spanish', pet='dog')),
    # lambda: print_sf(f'After 2: {Houses}', 'Succeed'),
    
    # 3. They drink coffee in the green house.
    lambda: Houses.has_member(House(drink='coffee', color='green')),
    # lambda: print_sf(f'After 3: {Houses}', 'Succeed'),
    
    # 4. The Ukrainians drink tea.
    lambda: Houses.has_member(House(nationality='Ukrainians', drink='tea')),
    # lambda: print_sf(f'After 4: {Houses}', 'Succeed'),
    
    # 5. The green house is immediately to the right of the white house.
    lambda: Houses.has_contiguous_sublist([House(color='white'), House(color='green')]),
    # lambda: print_sf(f'After 5: {Houses}', 'Succeed'),
    
    # 6. The Old Gold smokers have snails.
    lambda: Houses.has_member(House(smoke='Old Gold', pet='snails')),
    # lambda: print_sf(f'After 6: {Houses}', 'Succeed'),
    
    # 7. They smoke Kool in the yellow house.
    lambda: Houses.has_member(House(smoke='Kool', color='yellow')),
    # lambda: print_sf(f'After 7: {Houses}', 'Succeed'),
    
    # 8. They drink milk in the middle house.
    # Note the use of a slice. Houses[2] picks the middle house.
    lambda: unify(House(drink='milk'), Houses[2]),
    # lambda: print_sf(f'After 8: {Houses}', 'Succeed'),
    
    # 9. The Norwegians live in the first house on the left.
    lambda: unify(House(nationality='Norwegians'), Houses.head()),
    # lambda: print_sf(f'After 9: {Houses}', 'Succeed'),
    
    # 10. The Chesterfield smokers live next to the fox.
    lambda: Houses.has_adjacent_members(House(smoke='Chesterfield'), House(pet='fox')),
    # lambda: print_sf(f'After 10: {Houses}', 'Succeed'),
    
    # 11. They smoke Kool in the house next to the horse.
    lambda: Houses.has_adjacent_members(House(smoke='Kool'), House(pet='horse')),
    # lambda: print_sf(f'After 11: {Houses}', 'Succeed'),
    
    # 12. The Lucky smokers drink juice.
    lambda: Houses.has_member(House(drink='juice', smoke='Lucky')),
    # lambda: print_sf(f'After 12: {Houses}', 'Succeed'),
    
    # 13. The Japanese smoke Parliament.
    lambda: Houses.has_member(House(nationality='Japanese', smoke='Parliament')),
    # lambda: print_sf(f'After 13: {Houses}', 'Succeed'),
    
    # 14. The Norwegians live next to the blue house.
    lambda: Houses.has_adjacent_members(House(nationality='Norwegians'), House(color='blue')),

    lambda: print_sf(f'After 14: {Houses}', 'Succeed'),

    # Fill in unmentioned properties.
    lambda: Houses.has_members([House(pet='zebra'), House(drink='water')]),
  ]):
    yield


if __name__ == '__main__':

  """ Select either LinkedList or a PySequence (PyList or PyTuple) as the ListType. """

  # from sequence_options.linked_list import LinkedList
  # ListType = LinkedList
  #
  from sequence_options.sequences import PyList  # or PyTuple
  ListType = PyList  # or PyTuple

  """ additional_answer function, if any """

  def additional_answer(Houses):
    (Nat1, Nat2) = n_Vars(2)
    for _ in Houses.has_members([House(nationality=Nat1, pet='zebra'),
                                 House(nationality=Nat2, drink='water')]):
      ans = f'\n\tThe {Nat1} both own a zebra and drink water.' if Nat1 == Nat2 else \
            f'\n\tThe {Nat1} own a zebra, and the {Nat2} drink water.'
      print(ans)

  """ Set up the Answer list """
  Houses = ListType([House( ) for _ in range(5)])

  """ Run problem """
  run_puzzle(zebra_problem, ListType, Houses, additional_answer)
