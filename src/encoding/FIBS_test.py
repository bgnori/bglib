#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2006-2008 Noriyuki Hosaka nori@backgammon.gr.jp
#

import unittest

from FIBS import _FIBSBoardState

class FIBSTest(unittest.TestCase):
  def setUp(self):
    self.board = _FIBSBoardState('board:You:someplayer:3:0:0:0:-2:0:0:0:0:5:0:3:0:0:0:-5:5:0:0:0:-3:0:-5:0:0:0:0:2:0:1:6:2:0:0:1:1:1:0:1:-1:0:25:0:0:0:0:2:0:0:0')
  def tearDown(self):
    pass
  def data_test(self):
    self.assertEqual(self.board.data, ['board', 'You', 'someplayer', '3', '0', '0', '0', '-2', '0', '0', '0', '0', '5', '0', '3', '0', '0', '0', '-5', '5', '0', '0', '0', '-3', '0', '-5', '0', '0', '0', '0', '2', '0', '1', '6', '2', '0', '0', '1', '1', '1', '0', '1', '-1', '0', '25', '0', '0', '0', '0', '2', '0', '0', '0'])

  def index_access_test(self):
    b = self.board
    self.assertEqual(b.data[b.index['you'][0]:b.index['you'][1]], ['You'])

  def name_access_test(self):
    b = self.board
    self.assertEqual(b.you, 'You')
    self.assertEqual(b.him, 'someplayer')
    self.assertEqual(b.matchlength, 3)
    self.assertEqual(b.your_score, 0)

    self.assertEqual(b.his_score, 0)
    self.assertEqual(b.board, (0, -2, 0, 0, 0, 0, 5, 0, 3, 0, 0, 0, -5, 5, 0, 0, 0, -3, 0, -5, 0, 0, 0, 0, 2, 0))

    self.assertEqual(b.turn, 1)
    self.assertEqual(b.your_dice, (6, 2))

    self.assertEqual(b.his_dice, (0, 0))

    self.assertEqual(b.doubling_cube, 1)

    self.assertEqual(b.you_may_double, 1)

    self.assertEqual(b.he_may_double, 1)

    self.assertEqual(b.was_doubled, 0)

    # This means you are O. If got -1, your are X.
    self.assertEqual(b.your_colour, 1)

    # This means you are playing from position 24 to position 1. 
    # If got 1 yor are playing from position 1 to position 24.
    self.assertEqual(b.your_direction, -1)
    self.assertEqual(b.your_home, 0)
    self.assertEqual(b.your_bar, 25)
    self.assertEqual(b.your_chequers_on_home, 0)
    self.assertEqual(b.his_chequers_on_home, 0)

    self.assertEqual(b.your_chequers_on_bar, 0)

    self.assertEqual(b.his_chequers_on_bar, 0)

    # How many chequers can you play?
    self.assertEqual(b.your_chequers_to_play, 2)

    # redouble for unlimited games. we are talking about beaver!
    self.assertEqual(b.redoubles, 0)

    self.assertEqual(b.position(), 
      ((0, 0, 0, 0, 0, 5, 0, 3, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0),
       (0, 0, 0, 0, 0, 5, 0, 3, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0)))

  def decode_test(self):
    import bglib.model.board
    b = bglib.model.board.board()
    from FIBS import decode 
    decode(b, 'board:You:MonteCarlo:1:0:0:0:3:0:0:0:0:0:0:0:0:0:0:0:0:0:0:0:0:0:0:0:0:0:-1:-2:0:1:2:2:0:0:1:1:1:0:1:-1:0:25:12:12:0:0:3:1:0:0')
    self.assertEqual(b.position, 
      ((3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
       (2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0))
       )

