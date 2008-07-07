#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2006-2008 Noriyuki Hosaka nori@backgammon.gr.jp
#

import tempfile
import unittest
import nose

from bglib.protocol.fibs import CookieMonster

class FIBSTest(unittest.TestCase):
  def setUp(self):
    self.monster = CookieMonster()
    input_file = file('./bglib/protocol/fibs_test.in')
    self.input = input_file.readlines()
    input_file.close()
    output_file = file('./bglib/protocol/fibs_test.out')
    self.output = output_file.readlines()
    output_file.close()

  def tearDown(self):
    pass

  def cooike_test(self):
    m = self.monster
    for i, o in zip(self.input, self.output):
      i = i.strip('\n')
      o = o.strip('\n')
      self.assertEqual(m.make_cookie(i), o)

