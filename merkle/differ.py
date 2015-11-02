#! bin/python

import argparse
import hashtree
import merkle
import json
from binascii import hexlify

def cmp():
  parser = argparse.ArgumentParser()
  parser.add_argument("src", help="Source file")
  parser.add_argument("dsttree", help="Merkle Tree file of destination")
  parser.add_argument("-p","--patchfile", help="Write differnce as JSON to PATCHFILE")
  args = parser.parse_args()
  content = {}
  if args.patchfile:
    ld1 = merkle.text_merkle_tree(args.src,content)
  else:
    ld1 = merkle.text_merkle_tree(args.src)
  with open(args.dsttree,'r') as f:
    ld2 = json.load(f)
    ld2.pop('topdigest')
    dfile = ld2.pop('file')
  mt1 = hashtree.buildtree(ld1)
  mt2 = hashtree.buildtree(ld2)
  if mt1.digest != mt2.digest:
    print('files differ')
    l = []
    mt1.comparewith(mt2,l)
    l.sort()
    print('differing lines: ' + str(l))
    if args.patchfile:
      with open(args.patchfile,'w') as f:
        patch = {}
        patch['file'] = dfile
        patch['topdigest'] = hexlify(mt1.digest)
        patch['diff'] = [x[4:] for x in l]
        for x in l:
          patch[x[4:]] = content[x[4:]]
          patch[x] = ld1[x]
        json.dump(patch,f,indent=1)
        print('patch written to ' + args.patchfile)
  else:
    print('files identical')

if __name__ == "__main__":
  cmp()
