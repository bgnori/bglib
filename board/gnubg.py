#!/usrbin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2006-2008 Noriyuki Hosaka nori@backgammon.gr.jp
#
from base64 import standard_b64encode, standard_b64decode
from base import *


def encode_position(xs):
  """ encodes tuple expression into gnubg position id """
  return standard_b64encode(twoside_encode(xs)).rstrip('=')


def decode_position(s):
  """ decode tuple expression from gnubg position id """
  while True:
    try:
      bin = standard_b64decode(s)
    except TypeError, e:
      if str(e) != 'Incorrect padding':
        raise
      s += '='
    else:
      break
  return twoside_decode(bin)


bits_in_byte = 8 # 1 byte == 8 bits

def byte_length(length_in_bit):
  if length_in_bit % bits_in_byte:
    roundup = 1
  else:
    roundup = 0
  return length_in_bit / bits_in_byte + roundup


import struct

class BitArray:
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

  def _getpos(self, nth):
    if not isinstance(nth, int):
      raise TypeError('index must be int')
    if 0 >  nth or nth >= self.size:
      raise IndexError('out of range')


    pos_of_byte = nth/bits_in_byte

    if self.endian == '<':
      pos_in_byte = nth%bits_in_byte
    elif self.endian == '>':
      pos_in_byte =(7 - nth%bits_in_byte) 

    return (pos_of_byte, pos_in_byte)

  def __len__(self):
    return self.size

  def __getitem__(self, nth):
    pos_of_byte, pos_in_byte = self._getpos(nth)
    fmt = '%s%iB'%(self.endian, byte_length(self.size))
    byte = struct.unpack(fmt, self.binary)[pos_of_byte]

    if byte & 1 << pos_in_byte:
      return 1
    else:
      return 0

  def __setitem__(self, nth, value):
    if not value in (0, 1):
      raise ValueError('value for asignment must be 0 or 1')
    pos_of_byte, pos_in_byte = self._getpos(nth)

    #fmt = '%sB'%(self.endian) 
    fmt = '=B'
    data = list(struct.unpack(fmt, self.binary[pos_of_byte]))[0]

    if value:
        data |= 1 << pos_in_byte
    else:
      data &= ~(1 << pos_of_byte)
    self.binary = (self.binary[:pos_of_byte]
                   + struct.pack(fmt, data) 
                   + self.binary[pos_of_byte+1:]
                   )[:self.size]

  def __iter__(self):
    pass
      

  '''unsupported'''
  def __contains__(self, item):raise NotImplemented
  def __delitem__(self, key):raise NotImplemented
  def __add__(self, x):raise NotImplemented
  def __radd__(self, x):raise NotImplemented
  def __iadd__(self, x):raise NotImplemented
  def __mul__(self, x): raise NotImplemented
  def __rmul__(self, x): raise NotImplemented
  def __imul__(self, x): raise NotImplemented



class MatchProxy(object):
  '''you:him'''

  def __getattr__(self, name):
    pass
  def __setattr__(self, name, value):
    pass
  def __init__(self):
    self.__dict__['_data']=BitArray()

  def decode(self, s):
    self.__dict__['_data']=BitArray(s)

  def encode(self):
    return self.__dict__['_data']
    


def encode_match(s):
  mp = MatchProxy()
  return mp.encode()


def decode_match(s):
  return MatchProxy().decode(s)


def convert_to_urlsafe(s):
  return s.replace('+', '-').replace('/', '_')


def convert_from_urlsafe(s):
  return s.replace('-', '+').replace('_', '/')


if __name__ == '__main__':
  import doctest
  doctest.testfile('gnubg.test')

