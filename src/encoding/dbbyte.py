#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2006-2008 Noriyuki Hosaka nori@backgammon.gr.jp
#

from bglib.model.board import board as Board


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

def decode_position(s):
  assert isinstance(s, str)

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


class DatabaseBytesExpression(object):
  def __new__(cls, init=None):
    self = object.__new__(cls)
    if init is None:
      init = Board()
    assert isinstance(init , Board)
    for key, item in Board.defaults.items():
      if key == 'position':
        self.__dict__[key] = str(item)
      else:
        self.__dict__[key] = str(item)
    return self

  def __getattr__(self, name):
    assert name in Board.defaults
    return self._data[name]

  def __setattr__(self, name, value):
    assert False # immutable


