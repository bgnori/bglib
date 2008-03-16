#!/usrbin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2006-2008 Noriyuki Hosaka nori@backgammon.gr.jp
#

from base64 import urlsafe_b64encode, urlsafe_b64decode
from base import *
from gnubg import MatchProxy

def encode_position(xs):
  """ encode tuple expression into urlsafe gnubg position id"""
  return urlsafe_b64encode(twoside_encode(xs)).rstrip('=')

def decode_position(s):
  """decode tuple expression from urlsafe gnubg position id"""
  while True:
    try:
      bin = urlsafe_b64decode(s)
    except TypeError, e:
      if str(e) != 'Incorrect padding':
        raise
      s += '='
    else:
      break
  return twoside_decode(bin)


def encode_match(m):
  return urlsafe_b64encode(m.encode()).rstrip('=')


def decode_match(s):
  """ decode tuple expression from gnubg position id """
  while True:
    try:
      bin = urlsafe_b64decode(s)
    except TypeError, e:
      if str(e) != 'Incorrect padding':
        raise
      s += '='
    else:
      break
  return MatchProxy(bin)

if __name__ == '__main__':
  import doctest
  doctest.testfile('urlsafe.test')

