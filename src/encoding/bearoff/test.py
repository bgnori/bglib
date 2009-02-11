#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2006-2009 Noriyuki Hosaka bgnori@gmail.com
#
import unittest

from bglib.encoding.bearoff import * 

class recursiveDTest(unittest.TestCase):
  def bgcombination_1_test(self):
    sum = 0
    for m in range(0, 16):
      sum += BackgammonCombination(m)
    self.assertEqual(WTN, sum)

  def bgcombination_2_test(self):
    sum = 0
    for m in range(0, 16):
        sum += BackgammonCombination_allC(m)
    self.assertEqual(WTN, sum)

  def test(self):
    for i in range(1, 12):
      for j in range(1, 12):
        print i, j
        self.assertEqual(recursiveD(i, j), D(i, j))



