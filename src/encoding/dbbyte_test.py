#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2006-2008 Noriyuki Hosaka nori@backgammon.gr.jp
#

import unittest
import nose

from bglib.model.board import board as Board
from bglib.model import constants

from bglib.encoding.dbbyte import *

class utilTest(unittest.TestCase):
  def setUp(self):
    pass

  def tearDown(self):
    pass

  def signedord_test(self):
    self.assertEqual(signedord('\x00'), 0)
    self.assertEqual(signedord('\x01'), 1)
    self.assertEqual(signedord('\x7f'), 127)
    self.assertEqual(signedord('\xff'), -1)
    self.assertEqual(signedord('\x80'), -128)

  def signedchr_test(self):
    self.assertEqual(signedchr(0), '\x00')
    self.assertEqual(signedchr(1), '\x01')
    self.assertEqual(signedchr(127), '\x7f')
    self.assertEqual(signedchr(-1), '\xff')
    self.assertEqual(signedchr(-128), '\x80')

  def signedx_test(self):
    for i in range(-128, 128, 1):
      print i, repr(signedchr(i))
      self.assertEqual(signedord(signedchr(i)), i)

  def encode_position_test(self):
    pos = (
        (0, 0, 0, 0, 0, 5, 0, 3, 0, 0, 0, 0,
         5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0), 
        (0, 0, 0, 0, 0, 5, 0, 3, 0, 0, 0, 0,
         5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0)
      )
    expected = (
      '\x00'
      '\xfe\x00\x00\x00\x00\x05\x00\x03\x00\x00\x00\xfb'
      '\x05\x00\x00\x00\xfd\x00\xfb\x00\x00\x00\x00\x02'
      '\x00'
    )
    encoded = encode_position(pos)
    self.assertEqual(encoded, expected)

  def decode_position_test(self):
    src = (
      '\x00'
      '\xfe\x00\x00\x00\x00\x05\x00\x03\x00\x00\x00\xfb'
      '\x05\x00\x00\x00\xfd\x00\xfb\x00\x00\x00\x00\x02'
      '\x00'
    )
    expected = (
        (0, 0, 0, 0, 0, 5, 0, 3, 0, 0, 0, 0,
         5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0), 
        (0, 0, 0, 0, 0, 5, 0, 3, 0, 0, 0, 0,
         5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0)
    )
    decoded = decode_position(src)
    self.assertEqual(decoded, expected)


class dbbyteTest(unittest.TestCase):
  def setUp(self):
    pass

  def tearDown(self):
    pass

  def new_test(self):
    exp = DatabaseBytesExpression()
    self.assert_(isinstance(exp, DatabaseBytesExpression))

  def test_initialposition(self):
    exp = DatabaseBytesExpression()
    self.assertEqual(exp.position, 
      (
      '\x00'
      '\xfe\x00\x00\x00\x00\x05\x00\x03\x00\x00\x00\xfb'
      '\x05\x00\x00\x00\xfd\x00\xfb\x00\x00\x00\x00\x02'
      '\x00'
      )
    )

  def test_initialposition_you(self):
    exp = DatabaseBytesExpression(
            Board(position=(
                (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0), 
                (0, 0, 0, 0, 0, 5, 0, 3, 0, 0, 0, 0,
                 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0)
               ),
              on_action=constants.you))
    self.assertEqual(exp.position, 
      (
      '\x00'
      '\xfe\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xfb'
      '\x00\x00\x00\x00\xfd\x00\xfb\x00\x00\x00\x00\x00'
      '\x00'
      )
    )

  def test_initialposition_him(self):
    exp = DatabaseBytesExpression(
            Board(position=(
                (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0), 
                (0, 0, 0, 0, 0, 5, 0, 3, 0, 0, 0, 0,
                 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0)
               ),
              on_action=constants.him))
    self.assertEqual(exp.position, 
      (
      '\x00'
      '\x00\x00\x00\x00\x00\x05\x00\x03\x00\x00\x00\x00'
      '\x05\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02'
      '\x00'
      )
    )

  def test_decode(self):
    exp = DatabaseBytesExpression()
    b = exp.tomodel()

    for key, item in Board.defaults.items():
      self.assertEqual(getattr(b, key), item)


