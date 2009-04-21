#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2006-2008 Noriyuki Hosaka nori@backgammon.gr.jp
#
import unittest
import nose

from bglib.model import *
from bglib.model.constants import *
from bglib.record.gnubg import *


class GnuBGPythonTest(unittest.TestCase):
  def setUp(self):
    pass
  def tearDown(self):
    pass

  def decode_1_test(self):
    b = Board(
      rolled=(1, 3),
      match_length=17,
      game_state=ON_GOING,
      on_action=HIM,
      on_inner_action=HIM,
      )
    t = Tracer(board=b)
    d = {'action': 'move', 'player': 'O',
         'move': ((7, 4), (5, 4)), 'dice': (1, 3),
         'board': '4HPwATDgc/ABMA'}
    t.update(d)
    print t.get_pre_action()
    self.assertEqual(
                     ":".join(encode(t.get_on_roll())),
                     '4HPwATDgc/ABMA:cIksAgAAAAAA')
    self.assertEqual(t.get_on_move(),
                     '4HPwATCwZ/ABMA:cIkIAgAAAAAA')
    self.assertEqual(t.get_on_done(),
                     'sGfwATDgc/ABMA:MAEgAgAAAAAA')

  def decode_2_test(self):
    t = Tracer('sGfwATDgc/ABMA:MAEgAgAAAAAA')
    d = {'action': 'move', 'player': 'X',
          'move': ((12, 10), (5, 4)), 'dice': (1, 2),
          'board': 'sGfwATDgc/ABMA'}
    self.assertEqual(t.get_pre_action(), 
                     'sGfwATDgc/ABMA:MIEoAgAAAAAA')
    self.assertEqual(t.get_post_action(), 
                    '0HPkATCwZ/ABMA:cAkgAgAAAAAA')

  def decode_3_test(self):
    d = {'action': 'move', 'player': 'O', 'move': ((23, 20), (12, 6)), 'dice': (6, 3), 'board': '0HPkATCwZ/ABMA'}
  def decode_4_test(self):
    d = {'action': 'move', 'player': 'X', 'move': ((7, 4), (5, 3)), 'dice': (2, 3), 'board': 'sNfgASLQc+QBMA'}
  def decode_5_test(self):
    d = {'action': 'move', 'player': 'O', 'move': ((24, 22), (7, 6)), 'dice': (1, 2), 'board': 'aGfkATCw1+ABUA'}
  def decode_5_test(self):
    d = {'action': 'move', 'player': 'X', 'move': ((5, 2), (3, 2)), 'dice': (1, 3), 'board': 'sLfgAShoZ+QBMA'}
  def decode_5_test(self):
    d = {'action': 'move', 'player': 'O', 'move': ((23, 20), (12, 8)), 'dice': (3, 4), 'board': 'zGbkATCwt+ABKA'}
  def decode_5_test(self):
    d = {'action': 'move', 'player': 'X', 'move': ((12, 8), (8, 3)), 'dice': (4, 5), 'board': 'sLfCARLMZuQBMA'}
  def decode_5_test(self):
    d = {'action': 'move', 'player': 'O', 'move': ((24, 20), (7, 4)), 'dice': (3, 4), 'board': 'rM3IATCwt8IBSA'}
  def decode_5_test(self):
    d = {'action': 'move', 'player': 'X', 'move': (), 'dice': (5, 5), 'board': 'cG/CARLMZuQAWA'}
  def decode_5_test(self):
    d = {'action': 'move', 'player': 'O', 'move': ((22, 17), (20, 17)), 'dice': (3, 5), 'board': 'zGbkAFhwb8IBEg'}
  def decode_5_test(self):
    d = {'action': 'move', 'player': 'X', 'move': ((24, 23), (12, 10)), 'dice': (1, 2), 'board': 'cG/CwQDMZuQAWA'}
  def decode_5_test(self):
    d = {'action': 'move', 'player': 'O', 'move': ((12, 8), (12, 6)), 'dice': (6, 4), 'board': 'zGbMADhwb8LBAA'}
  def decode_5_test(self):
    d = {'action': 'move', 'player': 'X', 'move': ((23, 21), (21, 16)), 'dice': (2, 5), 'board': 'cO8MwQDMZswAOA'}
  def decode_5_test(self):
    d = {'action': 'move', 'player': 'O', 'move': ((12, 10), (10, 8), (5, 3), (5, 3)), 'dice': (2, 2), 'board': 'zGbMEDBw7wzBAA'}
  def decode_5_test(self):
    d = {'action': 'move', 'player': 'X', 'move': ((16, 11), (11, 8)), 'dice': (5, 3), 'board': '2O0cwADMZswQMA'}
  def decode_5_test(self):
    d = {'action': 'double', 'player': 'O', 'board': 'zGaZATDY7RzAAA'}
    d = {'action': 'take', 'player': 'X'}
    d = {'action': 'move', 'player': 'O', 'move': ((8, 7), (7, 2)), 'dice': (1, 5), 'board': 'zGaZATDY7RzAAA'}

  def decode_5_test(self):
    d = {'action': 'move', 'player': 'X', 'move': ((8, 3), (7, 3)), 'dice': (5, 4), 'board': 'tNsZwADMZpkBMA'}
  def decode_5_test(self):
    d = {'action': 'move', 'player': 'O', 'move': ((8, 3), (6, 2)), 'dice': (5, 4), 'board': 'bJuYATC02xnAAA'}
  def decode_5_test(self):
    d = {'action': 'move', 'player': 'X', 'move': ((7, 1), (3, 1)), 'dice': (6, 2), 'board': '7G4TwABsm5gBMA'}
  def decode_5_test(self):
    d = {'action': 'move', 'player': 'O', 'move': ((8, 7), (7, 5)), 'dice': (1, 2), 'board': 'tjaYATDsbhPAAA'}
  def decode_5_test(self):
    d = {'action': 'move', 'player': 'X', 'move': ((10, 7), (10, 5)), 'dice': (3, 5), 'board': '7O4GwAC2NpgBMA'}
  def decode_5_test(self):
    d = {'action': 'move', 'player': 'O', 'move': (), 'dice': (6, 6), 'board': 'tnaCATDs7gbAAA'}
  def decode_5_test(self):
    d = {'action': 'move', 'player': 'X', 'move': ((7, 3), (5, 3)), 'dice': (2, 4), 'board': '7O4GwAC2doIBMA'}
  def decode_5_test(self):
    d = {'action': 'move', 'player': 'O', 'move': ((5, 4), (4, 1)), 'dice': (1, 3), 'board': 'ttuAATDs7gbAAA'}
  def decode_5_test(self):
    d = {'action': 'move', 'player': 'X', 'move': ((23, 22), (12, 7)), 'dice': (1, 5), 'board': '2t0GwAC224ABMA'}
  def decode_5_test(self):
    d = {'action': 'move', 'player': 'O', 'move': ((24, 23), (4, 1)), 'dice': (1, 3), 'board': 'ttsEASjsbgNgQA'}
  def decode_5_test(self):
    d = {'action': 'move', 'player': 'X', 'move': (), 'dice': (5, 3), 'board': '2m0DYCC22wQBUA'}
  def decode_5_test(self):
    d = {'action': 'move', 'player': 'O', 'move': ((17, 16), (16, 11)), 'dice': (1, 5), 'board': 'ttsEAVDabQNgIA'}
  def decode_5_test(self):
    d = {'action': 'move', 'player': 'X', 'move': ((24, 23),), 'dice': (1, 3), 'board': '2m2DQCC22wAAdA'}
  def decode_5_test(self):
    d = {'action': 'move', 'player': 'O', 'move': ((11, 10), (10, 6)), 'dice': (1, 4), 'board': 'ttsAAGzabYNAIA'}
  def decode_5_test(self):
    d = {'action': 'move', 'player': 'X', 'move': ((24, 23),), 'dice': (1, 5), 'board': '2m0HQCC22wAAbA'}
  def decode_5_test(self):
    d = {'action': 'move', 'player': 'O', 'move': ((23, 17), (17, 13)), 'dice': (6, 4), 'board': 'ttsAAFzabQdAIA'}
  def decode_5_test(self):
    d = {'action': 'move', 'player': 'X', 'move': ((24, 22), (3, 1), (2, 0), (2, 0)), 'dice': (2, 2), 'board': '2m0HhAC22wAAXA'}
  def decode_5_test(self):
    d = {'action': 'move', 'player': 'O', 'move': (), 'dice': (1, 4), 'board': 'O9sAADrstgNCQA'}
  def decode_5_test(self):
    d = {'action': 'move', 'player': 'X', 'move': ((5, 3), (5, 1)), 'dice': (4, 2), 'board': '7LYDQkA72wAAOg'}
  def decode_5_test(self):
    d = {'action': 'move', 'player': 'O', 'move': (), 'dice': (5, 5), 'board': 'e24AADrstgNCQA'}
  def decode_5_test(self):
    d = {'action': 'move', 'player': 'X', 'move': ((3, 0),), 'dice': (3, 5), 'board': '7LYDQkB7bgAAOg'}
  def decode_5_test(self):
    d = {'action': 'move', 'player': 'O', 'move': ((24, 21), (17, 16)), 'dice': (1, 3), 'board': '92wAADrstgNCQA'}
  def decode_5_test(self):
    d = {'action': 'move', 'player': 'X', 'move': ((4, 1), (4, 0)), 'dice': (3, 4), 'board': '7LYDIgj3bAAAOg'}
  def decode_5_test(self):
    d = {'action': 'move', 'player': 'O', 'move': ((16, 12), (13, 9), (9, 5), (5, 1)), 'dice': (4, 4), 'board': '7zMAADrstgMiCA'}
  def decode_5_test(self):
    d = {'action': 'move', 'player': 'X', 'move': ((24, 22), (22, 16)), 'dice': (2, 6), 'board': '2m0HAgjvMwAAXA'}
  def decode_5_test(self):
    d = {'action': 'move', 'player': 'O', 'move': ((24, 18), (21, 17)), 'dice': (6, 4), 'board': '7zMACDjstgMBRA'}
  def decode_5_test(self):
    d = {'action': 'move', 'player': 'X', 'move': ((16, 13), (13, 9)), 'dice': (3, 4), 'board': '7LYDQQHvMwAIOA'}
    d = {'action': 'move', 'player': 'O', 'move': ((17, 16), (16, 11)), 'dice': (1, 5), 'board': '7zMQADjstgNBAQ'}
  def decode_5_test(self):
    d = {'action': 'move', 'player': 'X', 'move': ((9, 8), (8, 5)), 'dice': (1, 3), 'board': '7LaDAgHvMxAAOA'}
    d = {'action': 'move', 'player': 'O', 'move': (), 'dice': (1, 2), 'board': '7zMBADjstoMCQA'}
  def decode_5_test(self):
    d = {'action': 'move', 'player': 'X', 'move': ((5, 3), (3, 0)), 'dice': (2, 3), 'board': '7LaDAkDvMwEAOA'}
  def decode_5_test(self):
    d = {'action': 'move', 'player': 'O', 'move': ((24, 21), (6, 4)), 'dice': (2, 3), 'board': '32cAADjstoMCQA'}
  def decode_5_test(self):
    d = {'action': 'move', 'player': 'X', 'move': ((3, 1),), 'dice': (2, 5), 'board': '7G6DAgjfZwAAOA'}
  def decode_5_test(self):
    d = {'action': 'move', 'player': 'O', 'move': ((21, 20), (12, 6)), 'dice': (1, 6), 'board': '308AADjsboMCCA'}
  def decode_5_test(self):
    d = {'action': 'move', 'player': 'X', 'move': ((24, 22),), 'dice': (2, 2), 'board': '7G4HAQTfDwAAXA'}
  def decode_5_test(self):
    d = {'action': 'move', 'player': 'O', 'move': ((20, 19), (19, 13)), 'dice': (1, 6), 'board': '3w8AADrsbgcBBA'}
  def decode_5_test(self):
    d = {'action': 'move', 'player': 'X', 'move': (), 'dice': (4, 5), 'board': '7G4HCQDfDwAAOg'}
    d = {'action': 'move', 'player': 'O', 'move': ((11, 5), (3, 1)), 'dice': (2, 6), 'board': '3w8AADrsbgcJAA'}
  def decode_5_test(self):
    d = {'action': 'move', 'player': 'X', 'move': (), 'dice': (4, 5), 'board': '2u4OCADfDwAAXA'}
  def decode_5_test(self):
    d = {'action': 'move', 'player': 'O', 'move': ((6, 5), (4, 1)), 'dice': (1, 3), 'board': '3w8AAFza7g4IAA'}
  def decode_5_test(self):
    d = {'action': 'move', 'player': 'X', 'move': ((24, 23),), 'dice': (1, 4), 'board': 'tu0NCADfDwAAXA'}
  def decode_5_test(self):
    d = {'action': 'move', 'player': 'O', 'move': ((13, 7), (5, 3)), 'dice': (2, 6), 'board': '3w8AADy27Q0IAA'}
  def decode_5_test(self):
    d = {'action': 'move', 'player': 'X', 'move': (), 'dice': (2, 3), 'board': 'ttstAADfDwAAPA'}
  def decode_5_test(self):
    d = {'action': 'move', 'player': 'O', 'move': ((6, 3), (6, 2)), 'dice': (3, 4), 'board': '3w8AADy22y0AAA'}
  def decode_5_test(self):
    d = {'action': 'move', 'player': 'X', 'move': ((1, 0),), 'dice': (1, 5), 'board': 'dm8nAADfDwAAPA'}
  def decode_5_test(self):
    d = {'action': 'move', 'player': 'O', 'move': ((7, 2), (5, -1)), 'dice': (6, 5), 'board': 'vw8AADx2bycAAA'}
  def decode_5_test(self):
    d = {'action': 'move', 'player': 'X', 'move': ((23, 17), (17, 12)), 'dice': (5, 6), 'board': '9t4GAIDfBwAAHg'}
  def decode_5_test(self):
    d = {'action': 'move', 'player': 'O', 'move': ((4, 3), (4, -1)), 'dice': (1, 5), 'board': 'vw+AADj23gYAAA'}
  def decode_5_test(self):
    d = {'action': 'move', 'player': 'X', 'move': ((23, 17), (12, 10)), 'dice': (2, 6), 'board': '9j4DAMDvAyAADg'}
  def decode_5_test(self):
    d = {'action': 'move', 'player': 'O', 'move': ((3, -1), (2, -1)), 'dice': (3, 4), 'board': 'vw8gIDD2PgMAAA'}
    d = {'action': 'move', 'player': 'X', 'move': ((17, 15), (10, 5)), 'dice': (2, 5), 'board': 'ds8AAPD7AAICAw'}
  def decode_5_test(self):
    d = {'action': 'move', 'player': 'O', 'move': ((5, 4), (5, 4), (3, 2), (2, 1)), 'dice': (1, 1), 'board': 'vw8BCDB2zwAAAA'}
  def decode_5_test(self):
    d = {'action': 'move', 'player': 'X', 'move': ((23, 17), (15, 10)), 'dice': (5, 6), 'board': '7m4AAPD7EIAAAw'}
  def decode_5_test(self):
    d = {'action': 'move', 'player': 'O', 'move': ((4, -1), (3, -1)), 'dice': (4, 5), 'board': 'vw9BQCDubgAAAA'}
  def decode_5_test(self):
    d = {'action': 'move', 'player': 'X', 'move': ((17, 11), (10, 5)), 'dice': (6, 5), 'board': '7hYAAPw+BAGBAA'}
  def decode_5_test(self):
    d = {'action': 'move', 'player': 'O', 'move': ((4, -1), (3, -1), (3, -1), (2, -1)), 'dice': (6, 6), 'board': 'vw8DASDuFgAAAA'}
  def decode_5_test(self):
    d = {'action': 'move', 'player': 'X', 'move': ((23, 17), (17, 15)), 'dice': (6, 2), 'board': 'bgAAwO/DQAAIAA'}
  def decode_5_test(self):
    d = {'action': 'move', 'player': 'O', 'move': ((2, -1), (2, -1)), 'dice': (6, 5), 'board': 'vw8DIQBuAAAAAA'}
  def decode_5_test(self):
    d = {'action': 'move', 'player': 'X', 'move': ((15, 10), (11, 5)), 'dice': (6, 5), 'board': 'DgAA8PswEAIAAA'}
    d = {'action': 'move', 'player': 'O', 'move': ((1, 0), (1, -1)), 'dice': (1, 5), 'board': 'vw8HAQAOAAAAAA'}
  def decode_5_test(self):
    d = {'action': 'move', 'player': 'X', 'move': ((10, 9), (9, 6)), 'dice': (1, 3), 'board': 'BQAA+H04CAAAAA'}
  def decode_5_test(self):
    d = {'action': 'resign', 'player': 'X'}

