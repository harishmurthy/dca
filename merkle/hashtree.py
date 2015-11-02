#!/usr/bin/env python

import argparse
import json
from binascii import unhexlify,hexlify
from collections import deque
from hashlib import md5

"""
Class to represent a node in merkle tree.

contains two children - left and right.
chunk id  - indicating the line / block of the content.
digest - the md5 hash of the line / block
"""
class TreeNode:
  def __init__(self,left=None,right=None,chunkid=None,digest=None):
    self.left = left
    self.right= right
    self.chunkid = chunkid
    self.digest = digest

  """
  Comapare this tree with another tree.

  compares the two merkle trees and fills the list with differing chunks.
  """
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

  """
  Return the chunks of the sub tree if any of own chunkid
  """
  def getchunks(self,l):
    if self.left:
      self.left.getchunks(l)
    if self.right:
      self.right.getchunks(l)
    if self.chunkid:
      l.append(self.chunkid)

  """
  Print the merkle tree.
  """
  def printtree(self):
    if self.left:
      self.left.printtree()
    if self.right:
      self.right.printtree()
    if self.chunkid:
      print('chunk: ' + str(self.chunkid) + ' -> ' + hexlify(self.digest))

"""
Build merkle tree that can be compared in logarithmic time using
leaf dictoinary.
"""
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

"""
Build merkle tree of the file in the standard format.

Returns a dictionary with topdigest containing the hash of the entire file,
file containing the file name and rest containing the leaf dictionary.
It is possible to save this / send this to another node to rebuild the
merkle tree.
"""
def hashtreeify(infile):
  ld = text_merkle_tree(infile)
  mt = buildtree(ld)
  ld['topdigest'] = hexlify(mt.digest)
  ld['file'] = infile
  return ld

"""
Build leaf dictionary for the given file.

infile - Input file.
content - content of the file to be used to build patch later.
"""
def text_merkle_tree(infile,content=None):
  with open(infile,'r') as f:
    mer = {}
    lineid = 1
    for x in iter(lambda: f.readline(), ''):
      mer['line'+str(lineid)] = hexlify(md5(x).digest())
      if content is not None:
        content[str(lineid)] = hexlify(x)
      lineid = lineid + 1
    return mer

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("file", help="File for which hash tree is needed")
  parser.add_argument("outfile", help="Output File containing hash tree")
  args = parser.parse_args()
  ld = hashtreeify(args.file)
  with open(args.outfile,'w') as f:
    json.dump(ld,f,indent=1)
