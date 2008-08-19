#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2006-2008 Noriyuki Hosaka nori@backgammon.gr.jp
#

import viewer_type
import rst

class FormatterDuckTypeTest(viewer_type.FormatterDuckTypeTest):
  def setUp(self):
    self.target = rst.Formatter()

  def sample_test(self):
    self.target.make_html('hogehoge')

