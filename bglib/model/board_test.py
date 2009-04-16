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
    self.temp = tempfile.NamedTemporaryFile()

  def tearDown(self):
    pass

  def bad_setattr_test(self):
    try:
      board = Board()
      board.foobar = 1
      self.assert_(False)
    except:
      pass

  def position_test(self):
    board = Board()
    self.assert_(board.position, 
                ((0, 0, 0, 0, 0, 5,
                  0, 3, 0, 0, 0, 0,
                  5, 0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0, 2, 0),
                 (0, 0, 0, 0, 0, 5,
                  0, 3, 0, 0, 0, 0,
                  5, 0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0, 2, 0))
                )

  def find_src_of_bearoff_with_1_test(self):
    board = Board()
    self.assertEqual(board.find_src_of_bearoff_with(5), None)
    self.assertEqual(board.find_src_of_bearoff_with(2), None)

  def find_src_of_bearoff_with_2_test(self):
    board = Board(
                position=((0, 5, 0, 3, 4, 0,
                  0, 0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0, 0, 0),
                 (0, 0, 0, 0, 0, 5,
                  0, 3, 0, 0, 0, 0,
                  5, 0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0, 2, 0))
                  )
    self.assert_(board.has_chequer_to_move(4))
    self.assertEqual(board.find_src_of_bearoff_with(5), 4)
    self.assertFalse(board.has_chequer_to_move(5))
    self.assertEqual(board.find_src_of_bearoff_with(6), 4)
    self.assertEqual(board.find_src_of_bearoff_with(2), 1)
    self.assertFalse(board.has_chequer_to_move(2))
    self.assertEqual(board.find_src_of_bearoff_with(3), None)

  def is_open_to_land_test(self):
    board = Board()
    self.assertFalse(board.is_open_to_land(0))
    self.assert_(board.is_open_to_land(1))

  def is_hitting_to_land_2_test(self):
    board = Board()
    self.assertFalse(board.is_hitting_to_land(0))
    self.assertFalse(board.is_hitting_to_land(1))
  def is_hitting_to_land_1_test(self):
    board = Board(position = \
                ((0, 5, 0, 3, 4, 0,
                  0, 0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0, 0, 0),
                 (0, 0, 0, 0, 0, 5,
                  0, 3, 0, 0, 0, 0,
                  5, 0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0, 1, 1))
                  )
    self.assert_(board.is_hitting_to_land(0))

  def cube_owner_1_test(self):
    board = Board()
    self.assertEqual(board.cube_owner, CENTER)

  def cube_owner_2_test(self):
    board = Board(cube_owner = YOU)
    self.assertEqual(board.cube_owner, YOU)



