from random import random
import sys

# read the --paremreal= flag
paramreal = 0.0
for arg in sys.argv:
    if arg.startswith('--paramreal='):
        paramreal = float(arg[len('--paramreal='):])

# read the --x flag
x = 10
for arg in sys.argv:
    if arg.startswith('--x'):
        x = int(arg[len('--x'):])

print(paramreal / x, end='')
