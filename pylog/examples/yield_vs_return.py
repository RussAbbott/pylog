

# In this example, the results are sent backward through implicit yield's rather than returns. That is,
# the nested for-loops send their results to the previous ones essentially through yield statements.
print('1. ', end = '')
xyz_s = [ x+y+z for x in 'ab' for y in ("de" if x == 'a' else 'fg') for z in ('hi' if y == 'd' else 'jk')]
for xyz in xyz_s:
  print(xyz, end = ', ')
print()

# Can we do this with nested function calls? This is the same thing, but but done without yields.
# The results are the same, but the only way to get them is at the bottom of nested calls. Note that
# there are no return statements. Things are always passed forward.

print('2. ', end='')

def top2():
  for x in 'ab':
    middle2(x)

def middle2(x):
  for y in ("de" if x == 'a' else 'fg'):
    bottom2(x, y)

def bottom2(x, y):
  for z in ('hi' if y == 'd' else 'jk'):
    print(x+y+z, end = ', ')

top2()
print()


# Here's an attempted alternative using return.
# This produces only the first triple because each for-loop is exited after the first element.

def top3( ):
  for x in 'ab':
    return x+middle3(x)

def middle3(x):
  for y in ("de" if x == 'a' else 'fg'):
    return y+bottom3(x, y)

def bottom3(x, y):
  for z in ('hi' if y == 'd' else 'jk'):
    return z

print('3.', top3())


# But when done with yield instead of return, we get the same result as 1. The results are
# returned to and printed at the top. This works because the downward calls are done in for-loops
# rather than direct function calls, and the results are returned through yields rather than return
# statements. A yield does n0t terminate the for-loop within which it is embedded -- just like the
# first example.

def top4( ):
  for x in 'ab':
    for yz in middle4(x):
      yield x+yz

def middle4(x):
  for y in ("de" if x == 'a' else 'fg'):
    for z in bottom4(x, y):
      yield y+z

def bottom4(x, y):
  for z in ('hi' if y == 'd' else 'jk'):
    yield z

print('4. ', end='')
for xyz in top4():
  print(xyz, end = ', ')

