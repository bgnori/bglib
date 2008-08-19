#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2006-2008 Noriyuki Hosaka nori@backgammon.gr.jp
#
import unittest

import html
class HTMLEscapeTest(unittest.TestCase):
  def test_escape_lt(self):
    self.assertEqual(
      html.escape('<'),
      '&lt;')

  def test_escape_gt(self):
    self.assertEqual(
      html.escape('>'),
      '&gt;')

  def test_escape_amp(self):
    self.assertEqual(
      html.escape('&'),
      '&amp;')

  def test_escape_combined(self):
    self.assertEqual(
      html.escape('&<>'),
      '&amp;&lt;&gt;')

  def test_escape_combined(self):
    self.assertEqual(
      html.escape('!&<>'),
      '!&amp;&lt;&gt;')
