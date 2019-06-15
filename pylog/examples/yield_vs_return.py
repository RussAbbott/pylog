from typing import List, Optional

from control_structures import fails
from logic_variables import unify, Var
from sequence_options.sequences import PyList
from sequence_options.super_sequence import member

# In this example, the results are sent backward through implicit yield's rather than returns. That is,
# the nested for-loops send their results to the previous ones essentially through yield statements.
print('1. ', end='')
xyz_s = [ x+y+z for x in "abc" for y in '123' for z in 'xyz' ]
for xyz in xyz_s:
  print(xyz, end=', ')
print()

# Can we do this with nested function calls? This is the same thing, but but done without yields.
# The results are the same, but the only way to get them is at the bottom of nested calls. Note that
# there are no return statements. Things are always passed forward.

print('2. ', end='')


def top2():
  for x in "abc":
    middle2(x)


def middle2(x):
  for y in '123':
    bottom2(x, y)


def bottom2(x, y):
  for z in 'xyz':
    print(x+y+z, end=', ')


top2()
print()


# Here's an attempted alternative using return.
# This produces only the first triple because each for-loop is exited after the first element.

def top3( ):
  for x in 'abc':
    return x+middle3(x)


def middle3(x):
  for y in '123':
    return y+bottom3(x, y)


# noinspection PyUnusedLocal
def bottom3(x, y):
  for z in 'xyz':
    return z


print('3.', top3())


# But when done with yield instead of return, we get the same result as 1. The results are
# returned to and printed at the top. This works because the downward calls are done in for-loops
# rather than direct function calls, and the results are returned through yields rather than return
# statements. A yield does n0t terminate the for-loop within which it is embedded -- just like the
# first example.

def top4( ):
  for x in 'abc':
    for yz in middle4(x):
      yield x+yz


def middle4(x):
  for y in '123':
    for z in bottom4(x, y):
      yield y+z


# noinspection PyUnusedLocal
def bottom4(x, y):
  for z in 'xyz':
    yield z


print('4. ', end='')
for xyz in top4():
  print(xyz, end=', ')


"""
transversal([], SoFar, A) :-
    reverse(SoFar, A).
transversal([S|Ss], So_Far, Answer) :-
    member(X, S),
    print('S'/S-'X'/X-'So_Far'/So_Far), nl,
    \+ member(X, So_Far),
    transversal(Ss, [X|So_Far], Answer).
    
?- transversal([[1, 2, 3], [2], [1]], [], Ans).

'S' / [1, 2, 3] - 'X' / 1 - 'So_Far' / []
'S' / [2] - 'X' / 2 - 'So_Far' / [1]
'S' / [1] - 'X' / 1 - 'So_Far' / [2, 1]
'S' / [1, 2, 3] - 'X' / 2 - 'So_Far' / []
'S' / [2] - 'X' / 2 - 'So_Far' / [2]
'S' / [1, 2, 3] - 'X' / 3 - 'So_Far' / []
'S' / [2] - 'X' / 2 - 'So_Far' / [3]
'S' / [1] - 'X' / 1 - 'So_Far' / [2, 3]

Ans = [3, 2, 1]
"""


def transversal_yield(Sets: List[PyList], So_Far: PyList, Answer: Var):
  if not Sets:
    yield from unify(So_Far, Answer)
  else:
    [S, *Ss] = Sets
    X = Var()
    for _ in member(X, S):
      print(f'S/{S}; X/{X}; So_Far/{So_Far}')
      for _ in fails(member)(X, So_Far):
        yield from transversal_yield(Ss, So_Far + PyList([X]), Answer)


"""
S: [1, 2, 3], X: 1, So_Far: []
S: [2], X: 2, So_Far: [1]
S: [1], X: 1, So_Far: [2, 1]
S: [1, 2, 3], X: 2, So_Far: []
S: [2], X: 2, So_Far: [2]
S: [1, 2, 3], X: 3, So_Far: []
S: [2], X: 2, So_Far: [3]
S: [1], X: 1, So_Far: [2, 3]
transversal([[1, 2, 3], [2], [1]], [], Ans) => Ans: [3, 2, 1]
"""

"""
Kung, J. P., Rota, G. C., & Yan, C. H. (2009). Combinatorics: the Rota way. Cambridge University Press.

Let Y = (SJiel be a family of subsets of a set E. A set K C E is a transversal of the family 9’ if there exists a 
bijection p : K + I such that k E &h) for all k E K. Note that Y may contain the same set more than
once; hence the notation “9 = (S&i’ rather than “9’ = {Si}iEI .” 

Weinberger, D. B. (1974). Sufficient regularity conditions for common transversals. Journal of Combinatorial Theory, 
Series A, 16(3), 380-390.
https://www.sciencedirect.com/science/article/pii/0097316574900612/pdf?md5=2c5a36ee9f7460417ac00d6c8f1ebdbd&isDTMRedir=Y&pid=1-s2.0-0097316574900612-main.pdf&_valck=1
https://www.sciencedirect.com/science/article/pii/0097316574900612/pdf?md5=2c5a36ee9f7460417ac00d6c8f1ebdbd&isDTMRedir=Y&pid=1-s2.0-0097316574900612-main.pdf&_valck=1

https://pdf.sciencedirectassets.com/272565/1-s2.0-S0097316500X0074X/1-s2.0-0097316574900612/main.pdf?x-amz-security-token=AgoJb3JpZ2luX2VjENX%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLWVhc3QtMSJHMEUCIQCSV%2FEzcUzQSRJdZ7ZTJZJZIwVPm1%2BmUWY%2FidprBTISFQIgar1JrYwNR15%2BNG3jOZg66%2FbLg7%2Bdbh5esuotMR0gaDkq4wMI%2Ff%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FARACGgwwNTkwMDM1NDY4NjUiDAgPsRIEmCkoLE%2FH2Cq3A6AXClN77i8pWkteLtqG5nTBGyZS18YkwbQQMDR6yl%2FcvJOFa4TowhJ2Ah6YTJerGwzqsk5B8skx8Gh%2Flx5El9FKFfHdB7ANbS8u%2BXbUlk%2BaZaLTfxWkP5IQdkF2knwvrlVxiU%2F57D4RsGe%2B%2FcFTGvmX1GgjV9HRTDxCkcyVztP9MOnOs2bls1DzM2zI%2FrEFfpvx4VttMo17fXl6%2FEAGvMGvigx8ihTEjBpO7Dl1GgtGe6cSa%2F0Whi78QRcLeekp58%2BEQQFsSu09el75ADZEKx1xZwZGlMgXJWUx5WcgEDeCQWLZywWXw8sfqFLYx9guLJhQv5a09OCRqekkJt00XsPPm%2BAW%2BH0OUJvqKJrMgXzGTBZy5ILXmflQesE4TRoTEEBjCoCyEJmTSiw%2Fo4p%2FlgbgddrVq1UpzGYdvWTDZBkiadXySM%2Bl2XyIvxsuxaMZveed49KsHpd7yAbXixSWVHSKOvq4GCEvuspWv9qs6goDExLkdFt4ryFCrpBNdo6phbaB2A6AOSH2IHBsKt93lDe8XdXBjr2zwqd9RfM%2FGsy0Vm8UHzT1OePEC6Q0hsMFT7GBMP3vyNAwruSR6AU6tAHA2gv1a5rNaoGpgtSN8WF5wvYo%2F6QeLDageDy6KubWhoZKO7gA0h7EfURR6Sw0ltdQz0QLwso5qE8T0SPqcr5Lk9mEXpIarq%2Bdo9pOcOn2pDasO6k607B2QPqAxFIMaBRs3yk4K3idelgfObBpfPqAc487jD0gyWzURICzTYzt%2BwJxPGXMQ28dcTh4xyWOzxtDHEaXz1pk1Y%2Fo4XJmupqxpz%2FN%2FFEtdpMvScCrO4aj02fDGQg%3D&AWSAccessKeyId=ASIAQ3PHCVTY3WZ72OMK&Expires=1560576975&Signature=%2Fmxmfw52S7A0g8tqqcmv8diYfJo%3D&hash=7410251f32b246c05e68beff296ccb4827eb793adcafc62fd270d173e1060849&host=68042c943591013ac2b2430a89b270f6af2c76d8dfd086a07176afe7c76c2c61&pii=0097316574900612&tid=spdf-098ff2e0-6e74-449e-9d65-276882605973&sid=0d6c18b33aee7342af497d568cc659b709ffgxrqa&type=client
"""


def transversal_dfs_all(Sets: List[List[int]], So_Far: List[int]) -> List[List[int]]:
  if not Sets:
    return [So_Far]
  else:
    [S, *Ss] = Sets
    Ans = []
    for X in S:
      if X not in So_Far:
        Ans += transversal_dfs_all(Ss, So_Far + [X])
    return Ans


def transversal_dfs_first(Sets: List[List[int]], So_Far: List[int]) -> Optional[List[int]]:
  """ Looking for the first solution. """

  # print(f'Sets: {Sets}, So_Far: {So_Far}')
  if not Sets:
    return So_Far
  else:
    [[S1, *S], *Ss] = Sets
    t_result = None if S1 in So_Far else transversal_dfs_first(Ss, So_Far+[S1])
    return t_result if t_result else \
           None if not S else \
           transversal_dfs_first([S] + Ss, So_Far)


if __name__ == '__main__':
  print()
  print()
  Ans = Var()
  for _ in transversal_yield([PyList([1, 2, 3]), PyList([2, 4]), PyList([1])], PyList([]), Ans):
    print(f'transversal([[1, 2, 3], [2, 4], [1]], [], Ans) => {Ans}')

  print()
  print()
  print(f'transversal_dfs_all([[1, 2, 3], [2, 4], [1]], []) => ', end='')
  print(transversal_dfs_all([[1, 2, 3], [2, 4], [1]], []) )

  print()
  print()
  print(f'transversal_dfs_first([[1, 2, 3], [2, 4], [1]], []) => ', end='')
  print(transversal_dfs_first([[1, 2, 3], [2, 4], [1]], []))
