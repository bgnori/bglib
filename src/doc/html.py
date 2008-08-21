#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2006-2008 Noriyuki Hosaka nori@backgammon.gr.jp
#
import re

UNSAFE_LETTERS = '(?P<lt>[<])|(?P<gt>[>])|(?P<amp>[&])'
def escape(s):
  def handler(matchobj):
    d = matchobj.groupdict()
    if d['lt']:
      return '&lt;'
    if d['gt']:
      return '&gt;'
    if d['amp']:
      return '&amp;'
  return re.sub(UNSAFE_LETTERS, handler, s)

def is_valid_nesting(html):
  return True

