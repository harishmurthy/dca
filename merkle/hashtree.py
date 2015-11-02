#! bin/python

import argparse
import json
from merkle import text_merkle_tree
from binascii import unhexlify,hexlify
from collections import deque
from hashlib import md5

class TreeNode:
  def __init__(self,left=None,right=None,chunkid=None,digest=None):
    self.left = left
    self.right= right
    self.chunkid = chunkid
    self.digest = digest

  def comparewith(self,other,l):
    if self.left:
      if other.left:
        if self.left.digest != other.left.digest:
          self.left.comparewith(other.left,l)
      else:
        self.left.getchunks(l)
    if self.right:
      if other.right:
        if self.right.digest != other.right.digest:
          self.right.comparewith(other.right,l)
      else:
        self.right.getchunks(l)
    if self.left is None:
      if self.right is None:
        if other:
          if self.digest != other.digest:
            self.getchunks(l)
        else:
          self.getchunks(l)

  def getchunks(self,l):
    if self.left:
      self.left.getchunks(l)
    if self.right:
      self.right.getchunks(l)
    if self.chunkid:
      l.append(self.chunkid)

  def printtree(self):
    if self.left:
      self.left.printtree()
    if self.right:
      self.right.printtree()
    if self.chunkid:
      print('chunk: ' + str(self.chunkid) + ' -> ' + hexlify(self.digest))

def buildtree(leafdict):
  ml = deque()
  for x in leafdict:
    ml.append(TreeNode(chunkid=x,digest=unhexlify(leafdict[x])))
  if len(ml) % 2:
    t = ml.popleft()
    ml.append(TreeNode(right=t,digest=t.digest))
  while len(ml) > 1:
    l = ml.popleft()
    r = ml.popleft()
    ml.append(TreeNode(left=l,right=r,digest=md5(l.digest + r.digest).digest()))
  return ml.pop()

def hashtreeify(infile):
  ld = text_merkle_tree(infile)
  mt = buildtree(ld)
  ld['topdigest'] = hexlify(mt.digest)
  ld['file'] = infile
  return ld

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("file", help="File for which hash tree is needed")
  parser.add_argument("outfile", help="Output File containing hash tree")
  args = parser.parse_args()
  ld = hashtreeify(args.file)
  with open(args.outfile,'w') as f:
    json.dump(ld,f,indent=1)
