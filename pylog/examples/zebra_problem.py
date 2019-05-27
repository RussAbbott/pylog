from control_structures import forall, print_SF
from logic_variables import n_vars, unify

from examples.puzzles import Puzzle

""" 
    =================================================================================================================
      This and the scholarship problem are both written so that they can use either LinkedLists or one of the
      PySequence options: PyList or PyTuple.
      
      The list functions are written as static methods. It would have been better had that not been necessary.
      The problem is that LinkedLists may have variable tails, which means that when one takes the tail of such
      a list, one is left with a Var rather than a LinkedList object.  And Var's do not have these methods defined.
    =================================================================================================================
"""

"""
One version of the famous Zebra problem. (All versions are all structurally similar, but the names are often different.)

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


class House(Puzzle):
  def __init__(self, nationality=None, smoke=None, pet=None, drink=None, color=None):
    functor = type(self).__name__.lower()
    nationality = self.make_property(nationality)
    smoke = self.make_property(smoke)
    pet = self.make_property(pet)
    drink = self.make_property(drink)
    color = self.make_property(color)
    super( ).__init__( (functor, nationality, smoke, pet, drink, color) )


def zebra_problem(Houses, ListType):

  for _ in forall([
    # 1. The English live in the red house.
    lambda: ListType.member(House(nationality='English', color='red'), Houses),
    # lambda: print_SF(f'After 1: {Houses}', 'Succeed'),
    
    # 2. The Spanish have a dog.
    lambda: ListType.member(House(nationality='Spanish', pet='dog'), Houses),
    # lambda: print_SF(f'After 2: {Houses}', 'Succeed'),
    
    # 3. They drink coffee in the green house.
    lambda: ListType.member(House(drink='coffee', color='green'), Houses),
    # lambda: print_SF(f'After 3: {Houses}', 'Succeed'),
    
    # 4. The Ukrainians drink tea.
    lambda: ListType.member(House(nationality='Ukrainians', drink='tea'), Houses),
    # lambda: print_SF(f'After 4: {Houses}', 'Succeed'),
    
    # 5. The green house is immediately to the right of the white house.
    lambda: ListType.is_contiguous_in([House(color='white'), House(color='green')], Houses),
    # lambda: print_SF(f'After 5: {Houses}', 'Succeed'),
    
    # 6. The Old Gold smokers have snails.
    lambda: ListType.member(House(smoke='Old Gold', pet='snails'), Houses),
    # lambda: print_SF(f'After 6: {Houses}', 'Succeed'),
    
    # 7. They smoke Kool in the yellow house.
    lambda: ListType.member(House(smoke='Kool', color='yellow'), Houses),
    # lambda: print_SF(f'After 7: {Houses}', 'Succeed'),
    
    # 8. They drink milk in the middle house.
    # Note the use of a slice. Houses[2] picks the middle house.
    lambda: unify(House(drink='milk'), Houses[2]),
    # lambda: print_SF(f'After 8: {Houses}', 'Succeed'),
    
    # 9. The Norwegians live in the first house on the left.
    lambda: unify(House(nationality='Norwegians'), Houses.head()),
    # lambda: print_SF(f'After 9: {Houses}', 'Succeed'),
    
    # 10. The Chesterfield smokers live next to the fox.
    lambda: ListType.next_to(House(smoke='Chesterfield'), House(pet='fox'), Houses),
    # lambda: print_SF(f'After 10: {Houses}', 'Succeed'),
    
    # 11. They smoke Kool in the house next to the horse.
    lambda: ListType.next_to(House(smoke='Kool'), House(pet='horse'), Houses),
    # lambda: print_SF(f'After 11: {Houses}', 'Succeed'),
    
    # 12. The Lucky smokers drink juice.
    lambda: ListType.member(House(drink='juice', smoke='Lucky'), Houses),
    # lambda: print_SF(f'After 12: {Houses}', 'Succeed'),
    
    # 13. The Japanese smoke Parliament.
    lambda: ListType.member(House(nationality='Japanese', smoke='Parliament'), Houses),
    # lambda: print_SF(f'After 13: {Houses}', 'Succeed'),
    
    # 14. The Norwegians live next to the blue house.
    lambda: ListType.next_to(House(nationality='Norwegians'), House(color='blue'), Houses),
    lambda: print_SF(f'After 14: {Houses}', 'Succeed'),

    # Fill in unmentioned properties.
    lambda: ListType.members([House(pet='zebra'), House(drink='water')], Houses),
  ]):
    yield


if __name__ == '__main__':

  def run_zebra_problem(ListType):
    inp = None
    from timeit import default_timer as timer
    (start1, end1, start2, end2) = (timer( ), None, None, None)
    Houses = ListType([House( ) for _ in range(5)])
    for _ in zebra_problem(Houses, ListType):
      print('\nSolution: ')
      for (index, house) in enumerate(Houses.to_python_list()):
        print(f'\t{index + 1}. {house}')
      (Nat1, Nat2) = n_vars(2)
      for _ in ListType.members([House(nationality=Nat1, pet='zebra'),
                                 House(nationality=Nat2, drink='water')], Houses):
        ans = f'\n\tThe {Nat1} both own a zebra and drink water.' if Nat1 == Nat2 else \
              f'\n\tThe {Nat1} own a zebra, and the {Nat2} drink water.'
        end1 = timer( )
        print(ans)
      inp = input('\nMore? (y, or n)? > ').lower( )
      start2 = timer( )
      if inp != 'y':
        break
    end2 = timer( )
    if inp == 'y':
      print('No more solutions.')
    print(f'\nUsing {ListType.__name__}s, the total compute time was: {round(end1 + end2 - start1 - start2, 2)} sec')


  """ Select either LinkedList or PyList or PyTuple as the ListType. """

  # from sequence_options.linked_list import LinkedList
  # ListType = LinkedList

  from sequence_options.sequences import PyList  # or PyTuple
  ListType = PyList  # or PyTuple

  """ ---------------------------------------------------- """

  run_zebra_problem(ListType)
