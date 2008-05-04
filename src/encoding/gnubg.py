#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2006-2008 Noriyuki Hosaka nori@backgammon.gr.jp
#
from base64 import standard_b64encode, standard_b64decode

# local 
#from bglib.encoding.base import *
import bglib.encoding.base


def encode_position(xs):
  """ encodes tuple expression into gnubg position id """
  return standard_b64encode(bglib.encoding.base.twoside_encode(xs)).rstrip('=')


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
  return bglib.encoding.base.twoside_decode(bin)


def single_int(bitarray):
  return bitarray.int()
  
def single_boolean(bitarray):
  return bitarray.int()!=0

def double_int_tuple(bitarray):
  n = bitarray.size
  upper=bitarray[:n/2]
  bottom = bitarray[n/2:n]
  return upper.int(), bottom.int()

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
    begin, end, func = self.index[name]
    if func:
      return func(self._data[begin:end])
    return self._data[begin:end]

  def __setattr__(self, name, value):
    pass

  def __init__(self, s=None):
    self.__dict__['_data'] = bglib.encoding.base.BitArray(66, binary=s, endian='<')

  def decode(self, s):
    self._data = bglib.encoding.base.BitArray(s)

  def encode(self):
    return self._data.binary
    

def encode_match(m):
  return standard_b64encode(m.encode()).rstrip('=')

def decode_match(s):
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
  return MatchProxy(bin)

def encode(model):
  pid = bglib.encoding.gnubg.encode_position(model.position)
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
  return pid, mid

def decode(model, pid, mid):
  model.position = decode_position(pid)
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

def convert_to_urlsafe(s):
  return s.replace('+', '-').replace('/', '_')


def convert_from_urlsafe(s):
  return s.replace('-', '+').replace('_', '/')


if __name__ == '__main__':
  import doctest
  doctest.testfile('gnubg.test')

