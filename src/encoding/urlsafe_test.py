#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2006-2008 Noriyuki Hosaka nori@backgammon.gr.jp
#

import tempfile
import unittest
import nose

from urlsafe import *

class gnubgTest(unittest.TestCase):
  def setUp(self):
    pass
  def tearDown(self):
    pass
  def encode_position_1_test(self):
    p = encode_position(((6, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1),
                         (0, 3, 2, 2, 2, 3, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0)))
    self.assertEqual(p, 'vzsAAFhu2xFABA')

  def encode_position_2_test(self):
    p = encode_position(((0, 0, 0, 0, 0, 5, 0, 3, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0), 
                         (0, 0, 0, 0, 0, 5, 0, 3, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0)))
    self.assertEqual(p, '4HPwATDgc_ABMA')

  def decode_position_1_test(self):
    p = decode_position("vzsAAFhu2xFABA")
    self.assertEqual(p, 
          ((6, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1),
           (0, 3, 2, 2, 2, 3, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0))
           )

  def decode_position_2_test(self):
    p = decode_position("4HPwATDgc_ABMA")
    self.assertEqual(p, 
          ((0, 0, 0, 0, 0, 5, 0, 3, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0),
           (0, 0, 0, 0, 0, 5, 0, 3, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0))
           )

  def encode_match_test(self):
    import bglib.encoding.gnubg
    m = bglib.encoding.gnubg.MatchProxy('\x41\x89\x2A\x01\x20\x00\x20\x00\x00')
    self.assertEqual(encode_match(m), 'QYkqASAAIAAA')

  def decode_match_test(self):
    m = decode_match('QYkqASAAIAAA')
    self.assertEqual(''.join(map(str, list(m._data))),
                     '100000101001000101010100100000000000010000000000000001000000000000'
                     )

