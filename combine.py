import os, sys

args = sys.argv

def extractData(strs, col=1):
  return map(lambda s: s.split()[col], strs)

f = open(args[1], 'r')
tmp = f.read().splitlines()
f.close()

strs0 = extractData(tmp, 0)
strs1 = extractData(tmp)

f = open(args[2], 'r')
strs2 = extractData(f.read().splitlines())
f.close()

strs = reduce(lambda fs, xs: fs + xs, map(lambda (a, b, c): a + '\t' + b + '\t' + c + '\n', zip(strs0, strs1, strs2)))

f = open(args[3], 'w')
f.write(strs)
f.close()


