
#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2006-2008 Noriyuki Hosaka nori@backgammon.gr.jp
#

import markdown
import bglib.doc

class Formatter(bglib.doc.Formatter):
  '''
    this module implements markdown Formatter using markdown.py
    about markdown.py, see
    http://www.freewisdom.org/projects/python-markdown/ 
  '''
  def __init__(self):
    bglib.doc.Formatter.__init__(self)
    self.md = markdown.Markdown()
    #FIXME 
    # be html Safe
    # add extension

  def make_html(self, text):
    return self.md.convert(text)
  def make_pdf(self, text):
    return ''

