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
  def __init__(self, element, attribute=None, value=None, data=None):
    self.element = element
    self.attribute = attribute
    self.value = value
    self.date = data

  def select(self, element):
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


class Rule(object):
  def __init__(self):
    self.selectors = list()
    self.block = dict()

  def add(self, selector):
    self.selectors.append(selector)
  
  def __str__(self):
    "selector: %s"%self.selectors
    "block:"



css_line = re.compile(r"^(?P<selector>[^{]*)[ ]*(?P<block>{.*})")

x = r"""(?P<element>[a-zA-Z]+)(\[(?P<attribute>[a-zA-Z]+)=(?P<value>['"][a-zA-Z]+['"])\]|\b)(:data\("(?P<data>.+)"\)|\b)"""


exp = re.compile(x)



css = file('./bglib/image/safari.css')

rules = list()
for nth, line in enumerate(css.readlines()):
  m = css_line.search(line)
  if m:
    print 'at line:', nth + 1
    r  = Rule()

    #s = Selector()
    for pred in m.group('selector').split(' '):
      if pred:
        e = exp.search(pred)
        print 'element', e.group('element')
        print 'attribute', e.group('attribute')
        print 'value', e.group('value')
        print 'data', e.group('data')
        #a = t.search(elem)
        #if p:
        #d = data.search(elem)
        #if d:
        #  print 'data', d.group('data')

    block = m.group('block')
    print 'block', block
    block = block.strip('{}')
    print 'block', block
    for pair in block.split(';'):
      print pair
      attr, value = pair.split(':')
      print '  ', attr, '=', value
      
    print
  elif len(line) > 2:
    print 'bad format >', line
  else:
    pass
  
  
