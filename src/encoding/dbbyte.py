#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2006-2008 Noriyuki Hosaka nori@backgammon.gr.jp
#

from bglib.model.board import board as Board
from bglib.model import constants


# I do not need them in python 3.x
# we have bytes.

def signedord(c):
  assert isinstance(c, str)
  assert len(c) == 1
  o = ord(c)
  if o > 127:
    return o - 256
  return o

def signedchr(n):
  assert isinstance(n, int)
  assert -129 < n
  assert n < 128
  if n < 0:
    return chr(256 + n)
  return chr(n)


def encode_position(xs):
  assert isinstance(xs, tuple)
  onaction, opponent = xs
  assert len(onaction) == 25
  assert len(opponent) == 25

  # adding opp bar.
  onaction = (0,) + onaction 
  opponent = (0,) + opponent

  return  ''.join([signedchr(onaction[i] - opponent[25-i]) 
                   for i in range(0, 26)])


def decode_position(s):
  assert isinstance(s, str)
  assert len(s) == 26
  onaction = [n > 0 and n or 0 for n in 
              (signedord(c) for c in s)]
  opponent = [n < 0 and -n or 0 for n in 
              (signedord(c) for c in reversed(s))]
  return (tuple(onaction[1:]), tuple(opponent[1:]))


def distance(xs, ys):
  d = 0
  for x, y in zip(xs, ys):
    d += (signedord(x) - signedord(y))**2
  return d


class DatabaseBytesExpression(object):
  def __new__(cls, init=None):
    self = object.__new__(cls)
    if init is None:
      init = Board()
    assert isinstance(init , Board)
    for key in Board.defaults.keys():
      item = getattr(init, key)
      if key == 'position':
        if init.on_action == constants.you:
          self.__dict__[key] = encode_position(item)
        elif init.on_action == constants.him:
          self.__dict__[key] = encode_position((item[1], item[0]))
        else:
          assert False
      else:
        self.__dict__[key] = item
    return self

  def __getattr__(self, name):
    assert name in Board.defaults
    return self._data[name]

  def __setattr__(self, name, value):
    assert False # immutable

  def tomodel(self):
    b = Board()
    for key in Board.defaults.keys():
      item = getattr(self, key)
      if key == 'position':
        if self.on_action == constants.you:
          b.__dict__[key] = decode_position(item)
        elif init.on_action == constants.him:
          p = decode_position(item)
          b.__dict__[key] = (p[1], p[0])
        else:
          assert False
      else:
        b.__dict__[key] = item
    return b

