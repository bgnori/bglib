#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2006-2009 Noriyuki Hosaka bgnori@gmain.com
#

import unittest
from bglib.stat.rating import *

class ModelTest(unittest.TestCase):
  def setUp(self):
    pass
  def tearDown(self):
    pass
    
  def test_upset_chance(self):
    self.assertEqual(upset_chance(1100, 1000, 9),
                     0.41450132132819051)

  def test_winning_chance(self):
    self.assertEqual(winning_chance(1100, 1000, 9),
                     1.0 - 0.41450132132819051)

  def test_gain_on_win_0(self):
    self.assertEqual(gain_on_win(1000, 1100, 9),
                     5.2694881080462856)

  def test_gain_on_win_1(self):
    self.assertEqual(gain_on_win(1100, 1000, 9),
                     3.7305118919537144)



