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

  def is_open_to_land_test(self):
    self.assertFalse(self.board.is_open_to_land(0))
    self.assert_(self.board.is_open_to_land(1))

  def is_hitting_to_land_test(self):
    self.assertFalse(self.board.is_hitting_to_land(0))
    self.assertFalse(self.board.is_hitting_to_land(1))
    self.board.position = \
                ((0, 5, 0, 3, 4, 0,
                  0, 0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0, 0, 0),
                 (0, 0, 0, 0, 0, 5,
                  0, 3, 0, 0, 0, 0,
                  5, 0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0, 1, 1))
    self.assert_(self.board.is_hitting_to_land(0))

  def make_partial_move_1_test(self):
    pm = bglib.model.move.PartialMove(6, 12, 6, False)
    self.board.make_partial_move(pm)
    self.assert_(self.board.position, 
                ((0, 0, 0, 0, 0, 5,
                  1, 3, 0, 0, 0, 0,
                  4, 0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0, 2, 0),
                 (0, 0, 0, 0, 0, 5,
                  0, 3, 0, 0, 0, 0,
                  5, 0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0, 2, 0))
                )
  def make_partial_move_2_test(self):
    self.board.position = \
                ((0, 5, 0, 3, 4, 0,
                  0, 0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0, 0, 0),
                 (0, 0, 0, 0, 0, 5,
                  0, 3, 0, 0, 0, 0,
                  5, 0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0, 1, 1))
    pm = bglib.model.move.PartialMove(1, 1, 0, True)
    self.board.make_partial_move(pm)
    self.assert_(self.board.position, 
                ((1, 4, 0, 3, 4, 0,
                  0, 0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0, 0, 0),
                 (0, 0, 0, 0, 0, 5,
                  0, 3, 0, 0, 0, 0,
                  5, 0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0, 0, 2))
                )

  def make_test(self):
    pass

  def is_leagal_to_roll_test(self):
    self.assertFalse(self.board.is_leagal_to_roll(bglib.model.constants.you))
    self.board.game_state = bglib.model.constants.on_going
    self.assert_(self.board.is_leagal_to_roll(bglib.model.constants.you))
    
  def double_test(self):
    self.assertFalse(self.board.doubled)
    self.board.game_state = bglib.model.constants.on_going

    self.assertEqual(self.board.on_action, bglib.model.constants.you)
    self.assertEqual(self.board.on_inner_action, bglib.model.constants.you)

    self.assertFalse(self.board.is_cube_take_or_pass(bglib.model.constants.you))
    self.assertFalse(self.board.is_cube_take_or_pass(bglib.model.constants.him))
    self.assertFalse(self.board.is_to_accept_resign(bglib.model.constants.you))
    self.assertFalse(self.board.is_to_accept_resign(bglib.model.constants.him))
    self.assertFalse(self.board.is_leagal_to_roll(bglib.model.constants.him))
    self.assertFalse(self.board.is_leagal_to_move(bglib.model.constants.you))
    self.assertFalse(self.board.is_leagal_to_move(bglib.model.constants.him))
    self.assert_(self.board.is_leagal_to_double(bglib.model.constants.you))
    self.assertFalse(self.board.is_leagal_to_double(bglib.model.constants.him))

    self.board.double(bglib.model.constants.you)

    self.assertEqual(self.board.on_action, bglib.model.constants.you)
    self.assertEqual(self.board.on_inner_action, bglib.model.constants.him)
    self.assert_(self.board.doubled)
    self.assertFalse(self.board.is_cube_take_or_pass(bglib.model.constants.you))
    self.assert_(self.board.is_cube_take_or_pass(bglib.model.constants.him))
    self.assertFalse(self.board.is_to_accept_resign(bglib.model.constants.you))
    self.assertFalse(self.board.is_to_accept_resign(bglib.model.constants.him))
    self.assertFalse(self.board.is_leagal_to_roll(bglib.model.constants.you))
    self.assertFalse(self.board.is_leagal_to_roll(bglib.model.constants.him))
    self.assertFalse(self.board.is_leagal_to_move(bglib.model.constants.you))
    self.assertFalse(self.board.is_leagal_to_move(bglib.model.constants.him))
    self.assertFalse(self.board.is_leagal_to_double(bglib.model.constants.you))
    self.assertFalse(self.board.is_leagal_to_double(bglib.model.constants.him))
    
  def is_leagal_to_redouble_test(self):
    self.board.game_state = bglib.model.constants.on_going
    self.assertFalse(self.board.is_leagal_to_redouble(bglib.model.constants.you))
    self.assertFalse(self.board.is_leagal_to_redouble(bglib.model.constants.him))
    self.board.double(bglib.model.constants.you)
    self.assertFalse(self.board.is_leagal_to_redouble(bglib.model.constants.you))
    self.assert_(self.board.is_leagal_to_redouble(bglib.model.constants.him))
    self.board.match_length= 1
    self.assertFalse(self.board.is_leagal_to_redouble(bglib.model.constants.you))
    self.assertFalse(self.board.is_leagal_to_redouble(bglib.model.constants.him))

  def take_test(self):
    self.board.game_state = bglib.model.constants.on_going
    self.board.double(bglib.model.constants.you)
    self.board.take(bglib.model.constants.him)

    self.assert_(self.board.is_leagal_to_roll(bglib.model.constants.you))
    self.assertFalse(self.board.is_leagal_to_roll(bglib.model.constants.him))
    self.assertFalse(self.board.is_leagal_to_move(bglib.model.constants.you))
    self.assertFalse(self.board.is_leagal_to_move(bglib.model.constants.him))
    self.assertFalse(self.board.is_leagal_to_double(bglib.model.constants.you))
    self.assertFalse(self.board.is_leagal_to_double(bglib.model.constants.him))
    self.assertFalse(self.board.is_to_accept_resign(bglib.model.constants.you))
    self.assertFalse(self.board.is_to_accept_resign(bglib.model.constants.him))

  def drop_1_test(self):
    self.board.game_state = bglib.model.constants.on_going
    self.board.double(bglib.model.constants.you)

    self.board.drop(bglib.model.constants.him)

    self.assertEqual(self.board.game_state, bglib.model.constants.doubled_out)
    self.assertEqual(self.board.score, (1, 0))

  def drop_2_test(self):
    self.board.game_state = bglib.model.constants.on_going
    self.board.score = (1, 3)
    self.board.cube_in_logarithm = 3
    self.board.on_action = bglib.model.constants.him
    self.board.on_inner_action = bglib.model.constants.him
    self.board.double(bglib.model.constants.him)

    self.board.drop(bglib.model.constants.you)

    self.assertEqual(self.board.game_state, bglib.model.constants.doubled_out)
    self.assertEqual(self.board.score, (1, 11))

  def is_leagal_to_resign_test(self):
    self.board.game_state = bglib.model.constants.on_going
    self.assert_(self.board.is_leagal_to_resign(bglib.model.constants.you))

  def offer_resign_1_test(self):
    self.board.game_state = bglib.model.constants.on_going
    self.assertEqual(self.board.score, (0, 0))

    self.board.offer_resign(bglib.model.constants.you, bglib.model.constants.resign_single)
    self.assert_(self.board.is_to_accept_resign(bglib.model.constants.him))
    self.board.reject_resign(bglib.model.constants.him)

    self.assertEqual(self.board.on_action, bglib.model.constants.you)
    self.assertEqual(self.board.on_inner_action, bglib.model.constants.you)
    self.assertFalse(self.board.is_cube_take_or_pass(bglib.model.constants.you))
    self.assertFalse(self.board.is_cube_take_or_pass(bglib.model.constants.him))
    self.assertFalse(self.board.is_to_accept_resign(bglib.model.constants.you))
    self.assertFalse(self.board.is_to_accept_resign(bglib.model.constants.him))
    self.assertFalse(self.board.is_leagal_to_roll(bglib.model.constants.him))
    self.assertFalse(self.board.is_leagal_to_move(bglib.model.constants.you))
    self.assertFalse(self.board.is_leagal_to_move(bglib.model.constants.him))
    self.assert_(self.board.is_leagal_to_double(bglib.model.constants.you))
    self.assertFalse(self.board.is_leagal_to_double(bglib.model.constants.him))
    self.assertEqual(self.board.score, (0, 0))

  def offer_resign_2_test(self):
    self.board.game_state = bglib.model.constants.on_going
    self.board.cube_in_logarithm = 3
    self.assertEqual(self.board.score, (0, 0))

    self.board.on_action = bglib.model.constants.him
    self.board.on_inner_action = bglib.model.constants.him
    self.board.offer_resign(bglib.model.constants.him, bglib.model.constants.resign_backgammon)
    self.assert_(self.board.is_to_accept_resign(bglib.model.constants.you))

    self.board.accept_resign(bglib.model.constants.you)

    self.assertEqual(self.board.game_state, bglib.model.constants.resigned)
    self.assertEqual(self.board.score, (24, 0))



