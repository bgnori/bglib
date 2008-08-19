#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2006-2008 Noriyuki Hosaka nori@backgammon.gr.jp
#
import unittest
import bglib.doc
#.viewer

class ViewerDuckTypeTest(unittest.TestCase):
  def instance_viewer_test(self):
    self.assert_(isinstance(self.target, bglib.doc.Viewer))

  def has_make_html_test(self):
    self.assert_(hasattr(self.target, 'make_html'))
    self.assert_(callable(getattr(self.target, 'make_html')))

  def has_make_pdf_test(self):
    self.assert_(hasattr(self.target, 'make_pdf'))
    self.assert_(callable(getattr(self.target, 'make_pdf')))


class FormatterDuckTypeTest(ViewerDuckTypeTest):
  def instance_formatter_test(self):
    self.assert_(isinstance(self.target, bglib.doc.Formatter))

  def call_make_html_test(self):
    f = getattr(self.target, 'make_html')
    self.assert_(isinstance(f(''), (str, unicode)))

  def call_make_pdf_test(self):
    f = getattr(self.target, 'make_pdf')
    self.assert_(isinstance(f(''), (str, unicode)))


