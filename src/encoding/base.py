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


bits_in_byte = 8 # 1 byte == 8 bits

def byte_length(length_in_bit):
  if length_in_bit % bits_in_byte:
    roundup = 1
  else:
    roundup = 0
  return length_in_bit / bits_in_byte + roundup



class BitsArray(object):
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

  def set_shiftable(self, value, begin, end):
    d = value
    for n in range(begin, end):
      d, m = divmod(d, 2)
      self[n] = m

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
      assert isinstance(nth_or_slice.start, int)
      assert isinstance(nth_or_slice.stop, int)
      slice_length = nth_or_slice.stop - nth_or_slice.start
      ret = BitsArray(size=slice_length, 
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
    return "<BitsArray Instance '%s'>"%(':'.join(map(str, list(self))))

  '''unsupported'''
  def __contains__(self, item):raise NotImplemented
  def __delitem__(self, key):raise NotImplemented
  def __add__(self, x):raise NotImplemented
  def __radd__(self, x):raise NotImplemented
  def __iadd__(self, x):raise NotImplemented
  def __mul__(self, x): raise NotImplemented
  def __rmul__(self, x): raise NotImplemented
  def __imul__(self, x): raise NotImplemented

