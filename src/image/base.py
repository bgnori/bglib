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

class  ElementFactory(object):
  def __init__(self):
    self.ec = dict()

  def __call__(self, name, *args, **kw):
    kls = self.ec[name]
    return kls(*args, **kw)

  def register(self, kls):
    self.ec.update({kls.name: kls})


Element = ElementFactory()

class BaseElement(object):
  name = None
  DTD_ELEMENT = None
  DTD_ATTLIST = {'x':'CDATA', 'y':'CDATA', 'color':'CDATA', 'width':'CDATA', 'height':'CDATA', 'image':'CDATA'}

  def __init__(self,  **kw):
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
    if isinstance(e, BaseElement):
      assert e.name in self.DTD_ELEMENT
      e.parent = self
      self.children.append(e)
    elif isinstance(e, str):
      assert '#CDATA' in self.DTD_ELEMENT
      self.children.append(e)
    else:
      assert False

  def update(self, d):
    for key, value in d.items():
      if key not in self.DTD_ATTLIST:
        raise KeyError('no such attribute %s in %s'%(key, self.name))
      #value
      #self.DTD_ATTLIST[key]
    self.attributes.update(d)

  def format(self, indent):
    s = ' '*indent + "<%s"%(self.name)
    for n, v in self.attributes.items():
      s+= ' %s=%s'%(n, str(v))
    s+=">\n"
    for c in self.children:
      if isinstance(c, BaseElement):
        s += c.format(indent+2)
      else:
        s += ' '*(indent +2) + str(c) + '\n'
    s+= ' '*indent + "</%s>\n"%(self.name)
    return s

  def __getattr__(self, name):
    if name in self.attributes:
      return self.attributes[name]
    return getattr(self.parent, name) #inherit

  def make_DTD_ELEMENT(self):
    return "<!ELEMENT %s (%s)>"%(self.name, ','.join(self.DTD_ELEMENT))
  def make_DTD_ATTLIST(self):
    s = '<!ATTLIST %s'%self.name
    for key, value in self.DTD_ATTLIST.items():
        s+='%s %s\n'%(key, str(vaule))
    s+='>'
    return s


class Board(BaseElement):
  name = 'board'
  DTD_ELEMENT = ('match, position')
Element.register(Board)


class Match(BaseElement):
  name = 'match'
  DTD_ELEMENT = ('action', 'length', 'crawford', 'score', 'score')
Element.register(Match)

class Action(BaseElement):
  name = 'action'
  DTD_ELEMENT = ('#CDATA')
Element.register(Action)

class Length(BaseElement):
  name = 'length'
  DTD_ELEMENT = ('#CDATA')
Element.register(Length)


class Crawford(BaseElement):
  name = 'crawford'
  DTD_ELEMENT = ('#CDATA')
Element.register(Crawford)


class Score(BaseElement):
  name = 'score'
  DTD_ELEMENT = ('#CDATA')
Element.register(Score)


class Position(BaseElement):
  name = 'position'
  DTD_ELEMENT =('cubeholder', 'field', 'home', 'bar') + ('point',)*24 + ('bar', 'home', 'field')
Element.register(Position)


class CubeHolder(BaseElement):
  name = 'cubeholder'
  DTD_ELEMENT = ('EMPTY', 'cube', 'chip' )
Element.register(CubeHolder)


class Field(BaseElement):
  name = 'field'
  DTD_ELEMENT = ('EMPTY', 'die', 'die', 'cube', 'chip' )
  #FIXME <!ELEMENT field (EMPTY | (die, die) | cube | chip )>
  DTD_ATTLIST = dict(BaseElement.DTD_ATTLIST, player=('you', 'him'))
  #FIXME
  #<!ATTLIST field basic
  #                player (you|him) #REQUIRED
Element.register(Field)


class Die(BaseElement):
  name = 'die'
  DTD_ELEMENT = ('#CDATA')
  DTD_ATTLIST = dict(BaseElement.DTD_ATTLIST, x_offset="#CDATA", y_offset="#CDATA")
Element.register(Die)


class Cube(BaseElement):
  name = 'cube'
  DTD_ELEMENT = ('#CDATA')
Element.register(Cube)


class Chip(BaseElement):
  DTD_ATTLIST = dict(BaseElement.DTD_ATTLIST, x_offset="#CDATA", y_offset="#CDATA")
Element.register(Chip)


class Home(BaseElement):
  name = 'home'
  DTD_ELEMENT = ('EMPTY', 'cube', 'chequer')
  #FIXME <!ELEMENT home (EMPTY |  cube | chequer )>
  DTD_ATTLIST = dict(BaseElement.DTD_ATTLIST, player=('you', 'him'))
  #FIXME
  #<!ATTLIST home basic
  #                player (you|him) #REQUIRED
Element.register(Home)


class Chequer(BaseElement):
  name = 'chequer'
  DTD_ELEMENT = ('#CDATA')
  DTD_ATTLIST = dict(BaseElement.DTD_ATTLIST, player=('you', 'him'))
  #FIXME
  #<!ATTLIST chequerbasic
  #                player (you|him) #REQUIRED
Element.register(Chequer)


class Bar(BaseElement):
  name = 'bar'
  DTD_ELEMENT = ('EMPTY', 'chequer')
  DTD_ATTLIST = dict(BaseElement.DTD_ATTLIST, player=('you', 'him'))
  #FIXME
  #<!ATTLIST bar basic
  #                player (you|him) #REQUIRED
Element.register(Bar)


class Point(BaseElement):
  name = 'point'
  DTD_ELEMENT = ('#CDATA', 'chequer')
  DTD_ATTLIST = dict(BaseElement.DTD_ATTLIST, parity=('odd', 'even'))
  #FIXME
  #<!ATTLIST point basic
  #                parity (odd|even) #REQUIRED
Element.register(Point)





class Visit(object):
  def __init__(self, callback, *args, **kw):
    self.callback = callback
    self.args = args
    self.kw = kw

  def visit(self, path=None):
    self.callback(path, *self.args, **self.kw)
    for c in path[-1].children:
      if isinstance(c, bglib.image.base.BaseElement):
        path.append(c)
        self.visit(path)
        path.pop(-1)


def make_empty_tree():
  score = list()
  score.append(Element('score', player=you))
  score.append(Element('score',  player=him))
  length = Element('length')
  crawford = Element('crawford')
  action = Element('action')

  match = Element('match')
  match.append(action)
  match.append(crawford)
  match.append(length)
  match.append(score[bglib.model.constants.you])
  match.append(score[bglib.model.constants.him])


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
  cubeholder = CubeHolder()

  position = Element('position')
  position.append(cubeholder)
  position.append(field[bglib.model.constants.you])
  position.append(home[bglib.model.constants.you])
  position.append(bar[bglib.model.constants.him])
  for i in range(1, 25):
    if i%2:
      pt = Element('point', parity="odd")
    else:
      pt = Element('point', parity="even")
    pt.append(str(i))
    position.append(pt)
    points.append(pt)
  position.append(bar[bglib.model.constants.you])
  position.append(home[bglib.model.constants.him])
  position.append(field[bglib.model.constants.him])

  board = Element('board')
  board.append(position)
  board.append(match)
  return board, points, home, bar, field


if __name__ == '__main__':
  b, p, home, bar, field = make_empty_tree()
  print b.format(0)


