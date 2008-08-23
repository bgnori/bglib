
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

from bglib.doc.fuzzing import Gene
class mkdnGene(Gene):
  seps = '\n '
  symbols = """[]'"_~^`{}.:*=-+#|!<>/&Xx"""
  numeric = '1234567890'
  alpha_n = 'abcdefgh'
  romaon_n ='iv'
  words = [
           """##""", """###""", 
           """======""", """------""",
           """**""", """![hoge](Image""",]
  single = list(seps + symbols + numeric + alpha_n + romaon_n)
  multi = words

if __name__ == "__main__":
  from bglib.doc.fuzzing import fuzz_it
  fuzz_it(mkdnGene, Formatter())

