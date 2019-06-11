from pylog.control_structures import forall, trace
from pylog.logic_variables import PyValue, StructureItem, Var

from pylog.sequence_options.super_sequence import is_contiguous_in, is_a_subsequence_of, member

from puzzles import all_all_distinct, run_puzzle, SimpleCounter

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


class ScholarshipProblem():

  def __init__(self, Students):
    self.Items = Students

    # Map attribute name to tuple position in Student objects.
    self.attr_dict = {'name': 0, 'major': 1}
    self.rule_applications = SimpleCounter( )

    self.name_PyValues = [student.args[self.attr_dict['name']] for student in self.Items]
    self.major_PyValues = [student.args[self.attr_dict['major']] for student in self.Items]

    self.clues = {index+1: clue for (index, clue) in
                  enumerate([self.clue_1, self.clue_2, self.clue_3, self.clue_4, self.clue_5])}

  # Try not requiring the names and/or majors to be distinct.

  # Requires many more rule applications to get an answer.
  # name_PyValues = []

  # Gets the right answer after the same number of rule applications. But gets the wrong answer on backtracking.
  # major_PyValues = []

  def clue_1(self):
    """ 1. The student who studies Astronomy gets a smaller scholarship than Amy. """
    yield from is_a_subsequence_of([Student(major='Astronomy'), Student(name='Amy')], self.Items)

  def clue_2(self):
    """ 2. Amy studies either English or Philosophy. """
    # Local variable
    Major = PyValue( )
    yield from forall([
      # Note the use of Major as a PyValue, which gets instantiated *after* it is positioned.
      lambda: member(Student(name='Amy', major=Major), self.Items),
      # Since Philosophy is the right answer, more rule applications are required (36 vs. 33)
      # if English is first in the list.
      lambda: member(Major, PyList(['Philosophy', 'English'])),
    ])

  def clue_3(self):
    """ 3. The student who studies Comp Sci has a $5,000 larger scholarship than Carrie. """
    # To avoid arithmetic, take advantage of the known structure of the Scholarships list.
    yield from is_contiguous_in([Student(name='Carrie'), Student(major='Comp Sci')], self.Items)

  def clue_4(self):
    """ 4. Erma has a $10,000 larger scholarship than Carrie.
        This means that Erma comes after the person who comes after Carrie.
    """
    yield from is_contiguous_in([Student(name='Carrie'), Var( ), Student(name='Erma')], self.Items)

  def clue_5(self):
    """ 5. Tracy has a larger scholarship than the student who studies English. """
    yield from is_a_subsequence_of([Student(major='English'), Student(name='Tracy')], self.Items)

  def run_clue(self, index):
    """ Run clue_<index>, check the all_distinct constraints, and show progress. """
    for _ in forall([
      self.clues[index],
      lambda: all_all_distinct([self.name_PyValues, self.major_PyValues]),
      lambda: trace(f'{self.rule_applications.incr( )}) After clue {index}: {self.Items}'),
                     ]):
      yield

  def __call__(self):
    # All clues must succeed.
    for _ in forall([
                      lambda: trace(f'\n{self.rule_applications.incr( )}) At the start: {self.Items}'),

                      lambda: self.run_clue(1),
                      lambda: self.run_clue(2),
                      lambda: self.run_clue(3),
                      lambda: self.run_clue(4),
                      lambda: self.run_clue(5),
                     ]):
      yield


if __name__ == '__main__':

  """ Select either LinkedList or a PySequence (PyList or PyTuple) as the ListType. """

  # from sequence_options.linked_list import LinkedList
  # ListType = LinkedList
  #
  from pylog.sequence_options.sequences import PyList  # or PyTuple
  ListType = PyList  # or PyTuple

  """ additional_answer function, if any """

  # No additional_answer function.

  """ Set up the initial Answer list """
  # The answer list starts as an ordered list of Students with scholarship values.
  # To avoid arithmetic, we'll use the fact that the scholarships
  # are evenly spaced with $5,000 increments. The code deals with
  # scholarship numbers in thousands, i.e., 25, 30, 35, 40.
  Students = ListType([Student(scholarship=(25 + i*5)) for i in range(4)])

  """ Run problem """
  run_puzzle(ScholarshipProblem, ListType, Students)
