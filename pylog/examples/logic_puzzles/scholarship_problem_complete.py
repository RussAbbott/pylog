from examples.logic_puzzles.puzzles import SimpleCounter, all_all_distinct, timer, trace
from logic_variables import StructureItem, Var
from sequence_options.sequences import PyList, PyTuple
from sequence_options.super_sequence import SuperSequence, is_a_subsequence_of as is_subseq, \
                                            is_contiguous_in, member

"""
A puzzle from GeekOverdose: https://geekoverdose.wordpress.com/2015/10/31/solving-logic-puzzles-in-prolog-puzzle-1-of-3/
A relatively simple puzzle of this genre.
Prolog solution provided at that site.

                        ----------------------------------------------------------------

There are 4 students: Emmy, Lynn, Marie, and Ada. 
Each has one scholarship and one major subject.  
The available scholarships are: $25,000, $30,000, $35,000 and $40,000. 
The available majors are: CS, Bio, Math, and Phys,. 

Using the following clues, determine which student has which scholarship and studies which subject.

1. The student who studies Phys gets a smaller scholarship than Emmy.
2. Emmy studies either Bio or Math.
3. The student who studies CS has a $5,000 bigger scholarship than Lynn.
4. Marie has a $10,000 bigger scholarship than Lynn.
5. Ada has a bigger scholarship than the student who studies Bio.

The (unique) solution.

Students: 
    Lynn(Bio, 25)
    Ada(CS, 30)
    Marie(Phys, 35)
    Emmy(Math, 40)



    =================================================================================================================
      This and the zebra problem are both written so that they can use either LinkedLists or one of the
      PySequence options: PyList or PyTuple. Make a choice at the bottom of the file.
    =================================================================================================================
"""


class Stdnt(StructureItem):

  def __init__(self, name=None, major=None, scholarship=None, first_arg_as_str_functor=True):
    # Package the properties together and create a StructureItem for this Student.
    super( ).__init__( (name, major, scholarship), first_arg_as_str_functor)

  def __str__(self):
    name = self.args[0] if self.args[0].is_instantiated() else '_'
    major = self.args[1] if self.args[1].is_instantiated() else '_'
    # scholarship = self.args[2] if self.args[2].is_instantiated() else '_'
    return f'{name}/{major}'


# noinspection PyMethodMayBeStatic
class ScholarshipProblem:

  def __init__(self):
    self.all_distinct_lists = None
    self.clues = [self.clue_0]
    self.Students = None
    # self.ListType = None
    self.printing_time = 0
    self.rule_applications = SimpleCounter()
    self.show_trace_list = None

  def __call__(self):  # , ListType):
    """ Run the problem and display the answer. Take and display timing information. """

    # self.ListType = ListType
    inp = None  # needed below at this block level
    start = timer()

    last_rule_count = 0

    for _ in self.run_all_clues():
      rule_applications_increment = self.rule_applications.count() - last_rule_count
      last_rule_count = self.rule_applications.count()
      pause_timer = timer()
      print(f'\nAfter {rule_applications_increment} rule applications,\nSolution: ')
      scholarship = 25
      for (index, item) in enumerate(self.Students):
        print(f'\t{index + 1}. {item}\t(${scholarship},000 scholarship)')
        scholarship += 5
      # self.additional_answer(self.Students)
      inp = input('\nMore? (y, or n)? > ').lower()
      self.printing_time += timer() - pause_timer
      if inp != 'y':
        break
      else:
        print()
    end = timer()
    rule_applications_increment = self.rule_applications.count() - last_rule_count
    if inp == 'y':
      print(f'\nAfter {rule_applications_increment} final rule applications, no other solutions.')
    print(f'\nThe total compute time was: '
          f'{round(end - start - self.printing_time, 2)} sec')

  # def additional_answer(self, _):
  #   yield

  def check_all_for_distinctness(self, Class):
    """ Sets up to check all attributes for distinctness """
    nbr_attributes = len(Class().args)
    vars_lists = [[item.args[i] for item in self.Students] for i in range(nbr_attributes)]
    self.all_distinct_lists = vars_lists

  def clue_0(self, _):
    """ Override in subclass """
    yield

  # noinspection SpellCheckingInspection
  def run_clue(self, clue_nbr):
    """ Run clue_<clue_nbr>, check the all_distinct constraints, and show progress. """
    for _ in self.clues[clue_nbr](self.Students):
      for _ in all_all_distinct(self.all_distinct_lists):
        pause_timer = timer()
        self.rule_applications.incr()
        for _ in trace(f'{"Initially" if clue_nbr == 0 else ("Clue " + str(clue_nbr))}: '
                       f'{", ".join([str(std) for std in self.Students])}',
                       show_trace=clue_nbr in self.show_trace_list):
          self.printing_time += timer() - pause_timer
          yield

  def run_all_clues(self, clue_number=0):
    if clue_number >= len(self.clues):
      # Ran all the clues. Succeed.
      yield
    else:
      # Run the current clue and the rest of them.
      for _ in self.run_clue(clue_number):
        yield from self.run_all_clues(clue_number + 1)

  def set_clues_list(self, clues):
    self.clues = clues

  def set_all_distinct_lists(self, all_distinct_lists):
    self.all_distinct_lists = all_distinct_lists  # {index+1: clue for (index, clue) in enumerate(clue_names)}

  def clue_0(self, _: SuperSequence):
    """
    Problem setup.
      There are 4 students: Emmy, Lynn, Marie, and Ada.
      Each has one scholarship and one major subject.
      The available scholarships are: $25,000, $30,000, $35,000 and $40,000.
      The available majors are: Phys, CS, Bio, and Math.
    """

    # The Items list starts as an ordered list of Students with scholarship values.
    # To avoid arithmetic, we'll use the fact that the scholarships
    # are evenly spaced with $5,000 increments. The code deals with
    # scholarship numbers in thousands, i.e., 25, 30, 35, 40.
    Students = PyTuple(tuple([Stdnt(scholarship=(25 + i * 5)) for i in range(4)]))
    self.Students = Students

    # Map attribute name to tuple position in Student objects.
    attr_dict = {'name': 0, 'major': 1}
    # Get the Vars for the names and majors. (Used in all_distinct.)
    name_Vars = [student.args[attr_dict['name']] for student in self.Students]
    major_Vars = [student.args[attr_dict['major']] for student in self.Students]
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
  # def clue_1(self, Students: SuperSequence):
  #   """ 1. The student who studies Phys gets a smaller scholarship than Emmy. """
  #   yield from is_a_subsequence_of([Student(major='Phys'), Student(name='Emmy')], Students)
  #
  # def clue_2(self, Students: SuperSequence):
  #   """ 2. Emmy studies either Math or Bio. """
  #   # Create Major as a local logic variable.
  #   Major = PyValue( )
  #   for _ in member(Student(name='Emmy', major=Major), Students):
  #     yield from member(Major, PyList(['Math', 'Bio']))
  #
  # def clue_3(self, Students: SuperSequence):
  #   """ 3. The student who studies CS has a $5,000 larger scholarship than Lynn. """
  #   # To avoid arithmetic, take advantage of the known structure of the Scholarships list.
  #   yield from is_contiguous_in([Student(name='Lynn'), Student(major='CS')], Students)
  #
  # def clue_4(self, Students: SuperSequence):
  #   """ 4. Marie has a $10,000 larger scholarship than Lynn.
  #       This means that Marie comes after the person who comes after Lynn.
  #   """
  #   yield from is_contiguous_in([Student(name='Lynn'), Var( ), Student(name='Marie')], Students)
  #
  # def clue_5(self, Students: SuperSequence):
  #   """ 5. Ada has a larger scholarship than the student who studies Bio. """
  #   yield from is_a_subsequence_of([Student(major='Bio'), Student(name='Ada')], Students)


  def clue_1(self, Stdnts):
    """ The student who studies Phys gets a
        smaller scholarship than Emmy. """
    yield from is_subseq(
      [Stdnt(major='Phys'), Stdnt(name='Emmy')],
      Stdnts)

  def clue_2(self, Stdnts):
    """ Emmy studies either Math or Bio. """
    # Create Major as a local logic variable.
    Major = Var( )
    for _ in member(Stdnt(name='Emmy', major=Major),
                    Stdnts):
      yield from member(Major,
                        PyList(['Math',
                                'Bio']))

  def clue_3(self, Stdnts):
    """ The Stdnt who studies CS has a
        $5,000 larger scholarship than Lynn. """
    yield from is_contiguous_in(
      [Stdnt(name='Lynn'), Stdnt(major='CS')],
      Stdnts)

  def clue_4(self, Stdnts):
    """ Marie has a $10,000 larger scholarship than
        Lynn. """
    yield from is_contiguous_in(
      [Stdnt(name='Lynn'),
       Var(),
       Stdnt(name='Marie')],
      Stdnts)

  def clue_5(self, Stdnts):
    """ Ada has a larger scholarship than the Stdnt
        who studies Bio. """
    yield from is_subseq(
      [Stdnt(major='Bio'), Stdnt(name='Ada')],
      Stdnts)


if __name__ == '__main__':

  """ Select either LinkedList or a PySequence (PyList or PyTuple) as the ListType. """
  # from sequence_options.linked_list import PyTuple  # PyList
  ListType = PyTuple  # LinkedList

  """ Run problem """
  # Create an instance of the ScholarshipProblem and run it.
  # ScholarshipProblem is a subclass of the Problem class.
  # The Problem class has a __call__ method. So instances can be called.
  # That __call__ method runs the problem. See Problem.__call__.
  ScholarshipProblem()()
