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
  trice indexing
'''

def t2k(t):
  us, them = t
  if True:
    xs = [(us[i], them[i]) for i in range(6)]
    xs = list()
    for i, j in zip(us, them):
      xs.append(i)
      xs.append(j)
  else:
    xs = tuple(reversed(us + them))

  c = count(xs)
  if c == 0:
    return 0
  elif c == 1:
    b = [0]
    for i in xs:
      b += [1 for j in range(i)]
      b.append(0)
    return 1 + C_Hash(b, c)
  else:
    b = [0]
    for i in xs:
      b += [1 for j in range(i)]
      b.append(0)
    return D(c - 1, 7) ** 2 + C_Hash(b, c)

def trice_indexing(position):
  return 0

def human_readable_eq(t):
  CenterCubeEq, OpponentHasCubeEq, RollerHasCubeEq, CPW = t
  return CenterCubeEq, OpponentHasCubeEq*2, RollerHasCubeEq*2, CPW

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

