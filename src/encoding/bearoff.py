#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2006-2008 Noriyuki Hosaka nori@backgammon.gr.jp
#

import struct
from bglib.encoding.base import C
from bglib.encoding.gnubg import decode_position


def f(b, n, r):
  assert b > -1
  assert n > -1
  assert r > -1
  if n == r:
    return 0
  if b & ( 1 << n - 1):
    return C(n - 1, r) + f(b, n - 1, r - 1 )
  else:
    return f(b, n - 1, r)

def oneside_index(t, p, c):
  j = p - 1
  for i in range(0, p):
    j += t[i]
  bits = 1 << j

  for i in range(0, p):
    j -= t[i] + 1
    if j > -1:
      bits |= (1 << j)
    else:
      pass
      #bits |= (1 >> -j)
  return f(bits, p+c ,p)

def backward(t):
  i = 24
  while not t[i]:
    i -= 1
  return i + 1

def count(t):
  sum = 0
  for x in t:
    sum += x
  return sum

def bearoff_param(us, them):
  return max(backward(us), backward(them), 0), \
         max(count(us), count(them), 0)

def gnubg_Hugh_indexing(key):
  assert isinstance(key, str)
  pid, mid = key.split(":")[:2]
  us, them = decode_position(pid)

  points, chequers = bearoff_param(us, them)
  nUs = oneside_index(us, points, chequers)
  nThem = oneside_index(them, points, chequers)
  #return 54263*(nUs - 1) + (nThem - 1)
  #return  54264 * nUs + nThem # never this one. position 1(offset 0) is chequer less position
  '''
  C(6+15, 15) = 54264
  Trice has same format as Hugh does, I hope.
  from gnubg/bearoff.c, 
  commit 78145a54c041c66e67080791d1c40500e634c80
  /*
   * Hugh does not score positions will all chequers off:
   * gnubg calculate position# as 54264 * nUs + nThem.
   * Hugh uses                    54263 * ( nUs -1 ) + ( nThem - 1 )
   * The difference is:           nUs + 54263 + 1
   */
  '''

def trice_indexing(key):
  assert isinstance(key, str)
  pid, mid = key.split(":")[:2]
  us, them = decode_position(pid)
  points, chequers = bearoff_param(us, them)

  return oneside_index(us+them, points, chequers)


def key_to_index(key):
  assert isinstance(key, str)
  return trice_indexing(key)

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

