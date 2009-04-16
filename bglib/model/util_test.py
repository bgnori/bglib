#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2006-2008 Noriyuki Hosaka nori@backgammon.gr.jp
#

import tempfile
import unittest
import nose

from bglib.model import *
from bglib.model import util
from bglib.model.constants import *

class ModelTest(unittest.TestCase):
  def setUp(self):
    pass
  def tearDown(self):
    pass


  def t001_test(self):
    self.assertEqual(util.position_pton('1', YOU), 0)

  def t002_test(self):
    self.assertEqual(util.position_ntop(0, YOU), '1')

  def t003_test(self):
    self.assertEqual(util.position_pton('24', YOU), 23)

  def t004_test(self):
    self.assertEqual(util.position_ntop(23, YOU), '24')

  def t005_test(self):
    self.assertEqual(util.position_pton('your home', YOU), -1)

  def t006_test(self):
    self.assertEqual(util.position_ntop(-1, YOU), 'your home')

  def t008_test(self):
    self.assertEqual(util.position_pton('your bar', YOU), 24)

  def t009_test(self):
    self.assertEqual(util.position_ntop(24, YOU), 'your bar')

  def t010_test(self):
    self.assertEqual(util.position_pton('1', HIM), 23)

  def t011_test(self):
    self.assertEqual(util.position_ntop(23, HIM), '1')

  def t012_test(self):
    self.assertEqual(util.position_pton('24', HIM), 0)

  def t013_test(self):
    self.assertEqual(util.position_ntop(0, HIM), '24')

  def t014_test(self):
    self.assertEqual(util.position_pton('his home', HIM), -1)

  def t015_test(self):
    self.assertEqual(util.position_ntop(-1, HIM), 'his home')

  def t016_test(self):
    self.assertEqual(util.position_pton('his bar', HIM), 24)

  def t017_test(self):
    self.assertEqual(util.position_ntop(24, HIM), 'his bar')

  def t018_test(self):
    self.assertEqual(util.move_ntop(24), 'bar')

  def t019_test(self):
    self.assertEqual(util.move_pton('bar'), 24)

  def t020_test(self):
    self.assertEqual(util.move_ntop(0), '1')

  def t021_test(self):
    self.assertEqual(util.move_pton('1'), 0)

  def t022_test(self):
    self.assertEqual(util.move_ntop(-1), 'off')

  def t023_test(self):
    self.assertEqual(util.move_pton('off'), -1)

  def t024_test(self):
    try:
      util.position_pton('100', YOU)
      self.assert_(False)
    except ValueError:
      pass

  def t025_test(self):
    try:
      util.position_pton('abc', YOU)
      self.assert_(False)
    except ValueError:
      pass

  def t026_test(self):
    try:
      util.position_ntop(0, CENTER)
      self.assert_(False)
    except ValueError:
      pass

  def t027_test(self):
    try:
      util.position_ntop(26, YOU)
      self.assert_(False)
    except ValueError:
      pass

  def t028_test(self):
    try: 
      util.move_ntop(25)
      self.assert_(False)
    except ValueError:
      pass

  def t029_test(self):
    try: 
      util.move_pton('hoge')
      self.assert_(False)
    except ValueError:
      pass

  def t030_test(self):
    try: 
      util.move_pton('100')
      self.assert_(False)
    except ValueError:
      pass

  def t031_test(self):
    try: 
      util.get_opp(CENTER)
      self.assert_(False)
    except ValueError:
      pass
