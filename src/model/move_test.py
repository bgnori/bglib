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

class MoveTest(unittest.TestCase):
  def setUp(self):
    self.board = bglib.model.board.board()
    self.pm = bglib.model.move.PartialMove(6, 23, 17, False)
    self.mv = bglib.model.move.Move()
    self.mf = bglib.model.move.MoveFactory(self.board)
    self.temp = tempfile.NamedTemporaryFile()

  def tearDown(self):
    pass

  def av_non_doubles_test(self):
    av = bglib.model.move.AvailableToPlay((3, 2))
    self.assertEqual(av[1], 0)
    self.assertEqual(av[2], 1)
    self.assertEqual(av[3], 1)
    self.assertEqual(av[4], 0)
    self.assertEqual(av[5], 0)
    self.assertEqual(av[6], 0)

    self.assertFalse(1 in av)
    self.assert_(2 in av)
    self.assert_(3 in av)
    self.assertFalse(4 in av)
    self.assertFalse(5 in av)
    self.assertFalse(6 in av)

    self.assertEqual(len(av), 2)
    self.assertEqual(av.items(), [(1, 0), (2, 1), (3, 1), (4, 0), (5, 0), (6, 0)])
    self.assertFalse(av.is_doubles())
    self.assertEqual(repr(av), '<AvailableToPlay: [(1, 0), (2, 1), (3, 1), (4, 0), (5, 0), (6, 0)]>')
    self.assertEqual(3, av.get_max())

    av.consume(2)
    
    self.assertEqual(av[1], 0)
    self.assertEqual(av[2], 0)
    self.assertEqual(av[3], 1)
    self.assertEqual(av[4], 0)
    self.assertEqual(av[5], 0)
    self.assertEqual(av[6], 0)

    self.assertFalse(1 in av)
    self.assertFalse(2 in av)
    self.assert_(3 in av)
    self.assertFalse(4 in av)
    self.assertFalse(5 in av)
    self.assertFalse(6 in av)

    self.assertEqual(len(av), 1)
    self.assertEqual(av.items(), [(1, 0), (2, 0), (3, 1), (4, 0), (5, 0), (6, 0)])
    self.assertFalse(av.is_doubles())
    self.assertEqual(repr(av), '<AvailableToPlay: [(1, 0), (2, 0), (3, 1), (4, 0), (5, 0), (6, 0)]>')
    self.assertEqual(3, av.get_max())

    try:
      av.consume(4)
      self.assertFalse(True, 'exception must be raised')
    except:
      pass

    av.add(4)

    self.assertEqual(av[1], 0)
    self.assertEqual(av[2], 0)
    self.assertEqual(av[3], 1)
    self.assertEqual(av[4], 1)
    self.assertEqual(av[5], 0)
    self.assertEqual(av[6], 0)

    self.assertFalse(1 in av)
    self.assertFalse(2 in av)
    self.assert_(3 in av)
    self.assert_(4 in av)
    self.assertFalse(5 in av)
    self.assertFalse(6 in av)

    self.assertEqual(len(av), 2)
    self.assertEqual(av.items(), [(1, 0), (2, 0), (3, 1), (4, 1), (5, 0), (6, 0)])
    self.assertFalse(av.is_doubles())
    self.assertEqual(repr(av), '<AvailableToPlay: [(1, 0), (2, 0), (3, 1), (4, 1), (5, 0), (6, 0)]>')

    self.assertEqual(4, av.get_max())


  def av_doubles_test(self):
    av = bglib.model.move.AvailableToPlay((4, 4))
    self.assertEqual(av[1], 0)
    self.assertEqual(av[2], 0)
    self.assertEqual(av[3], 0)
    self.assertEqual(av[4], 4)
    self.assertEqual(av[5], 0)
    self.assertEqual(av[6], 0)

    self.assertFalse(1 in av)
    self.assertFalse(2 in av)
    self.assertFalse(3 in av)
    self.assert_(4 in av)
    self.assertFalse(5 in av)
    self.assertFalse(6 in av)

    self.assertEqual(len(av), 4)
    self.assertEqual(av.items(), [(1, 0), (2, 0), (3, 0), (4, 4), (5, 0), (6, 0)])
    self.assert_(av.is_doubles())
    self.assertEqual(repr(av), '<AvailableToPlay: [(1, 0), (2, 0), (3, 0), (4, 4), (5, 0), (6, 0)]>')

  def av_creation_by_copy_test(self):
    src = bglib.model.move.AvailableToPlay((3, 2))
    av = bglib.model.move.AvailableToPlay(copy_src=src)
    self.assertNotEqual(id(src), id(av))

    self.assertEqual(av[1], 0)
    self.assertEqual(av[2], 1)
    self.assertEqual(av[3], 1)
    self.assertEqual(av[4], 0)
    self.assertEqual(av[5], 0)
    self.assertEqual(av[6], 0)

    self.assertFalse(1 in av)
    self.assert_(2 in av)
    self.assert_(3 in av)
    self.assertFalse(4 in av)
    self.assertFalse(5 in av)
    self.assertFalse(6 in av)

    self.assertEqual(len(av), 2)
    self.assertEqual(av.items(), [(1, 0), (2, 1), (3, 1), (4, 0), (5, 0), (6, 0)])
    self.assertFalse(av.is_doubles())
    self.assertEqual(repr(av), '<AvailableToPlay: [(1, 0), (2, 1), (3, 1), (4, 0), (5, 0), (6, 0)]>')

  def pm_1_test(self):
    pm = bglib.model.move.PartialMove(6, 12, 6, True)
    self.assertEqual(repr(pm), "<PartialMove: 13/7*>")
    self.assert_(pm.is_hitting)
    self.assertFalse(pm.is_undo())

  def pm_2_test(self):
    pm = bglib.model.move.PartialMove(1, 24, 23, False)
    self.assertEqual(repr(pm), "<PartialMove: bar/24>")
    self.assertFalse(pm.is_hitting)
    self.assertFalse(pm.is_undo())

  def pm_3_test(self):
    pm = bglib.model.move.PartialMove(4, 3, -1, False)
    self.assertEqual(repr(pm), "<PartialMove: 4/off>")
    self.assertFalse(pm.is_hitting)
    self.assertFalse(pm.is_undo())

  def pm_4_test(self):
    pm = bglib.model.move.PartialMove(4, 3, 3, False)
    self.assertFalse(pm.is_undo())
    self.assert_(pm.is_dance())

  def pm_5_test(self):
    pm = bglib.model.move.PartialMove(4, -1, 3, False)
    self.assertEqual(repr(pm), "<PartialMove: off/4>")
    self.assert_(pm.is_undo())

    pm2 = bglib.model.move.PartialMove(4, 3, -1, False)
    self.assert_(pm2.are_invertible_element(pm))

