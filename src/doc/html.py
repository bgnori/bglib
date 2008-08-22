#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2006-2008 Noriyuki Hosaka nori@backgammon.gr.jp
#
import re
import xml.parsers.expat

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


def validate(html_fragment):
  p = xml.parsers.expat.ParserCreate()
  p.Parse(
  '''<?xml version="1.0" encoding="us-ascii"?>\n''')
  p.Parse(
  '''<!DOCTYPE html PUBLIC "'''
  '''-//W3C//DTD XHTML 1.0 Strict//EN"\n'''
  '''"http://www.w3.org/TR/xhtml1'''
  '''/DTD/xhtml1-strict.dtd">\n''')
  p.Parse(
  '''<html xmlns="http://www.w3.org/\n'''
  '''1999/xhtml" xml:lang="en">\n''')
  #'''lang="en">\n''')
  p.Parse(
  '''<head><title>test</title></head>\n''')
  p.Parse('''<body>\n''')

  p.Parse(html_fragment)
  p.Parse('''</body></html>\n''', True)

