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

class ModelTest(unittest.TestCase):
  def setUp(self):
    self.board = bglib.model.board.board()
    self.temp = tempfile.NamedTemporaryFile()

  def tearDown(self):
    pass

  def position_test(self):
    self.assert_(self.board.position, 
                ((0, 0, 0, 0, 0, 5,
                  0, 3, 0, 0, 0, 0,
                  5, 0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0, 2, 0),
                 (0, 0, 0, 0, 0, 5,
                  0, 3, 0, 0, 0, 0,
                  5, 0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0, 2, 0))
                )

  def cube_in_logarithm_test(self):
    self.assertEqual(self.board.cube_in_logarithm, 0)
    self.board.cube_in_logarithm = 3
    self.assertEqual(self.board.cube_in_logarithm, 3)

  def cube_owner_test(self):
    self.assertEqual(self.board.cube_owner, bglib.model.constants.center)
    self.board.cube_owner = bglib.model.constants.you
    self.assertEqual(self.board.cube_owner, bglib.model.constants.you)

  def default_value_test(self):
    self.assertEqual(self.board.on_action, bglib.model.constants.you)
    self.assertEqual(self.board.crawford, False)
    self.assertEqual(self.board.game_state, bglib.model.constants.not_started)
    self.assertEqual(self.board.on_inner_action, bglib.model.constants.you)
    self.assertEqual(self.board.doubled, False)
    self.assertEqual(self.board.resign_offer,
                     bglib.model.constants.resign_none)
    self.assertEqual(self.board.rolled, (0, 0))
    self.assertEqual(self.board.match_length, 0)
    self.assertEqual(self.board.score, (0, 0))

  def move_test(self):
    self.assert_(self.board.has_chequer_to_move(23))
    self.assertFalse(self.board.has_chequer_to_move(24))
    #FIXME need test for hitting case
    #FIXME need test for enter
    #FIXME need test for bear off

  def bearoff_test(self):
    self.assertFalse(self.board.is_ok_to_bearoff_from(5 ,6))
    self.assertFalse(self.board.is_ok_to_bearoff_from(2 ,5))
    self.board.position = \
                ((0, 5, 0, 3, 4, 0,
                  0, 0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0, 0, 0),
                 (0, 0, 0, 0, 0, 5,
                  0, 3, 0, 0, 0, 0,
                  5, 0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0, 2, 0))
    self.assert_(self.board.is_ok_to_bearoff_from(4, 5))
    self.assert_(self.board.is_ok_to_bearoff_from(4, 6))
    self.assertFalse(self.board.is_ok_to_bearoff_from(5, 6))
    self.assert_(self.board.is_ok_to_bearoff_from(4, 5))
    self.assertFalse(self.board.is_ok_to_bearoff_from(2, 5))
    self.assertFalse(self.board.is_ok_to_bearoff_from(3, 2))

  def find_src_of_bearoff_with_test(self):
    self.assertEqual(self.board.find_src_of_bearoff_with(5), None)
    self.assertEqual(self.board.find_src_of_bearoff_with(2), None)
    self.board.position = \
                ((0, 5, 0, 3, 4, 0,
                  0, 0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0, 0, 0),
                 (0, 0, 0, 0, 0, 5,
                  0, 3, 0, 0, 0, 0,
                  5, 0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0, 2, 0))
    self.assert_(self.board.has_chequer_to_move(4))
    self.assertEqual(self.board.find_src_of_bearoff_with(5), 4)
    self.assertFalse(self.board.has_chequer_to_move(5))
    self.assertEqual(self.board.find_src_of_bearoff_with(6), 4)
    self.assertEqual(self.board.find_src_of_bearoff_with(2), 1)
    self.assertFalse(self.board.has_chequer_to_move(2))
    self.assertEqual(self.board.find_src_of_bearoff_with(3), None)




