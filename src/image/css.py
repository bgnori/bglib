#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2006-2008 Noriyuki Hosaka nori@backgammon.gr.jp
#


'''
It implements subset + extention of css(http://www.w3.org/TR/CSS21/)


Support Status of subset
N = No, Y= Yes, P= Partial

N | Universal selector
Y | Type selectors
P | Descendant selectors
N | Child selectors
N | The :first-child pseudo-class
N | The link pseudo-classes
N | The dynamic pseudo-classes
N | The :lang() pseudo-class
N | Adjacent selectors
P | Attribute selectors
N |  E[foo]  
Y |  E[foo="warning"]  
N |  E[foo~="warning"] 
N |  E[lang|="en"] 
N |  DIV.warning 
N | Class selectors
N | E#myid  Matches any E element with ID equal to "myid".

Extensions
:data() pseudo-class
E[x='100'] F[y='200'] conditioned ancestor


:data() pseudo-class
E:data('1')

samples:
<E>1</E> is applied
<E>1<F></F></E> is applied
<E><F>2</F>1</E> is applied

<E></E> is not applied
<E>2<F>1</F></E> is not applied
<E>2</E> is not applied


E[x='100'] F[y='200'] conditioned ancestor
samples:
<E x='100'><F y='200'> </F> </E> is applied

<F y='200'> </F> not is applied
<E x='200'><F y='200'> </F> </E> not is applied
<E x='100'><F y='100'> </F> </E> not is applied


'''

import re


class Selector(object):
  def __init__(self, element, name=None, value=None, data=None):
    self.element = element
    self.name = name
    self.value = value
    self.data = data

  def is_match(self, element):
    ret = True
    assert self.element is not None
    ret &= (element.name == self.element)
    if ret and self.name is not None:
      ret &= (self.name in element.attributes)
    if ret and self.value is not None:
      ret &= (element.attributes[self.name] == self.value)
    if ret and self.data is not None:
      ret &= (self.data in element.children)
    return ret
 
  def __str__(self):
    s = "<%s"%self.element
    if self.name:
      s += " %s=%s"%(self.name, self.value)
    s += ">"
    if self.data:
      s += "%s"%self.data
    s += "</%s>"%self.element
    return s
  __repr__ = __str__


class Rule(object):
  def __init__(self, lineno):
    self.lineno = lineno
    self.pattern = list()
    self.block = dict()

  def add(self, selector):
    self.pattern.append(selector)

  def update(self, d):
    self.block.update(d)

  def is_match(self, path):
    ''' match last item first. '''
    pattern = self.pattern[:]
    assert pattern
    for element in reversed(path):
      if pattern[-1].is_match(element):
        pattern.pop(-1)
        if not pattern:
          return True
    assert pattern
    return False
    
  def apply(self, path):
    if self.is_match(path):
      path[-1].update(self.block)
  
  def __str__(self):
    r = "in line: %i\n"%self.lineno
    r += "pattern: "+ ' '.join([str(s) for s in self.pattern]) + '\n'
    r += "block: %s"%str(self.block)
    return r
  __repr__ = __str__


class CSSParser(object):
  def rule(self, lineno, s):
    if not s:
      return 
    r = re.compile(r"^[ ]*(?P<pattern>[^{]*)[ ]*{(?P<block>[^]]*)}")
    m = r.search(s)
    if m:
      rule = Rule(lineno)
      self.pattern(rule, m.group('pattern'))
      self.block(rule, m.group('block'))
      return rule

  def pattern(self, rule, s):
    assert s
    for t in s.split(' '):
      if t:
        self.selector(rule, t)

  def selector(self, rule, s):
    assert s
    r = re.compile("""
        (?P<element>[a-zA-Z]+)
        (?P<attribute>\[(?P<name>[a-zA-Z]+)=(?P<value>['"][a-zA-Z]+['"])\])?
        (:data\("(?P<data>.+)"\))?
      """, re.VERBOSE)
    m = r.search(s)
    if m:
      rule.add(Selector(m.group('element'),
                        m.group('name'), 
                        m.group('value'),
                        m.group('data')))

  def block(self, rule, s):
    assert s
    for t in s.split(";"):
      if t:
        self.attribute(rule, t)

  def attribute(self, rule, s):
    assert s
    r = re.compile(""" *(?P<name>[a-zA-Z]+) *: *(?P<value>[^ ]+) *""")
    m = r.search(s)
    if m:
      rule.update({m.group('name'): m.group('value')})



if __name__ == '__main__':
  import doctest
  doctest.testfile('css.test', )

