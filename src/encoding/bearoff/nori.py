#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2006-2009 Noriyuki Hosaka nori@backgammon.gr.jp
#
import struct
from bglib.encoding.gnubgid import decode_position
from bglib.encoding import bearoff
from bglib.encoding.bearoff import C, C_Hash, C_RHash, D, D_Hash
from bglib.encoding.bearoff import count, backward

'''
  nori's original indexing
'''
sigmaD = dict(((-1, 0), (0, 1),))

for i in range(0, 16):
  sigmaD[i] = sigmaD[i-1] + D(6 , i)

def oneside_upto6_t2k(t):
  assert len(t) == 6
  xs = []
  c = count(t)
  for i in t:
    xs += [1 for j in  range(i)]
    xs.append(0)

  #C_Hash treats  highest bit as Least Significant bit
  xs.reverse()
  return sigmaD[c-1] + C_Hash(xs, c)


def oneside_upto6_k2t(n):
  for c in range(15):
    if n < sigmaD[c]:
      k = 0
      xs = [0, 0, 0, 0, 0, 0]
      print n-sigmaD[c-1],  c
      b = C_RHash(n - sigmaD[c-1], 6+c-1, c)
      print b
      for j in b:
        if j == 1:
          xs[k]+=1
        elif j == 0:
          k+=1
        else:
          assert False
      print xs
      return tuple(reversed(xs))
  assert False


class DBRreader(bearoff.DBReader):
  datalen = 16
  def dump(self, index):
    '''
    chunk is a tuple of four float.
    (CenterCubeEq, OpponentHasCubeEq, RollerHasCubeEq, CPW(??))
    '''
    chunk = self.rawread(index)
    return struct.unpack('ffff', chunk)
  
  def human_readable(self, position_number):
    return human_readable_eq(self.dump(position_number - 1))

  def key_to_index(self):
    return 0


