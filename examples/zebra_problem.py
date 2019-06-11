from pylog.control_structures import forall, trace
from pylog.logic_variables import n_Vars, StructureItem, unify

from puzzles import run_puzzle
from pylog.sequence_options.super_sequence import is_contiguous_in, member, members, next_to_in

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

""" 
    =================================================================================================================
      This and the scholarship problem are both written so that they can use either LinkedLists or one of the
      PySequence options: PyList or PyTuple.
    =================================================================================================================
"""


class House(StructureItem):
  def __init__(self, nationality=None, smoke=None, pet=None, drink=None, color=None, first_arg_as_str_functor=True):
    # Package the properties together and create a StructureItem for this Student.
    super( ).__init__( (nationality, smoke, pet, drink, color), first_arg_as_str_functor)


def zebra_problem(Houses):

  for _ in forall([
    # 1. The English live in the red house.
    lambda: member(House(nationality='English', color='red'), Houses),
    # lambda: trace(f'After 1: {Houses}'),
    
    # 2. The Spanish have a dog.
    lambda: member(House(nationality='Spanish', pet='dog'), Houses),
    # lambda: trace(f'After 2: {Houses}'),
    
    # 3. They drink coffee in the green house.
    lambda: member(House(drink='coffee', color='green'), Houses),
    # lambda: trace(f'After 3: {Houses}'),
    
    # 4. The Ukrainians drink tea.
    lambda: member(House(nationality='Ukrainians', drink='tea'), Houses),
    # lambda: trace(f'After 4: {Houses}'),
    
    # 5. The green house is immediately to the right of the white house.
    lambda: is_contiguous_in([House(color='white'), House(color='green')], Houses),
    # lambda: trace(f'After 5: {Houses}'),
    
    # 6. The Old Gold smokers have snails.
    lambda: member(House(smoke='Old Gold', pet='snails'), Houses),
    # lambda: trace(f'After 6: {Houses}'),
    
    # 7. They smoke Kool in the yellow house.
    lambda: member(House(smoke='Kool', color='yellow'), Houses),
    # lambda: trace(f'After 7: {Houses}'),
    
    # 8. They drink milk in the middle house.
    # Note the use of a slice. Houses[2] picks the middle house.
    lambda: unify(House(drink='milk'), Houses[2]),
    # lambda: trace(f'After 8: {Houses}'),
    
    # 9. The Norwegians live in the first house on the left.
    lambda: unify(House(nationality='Norwegians'), Houses.head()),
    # lambda: trace(f'After 9: {Houses}'),
    
    # 10. The Chesterfield smokers live next to the fox.
    lambda: next_to_in(House(smoke='Chesterfield'), House(pet='fox'), Houses),
    # lambda: trace(f'After 10: {Houses}'),
    
    # 11. They smoke Kool in the house next to the horse.
    lambda: next_to_in(House(smoke='Kool'), House(pet='horse'), Houses),
    # lambda: trace(f'After 11: {Houses}'),
    
    # 12. The Lucky smokers drink juice.
    lambda: member(House(drink='juice', smoke='Lucky'), Houses),
    # lambda: trace(f'After 12: {Houses}'),
    
    # 13. The Japanese smoke Parliament.
    lambda: member(House(nationality='Japanese', smoke='Parliament'), Houses),
    # lambda: trace(f'After 13: {Houses}'),
    
    # 14. The Norwegians live next to the blue house.
    lambda: next_to_in(House(nationality='Norwegians'), House(color='blue'), Houses),

    lambda: trace(f'After 14: {Houses}'),

    # Fill in unmentioned properties.
    lambda: members([House(pet='zebra'), House(drink='water')], Houses),
  ]):
    yield


if __name__ == '__main__':

  """ Select either LinkedList or a PySequence (PyList or PyTuple) as the ListType. """

  from pylog.sequence_options.linked_list import LinkedList
  ListType = LinkedList

  # from sequence_options.sequences import PyList  # or PyTuple
  # ListType = PyList  # or PyTuple

  """ additional_answer function, if any """

  def additional_answer(Houses):
    (Nat1, Nat2) = n_Vars(2)
    for _ in members([House(nationality=Nat1, pet='zebra'),
                      House(nationality=Nat2, drink='water')], Houses):
      ans = f'\n\tThe {Nat1} both own a zebra and drink water.' if Nat1 == Nat2 else \
            f'\n\tThe {Nat1} own a zebra, and the {Nat2} drink water.'
      print(ans)

  """ Set up the Answer list """
  Houses = ListType([House( ) for _ in range(5)])

  """ Run problem """
  run_puzzle(ZebraProblem(Houses), ListType, additional_answer)
