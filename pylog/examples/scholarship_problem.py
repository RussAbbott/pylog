from logic_variables import PyValue, StructureItem, Var

from sequence_options.super_sequence import is_contiguous_in, is_a_subsequence_of, member, SuperSequence

from examples.puzzles import Problem

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

The (unique) solution.

Students: 
	Carrie(English, 25)
	Tracy(Comp Sci, 30)
	Erma(Astronomy, 35)
	Amy(Philosophy, 40)



    =================================================================================================================
      This and the zebra problem are both written so that they can use either LinkedLists or one of the
      PySequence options: PyList or PyTuple. Make a choice at the bottom of the file.
    =================================================================================================================
"""


class Student(StructureItem):

  def __init__(self, name=None, major=None, scholarship=None, first_arg_as_str_functor=True):
    # Package the properties together and create a StructureItem for this Student.
    super( ).__init__( (name, major, scholarship), first_arg_as_str_functor)


# noinspection PyMethodMayBeStatic
class ScholarshipProblem(Problem):

  def clue_0(self, _: SuperSequence):
    """
    Problem setup.
      There are 4 students: Amy, Carrie, Erma, and Tracy.
      Each has one scholarship and one major subject.
      The available scholarships are: $25,000, $30,000, $35,000 and $40,000.
      The available majors are: Astronomy, Comp Sci, English, and Philosophy.
    """

    # The Items list starts as an ordered list of Students with scholarship values.
    # To avoid arithmetic, we'll use the fact that the scholarships
    # are evenly spaced with $5,000 increments. The code deals with
    # scholarship numbers in thousands, i.e., 25, 30, 35, 40.
    Students = ListType([Student(scholarship=(25 + i * 5)) for i in range(4)])
    self.Items = Students

    # Map attribute name to tuple position in Student objects.
    attr_dict = {'name': 0, 'major': 1}
    # Get the Vars for the names and majors. (Used in all_distinct.)
    name_Vars = [student.args[attr_dict['name']] for student in self.Items]
    major_Vars = [student.args[attr_dict['major']] for student in self.Items]
    # Try not requiring the names and/or majors to be distinct. They are both initially [] at the Problem level.
    # So the assignments here can be left out here.
    # name_Vars = []   # Requires many more rule applications to get an answer.
    # major_Vars = []  # Gets the right answer after the same number of rule applications.
                       # But gets the wrong answer on backtracking.
    # These lists will be checked for distinctness after each clue.
    self.all_distinct_lists = [name_Vars, major_Vars]

    # self.clues at the Problem level is [self.clue_0]. That ensures that this setup clue will run.
    # We append the actual clues so that the clues will be in their correct list index positions,
    # i.e., clue_i at self.clues[i].
    self.clues += [self.clue_1, self.clue_2, self.clue_3, self.clue_4, self.clue_5]

    # Show trace on all clues.
    self.show_trace_list = list(range(len(self.clues)+1))
    yield

  # If we make the clues static, it's difficult (and strange) to make a list of them.
  # See: https://stackoverflow.com/questions/41921255/staticmethod-object-is-not-callable-switch-case.
  def clue_1(self, Students: SuperSequence):
    """ 1. The student who studies Astronomy gets a smaller scholarship than Amy. """
    yield from is_a_subsequence_of([Student(major='Astronomy'), Student(name='Amy')], Students)

  def clue_2(self, Students: SuperSequence):
    """ 2. Amy studies either Philosophy or English. """
    # Create Major as a local logic variable.
    Major = PyValue( )
    for _ in member(Student(name='Amy', major=Major), Students):
      yield from member(Major, PyList(['Philosophy', 'English']))

  def clue_3(self, Students: SuperSequence):
    """ 3. The student who studies Comp Sci has a $5,000 larger scholarship than Carrie. """
    # To avoid arithmetic, take advantage of the known structure of the Scholarships list.
    yield from is_contiguous_in([Student(name='Carrie'), Student(major='Comp Sci')], Students)

  def clue_4(self, Students: SuperSequence):
    """ 4. Erma has a $10,000 larger scholarship than Carrie.
        This means that Erma comes after the person who comes after Carrie.
    """
    yield from is_contiguous_in([Student(name='Carrie'), Var( ), Student(name='Erma')], Students)

  def clue_5(self, Students: SuperSequence):
    """ 5. Tracy has a larger scholarship than the student who studies English. """
    yield from is_a_subsequence_of([Student(major='English'), Student(name='Tracy')], Students)


if __name__ == '__main__':

  """ Select either LinkedList or a PySequence (PyList or PyTuple) as the ListType. """
  # from sequence_options.linked_list import LinkedList
  # ListType = LinkedList
  #
  from sequence_options.sequences import PyList  # or PyTuple
  ListType = PyList  # or PyTuple

  """ Run problem """
  # Create an instance of the ScholarshipProblem and run it.
  # ScholarshipProblem is a subclass of the Problem class.
  # The Problem class has a __call__ method. So instances can be called.
  # That __call__ method runs the problem. See Problem.__call__.
  ScholarshipProblem()(ListType)
