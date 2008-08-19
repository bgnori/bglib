#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2006-2008 Noriyuki Hosaka nori@backgammon.gr.jp
#

class Viewer(object):
  def make_html(self, *args, **kw):
    pass
  def make_pdf(self, *args, **kw):
    pass

class Formatter(Viewer):
  def make_html(self, text):
    pass
  def make_pdf(self, text):
    pass


