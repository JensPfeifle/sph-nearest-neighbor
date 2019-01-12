import numpy as numpy

file1 = "interactionpairs.dat"
file2 = "interactionpairs_compare.dat"

with open(file1, 'r') as f:
    pairs1 = [line.split() for line in f.readlines()[1:]]


with open(file2, 'r') as f:
    pairs2 = [line.split() for line in f.readlines()[1:]]

diff1 = [p for p in pairs1 if p not in pairs2]
print("{} points in file1 but not in {}".format(len(diff1), file2))

diff2 = [p for p in pairs2 if p not in pairs1]
print("{} points in file2 but not in {}".format(len(diff2), file1))

