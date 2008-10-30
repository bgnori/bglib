#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2006-2008 Noriyuki Hosaka nori@backgammon.gr.jp
#

import struct
import bglib.encoding.base

def key_to_index(key):
  assert isinstance(key, (tuple, str))
  return 0

def human_readable_eq(t):
  CenterCubeEq, OpponentHasCubeEq, RollerHasCubeEq, CPW = t
  return CenterCubeEq, OpponentHasCubeEq*2, RollerHasCubeEq*2, CPW

DATALEN = 16
class DBReader(object):
  def __init__(self):
    self.f = None
  
  def open(self, path):
    self.f = file(path, 'rb', 16)

  def close(self):
    self.f.close()

  def rawread(self, index):
    assert index is not None
    self.f.seek(index*DATALEN)
    buf = ''
    while len(buf) < DATALEN:
      read = self.f.read(DATALEN, )
      if read:
        buf += read
      else:
        raise IndexError('Database: out of range')
    return buf[:DATALEN]

  def dump(self, index):
    '''
    chunk is a tuple of four float.
    (CenterCubeEq, OpponentHasCubeEq, RollerHasCubeEq, CPW(??))
    '''
    chunk = self.rawread(index)
    return struct.unpack('ffff', chunk)

  def human_readable(self, position_number):
    return human_readable_eq(self.dump(position_number - 1))

  def __getitem__(self, key):
    return self.dump(key_to_index(key))

