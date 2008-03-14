#!/usrbin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2006-2008 Noriyuki Hosaka nori@backgammon.gr.jp
#

from struct import pack, unpack

def _fact(n):
  if n == 0:
    return 1
  elif n == 1:
    return 1
  else:
    return fact(n-1)*n

class Fact:
  def __init__(self):
    self._cache = list()
    self._cache.append(1) #  0! = 1
    self._cache.append(1) #  1! = 1

  def _expand(self):
    self._cache.append(self._cache[-1] * len(self._cache))

  def __contains__(self, n):
    return len(self._cache) > n
    
  def __call__(self, n):
    assert(n >= 0)
    while n not in self:
      self._expand()
    return self._cache[n]

fact = Fact()


class Combination:
  def __init__(self):
    self._cache = dict()
    self._update(0, 0, 1) # C(0, 0)
    self._size = 1

  def _update(self, n, r, value):
    self._cache.update({(n, r): value})

  def _read(self, n, r):
    if n < 0 or r < 0:
      return 0
    elif n < r:
      return 0
    else:
      return self._cache[(n, r)]

  def _expand(self):
    if self._size > 100:
      import sys
      print len(self._cache)
      sys.exit('too big cache')
    n = self._size 
    for i in range(0, n+1):
      self._update(n=n, 
                   r=i, 
                   value=self._read(n=n-1, r=i-1)+self._read(n=n-1, r=i)
                  )
    self._size = n + 1

  def __contains__(self, n):
    return self._size > n

  def __call__(self, n, r):
    while n not in self:
      self._expand()
    return self._read(n, r)
C = Combination()


def D(n, m):
  '''D of Walter Trice.
  http://www.bkgm.com/rgb/rgb.cgi?view+371
  '''
  return C(n+m-1, m)

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


def C_Hash(xs, r):
  '''perfect hash for Combination, such as
    C(5, 2)  xs = [1, 0, 1, 0, 0]
  '''
  n = len(xs) - 1
  i = 0
  hash = 0
  while n >= r and r > 0:
    if xs[i]:
      hash += C(n, r)
      r-=1
    i+=1
    n-=1
  return hash


def C_RHash(x, n, r):
  '''Reverse function of C_Hash.
  parameters are hash value x, and C(n, r)
  retuns xs
  '''
  result = list()
  for i in range(n, 0, -1):
    if x >= C(i - 1, r):
      result.append(1)
      x -= C(i - 1, r)
      r -= 1
    else:
      result.append(0)
  return result


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
    r = pack('<B', self.byte)
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
    byte = unpack('<B', fragment)[0]
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
  return (tuple(xs[:25]), tuple(xs[25:50]))


if __name__ == '__main__':
  import doctest
  doctest.testfile('base.test', )
