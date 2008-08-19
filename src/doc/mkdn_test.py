#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2006-2008 Noriyuki Hosaka nori@backgammon.gr.jp
#

import bglib.doc.viewer_type
import bglib.doc.mkdn

class FormatterDuckTypeTest(bglib.doc.viewer_type.FormatterDuckTypeTest):
  def setUp(self):
    self.target = bglib.doc.mkdn.Formatter()

  def sample_test(self):
    self.target.make_html('hogehoge')

