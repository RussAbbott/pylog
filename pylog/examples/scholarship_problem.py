from control_structures import would_succeed, forall, forany, print_sf
from logic_variables import StructureItem, Var

from sequence_options.super_sequence import is_contiguous_in, is_a_subsequence_of, member, members

from examples.puzzles import run_puzzle, SimpleCounter

"""
A puzzle from GeekOverdose: https://geekoverdose.wordpress.com/2015/10/31/solving-logic-puzzles-in-prolog-puzzle-1-of-3/
A relatively simple puzzle of this genre.
Prolog solution provided at that site.

                        ----------------------------------------------------------------

There are 4 students: Amy, Carrie, Erma, and Tracy. 
Each has one scholarship and one major subject.  
The available scholarships are: $25,000, $30,000, $35,000 and $40,000. 
The available majors are: Astronomy, Comp Sci, English, and Philosophy. 

Using the following clues, determine which student has which scholarship and studies which subject.

1. The student who studies Astronomy gets a smaller scholarship than Amy.
2. Amy studies either English or Philosophy.
3. The student who studies Comp Sci has a $5,000 bigger scholarship than Carrie.
4. Erma has a $10,000 bigger scholarship than Carrie.
5. Tracy has a bigger scholarship than the student who studies English.

The answer.

Students: 
	Carrie(English, 25)
	Tracy(Comp Sci, 30)
	Erma(Astronomy, 35)
	Amy(Philosophy, 40)
More? (y, or n)? > y
No more.
"""

"""
    =================================================================================================================
      This and the zebra problem are both written so that they can use either LinkedLists or one of the
      PySequence options: PyList or PyTuple.
    =================================================================================================================
"""


class Student(StructureItem):

  def __init__(self, name=None, major=None, scholarship=None, first_arg_as_str_functor=True):
    # Package the properties together and create a StructureItem for this Student.
    super( ).__init__( (name, major, scholarship), first_arg_as_str_functor)


def scholarship_problem(Students):

  # Keeps count of the number of successful rule applications.
  rule_applications = SimpleCounter( )

  # A list of students with all the student names.
  Student_names = [Student(name='Amy'),  Student(name='Carrie'),
                   Student(name='Erma'), Student(name='Tracy')]

  # A list of students with all the majors.
  Majors = [Student(major='Astronomy'), Student(major='Comp Sci'),
            Student(major='English'),   Student(major='Philosophy')]

  # All the clues must succeed.
  for _ in forall([
    # print_sf allows us to trace the progress of the solution.
    # Since the print_sf statements are included in a forall list, they should all succeed, (the second argument).
    lambda: print_sf(f'\n{rule_applications.incr( )}) At the start: {Students}', 'Succeed'),

    # 1. The student who studies Astronomy gets a smaller scholarship than Amy.
    # We are taking advantage of the fact that the Students list is ordered by scholarship amount.
    lambda: forall([lambda: is_a_subsequence_of([Student(major='Astronomy'), Student(name='Amy')], Students),

                    # Make sure that all students and majors can be included, i.e., no duplicate names or majors.
                    # would_succeed(x) is equivalent to  not not x  in Prolog.
                    lambda: would_succeed(members)(Student_names, Students),
                    lambda: would_succeed(members)(Majors, Students)
                    ]),
    lambda: print_sf(f'{rule_applications.incr()}) After 1: {Students}', 'Succeed'),

    # 2. Amy studies either English or Philosophy.
    lambda: forall([lambda: forany([
                                    lambda: member(Student(name='Amy', major='English'), Students),
                                    lambda: member(Student(name='Amy', major='Philosophy'), Students),
    ]),

                    # Make sure that all students and majors can be included, i.e., no duplicate names or majors.
                    lambda: would_succeed(members)(Student_names, Students),
                    lambda: would_succeed(members)(Majors, Students)
                    ]),
    lambda: print_sf(f'{rule_applications.incr()}) After 2: {Students}', 'Succeed'),

    # 3. The student who studies Comp Sci has a $5,000 larger scholarship than Carrie.
    # To avoid arithmetic, take advantage of the known structure of the Scholarships list.
    lambda: forall([
                    lambda: is_contiguous_in([Student(name='Carrie'), Student(major='Comp Sci')], Students),

                    # Make sure that all students and majors can be included, i.e., no duplicate names or majors.
                    lambda: would_succeed(members)(Student_names, Students),
                    lambda: would_succeed(members)(Majors, Students)
                    ]),
    lambda: print_sf(f'{rule_applications.incr()}) After 3: {Students}', 'Succeed'),

    # 4. Erma has a $10,000 larger scholarship than Carrie.
    # This means that Erma comes after Carrie and that there is one person between them.
    lambda: forall([
                    lambda: is_contiguous_in([Student(name='Carrie'), Var( ), Student(name='Erma')], Students),

                    # Make sure that all students and majors can be included, i.e., no duplicate names or majors.
                    lambda: would_succeed(members)(Student_names, Students),
                    lambda: would_succeed(members)(Majors, Students)
                    ]),
    lambda: print_sf(f'{rule_applications.incr()}) After 4: {Students}', 'Succeed'),

    # 5. Tracy has a larger scholarship than the student who studies English.
    lambda: forall([lambda: is_a_subsequence_of([Student(major='English'), Student(name='Tracy')], Students),

                    # Make sure that all students and majors can be included, i.e., no duplicate names or majors.
                    lambda: would_succeed(members)(Student_names, Students),
                    lambda: would_succeed(members)(Majors, Students)
                    ]),
    lambda: print_sf(f'{rule_applications.incr()}) After 5: {Students}', 'Succeed'),

  ]):
    yield


if __name__ == '__main__':

  """ Select either LinkedList or a PySequence (PyList or PyTuple) as the ListType. """

  from sequence_options.linked_list import LinkedList
  ListType = LinkedList

  # from sequence_options.sequences import PyList  # or PyTuple
  # ListType = PyList  # or PyTuple

  """ additional_answer function, if any """

  # No additional answers.

  """ Set up the initial Answer list """
  # The answer list starts as an ordered list of Students with scholarship values.
  # To avoid arithmetic, we'll use the fact that the scholarships
  # are evenly spaced with $5,000 increments. The code deals with
  # scholarship numbers in thousands, i.e., 25, 30, 35, 40.
  Students = ListType([Student(scholarship=(25 + i*5)) for i in range(4)])

  """ Run problem """
  run_puzzle(scholarship_problem, ListType, Students)
