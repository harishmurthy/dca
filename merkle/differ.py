#!/usr/bin/env python

import argparse
import hashtree
import json
from binascii import hexlify

"""
Compare given two files and print the difference / create JSON patch file.

args:
file1: First file to be compared. Patch file will be created with reference to this.
file2: Second file to be compared with.
patchfile: Optional, if provided, JSON patch is written to this.
"""
def cmp(file1,file2,patchfile=None):
  content = {}
  if patchfile:
    ld1 = hashtree.text_merkle_tree(file1,content)
  else:
    ld1 = hashtree.text_merkle_tree(file1)
  ld2 = hashtree.text_merkle_tree(file2)
  mt1 = hashtree.buildtree(ld1)
  mt2 = hashtree.buildtree(ld2)
  if mt1.digest != mt2.digest:
    print('files differ')
    l = []
    mt1.comparewith(mt2,l)
    l.sort()
    print('differing lines: ' + str(l))
    if patchfile:
      with open(patchfile,'w') as f:
        patch = {}
        patch['file'] = file2
        patch['topdigest'] = hexlify(mt1.digest)
        patch['diff'] = [x[4:] for x in l]
        for x in l:
          patch[x[4:]] = content[x[4:]]
          patch[x] = ld1[x]
        json.dump(patch,f,indent=1)
        print('patch written to ' + patchfile)
  else:
    print('files identical')

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("file1", help="Input File 1")
  parser.add_argument("file2", help="Input File 2")
  parser.add_argument("-p","--patchfile", help="Write differnce as JSON to PATCHFILE")
  args = parser.parse_args()
  cmp(args.file1,args.file2,args.patchfile)
