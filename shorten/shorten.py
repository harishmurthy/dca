#!/usr/bin/env python

import hashlib
import hmac
import argparse
import struct

_table = ['s', 'H', 'o', 'R', 't', 'E', 'n', 'U', 'r', 'L' ]

_key = "shortenurl"

_shorturl = 'http://short.xyz/'

def _truncated_value(h):
    v = h[-1]
    if not isinstance(v, int): v = ord(v) # Python 2.x
    offset = v & 0xF
    (value,) = struct.unpack('>I', h[offset:offset + 4])
    return value & 0x7FFFFFFF

def _dec(h,p):
    th = _truncated_value(h)
    digits = str(th)
    return digits[-p:].zfill(p)

def shorten(long_url):
    s = ''
    h = hmac.new(_key,long_url, hashlib.sha1).digest()
    d = _dec(h, 8)
    for i in d:
        s += _table[int(i)]
    return _shorturl + s

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  group = parser.add_mutually_exclusive_group(required=True)
  group.add_argument('-l', '--longurl', help="Url to be shortened")
  group.add_argument("-f", "--urlfile", help="Input file with long urls separated by newline")
  args = parser.parse_args()
  if args.longurl:
      print(shorten(args.longurl))
  else:
      with open(args.urlfile,'r') as f:
          for l in f:
              print(shorten(l))
