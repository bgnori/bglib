#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2006-2008 Noriyuki Hosaka nori@backgammon.gr.jp
#
class Viewer(object):
  def parse(self, *args, **kw):
    pass
  def make_html(self):
    pass
  def make_pdf(self):
    pass

class Formatter(Viewer):
  def parse(self, text):
    pass
  def make_html(self):
    pass
  def make_pdf(self):
    pass


class Document(object):
  pass

