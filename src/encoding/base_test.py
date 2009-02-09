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
class BitArrayTest(unittest.TestCase):
  def BitArrayCreation_test(self):
    b = BitArray(8, '\x00')
    self.assertEqual(b.endian, '<')
    self.assertEqual(b.binary, '\x00')

  def BitArrayIndex_test(self):
    b = BitArray(8, '\x00')
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

  def BitArraySlice1_test(self):
    b = BitArray(8, '\x00')
    self.assertEqual(b[0:1].binary, '\x00')

  def BitArraySlice2_test(self):
    b = BitArray(8, '\x00')
    c = b[0:2]
    c[0] = 0
    self.assertEqual(c.binary, '\x00')

    c[1] = 1
    self.assertEqual(c.binary, '\x02')

    c[0] = 1
    self.assertEqual(c.binary, '\x03')

    self.assertEqual(repr(c), "<BitArray Instance '1:1'>")

    b[3] = 1
    c = b[0:4]
    self.assertEqual(c.binary, '\x08')
    self.assertEqual(repr(c), "<BitArray Instance '0:0:0:1'>")

  def BitArraySlice3_test(self):
    b = BitArray(8, '\x00')
    b[0] = 1
    self.assertEqual(b.int(), 1)

  def BitArraySlice4_test(self):
    b = BitArray(8, '\x00')
    b[7] = 1
    self.assertEqual(b.int(), 128)

  def BitArraySlice5_test(self):
    b = BitArray(8, '\x00')
    b[0] = 1
    b[7] = 1
    self.assertEqual(b.int(), 129)

  def BitArraySlice6_test(self):
    b = BitArray(16, '\x41\x89')
    self.assertEqual(ord(b.binary[0]), ord('\x41'))
    self.assertEqual(ord(b.binary[1]), ord('\x89'))
    self.assertEqual(''.join(map(str, list(b))), '1000001010010001')
    self.assertEqual(repr(b), "<BitArray Instance '1:0:0:0:0:0:1:0:1:0:0:1:0:0:0:1'>")
    self.assertEqual(repr(b[0:16]), "<BitArray Instance '1:0:0:0:0:0:1:0:1:0:0:1:0:0:0:1'>")
    self.assertEqual(repr(b[0:8]), "<BitArray Instance '1:0:0:0:0:0:1:0'>")
    self.assertEqual(ord('\x41'), 65)
    self.assertEqual(ord(b[0:8].binary), 65)
    self.assertEqual(repr(b[8:16]), "<BitArray Instance '1:0:0:1:0:0:0:1'>")

  def BitArraySetter_test(self):
    b = BitArray(16)
    for i,x in enumerate('1000001010010001'):
        b[i] = int(x)
    self.assertEqual(repr(b), "<BitArray Instance '1:0:0:0:0:0:1:0:1:0:0:1:0:0:0:1'>")

  def BitArrayEndian1_test(self):
    b = BitArray(8, endian='<')
    b[7] = 1
    self.assertEqual(b.binary, '\x80')

  def BitArrayEndian2_test(self):
    b = BitArray(8, endian='>')
    self.assertEqual(b.binary, '\x00')
    self.assertEqual(b.endian, '>')
    b[0] = 1
    self.assertEqual(b.binary, '\x80')

  def BitArrayEndian3_test(self):
    b = BitArray(8, endian='>')
    b[7] = 1
    self.assertEqual(b.binary, '\x01')

  def BitArrayEndian3_test(self):
    b = BitArray(16, endian='<')
    b[0] = 1
    self.assertEqual(b.binary, '\x01\x00')

  def BitArrayEndian5_test(self):
    b = BitArray(16, endian='<')
    b[15] = 1
    self.assertEqual(b.binary, '\x00\x80')


  def BitArrayEndian6_test(self):
    b = BitArray(16, endian='>')
    b[0] = 1
    self.assertEqual(b.binary, '\x80\x00')

  def BitArrayEndian7_test(self):
    b = BitArray(16, endian='>')
    b[15] = 1
    self.assertEqual(b.binary, '\x00\x01')


  def BitArrayEndian8_test(self):
    b = BitArray(12, endian='>')
    self.assertEqual(b.binary, '\x00\x00')
    b[0] = 1
    self.assertEqual(b.binary, '\x80\x00')

  def BitArrayEndian9_test(self):
    b = BitArray(12, endian='>')
    b[11] = 1
    self.assertEqual(b.binary, '\x00\x10')

  def BitArrayEndian10_test(self):
    b = BitArray(12, endian='<')
    self.assertEqual(b.binary, '\x00\x00')
    b[0] = 1
    self.assertEqual(b.binary, '\x01\x00')

  def BitArrayCasting1_test(self):
    b = BitArray(12, endian='<')
    b[0] = 1
    self.assertEqual(b.int(), 1)

  def BitArrayCasting2_test(self):
    b = BitArray(12, endian='<')
    b[11] = 1
    self.assertEqual(b.binary, '\x00\x08')
    self.assertEqual(b.int(), 2048)

  def BitArrayCasting3_test(self):
    b = BitArray(20, endian='<')
    self.assertEqual(b.binary, '\x00\x00\x00')
    b[0] = 1
    self.assertEqual(b.binary, '\x01\x00\x00')
    b[8] = 1
    self.assertEqual(b.binary, '\x01\x01\x00')
    b[15] = 1
    self.assertEqual(b.binary, '\x01\x81\x00')
    b[14] = 1
    self.assertEqual(b.binary, '\x01\xc1\x00')


