#! bin/python

import random

_table = ["%c" % x for x in range(ord('A'),ord('Z')+1)]
_table = _table + ["%c" % x for x in range(ord('a'),ord('z')+1)]
_table = _table + ["%c" % x for x in range(ord('0'),ord('9')+1)]
_table.append('#')
_table.append('$')

_pows = [(len(_table)**x)-1 for x in range(1,10)]

_numdigits = 1

_counter = 0

_mem = {}
_mem[0] = _table
random.shuffle(_mem[0])

def gethint():
  global _table
  global _pows
  global _numdigits
  global _counter
  global _mem
  h = ''
  curr = _counter
  for x in range(_numdigits):
    digit = curr & 0x3f
    curr = curr >> 6
    h = h + _mem[x][digit]
  _counter = _counter + 1
  if _counter in _pows:
    _mem[_numdigits] = _table
    random.shuffle(_mem[_numdigits])
    _numdigits = _numdigits + 1
  return h[::-1]

if __name__ == "__main__":
  for x in range(1000):
    print(gethint())
