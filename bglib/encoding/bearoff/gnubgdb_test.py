#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2006-2009 Noriyuki Hosaka nori@backgammon.gr.jp
#
import unittest

from bglib.encoding.bearoff.gnubgdb import *

class ReaderTest(unittest.TestCase):
  def setUp(self):
    self.reader = DBRreader()
    self.reader.open('./bglib/encoding/bearoff/BEAR4.DTA')  
    ''' UGH! '''

  def tearDown(self):
    self.reader.close()

  def oneside_index_1_test(self):
    self.assertEqual(1, oneside_index((1,0,0,0,0,0, 0,0,0,0,0,0, 0,0,0,0,0,0, 0,0,0,0,0,0, 0), 1, 1))

  def oneside_index_1_test(self):
    self.assertEqual(1, oneside_index((1,0,0,0,0,0, 0,0,0,0,0,0, 0,0,0,0,0,0, 0,0,0,0,0,0, 0), 1, 1))

  def oneside_index_2_test(self):
    self.assertEqual(4927, oneside_index((0, 0, 1, 2, 5, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0), 6, 9))

  def oneside_index_3_test(self):
    self.assertEqual(505, oneside_index((2, 3, 0, 1, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0), 6, 8))

