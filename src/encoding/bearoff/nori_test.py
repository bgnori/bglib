#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2006-2009 Noriyuki Hosaka bgnori@gmail.com
#
import unittest
from bglib.encoding.bearoff.nori import *

class oneside_t2kTest(unittest.TestCase):
  def test_000000(self):
    self.assertEqual(oneside_upto6_t2k((0, 0, 0, 0, 0, 0,)), 0)

  def test_100000(self):
    self.assertEqual(oneside_upto6_t2k((1, 0, 0, 0, 0, 0,)), 1)

  def test_010000(self):
    self.assertEqual(oneside_upto6_t2k((0, 1, 0, 0, 0, 0,)), 2)

  def test_001000(self):
    self.assertEqual(oneside_upto6_t2k((0, 0, 1, 0, 0, 0,)), 3)

  def test_000100(self):
    self.assertEqual(oneside_upto6_t2k((0, 0, 0, 1, 0, 0,)), 4)

  def test_000010(self):
    self.assertEqual(oneside_upto6_t2k((0, 0, 0, 0, 1, 0,)), 5)

  def test_000001(self):
    self.assertEqual(oneside_upto6_t2k((0, 0, 0, 0, 0, 1,)), 6)

  def test_200000(self):
    self.assertEqual(oneside_upto6_t2k((2, 0, 0, 0, 0, 0,)), 7)

  def test_110000(self):
    self.assertEqual(oneside_upto6_t2k((1, 1, 0, 0, 0, 0,)), 8)

  def test_101000(self):
    self.assertEqual(oneside_upto6_t2k((1, 0, 1, 0, 0, 0,)), 8)

  def test_300000(self):
    self.assertEqual(oneside_upto6_t2k((3, 0, 0, 0, 0, 0,)), 28)

  def test_x(self):
    self.assertEqual(oneside_upto6_t2k((15, 0, 0, 0, 0, 0,)), sigmaD[14])
  def test_y(self):
    self.assertEqual(oneside_upto6_t2k((0, 0, 0, 0, 1, 14,)), sigmaD[15] - 2)
  def test_z(self):
    self.assertEqual(oneside_upto6_t2k((0, 0, 0, 0, 0, 15,)), sigmaD[15] - 1)

class oneside_k2tTest(unittest.TestCase):
  def test_000000(self):
    self.assertEqual(oneside_upto6_k2t(0), (0, 0, 0, 0, 0, 0,))

  def test_100000(self):
    self.assertEqual(oneside_upto6_k2t(1), (1, 0, 0, 0, 0, 0,))

  def test_010000(self):
    self.assertEqual(oneside_upto6_k2t(2), (0, 1, 0, 0, 0, 0,))

  def test_001000(self):
    self.assertEqual(oneside_upto6_k2t(3), (0, 0, 1, 0, 0, 0,))

  def test_000001(self):
    self.assertEqual(oneside_upto6_k2t(6), (0, 0, 0, 0, 0, 1,))

  def test_200000(self):
    self.assertEqual(oneside_upto6_k2t(7), (2, 0, 0, 0, 0, 0,))

  def test_110000(self):
    self.assertEqual(oneside_upto6_k2t(8), (1, 1, 0, 0, 0, 0,))

  def test_300000(self):
    self.assertEqual(oneside_upto6_k2t(28), (3, 0, 0, 0, 0, 0,))

class ReaderTest(unittest.TestCase):
  def setUp(self):
    self.reader = DBRreader()
  def tearDown(self):
    self.reader.close()

