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
    if element.name() != self.element:
      return False
    if self.attribute is None:
      return True
    if self.value is not None:
      assert self.attributes is not None
      v = element.attributes,get(self.attribute, None)
      if not v or v != self.value:
        return False
    if self.data is not None:
      return self.data == data
    return True
  def __str__(self):
    s = "<%s"%self.element
    if self.name:
      s += " %s=%s"%(self.name, self.value)
    s += ">"
    if self.data:
      s += "%s"%self.data
    s += "</%s>"%self.element
    return s


class Rule(object):
  def __init__(self, lineno):
    self.lineno = lineno
    self.selectors = list()
    self.block = dict()

  def add(self, selector):
    self.selectors.append(selector)

  def update(self, name, value):
    self.block.update({name: value})

  def apply(self, e):
    pass
  
  def __str__(self):
    r = "selectors: "+ ''.join([str(s) for s in self.selectors]) + '\n'
    r += "block: %s"%str(self.block)
    return r


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
      rule.update(m.group('name'), m.group('value'))


if __name__ == '__main__':
  p = CSSParser()
  css = file('./bglib/image/safari.css')
  for lineno, line in enumerate(css.readlines()):
    r = p.rule(lineno, line)
    if r:
      print r



