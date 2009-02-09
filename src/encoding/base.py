#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2006-2008 Noriyuki Hosaka nori@backgammon.gr.jp
#

import struct

from tonic.math import fact, C, C_Hash, C_RHash
from tonic.cache import hub
from tonic.cache.imp import Dict
from tonic.cache import memoize

hub.connect(Dict())

@memoize(hub)
def D(n, m):
  '''D of Walter Trice.
  http://www.bkgm.com/rgb/rgb.cgi?view+371
  '''
  return C(n+m-1, m)

def recursiveD(n, m):
  if n == 1:
    return 1
  elif m == 1:
    return n
  else:
    return recursiveD(n, m-1) + recursiveD(n-1, m)


WTN = 18528584051601162496
'''
WTN : Walter Trice Number, number of Possible Backgammon Position.
  http://www.bkgm.com/rgb/rgb.cgi?view+371
'''

def BackgammonCombination(m):
  '''possible backgammon position'''
  return C(24, m) * D(m+2, 15-m) * D(26-m, 15)


def BackgammonCombination_allC(m):
  '''by definition of D, it must give same result.'''
  return C(24, m) * C(16, 15-m) * C(40-m, 15)


def D_Hash(xs, m):
  ''' perfect hash for D)(n, m)  = C(n+m-1, m) # definition
#>>> D_Hash((6, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0,\
             0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1), 15)

#>>> D_Hash((0, 3, 2, 2, 2, 3, 0, 0, 1, 0, 0, 0, \
             0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0), 15)
  '''
  count = 0
  for x in xs:
    if x:
      count+=1
  return C_Hash(xs, count)


class ByteContext:
  def __init__(self):
    self.byte = 0 # r'\x00'
    self.count = 0
    
  def write(self, bit):
    self.byte |= bit << self.count
    self.count += 1
    return self.count < 8
    
  def pack(self):
    r = struct.pack('<B', self.byte)
    self.reset()
    return r

  def pad(self):
    for i in range(self.count, 8): # padding
      self.write(0)
    return self.pack()

  def reset(self):
    self.byte = 0 # r'\x00'
    self.count = 0


def encode(xs):
  """encode given xs to binary.
  0 2 3 0 ---> 0 110 1110 0 : D mapping to binary.
  and endian is little endian.
  """
  byte = ByteContext()
  for x in xs:
    for i in range(0, x):
      if not byte.write(1):
        yield byte.pack()
    if not byte.write(0):
      yield byte.pack()
  if byte.count == 0:
    raise StopIteration
  else:
    yield byte.pad()


def decode(b):
  n = 0
  for fragment in b:
    byte = struct.unpack('<B', fragment)[0]
    for j in range(8):
      if byte & (1 << j):
        n += 1
      else:
        yield n
        n = 0
  yield n


def oneside_encode(xs):
  return ''.join(list(encode(xs)))


def oneside_decode(s):
  return tuple(decode(s))[:25]


def twoside_encode(xs):
  s = list(encode( list(xs[0])+ list(xs[1])))
  return ''.join(s)


def twoside_decode(s):
  xs = list(decode(s))
  return tuple(xs[:25]), tuple(xs[25:50]) # (on_action, opp)

