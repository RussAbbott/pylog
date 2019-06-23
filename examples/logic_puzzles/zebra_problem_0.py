from pylog.control_structures import forall  #, print_SF  # Uncomment when we use it.
from pylog.logic_variables import n_Vars, StructureItem, unify

from pylog.sequence_options.super_sequence import is_contiguous_in, member, members, next_to
from pylog.sequence_options.linked_list import LinkedList

"""
One version of the famous Zebra problem. (They are all similar, but the names are often different.)

There are 5 houses in a row. Each has a family of a unique nationality.
Each house also has a color, a pet, a favorite smoke, and a favorite drink.

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
"""

class House(StructureItem):
  def __init__(self, nationality=None, smoke=None, pet=None, drink=None, color=None, first_arg_as_str_functor=True):
    # Package the properties together and create a StructureItem for this Student.
    super( ).__init__( (nationality, smoke, pet, drink, color), first_arg_as_str_functor)



def zebra_problem(Houses):
  for _ in forall([
    # 1. The English live in the red house.
    lambda: member(House(nationality='English', color='red'), Houses),
    # lambda: print_SF(f'After 1: {Houses}', 'Succeed'),

    # 2. The Spanish have a dog.
    lambda: member(House(nationality='Spanish', pet='dog'), Houses),
    # lambda: print_SF(f'After 2: {Houses}', 'Succeed'),

    # 3. They drink coffee in the green house.
    lambda: member(House(drink='coffee', color='green'), Houses),
    # lambda: print_SF(f'After 3: {Houses}', 'Succeed'),

    # 4. The Ukrainians drink tea.
    lambda: member(House(nationality='Ukrainians', drink='tea'), Houses),
    # lambda: print_SF(f'After 4: {Houses}', 'Succeed'),

    # 5. The green house is immediately to the right of the white house.
    lambda: is_contiguous_in([House(color='white'), House(color='green')], Houses),
    # lambda: print_SF(f'After 5: {Houses}', 'Succeed'),

    # 6. The Old Gold smokers have snails.
    lambda: member(House(smoke='Old Gold', pet='snails'), Houses),
    # lambda: print_SF(f'After 6: {Houses}', 'Succeed'),

    # 7. They smoke Kool in the yellow house.
    lambda: member(House(smoke='Kool', color='yellow'), Houses),
    # lambda: print_SF(f'After 7: {Houses}', 'Succeed'),

    # 8. They drink milk in the middle house.
    # Note the use of a slice. Houses[2] picks the middle house.
    lambda: unify(House(drink='milk'), Houses[2]),
    # lambda: print_SF(f'After 8: {Houses}', 'Succeed'),

    # 9. The Norwegians live in the first house on the left.
    lambda: unify(House(nationality='Norwegians'), Houses.head()),
    # lambda: print_SF(f'After 9: {Houses}', 'Succeed'),

    # 10. The Chesterfield smokers live next to the fox.
    lambda: next_to(House(smoke='Chesterfield'), House(pet='fox'), Houses),
    # lambda: print_SF(f'After 10: {Houses}', 'Succeed'),

    # 11. They smoke Kool in the house next to the horse.
    lambda: next_to(House(smoke='Kool'), House(pet='horse'), Houses),
    # lambda: print_SF(f'After 11: {Houses}', 'Succeed'),

    # 12. The Lucky smokers drink juice.
    lambda: member(House(drink='juice', smoke='Lucky'), Houses),
    # lambda: print_SF(f'After 12: {Houses}', 'Succeed'),

    # 13. The Japanese smoke Parliament.
    lambda: member(House(nationality='Japanese', smoke='Parliament'), Houses),
    # lambda: print_SF(f'After 13: {Houses}', 'Succeed'),

    # 14. The Norwegians live next to the blue house.
    lambda: next_to(House(nationality='Norwegians'), House(color='blue'), Houses),
    # lambda: print_SF(f'After 14: {Houses}', 'Succeed'),

    # Fill in unmentioned properties.
    lambda: members([House(pet='zebra'), House(drink='water')], Houses),
  ]):
    yield


if __name__ == '__main__':

  from timeit import default_timer as timer

  (start1, end1, start2, end2) = (timer( ), None, None, None)

  Houses = LinkedList( [House( ) for _ in range(5)] )
  inp = None
  for _ in zebra_problem(Houses):
    print('\nHouses: ')
    for (indx, house) in enumerate(Houses.to_python_list()):
      print(f'\t{indx+1}. {house}')
    (Nat1, Nat2) = n_Vars(2)
    for _ in members([House(nationality=Nat1, pet='zebra'),
                      House(nationality=Nat2, drink='water')], Houses):
      ans = f'The {Nat1} both own a zebra and drink water.' if Nat1 == Nat2 else \
            f'The {Nat1} own a zebra, and the {Nat2} drink water.'
      end1 = timer( )
      print(ans)
    inp = input('\nMore? (y, or n)? > ').lower()
    start2 = timer( )
    if inp != 'y':
      break

  if inp == 'y':
    print('No more solutions.')

  end2 = timer( )

  print(f'\nTotal compute time: {round(end1 + end2 - start1 - start2, 2)} sec')

"""
Houses:
	1. Norwegians(Kool, fox, water, yellow)
	2. Ukrainians(Chesterfield, horse, tea, blue)
	3. English(Old Gold, snails, milk, red)
	4. Spanish(Lucky, dog, juice, white)
	5. Japanese(Parliament, zebra, coffee, green)
The Japanese own a zebra, and the Norwegians drink water.
More? (y, or n)? > y
No more.
"""
