#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2006-2009 Noriyuki Hosaka nori@backgammon.gr.jp
#
import struct

from tonic.math import fact, C, C_Hash, C_RHash

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


