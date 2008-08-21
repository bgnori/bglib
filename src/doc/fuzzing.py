#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2006-2008 Noriyuki Hosaka nori@backgammon.gr.jp
#

import random
import bglib.doc.html

class Gene(object):
  seps = '\n '
  symbols = """[]'"_~^`{}.:*=-+#|!<>/&"""
  numeric = '1234567890'
  alpha_n = 'abcdefgh'
  romaon_n ='iv'
  words = ["""http:""", """https:""", 
           """query:""", """entry:""", 
           """match:""", """wiki:""",]
  single = list(seps + symbols + numeric + alpha_n + romaon_n)
  multi = words

  @classmethod
  def count(cls):
    return len(cls.single) + len(cls.multi)

  @classmethod
  def num_to_text(cls, n):
    x = cls.single + cls.multi
    return x[n]

  def __init__(self, code):
    self.code = code

  def get_text(self):
    return ''.join([Gene.num_to_text(c) for c in self.code])

  def is_ok(self, formatter):
    text = self.get_text()
    try:
      html = formatter.make_html(text)
    except Exception, e:
      print e
      return False
    return bglib.doc.html.is_valid_nesting(html)

  def subg(self):
    for i, c in enumerate(self.code):
      yield Gene(self.code[:i] + self.code[i+1:])
  
  def shorter_fails(self):
    for sub in subg(g):
      if not is_ok(sub):
        yield sub

class Vat(object):
  def __init__(self):
    pass
  

if __name__ == "__main__":
  '''
  start fuzzing test
  and 
  generate Unittests based on failures.

  '''
  from bglib.doc.bgwiki import Formatter
  from bglib.doc.mock import DataBaseMock
  db = DataBaseMock()
  f = Formatter(db)
  for j in range(100):
    g = Gene([random.randint(0, Gene.count() - 1 ) for i in range(100)])
    print repr(g.get_text()), repr(f.make_html(g.get_text()))
  

