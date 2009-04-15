#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2006-2009 Noriyuki Hosaka bgnori@gmain.com
#

import unittest
from bglib.stat.tourney import *

class ModelTest(unittest.TestCase):
  def setUp(self):
    pass
  def tearDown(self):
    pass

  def test_tourney_chance_0(self):
    self.assertEqual(tourney_chance(1000.0, 1000.0, 3, 7),
                     (0.125, 0.125))

  def test_tourney_chance_1(self):
    self.assertEqual(tourney_chance(1000.0, 1000.0, 3, 5),
                     (0.125, 0.125))

  def test_tourney_chance_2(self):
    self.assertEqual(tourney_chance(1000.0, 1000.0, 2, 5),
                     (0.25, 0.25))

  def test_tourney_chance_3(self):
    self.assertEqual(
        tourney_chance(1100.0, 1000.0, 2, 5),
        (0.31810288776584317, 0.24590321837649565))

  def test_tourney_chance_4(self):
    self.assertEqual(
        tourney_chance(1000.0, 1100.0, 2, 5),
        (0.19009067548116554, 0.24590321837649565))

  def test_prize_handicap(self):
    self.assertEqual(
        prize_handicap(1000.0, 1000.0, 4, 7, 100.0, 30.0),
        (100.0, 30.0))

  def test_entryfee_handicap(self):
    self.assertEqual(
        entryfee_handicap(1000.0, 1000.0, 4, 7, 100.0),
        100.0)

  def test_make_tourney_and_run(self):
    t = Tourney(2)
    while len(t.alive) > 1:
      t.round()
    self.assertEqual(len(t.alive), 1)
    
  def test_make_tourney_and_run(self):
    t = Tourney(2, 
        entries={'a':Player(1, 1010),
                'b':Player(1, 1110),
                'c':Player(1, 910),
                'd':Player(1, 1210),}
        )
    while len(t.alive) > 1:
      t.round()
    self.assertEqual(len(t.alive), 1)
    
