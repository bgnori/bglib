#!/usrbin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2006-2008 Noriyuki Hosaka nori@backgammon.gr.jp
#
from base64 import standard_b64encode, standard_b64decode
from base import *


def gnubg_position_encode(xs):
  """ encodes tuple expression into gnubg position id """
  return standard_b64encode(twoside_encode(xs)).rstrip('=')


def gnubg_position_decode(s):
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


def convert_to_urlsafe(s):
  return s.replace('+', '-').replace('/', '_')


def convert_from_urlsafe(s):
  return s.replace('-', '+').replace('_', '/')


if __name__ == '__main__':
  import doctest
  doctest.testfile('gnubg.test')

