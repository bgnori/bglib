#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2006-2008 Noriyuki Hosaka nori@backgammon.gr.jp
#

import unittest
import bglib.doc 
from bglib.doc.fuzzing import Gene

class MockFormatter(bglib.doc.Formatter):
  pass

class GeneTest(unittest.TestCase):
  def setUp(self):
    self.gene = Gene('')
    self.formatter = MockFormatter()

  def get_text_test(self):
    self.assertEqual(self.gene.get_text(), '')

  def is_ok_test(self):
    self.assert_(self.gene.is_ok(self.formatter))


