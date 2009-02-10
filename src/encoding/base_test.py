#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2006-2008 Noriyuki Hosaka nori@backgammon.gr.jp
#
import tempfile
import unittest
import nose

import bglib.model.constants
import bglib.model.board
import bglib.model.move
from bglib.encoding.base import * 

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


