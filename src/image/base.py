#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2006-2008 Noriyuki Hosaka nori@backgammon.gr.jp
#

import bglib.image.css
import bglib.model.constants

you = bglib.model.constants.player_string[bglib.model.constants.you]
him = bglib.model.constants.player_string[bglib.model.constants.him]


class Element(object):
  def __init__(self, name, **kw):
    self.__dict__['name'] = name
    self.__dict__['children'] = list()
    self.__dict__['attributes'] = dict(kw)
    self.__dict__['parent'] = None
    self.__dict__['css_lineno'] = list()

  def __str__(self):
    s = "<%s"%self.name
    for name, value in self.attributes.items():
      s += " %s=%s"%(name, value)
    s += ">"
    for c in self.children:
      s += "%s"%str(c)
    s += "</%s>"%self.name
    return s
  __repr__ = __str__

  def append(self, e):
    assert isinstance(e, (Element, str))
    self.children.append(e)
    if isinstance(e, Element):
      e.parent = self

  def update(self, d):
    self.attributes.update(d)

  def format(self, indent):
    s = ' '*indent + "<%s"%(self.name)
    for n, v in self.attributes.items():
      s+= ' %s=%s'%(n, str(v))
    s+=">\n"
    for c in self.children:
      if isinstance(c, Element):
        s += c.format(indent+2)
      else:
        s += ' '*(indent +2) + str(c) + '\n'
    s+= ' '*indent + "</%s>\n"%(self.name)
    return s

  def __getattr__(self, name):
    if name in self.attributes:
      return self.attributes[name]
    return getattr(self.parent, name) #inherit

class Visit(object):
  def __init__(self, callback, *args, **kw):
    self.callback = callback
    self.args = args
    self.kw = kw

  def visit(self, path=None):
    self.callback(path, *self.args, **self.kw)
    for c in path[-1].children:
      if isinstance(c, bglib.image.base.Element):
        path.append(c)
        self.visit(path)
        path.pop(-1)


def make_empty_tree():
  points = list()
  points.append(None)
  home = list()
  home.append(Element('home', player=you))
  home.append(Element('home', player=him))
  bar = list()
  bar.append(Element('bar', player=you))
  bar.append(Element('bar', player=him))
  field = list()
  field.append(Element('field', player=you))
  field.append(Element('field', player=him))

  b = Element('board')
  b.append(field[bglib.model.constants.you])
  b.append(home[bglib.model.constants.you])
  b.append(bar[bglib.model.constants.him])
  for i in range(1, 25):
    if i%2:
      pt = Element('point', parity="odd")
    else:
      pt = Element('point', parity="even")
    pt.append(str(i))
    b.append(pt)
    points.append(pt)
  b.append(bar[bglib.model.constants.you])
  b.append(home[bglib.model.constants.him])
  b.append(field[bglib.model.constants.him])
  return b, points, home, bar, field


if __name__ == '__main__':
  b, p, home, bar, field = make_empty_tree()
  print b.format(0)


