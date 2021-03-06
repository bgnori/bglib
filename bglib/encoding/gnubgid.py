#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2006-2011 Noriyuki Hosaka bgnori@gmail.com
#
import struct

from base64 import standard_b64encode, standard_b64decode

# local 
from tonic import BitsArray
from bglib.model.constants import *
import bglib.encoding


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


def seq2bytes (xs):
  """encode given xs to binary.
  0 2 3 0 ---> 0 110 1110 0 : D mapping to binary.
  and endian is little endian.
  """
  count = 0
  byte = ByteContext()
  for x in xs:
    for i in range(0, x):
      if not byte.write(1):
        count += 1
        yield byte.pack()
    if not byte.write(0):
      count += 1
      yield byte.pack()
  if byte.count != 0:
    yield byte.pad()
  while count < 9:
    count += 1
    yield byte.pad()


def byts2seq(b):
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


#def oneside_encode(xs):
#  return ''.join(list(encode(xs)))


#def oneside_decode(s):
#  return tuple(decode(s))[:25]


def twoside_encode(xs):
  s = list(seq2bytes( list(xs[0])+ list(xs[1])))
  return ''.join(s)


def twoside_decode(s):
  xs = list(byts2seq(s))
  return tuple(xs[:25]), tuple(xs[25:50]) # (on_action, opp)

def encode_position(xs):
  """ encodes tuple expression into gnubg position id """
  return standard_b64encode(twoside_encode(xs)).rstrip('=')


def decode_position(s):
  """ decode tuple expression from gnubg position id """
  if '=' in s:
    raise TypeError
  while True:
    try:
      bin = standard_b64decode(s)
    except TypeError, e:
      if str(e) != 'Incorrect padding':
        raise
      s += '='
    else:
      break
  r = twoside_decode(bin)
  if not len(r) == 2 or not len(r[0])==25 or not len(r[1])==25:
    raise bglib.encoding.DecodeError('got bad data: %s '%(s,))
  return r

class Validator(object):
  def to_bitsarray(self, value, bitsarray, begin, end):
    raise
  def from_bitsarray(self, bitsarray):
    raise

class SingleIntValidator(Validator):
  def to_bitsarray(self, value, bitsarray, begin, end):
    assert isinstance(bitsarray, BitsArray)
    bitsarray.set_shiftable(value, begin, end)
  def from_bitsarray(self, bitsarray):
    return int(bitsarray)

single_int = SingleIntValidator()

class SingleBooleanValidator(Validator):
  def to_bitsarray(self, value, bitsarray, begin, end):
    assert isinstance(bitsarray, BitsArray)
    bitsarray.set_shiftable(value, begin, end)
  def from_bitsarray(self, bitsarray):
    return bool(bitsarray)
single_boolean = SingleBooleanValidator()

class DoubleIntValidator(Validator):
  def to_bitsarray(self, value, bitsarray, begin, end):
    top, bottom = value
    top_begin = begin
    bottom_end = end
    top_end = bottom_begin = begin + (end - begin)/2
    bitsarray.set_shiftable(top, top_begin, top_end)
    bitsarray.set_shiftable(bottom, bottom_begin, bottom_end)

  def from_bitsarray(self, bitsarray):
    n = bitsarray.size
    assert n
    assert isinstance(n, int)
    upper=bitsarray[0:n/2]
    bottom = bitsarray[n/2:n]
    return int(upper), int(bottom)
double_int_tuple = DoubleIntValidator()

class MatchProxy(object):
  '''you:him'''
  index = dict(
      cube_in_logarithm=(0, 4, single_int),
      cube_owner = (4, 6, single_int),
      on_action = (6, 7, single_int),
      crawford = (7, 8, single_boolean),
      game_state = (8, 11, single_int),
      on_inner_action = (11, 12, single_int),
      doubled = (12, 13, single_boolean),
      resign_offer = (13, 15, single_int),
      rolled = (15, 21, double_int_tuple),
      match_length = (21, 36, single_int),
      score = (36, 66, double_int_tuple),
      )

  def __getattr__(self, name):
    begin, end, validator = self.index[name]
    assert validator
    return validator.from_bitsarray(self._data[begin:end])

  def __setattr__(self, name, value):
    begin, end, validator = self.index[name]
    assert validator
    validator.to_bitsarray(value, self._data, begin, end)

  def __init__(self, s=None):
    self.__dict__['_data'] = BitsArray(66, binary=s, endian='<')

  #def decode(self, s):
  #  self._data = BitsArray(s)

  def encode(self):
    return self._data.binary
    

def encode_match(m):
  return standard_b64encode(m.encode()).rstrip('=')

def decode_match(s):
  """ decode tuple expression from gnubg position id """
  if '=' in s:
    raise TypeError
  while True:
    try:
      bin = standard_b64decode(s)
    except TypeError, e:
      if str(e) != 'Incorrect padding':
        raise
      s += '='
    else:
      break
  return MatchProxy(bin)

def encode(model):
  mp = MatchProxy()
  mp.cube_in_logarithm = model.cube_in_logarithm 
  mp.cube_owner = model.cube_owner 
  mp.on_action = model.on_action 
  mp.crawford = model.crawford 
  mp.game_state = model.game_state 
  mp.on_inner_action = model.on_inner_action 
  mp.doubled = model.doubled 
  mp.resign_offer = model.resign_offer 
  mp.rolled = model.rolled 
  mp.match_length = model.match_length 
  mp.score = model.score
  mid = encode_match(mp)

  # this is the difference between gnubg and bglib
  # gnubg's view from on_action 
  # bglib's view from you
  # FIXME: what about on_inner_action?
  if mp.on_action == YOU:
    opp, on_action = model.position
  elif mp.on_action == HIM:
    on_action, opp = model.position
  else:
    assert False
  pid = encode_position((on_action, opp))
  return pid, mid

def decode(model, pid, mid):
  msg = None
  mp = decode_match(mid)
  model.cube_in_logarithm = mp.cube_in_logarithm
  model.cube_owner = mp.cube_owner
  model.on_action = mp.on_action
  model.crawford = mp.crawford
  model.game_state = mp.game_state
  model.on_inner_action = mp.on_inner_action
  model.doubled = mp.doubled
  model.resign_offer = mp.resign_offer
  model.rolled = mp.rolled
  model.match_length = mp.match_length
  model.score = mp.score
 
  # FIXME not sure... 
  if model.game_state == ON_GOING and \
    model.match_length == 0 and  \
    (model.score[0] > model.match_length or \
     model.score[1] > model.match_length):
    msg = 'bad score'

  if msg:
    raise bglib.encoding.InconsistentData(msg + ', got bad data: %s '%(mid,))

  # this is the difference between gnubg and bglib
  # gnubg's view from on_action 
  # bglib's view from you
  # FIXME: what about on_inner_action?
  on_action, opp = decode_position(pid)
  if mp.on_action == 0:#gnubg player 0 == HIM
    you = opp
    him = on_action 
  elif mp.on_action == 1:#gnubg player 1 == YOU
    you = on_action
    him = opp
  else:
    raise bglib.encoding.UndefinedTurn('failed to find who to play. data: %s '%(mid,))
  model.position = (you, him)


#def convert_to_urlsafe(s):
#  return s.replace('+', '-').replace('/', '_')

#def convert_from_urlsafe(s):
#  return s.replace('-', '+').replace('_', '/')



