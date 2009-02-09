#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2006-2008 Noriyuki Hosaka nori@backgammon.gr.jp
#
from base import * 
import tempfile
import unittest
import nose

import bglib.model.constants
import bglib.model.board
import bglib.model.move

class EncodingTest(unittest.TestCase):
  def setUp(self):
    pass
  def tearDown(self):
    pass

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

  def encode_test(self):
    x = list(encode((0, 0, 0, 0, 0, 5, 2, 3, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)))
    self.assertEqual(x, ['\xe0', '\xdb', '\xc1', '\x03', '\x00'])

  def decode_test(self):
    self.assertEqual(list(decode('\xe0\xdb\xc1\x03\x00')),
      [0, 0, 0, 0, 0, 5, 2, 3, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

  def oneside_decode_encode__test(self):
    self.assertEqual(oneside_decode(oneside_encode((6, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1))),
(6, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1))

  def oneside_encode_decode_test(self):
    self.assertEqual(oneside_decode(oneside_encode((0, 3, 2, 2, 2, 3, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0))), (0, 3, 2, 2, 2, 3, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0))


  def twoside_decode_test(self):
    self.assertEqual(twoside_decode(twoside_encode(((6, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1), (0, 3, 2, 2, 2, 3, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0)))), 
((6, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1), (0, 3, 2, 2, 2, 3, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0)))

class recursiveDTest(unittest.TestCase):
  def test(self):
    for i in range(1, 12):
      for j in range(1, 12):
        print i, j
        self.assertEqual(recursiveD(i, j), D(i, j))


