#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2006-2008 Noriyuki Hosaka nori@backgammon.gr.jp
#

import tempfile
import unittest
import nose

import bglib.model.board

from bglib.encoding.gnubg import *

class gnubgTest(unittest.TestCase):
  def setUp(self):
    pass
  def tearDown(self):
    pass
  def encode_1_test(self):
    self.assertEqual(encode_position(
         ((6, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1),
          (0, 3, 2, 2, 2, 3, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0))),
        'vzsAAFhu2xFABA')
  def encode_2_test(self):
    self.assertEqual(encode_position(
         ((0, 0, 0, 0, 0, 5, 0, 3, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0),
          (0, 0, 0, 0, 0, 5, 0, 3, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0))),
        '4HPwATDgc/ABMA')

  def decode_1_test(self):
    self.assertEqual(decode_position("vzsAAFhu2xFABA"),
                    ((6, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1),
                     (0, 3, 2, 2, 2, 3, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0)))
  def decode_2_test(self):
    self.assertEqual(decode_position("4HPwATDgc/ABMA"),
                    ((0, 0, 0, 0, 0, 5, 0, 3, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0),
                     (0, 0, 0, 0, 0, 5, 0, 3, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0)))

    # This test based on the document from
    # http://www.gnu.org/manual/gnubg/html_node/A-technical-description-of-the-Match-ID.html
    # initialize MatchProxy with little endian.

class MatchProxyTest(unittest.TestCase):
  def setUp(self):
    self.m = MatchProxy('\x41\x89\x2a\x01\x20\x00\x20\x00\x00')
  def tearDown(self):
    pass
  def MatchProxy_bitsarray_test(self):
    m = self.m
    s = ''.join(map(str, list(m._data)))
    self.assertEqual(s, '100000101001000101010100100000000000010000000000000001000000000000')

    # this is big endian, because we but bits in order of from m[0] to m[7], m[8] to m[-1]
    # In little endian, it is 
    # '010000011000100100101010000000010010000000000000001000000000000000'

    self.assertEqual(m._data[0], 1)
    self.assertEqual(m._data[1], 0)
    self.assertEqual(m._data[2], 0)
    self.assertEqual(m._data[3], 0)

    self.assertEqual(repr(m._data[0:4]), "<BitsArray Instance '1:0:0:0'>")
    self.assertEqual(repr(m._data[0:8]), "<BitsArray Instance '1:0:0:0:0:0:1:0'>")
    self.assertEqual(repr(m._data[8:16]), "<BitsArray Instance '1:0:0:1:0:0:0:1'>")

  def MatchProxy_bit_from_1_to_5_test(self):
    """Bit 1-4 contains the 2-logarithm of the cube value. For example, a 8-cube is encoded as 0011 binary (or 3), since 2 to the power of 3 is 8. The maximum value of the cube in with this encoding is 2 to the power of 15, i.e., a 32768-cube."""
    m = self.m
    self.assertEqual(m.cube_in_logarithm, 1)

  def MatchProxy_bit_from_5_to_7_test(self):
    """Bit 5-6 contains the cube owner. 00 if player 0 owns the cube, 01 if player 1 owns the cube, or 11 for a centered cube. """
    m = self.m
    self.assertEqual(m.cube_owner, 0)

  def MatchProxy_bit_from_7_to_8_test(self):
    '''Bit 7 is the player on roll or the player who did roll (0 and 1 for player 0 and 1, respectively).'''
    m = self.m
    self.assertEqual(m.on_action, 1)

  def MatchProxy_bit_from_8_to_9_test(self):
    """Bit 8 is the Crawford flag: 1 if this game is the Crawford game, 0 otherwise."""
    m = self.m
    self.assertEqual(m.crawford, False)

  def MatchProxy_bit_from_9_to_11_test(self):
    """Bit 9-11 is the game state: 
       000 for no game started, 
       001 for playing a game, 
       010 if the game is over, 
       011 if the game was resigned, or 
       100 if the game was ended by dropping a cube.
      0 000 no game started  < 1
      1 001 playing game   1 == 
      2 010 games is over  1 < 
      3 011 game was resigned
      4 100 game was over with pass"""
    m = self.m
    self.assertEqual(m.game_state, 1)

  def MatchProxy_bit_from_11_to_12_test(self):
    """Bit 12 indicates whose turn it is. For example, 
       suppose player 0 is on roll then bit 7 above will be 0. 
       Player 0 now decides to double, this will make bit 12 equal to 1, 
       since it is now player 1's turn to decide whether she takes or passes the cube."""
    m = self.m
    self.assertEqual(m.on_inner_action, 1)

  def MatchProxy_bit_from_12_to_13_test(self):
    """Bit 13 indicates whether an doubled is being offered. 
       0 if no double is being offered and 1 if a double is being offered."""
    m = self.m
    self.assertFalse(m.doubled)

  def MatchProxy_bit_from_14_to_16_test(self):
    """Bit 14-15 indicates whether an resignation was offered. 
       00 for no resignation, 01 for resign of a single game, 
       10 for resign of a gammon, or 11 for resign of a backgammon. 
       The player offering the resignation is the inverse of bit 12, 
       e.g., if player 0 resigns a gammon then bit 12 will be 1 
       (as it is now player 1 now has to decide whether to accept or reject the resignation) 
       and bit 13-14 will be 10 for resign of a gammon."""
    m = self.m
    self.assertEqual(m.resign_offer, 0)

  def MatchProxy_bit_from_16_to_22_test(self):
    """Bit 16-18 and bit 19-21 is the first and second die, 
       respectively. 0 if the dice has not yet be rolled, 
       otherwise the binary encoding of the dice,
       e.g., if 5-2 was rolled bit 16-21 will be 101-010."""
    m = self.m
    self.assertEqual(m.rolled, (5, 2))

  def MatchProxy_bit_from_22_to_37_test(self):
    """Bitt 22 to 36 is the match length. 
       The maximum value for the match length is 32767. 
       A match score of zero indicates that the game is a money game."""
    m = self.m
    self.assertEqual(m.match_length, 9)

  def MatchProxy_bit_from_37_to_52_test(self):
    """Bit 37-51 and bit 52-66 is the score for player 0 and player 1 respectively.
       The maximum value of the match score is 32767. """
    m = self.m
    self.assertEqual(m.score, (2, 4))

  def MatchProxy_encode_test(self):
    m = self.m
    self.assertEqual(encode_match(m), 'QYkqASAAIAAA')

  def MatchProxy_decode_1_test(self):
    m = decode_match('QYkqASAAIAAA')
    s = ''.join(map(str, list(m._data)))
    self.assertEqual(s, '100000101001000101010100100000000000010000000000000001000000000000')

  def MatchProxy_decode_2_test(self):
    b = bglib.model.board.board()
    self.assertEqual(b.cube_owner, 3)

    mp = MatchProxy()
    mp.cube_owner = b.cube_owner
    self.assertEqual(mp.cube_owner, 3)

    print b
    pid, mid = encode(b)
    decode(b, pid, mid)
    print b
    self.assertEqual(pid, '4HPwATDgc/ABMA')
    self.assertEqual(mid, 'MAAAAAAAAAAA')

  def MatchProxy_decode_3_test(self):
    b = bglib.model.board.board()
    assert b.position
    decode(b, 'vzsAAFhu2xFABA','QYkqASAAIAAA')
    print b
    pid, mid = encode(b)
    decode(b, pid, mid)
    print b
    self.assertEqual(pid, 'vzsAAFhu2xFABA')
    self.assertEqual(mid, 'QYkqASAAIAAA')

  def MatchProxy_decode_4_test(self):
    b = bglib.model.board.board()
    decode(b, 's+sNAAhwtxsAGA', 'QYlyASAAGAAA')
    print b
    pid, mid = encode(b)
    decode(b, pid, mid)
    print b
    self.assertEqual(pid, 's+sNAAhwtxsAGA')
    self.assertEqual(mid, 'QYlyASAAGAAA')

  def MatchProxy_decode_5_test(self):
    b = bglib.model.board.board()
    decode(b, 'd5sBIQJurwcAQA', 'AYH0ACAAAAAA')
    print b
    pid, mid = encode(b)
    decode(b, pid, mid)
    print b
    self.assertEqual(pid, 'd5sBIQJurwcAQA')
    self.assertEqual(mid, 'AYH0ACAAAAAA')

  def MatchProxy_decode_6_test(self):
    b = bglib.model.board.board()
    decode(b, '29kDAICdOwAAAA', 'cAmgACAAGAAA')
    print b
    pid, mid = encode(b)
    decode(b, pid, mid)
    print b
    self.assertEqual(pid, '29kDAICdOwAAAA')
    self.assertEqual(mid, 'cAmgACAAGAAA')



