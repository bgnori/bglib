#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2006-2008 Noriyuki Hosaka nori@backgammon.gr.jp
#
from base import *

import tempfile
import unittest
import nose

import bglib.model.constants
import bglib.model.board
import bglib.model.move

class EncodingTest(unittest.TestCase):
  def setUp(self):
    pass
  def tearDown(self):
    pass

  def bgcombination_1_test(self):
    sum = 0
    for m in range(0, 16):
      sum += BackgammonCombination(m)
    self.assertEqual(WTN, sum)

  def bgcombination_2_test(self):
    sum = 0
    for m in range(0, 16):
        sum += BackgammonCombination_allC(m)
    self.assertEqual(WTN, sum)

  def encode_test(self):
    x = list(encode((0, 0, 0, 0, 0, 5, 2, 3, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)))
    self.assertEqual(x, ['\xe0', '\xdb', '\xc1', '\x03', '\x00'])

  def decode_test(self):
    self.assertEqual(list(decode('\xe0\xdb\xc1\x03\x00')),
      [0, 0, 0, 0, 0, 5, 2, 3, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

  def oneside_decode_encode__test(self):
    self.assertEqual(oneside_decode(oneside_encode((6, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1))),
(6, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1))

  def oneside_encode_decode_test(self):
    self.assertEqual(oneside_decode(oneside_encode((0, 3, 2, 2, 2, 3, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0))), (0, 3, 2, 2, 2, 3, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0))


  def twoside_decode_test(self):
    self.assertEqual(twoside_decode(twoside_encode(((6, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1), (0, 3, 2, 2, 2, 3, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0)))), 
((6, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1), (0, 3, 2, 2, 2, 3, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0)))

class recursiveDTest(unittest.TestCase):
  def test(self):
    for i in range(1, 12):
      for j in range(1, 12):
        print i, j
        self.assertEqual(recursiveD(i, j), D(i, j))
class BitsArrayTest(unittest.TestCase):
  def BitsArrayCreation_test(self):
    b = BitsArray(8, '\x00')
    self.assertEqual(b.endian, '<')
    self.assertEqual(b.binary, '\x00')

  def BitsArrayIndex_test(self):
    b = BitsArray(8, '\x00')
    self.assertEqual(b[0], 0)
    self.assertEqual(b[7], 0)
    try:
      b[8]
    except IndexError, e:
      self.assertEqual(str(e),"out of range")
    try:
      b['a'] #doctest: +ELLIPSIS
    except TypeError, e:
      self.assertEqual(str(e), "index must be int or slice, but got <type 'str'>")
    try:
      b[0] = 'a'#doctest: +ELLIPSIS
    except ValueError, e:
      self.assertEqual(str(e), "value for asignment must be 0 or 1")

  def BitsArraySlice1_test(self):
    b = BitsArray(8, '\x00')
    self.assertEqual(b[0:1].binary, '\x00')

  def BitsArraySlice2_test(self):
    b = BitsArray(8, '\x00')
    c = b[0:2]
    c[0] = 0
    self.assertEqual(c.binary, '\x00')

    c[1] = 1
    self.assertEqual(c.binary, '\x02')

    c[0] = 1
    self.assertEqual(c.binary, '\x03')

    self.assertEqual(repr(c), "<BitsArray Instance '1:1'>")

    b[3] = 1
    c = b[0:4]
    self.assertEqual(c.binary, '\x08')
    self.assertEqual(repr(c), "<BitsArray Instance '0:0:0:1'>")

  def BitsArraySlice3_test(self):
    b = BitsArray(8, '\x00')
    b[0] = 1
    self.assertEqual(b.int(), 1)

  def BitsArraySlice4_test(self):
    b = BitsArray(8, '\x00')
    b[7] = 1
    self.assertEqual(b.int(), 128)

  def BitsArraySlice5_test(self):
    b = BitsArray(8, '\x00')
    b[0] = 1
    b[7] = 1
    self.assertEqual(b.int(), 129)

  def BitsArraySlice6_test(self):
    b = BitsArray(16, '\x41\x89')
    self.assertEqual(ord(b.binary[0]), ord('\x41'))
    self.assertEqual(ord(b.binary[1]), ord('\x89'))
    self.assertEqual(''.join(map(str, list(b))), '1000001010010001')
    self.assertEqual(repr(b), "<BitsArray Instance '1:0:0:0:0:0:1:0:1:0:0:1:0:0:0:1'>")
    self.assertEqual(repr(b[0:16]), "<BitsArray Instance '1:0:0:0:0:0:1:0:1:0:0:1:0:0:0:1'>")
    self.assertEqual(repr(b[0:8]), "<BitsArray Instance '1:0:0:0:0:0:1:0'>")
    self.assertEqual(ord('\x41'), 65)
    self.assertEqual(ord(b[0:8].binary), 65)
    self.assertEqual(repr(b[8:16]), "<BitsArray Instance '1:0:0:1:0:0:0:1'>")

  def BitsArraySetter_test(self):
    b = BitsArray(16)
    for i,x in enumerate('1000001010010001'):
        b[i] = int(x)
    self.assertEqual(repr(b), "<BitsArray Instance '1:0:0:0:0:0:1:0:1:0:0:1:0:0:0:1'>")

  def BitsArrayEndian1_test(self):
    b = BitsArray(8, endian='<')
    b[7] = 1
    self.assertEqual(b.binary, '\x80')

  def BitsArrayEndian2_test(self):
    b = BitsArray(8, endian='>')
    self.assertEqual(b.binary, '\x00')
    self.assertEqual(b.endian, '>')
    b[0] = 1
    self.assertEqual(b.binary, '\x80')

  def BitsArrayEndian3_test(self):
    b = BitsArray(8, endian='>')
    b[7] = 1
    self.assertEqual(b.binary, '\x01')

  def BitsArrayEndian3_test(self):
    b = BitsArray(16, endian='<')
    b[0] = 1
    self.assertEqual(b.binary, '\x01\x00')

  def BitsArrayEndian5_test(self):
    b = BitsArray(16, endian='<')
    b[15] = 1
    self.assertEqual(b.binary, '\x00\x80')


  def BitsArrayEndian6_test(self):
    b = BitsArray(16, endian='>')
    b[0] = 1
    self.assertEqual(b.binary, '\x80\x00')

  def BitsArrayEndian7_test(self):
    b = BitsArray(16, endian='>')
    b[15] = 1
    self.assertEqual(b.binary, '\x00\x01')


  def BitsArrayEndian8_test(self):
    b = BitsArray(12, endian='>')
    self.assertEqual(b.binary, '\x00\x00')
    b[0] = 1
    self.assertEqual(b.binary, '\x80\x00')

  def BitsArrayEndian9_test(self):
    b = BitsArray(12, endian='>')
    b[11] = 1
    self.assertEqual(b.binary, '\x00\x10')

  def BitsArrayEndian10_test(self):
    b = BitsArray(12, endian='<')
    self.assertEqual(b.binary, '\x00\x00')
    b[0] = 1
    self.assertEqual(b.binary, '\x01\x00')

  def BitsArrayCasting1_test(self):
    b = BitsArray(12, endian='<')
    b[0] = 1
    self.assertEqual(b.int(), 1)

  def BitsArrayCasting2_test(self):
    b = BitsArray(12, endian='<')
    b[11] = 1
    self.assertEqual(b.binary, '\x00\x08')
    self.assertEqual(b.int(), 2048)

  def BitsArrayCasting3_test(self):
    b = BitsArray(20, endian='<')
    self.assertEqual(b.binary, '\x00\x00\x00')
    b[0] = 1
    self.assertEqual(b.binary, '\x01\x00\x00')
    b[8] = 1
    self.assertEqual(b.binary, '\x01\x01\x00')
    b[15] = 1
    self.assertEqual(b.binary, '\x01\x81\x00')
    b[14] = 1
    self.assertEqual(b.binary, '\x01\xc1\x00')


