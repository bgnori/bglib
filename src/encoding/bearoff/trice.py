#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2006-2009 Noriyuki Hosaka nori@backgammon.gr.jp
#
import struct
from bglib.encoding.gnubgid import decode_position
import bglib.encoding.bearoff
from bglib.encoding.bearoff import C, count, backward

'''
  trice indexing
'''
def oneside(xs):
  assert highest(xs) < 6
  return D(count(xs) - 1, 7) + D_Hash(xs, 6)

def recursive_onside(key):
  assert isinstance(key, str)
  pid, mid = key.split(":")[:2]
  us, them = decode_position(pid)
  assert backward(us) < 6
  assert backward(them) < 6
  assert count(us) >= 0
  assert count(them) >= 0
  c = count(us)

  return D(7, c - 1) + C_Hash(us[:6], 6)

def trice_indexing(position):
  pass

def human_readable_eq(t):
  CenterCubeEq, OpponentHasCubeEq, RollerHasCubeEq, CPW = t
  return CenterCubeEq, OpponentHasCubeEq*2, RollerHasCubeEq*2, CPW

class DBRreader(bglib.encoding.bearoff.DBReader):
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

