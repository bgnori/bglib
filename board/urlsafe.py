#!/usrbin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2006-2008 Noriyuki Hosaka nori@backgammon.gr.jp
#

from base64 import urlsafe_b64encode, urlsafe_b64decode
from base import *

def urlsafe_position_encode(xs):
  """ encode tuple expression into urlsafe gnubg position id"""
  return urlsafe_b64encode(twoside_encode(xs)).rstrip('=')

def urlsafe_position_decode(s):
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

def urlsafe_match_encode(m):
  pass

def urlsafe_match_decode(s):
  pass

if __name__ == '__main__':
  import doctest
  doctest.testfile('urlsafe.test')

