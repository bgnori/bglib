#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2006-2008 Noriyuki Hosaka nori@backgammon.gr.jp
#

from bglib.encoding.gnubgid import decode_position
import bglib.encoding.bearoff
from bglib.encoding.bearoff import C, count, backward


'''
  gnubg indexing
'''
def f(b, n, r):
  assert b > -1
  assert n > -1
  assert r > -1
  if n == r:
    return 0
  if b & ( 1 << n - 1):
    return C(n - 1, r) + f(b, n - 1, r - 1 )
  else:
    return f(b, n - 1, r)

def oneside_index(t, p, c):
  j = p - 1
  for i in range(0, p):
    j += t[i]
  bits = 1 << j

  for i in range(0, p):
    j -= t[i] + 1
    if j > -1:
      bits |= (1 << j)
    else:
      pass
      #bits |= (1 >> -j)
  return f(bits, p+c ,p)

def bearoff_param(us, them):
  return max(backward(us), backward(them), 0), \
         max(count(us), count(them), 0)

def gnubg_Hugh_indexing(key):
  assert isinstance(key, str)
  pid, mid = key.split(":")[:2]
  us, them = decode_position(pid)

  points, chequers = bearoff_param(us, them)
  nUs = oneside_index(us, points, chequers)
  nThem = oneside_index(them, points, chequers)
  #return 54263*(nUs - 1) + (nThem - 1)
  #return  54264 * nUs + nThem # never this one. position 1(offset 0) is chequer less position
  '''
  C(6+15, 15) = 54264
  Trice has same format as Hugh does, I hope.
  from gnubg/bearoff.c, 
  commit 78145a54c041c66e67080791d1c40500e634c80
  /*
   * Hugh does not score positions will all chequers off:
   * gnubg calculate position# as 54264 * nUs + nThem.
   * Hugh uses                    54263 * ( nUs -1 ) + ( nThem - 1 )
   * The difference is:           nUs + 54263 + 1
   */
  '''

class DBRreader(bglib.encoding.bearoff.DBReader):
  datalen = 16 #ugh!
  def key_to_index(self):
    return 0

