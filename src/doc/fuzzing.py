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
  single = ['g','t', 'a', 'c']
  multi = []
  def count(self):
    return len(self.single) + len(self.multi)

  def num_to_text(self, n):
    x = self.single + self.multi
    return x[n]

  def __init__(self, length):
    self.code = tuple([random.randint(0, self.count() - 1 ) for i in range(length)])
    self.html = None

  def __hash__(self):
    return hash(self.code)

  def __str__(self):
    return '<Gene: code:%s\n, text:%s\n, html:%s\n>'%\
             (repr(self.code), repr(self.get_text()), repr(self.html))

  def get_text(self):
    return ''.join([self.num_to_text(c) for c in self.code])

  def format(self, formatter):
    text = self.get_text()
    try:
      formatter.parse(text)
    except Exception, e:
      return FormatError(e) 
    try:
      self.html = formatter.make_html()
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

def fuzz_it(gklass, formatter):
  import os
  import select
  import signal
  length = int(sys.argv[1])
  trials = int(sys.argv[2])
  for j in range(trials):
    g = gklass(length)
    r, w = os.pipe()
    pid = os.fork()

    if pid:
      try:
        i, o, e = select.select([r], [], [], 3)
        assert not o
        assert not e
        if i:
          pass
        else:
          print 'timed out'
          print g
          os.kill(pid, signal.SIGKILL)
      finally:
        os.close(r)
        os.close(w)
    else:
      try:
        ok_or_error = g.format(formatter)
        if not ok_or_error:
          print ok_or_error.exception, ok_or_error.stacktrace
          print g
          os._exit(1)
        ok_or_error = g.verify()
        if not ok_or_error:
          print ok_or_error.exception, ok_or_error.stacktrace
          print g
          os._exit(1)
        os.write(w, '.')
        os._exit(0)
      finally:
        os.close(r)
        os.close(w)
      
