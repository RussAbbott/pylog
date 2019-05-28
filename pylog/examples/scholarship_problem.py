from control_structures import would_succeed, forall, forany, print_sf
from logic_variables import Container, Var

from sequence_options.super_sequence import is_subsequence

from examples.puzzles import Puzzle_Item, run_problem

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
A puzzle from GeekOverdose: https://geekoverdose.wordpress.com/2015/10/31/solving-logic-puzzles-in-prolog-puzzle-1-of-3/
Prolog solution provided at that site.

                        ----------------------------------------------------------------

There are 4 students: Carrie, Erma, Amy and Tracy. 
Each has one scholarship and one major subject. 
Find which student has which scholarship and studies which subject--
assuming that all scholarships and majors are distinct. 
The available scholarships are: 25000, 30000, 35000 and 40000 USD. 
The available majors are: Astronomy, English, Philosophy, Comp Sci. 

1. The student who studies Astronomy gets a smaller scholarship than Amy.
2. Amy studies either English or Philosophy.
3. The student who studies Comp Sci has a $5,000 bigger scholarship than Carrie.
4. Erma has a $10,000 bigger scholarship than Carrie.
5. Tracy has a bigger scholarship than the student that studies English.

The answer.

Students: 
	Carrie(English, 25)
	Tracy(Comp Sci, 30)
	Erma(Astronomy, 35)
	Amy(Philosophy, 40)
More? (y, or n)? > y
No more.
"""


class Student(Puzzle_Item):

  def __init__(self, name=None, major=None, scholarship=None):
    functor = type(self).__name__.lower( )
    name = self.make_property(name)
    major = self.make_property(major)
    scholarship = self.make_property(scholarship)
    # Create a Structure for this Student.
    super( ).__init__((functor, name, major, scholarship))


def scholarship_problem(Students, ListType):

  # Keeps count of the number of successful rule applications.
  rule_applications = Container(0)

  # A list of students with all the student names.
  Student_names = [Student(name='Amy'),  Student(name='Carrie'),
                   Student(name='Erma'), Student(name='Tracy')]

  # All the clues must succeed.
  for _ in forall([
    # Unify the answer parameter (Ss) with the internal answer list (Students).
    # lambda: unify(Students, Ss),
    # print_sf allows us to leave a trace of progress.
    # Since the print_sf statements are all included in a forall list, they should all succeed.
    lambda: print_sf(f'\n{rule_applications.incr_and_return( )}) At the start: {Students}', 'Succeed'),

    # 1. The student who studies Astronomy gets a smaller scholarship than Amy.
    # Could have used inThisOrder rather than splitAt.
    lambda: forall([lambda: is_subsequence([Student(major='Astronomy'), Student(name='Amy')], Students),

                    # Make sure that all students can be included, i.e., no duplicate names.
                    lambda: would_succeed(ListType.members)(Student_names, Students)
                    ]),
    lambda: print_sf(f'{rule_applications.incr_and_return()}) After 1: {Students}', 'Succeed'),

    # 2. Amy studies either English or Philosophy.
    # Runs slightly faster with Philosophy tried first (33 vs 37). Gets the same result either way.
    lambda: forall([lambda: forany([
                                    lambda: ListType.member(Student(name='Amy', major='English'), Students),
                                    lambda: ListType.member(Student(name='Amy', major='Philosophy'), Students),
                                   ]),

                    # Make sure that all students can be included, i.e., no duplicate names.
                    lambda: would_succeed(ListType.members)(Student_names, Students)]),
    lambda: print_sf(f'{rule_applications.incr_and_return()}) After 2: {Students}', 'Succeed'),

    # 3. The student who studies Comp Sci has a $5,000 larger scholarship than Carrie.
    # To avoid arithmetic, take advantage of the known structure of the Scholarships list.
    lambda: forall([lambda: ListType.is_contiguous_in([Student(name='Carrie'), Student(major='Comp Sci')], Students),

                    # Make sure that all students can be included, i.e., no duplicate names.
                    lambda: would_succeed(ListType.members)(Student_names, Students)
                    ]),
    lambda: print_sf(f'{rule_applications.incr_and_return()}) After 3: {Students}', 'Succeed'),

    # 4. Erma has a $10,000 larger scholarship than Carrie.
    # This means that Erma comes after Carrie and that there is one person between them.
    lambda: forall([lambda: ListType.is_contiguous_in([Student(name='Carrie'), Var(), Student(name='Erma')], Students),

                    # Make sure that all students can be included, i.e., no duplicate names.
                    lambda: would_succeed(ListType.members)(Student_names, Students)
                    ]),
    lambda: print_sf(f'{rule_applications.incr_and_return()}) After 4: {Students}', 'Succeed'),

    # 5. Tracy has a larger scholarship than the student that studies English.
    lambda: forall([lambda: is_subsequence([Student(major='English'), Student(name='Tracy')], Students),

                    # Make sure that all students can be included, i.e., no duplicate names.
                    lambda: would_succeed(ListType.members)(Student_names, Students),
                    ]),
    lambda: print_sf(f'{rule_applications.incr_and_return()}) After 5: {Students}', 'Succeed'),

    # Make sure all majors are mentioned.
    lambda: ListType.members([Student(major='Astronomy'),  Student(major='English'),
                              Student(major='Philosophy'), Student(major='Comp Sci')],
                             Students)
  ]):
    yield


if __name__ == '__main__':

  """ Select either LinkedList or a PySequence (PyList or PyTuple) as the ListType. """

  from sequence_options.linked_list import LinkedList
  ListType = LinkedList

  # from sequence_options.sequences import PyList  # or PyTuple
  # ListType = PyList  # or PyTuple

  """ additional_answer function, if any """

  # No additional answers

  """ Set up the Answer list """
  # The answer list starts as an ordered list of scholarship values.
  # To avoid arithmetic, we'll use the fact that the scholarships
  # are evenly spaced with $5,000 increments. The code deals with
  # scholarship numbers in thousands, i.e., 25, 30, 35, 40.
  Students = ListType([Student(scholarship=25 + i * 5) for i in range(4)])

  """ Run problem """
  run_problem(scholarship_problem, ListType, Students)
