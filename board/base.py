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



bits_in_byte = 8 # 1 byte == 8 bits

def byte_length(length_in_bit):
  if length_in_bit % bits_in_byte:
    roundup = 1
  else:
    roundup = 0
  return length_in_bit / bits_in_byte + roundup


import struct

class BitArray:
  strcut_fmt = '!B'
  def __init__(self, size, binary=None, endian=None):
    self.size = size
    if binary: 
      if len(binary) > byte_length(size):
        raise ValueError('spilling data, %i byte is too long for array size %i bits !'
                         %(len(binary), size))
      self.binary = binary
    else:
      self.binary = '\x00'*byte_length(self.size)
    if endian:
      self.endian = endian
    else:
      self.endian = '<' # little endian

  def __len__(self):
    return self.size

  def int(self):
    ret = 0
    mask = 1
    for bit in self:
      if bit:
        ret |= mask
      mask = mask << 1
    return ret


  def _getbyte(self, pos_of_byte):
    return struct.unpack(self.strcut_fmt, self.binary[pos_of_byte])[0]
  
  def _setbyte(self, pos_of_byte, value):
    self.binary = (self.binary[:pos_of_byte]
                   + struct.pack(self.strcut_fmt, value) 
                   + self.binary[pos_of_byte+1:]
                   )[:self.size]

  def _pos_in_byte(self, nth):
    assert(isinstance(nth, int))
    assert(nth < bits_in_byte)
    assert(0 <= nth)
    if self.endian == '<':
      return nth%bits_in_byte
    elif self.endian == '>':
      return 7 - nth%bits_in_byte
    
  def _getpos(self, nth):
    assert(isinstance(nth, int))
    if 0 >  nth or nth >= self.size:
      raise IndexError('out of range')
    return (nth/bits_in_byte, self._pos_in_byte(nth%bits_in_byte))

  def getnth(self, nth):
    pos_of_byte, pos_in_byte = self._getpos(nth)

    byte = self._getbyte(pos_of_byte)
    if byte & 1 << pos_in_byte:
      return 1
    else:
      return 0

  def __getitem__(self, nth_or_slice):
    if isinstance(nth_or_slice, int):
      return self.getnth(nth_or_slice)
    elif isinstance(nth_or_slice, slice):
      assert(nth_or_slice.step is None)# or nth_or_slice.step == 1)
      slice_length = nth_or_slice.stop - nth_or_slice.start
      ret = BitArray(size=slice_length, 
                     endian=self.endian
                      )
      for i in range(ret.size):
        ret[i] = self.getnth(nth_or_slice.start + i)
      return ret
    else:
      raise TypeError('index must be int or slice, but got %s'%str(type(nth_or_slice)))

  def __setitem__(self, nth, value):
    assert(isinstance(nth, int))
    if not value in (0, 1):
      raise ValueError('value for asignment must be 0 or 1')
    pos_of_byte, pos_in_byte = self._getpos(nth)
    data = self._getbyte(pos_of_byte)

    if value:
      data |= 1 << pos_in_byte
    else:
      data &= ~(1 << pos_in_byte)

    self._setbyte(pos_of_byte, data)

  def __iter__(self):
    for i in range(self.size):
      yield self[i]

  def __repr__(self):
    return "<BitArray Instance '%s'>"%(':'.join(map(str, list(self))))

  '''unsupported'''
  def __contains__(self, item):raise NotImplemented
  def __delitem__(self, key):raise NotImplemented
  def __add__(self, x):raise NotImplemented
  def __radd__(self, x):raise NotImplemented
  def __iadd__(self, x):raise NotImplemented
  def __mul__(self, x): raise NotImplemented
  def __rmul__(self, x): raise NotImplemented
  def __imul__(self, x): raise NotImplemented


def single_int(bitarray):
  return bitarray.int()
  
def single_boolean(bitarray):
  return bitarray.int()!=0

def double_int_tuple(bitarray):
  n = bitarray.size
  upper=bitarray[:n/2]
  bottom = bitarray[n/2:n]
  return upper.int(), bottom.int()


if __name__ == '__main__':
  import doctest
  doctest.testfile('base.test', )
