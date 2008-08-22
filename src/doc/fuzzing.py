#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2006-2008 Noriyuki Hosaka nori@backgammon.gr.jp
#

import sys
import StringIO
import traceback
import random

import bglib.doc.html

class Error(object):
  def __init__(self, e):
    self.exception = e
    buf = StringIO.StringIO()
    traceback.print_tb(sys.exc_info()[2], file=buf)
    self.stacktrace = buf.getvalue()
    buf.close()
  def __nonzero__(self):
    return False

class FormatError(Error):
  pass

class ParseError(Error):
  pass


class Gene(object):
  seps = '\n '
  symbols = """[]'"_~^`{}.:*=-+#|!<>/&"""
  numeric = '1234567890'
  alpha_n = 'abcdefgh'
  romaon_n ='iv'
  words = ["""http:""", """https:""", 
           """query:""", """entry:""", 
           """match:""", """wiki:""",
           """||""", """CamelWord""",]
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
    self.code = tuple(code)
    self.html = None

  def __hash__(self):
    return hash(self.code)

  def __str__(self):
    return '<Gene: code:%s\n, text:%s\n, html:%s\n>'%\
             (repr(self.code), repr(self.get_text()), repr(self.html))

  def get_text(self):
    return ''.join([Gene.num_to_text(c) for c in self.code])

  def format(self, formatter):
    text = self.get_text()
    try:
      self.html = formatter.make_html(text)
    except Exception, e:
      return FormatError(e) 
    return True

  def verify(self):
    assert self.html
    try:
      bglib.doc.html.validate(self.html)
    except Exception, e:
      return ParseError(e)
    return True

  def iter_subset(self):
    for i, c in enumerate(self.code):
      yield Gene(self.code[:i] + self.code[i+1:])
  
  def shorter_fails(self):
    for sub in iter_subset(g):
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
  import sys
  from bglib.doc.bgwiki import Formatter
  from bglib.doc.mock import DataBaseMock
  db = DataBaseMock()
  f = Formatter(db)
  length = int(sys.argv[1])
  trials = int(sys.argv[2])
  for j in range(trials):
    g = Gene([random.randint(0, Gene.count() - 1 ) for i in range(length)])
    ok_or_error = g.format(f)
    if not ok_or_error:
      print ok_or_error.exception, ok_or_error.stacktrace
      print g
      continue
    ok_or_error = g.verify()
    if not ok_or_error:
      print ok_or_error.exception, ok_or_error.stacktrace
      print g
      continue

