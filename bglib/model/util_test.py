#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2006-2008 Noriyuki Hosaka nori@backgammon.gr.jp
#

import tempfile
import unittest
import nose

import bglib.model.constants
import bglib.model.board
import bglib.model.move

class ModelTest(unittest.TestCase):
  def setUp(self):
    pass
  def tearDown(self):
    pass

  def t001_test(self):
    self.assertEqual(bglib.model.util.position_pton('1', bglib.model.constants.you), 0)

  def t002_test(self):
    self.assertEqual(bglib.model.util.position_ntop(0, bglib.model.constants.you), '1')

  def t003_test(self):
    self.assertEqual(bglib.model.util.position_pton('24', bglib.model.constants.you), 23)

  def t004_test(self):
    self.assertEqual(bglib.model.util.position_ntop(23, bglib.model.constants.you), '24')

  def t005_test(self):
    self.assertEqual(bglib.model.util.position_pton('your home', bglib.model.constants.you), -1)

  def t006_test(self):
    self.assertEqual(bglib.model.util.position_ntop(-1, bglib.model.constants.you), 'your home')

  def t008_test(self):
    self.assertEqual(bglib.model.util.position_pton('your bar', bglib.model.constants.you), 24)

  def t009_test(self):
    self.assertEqual(bglib.model.util.position_ntop(24, bglib.model.constants.you), 'your bar')

  def t010_test(self):
    self.assertEqual(bglib.model.util.position_pton('1', bglib.model.constants.him), 23)

  def t011_test(self):
    self.assertEqual(bglib.model.util.position_ntop(23, bglib.model.constants.him), '1')

  def t012_test(self):
    self.assertEqual(bglib.model.util.position_pton('24', bglib.model.constants.him), 0)

  def t013_test(self):
    self.assertEqual(bglib.model.util.position_ntop(0, bglib.model.constants.him), '24')

  def t014_test(self):
    self.assertEqual(bglib.model.util.position_pton('his home', bglib.model.constants.him), -1)

  def t015_test(self):
    self.assertEqual(bglib.model.util.position_ntop(-1, bglib.model.constants.him), 'his home')

  def t016_test(self):
    self.assertEqual(bglib.model.util.position_pton('his bar', bglib.model.constants.him), 24)

  def t017_test(self):
    self.assertEqual(bglib.model.util.position_ntop(24, bglib.model.constants.him), 'his bar')

  def t018_test(self):
    self.assertEqual(bglib.model.util.move_ntop(24), 'bar')

  def t019_test(self):
    self.assertEqual(bglib.model.util.move_pton('bar'), 24)

  def t020_test(self):
    self.assertEqual(bglib.model.util.move_ntop(0), '1')

  def t021_test(self):
    self.assertEqual(bglib.model.util.move_pton('1'), 0)

  def t022_test(self):
    self.assertEqual(bglib.model.util.move_ntop(-1), 'off')

  def t023_test(self):
    self.assertEqual(bglib.model.util.move_pton('off'), -1)

