#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2006-2008 Noriyuki Hosaka nori@backgammon.gr.jp
#

import tempfile
import unittest
import nose

from bglib.model import *
from bglib.model.constants import *


class BoardTest(unittest.TestCase):
  def setUp(self):
    self.board = Board()
    self.temp = tempfile.NamedTemporaryFile()

  def tearDown(self):
    pass

  def bad_setattr_test(self):
    try:
      self.board.foobar = 1
      self.assert_(False)
    except:
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

class BoardEditorTest(unittest.TestCase):
  def setUp(self):
    self.board = BoardEditor()
    self.temp = tempfile.NamedTemporaryFile()

  def tearDown(self):
    pass



  def cube_in_logarithm_test(self):
    self.assertEqual(self.board.cube_in_logarithm, 0)
    self.board.cube_in_logarithm = 3
    self.assertEqual(self.board.cube_in_logarithm, 3)

  def cube_owner_test(self):
    self.assertEqual(self.board.cube_owner, CENTER)
    self.board.cube_owner = YOU
    self.assertEqual(self.board.cube_owner, YOU)

  def default_value_test(self):
    self.assertEqual(self.board.on_action, YOU)
    self.assertEqual(self.board.crawford, False)
    self.assertEqual(self.board.game_state, NOT_STARTED)
    self.assertEqual(self.board.on_inner_action, YOU)
    self.assertEqual(self.board.doubled, False)
    self.assertEqual(self.board.resign_offer,
                     RESIGN_NONE)
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
    pm = PartialMove(6, 12, 6, False)
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
    pm = PartialMove(1, 1, 0, True)
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
    self.assertFalse(self.board.is_leagal_to_roll(YOU))
    self.board.game_state = ON_GOING
    self.assert_(self.board.is_leagal_to_roll(YOU))
    
  def double_test(self):
    self.assertFalse(self.board.doubled)
    self.board.game_state = ON_GOING

    self.assertEqual(self.board.on_action, YOU)
    self.assertEqual(self.board.on_inner_action, YOU)

    self.assertFalse(self.board.is_cube_take_or_pass(YOU))
    self.assertFalse(self.board.is_cube_take_or_pass(HIM))
    self.assertFalse(self.board.is_to_accept_resign(YOU))
    self.assertFalse(self.board.is_to_accept_resign(HIM))
    self.assertFalse(self.board.is_leagal_to_roll(HIM))
    self.assertFalse(self.board.is_leagal_to_move(YOU))
    self.assertFalse(self.board.is_leagal_to_move(HIM))
    self.assert_(self.board.is_leagal_to_double(YOU))
    self.assertFalse(self.board.is_leagal_to_double(HIM))

    self.board.double(YOU)

    self.assertEqual(self.board.on_action, YOU)
    self.assertEqual(self.board.on_inner_action, HIM)
    self.assert_(self.board.doubled)
    self.assertFalse(self.board.is_cube_take_or_pass(YOU))
    self.assert_(self.board.is_cube_take_or_pass(HIM))
    self.assertFalse(self.board.is_to_accept_resign(YOU))
    self.assertFalse(self.board.is_to_accept_resign(HIM))
    self.assertFalse(self.board.is_leagal_to_roll(YOU))
    self.assertFalse(self.board.is_leagal_to_roll(HIM))
    self.assertFalse(self.board.is_leagal_to_move(YOU))
    self.assertFalse(self.board.is_leagal_to_move(HIM))
    self.assertFalse(self.board.is_leagal_to_double(YOU))
    self.assertFalse(self.board.is_leagal_to_double(HIM))
    
  def is_leagal_to_redouble_test(self):
    self.board.game_state = ON_GOING
    self.assertFalse(self.board.is_leagal_to_redouble(YOU))
    self.assertFalse(self.board.is_leagal_to_redouble(HIM))
    self.board.double(YOU)
    self.assertFalse(self.board.is_leagal_to_redouble(YOU))
    self.assert_(self.board.is_leagal_to_redouble(HIM))
    self.board.match_length= 1
    self.assertFalse(self.board.is_leagal_to_redouble(YOU))
    self.assertFalse(self.board.is_leagal_to_redouble(HIM))

  def take_test(self):
    self.board.game_state = ON_GOING
    self.board.double(YOU)
    self.board.take(HIM)

    self.assert_(self.board.is_leagal_to_roll(YOU))
    self.assertFalse(self.board.is_leagal_to_roll(HIM))
    self.assertFalse(self.board.is_leagal_to_move(YOU))
    self.assertFalse(self.board.is_leagal_to_move(HIM))
    self.assertFalse(self.board.is_leagal_to_double(YOU))
    self.assertFalse(self.board.is_leagal_to_double(HIM))
    self.assertFalse(self.board.is_to_accept_resign(YOU))
    self.assertFalse(self.board.is_to_accept_resign(HIM))

  def drop_1_test(self):
    self.board.game_state = ON_GOING
    self.board.double(YOU)

    self.board.drop(HIM)

    self.assertEqual(self.board.game_state, DOUBLED_OUT)
    self.assertEqual(self.board.score, (1, 0))

  def drop_2_test(self):
    self.board.game_state = ON_GOING
    self.board.score = (1, 3)
    self.board.cube_in_logarithm = 3
    self.board.on_action = HIM
    self.board.on_inner_action = HIM
    self.board.double(HIM)

    self.board.drop(YOU)

    self.assertEqual(self.board.game_state, DOUBLED_OUT)
    self.assertEqual(self.board.score, (1, 11))

  def is_leagal_to_resign_test(self):
    self.board.game_state = ON_GOING
    self.assert_(self.board.is_leagal_to_resign(YOU))

  def offer_resign_1_test(self):
    self.board.game_state = ON_GOING
    self.assertEqual(self.board.score, (0, 0))

    self.board.offer_resign(YOU, RESIGN_SINGLE)
    self.assert_(self.board.is_to_accept_resign(HIM))
    self.board.reject_resign(HIM)

    self.assertEqual(self.board.on_action, YOU)
    self.assertEqual(self.board.on_inner_action, YOU)
    self.assertFalse(self.board.is_cube_take_or_pass(YOU))
    self.assertFalse(self.board.is_cube_take_or_pass(HIM))
    self.assertFalse(self.board.is_to_accept_resign(YOU))
    self.assertFalse(self.board.is_to_accept_resign(HIM))
    self.assertFalse(self.board.is_leagal_to_roll(HIM))
    self.assertFalse(self.board.is_leagal_to_move(YOU))
    self.assertFalse(self.board.is_leagal_to_move(HIM))
    self.assert_(self.board.is_leagal_to_double(YOU))
    self.assertFalse(self.board.is_leagal_to_double(HIM))
    self.assertEqual(self.board.score, (0, 0))

  def offer_resign_2_test(self):
    self.board.game_state = ON_GOING
    self.board.cube_in_logarithm = 3
    self.assertEqual(self.board.score, (0, 0))

    self.board.on_action = HIM
    self.board.on_inner_action = HIM
    self.board.offer_resign(HIM, RESIGN_BACKGAMMON)
    self.assert_(self.board.is_to_accept_resign(YOU))

    self.board.accept_resign(YOU)

    self.assertEqual(self.board.game_state, RESIGNED)
    self.assertEqual(self.board.score, (24, 0))



