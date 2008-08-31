#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2006-2008 Noriyuki Hosaka nori@backgammon.gr.jp
#

import unittest
import bglib.doc 
import bglib.doc.bgwiki
import bglib.doc.mock
from bglib.doc.fuzzing import Gene, FormatError, ParseError

class MockErrorFormatter(bglib.doc.Formatter):
  def make_html(self, text):
    raise AssertionError, "MockErrorFormatter's mock AssertionError"

class MockBadHTMLFormatter(bglib.doc.Formatter):
  def make_html(self, text):
    return "<div><table></div></table>"

class GeneTest(unittest.TestCase):
  def setUp(self):
    self.gene = Gene((0, 1))
    self.errorformatter = MockErrorFormatter()
    self.badformatter = MockBadHTMLFormatter()
    db = bglib.doc.mock.DataBaseMock()
    self.goodformatter = bglib.doc.bgwiki.Formatter(db)

  def get_text_test(self):
    self.assertEqual(self.gene.get_text(), '\n ')

  def format_bool_test(self):
    self.assertFalse(self.gene.format(self.errorformatter))
    
  def format_error_test(self):
    e = self.gene.format(self.errorformatter)
    self.assert_(isinstance(e, FormatError))
    self.assert_(isinstance(e.exception, Exception))
    self.assertEqual(str(e.exception), '''MockErrorFormatter's mock AssertionError''')
    self.assertEqual(e.stacktrace, (
      '''  File "/home/nori/Desktop/work/bglib/src/bglib/doc/fuzzing.py", line 71, in format\n'''
      '''    self.html = formatter.make_html(text)\n'''
      '''  File "/home/nori/Desktop/work/bglib/src/bglib/doc/fuzzing_test.py", line 16, in make_html\n'''
      '''    raise AssertionError, "MockErrorFormatter's mock AssertionError"\n'''))

  def parse_error_test(self):
    e = self.gene.format(self.badformatter)
    self.assert_(e)
    e = self.gene.verify()
    self.assert_(isinstance(e.exception, Exception))
    self.assert_(str(e.exception).startswith('mismatched tag: line '))

  def ok_test(self):
    e = self.gene.format(self.goodformatter)
    self.assert_(e)
    e = self.gene.verify()
    self.assert_(e)