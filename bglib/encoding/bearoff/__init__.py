#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2006-2009 Noriyuki Hosaka nori@backgammon.gr.jp
#
from tonic.combination import fact, C, C_Hash, C_RHash


'''
  utilities
'''

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


def D(n, m):
  '''D of Walter Trice.
  http://www.bkgm.com/rgb/rgb.cgi?view+371

  rem.
  D(n, m) == D(n, m -1) + D(n -1, m)
  '''
  return C(n+m-1, m)


def D_Hash(t, x):
  pass

def D_RHash():
  pass


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


class DBReader(object):
  def __init__(self):
    self.f = None
  
  def open(self, path):
    self.f = file(path, 'rb', self.datalen)

  def close(self):
    self.f.close()

  def rawread(self, index):
    assert index is not None
    self.f.seek(index*self.datalen)
    buf = ''
    while len(buf) < self.datalen:
      read = self.f.read(self.datalen, )
      if read:
        buf += read
      else:
        raise IndexError('Database: out of range')
    return buf[:self.datalen]

  def dump(self, index):
    pass
  def human_readable(self, position_number):
    pass

  def __getitem__(self, key):
    return self.dump(self.key_to_index(key))

