#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2006-2008 Noriyuki Hosaka nori@backgammon.gr.jp
#

import os.path

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


class BaseAttribute(object):
  def __init__(self, css_path, defualt=None):
    self.css_path = css_path
    self._value = defualt
 
  def parse(self, s):
    pass

  @classmethod
  def is_inherit(cls):
    return False
  def set(self, value):
    self._value = value
  def get(self):
    return self._value
  def __hash__(self):
    return hash(self.value)
  def __str__(self):
    return str(self.get())

class InheritMixIn(object):
  @classmethod
  def is_inherit(cls):
    return True

class IntAttribute(InheritMixIn, BaseAttribute):
  def parse(self, s):
    self.set(int(s))

class StringAttribute(BaseAttribute):
  def parse(self, s):
    self.set(s)

class ColorAttribute(StringAttribute):
  def parse(self, s):
    #FIXME validation is needed
    self.set(s)

class URIAttribute(StringAttribute):
  def parse(self, s):
    dir = os.path.dirname(self.css_path)
    fn = s.split('"')[1]
    self.set(os.path.join(dir, fn))
  
class FlipAttribute(InheritMixIn, StringAttribute):
  pass
class ParityAttribute(StringAttribute):
  pass
class PlayerAttribute(StringAttribute):
  pass


class BaseElement(object):
  name = None
  DTD_ELEMENT = None
  DTD_ATTLIST = {'x':IntAttribute, 'y':IntAttribute,
                  'width':IntAttribute, 'height':IntAttribute,
                 'image':URIAttribute, 'flip': FlipAttribute,
                 'background': ColorAttribute, 'color':ColorAttribute, 
                 'font':StringAttribute}

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
      assert '#PCDATA' in self.DTD_ELEMENT
      self.children.append(e)
    else:
      assert False

  def update(self, css_path, d):
    for key, value in d.items():
      if key not in self.DTD_ATTLIST:
        raise KeyError('no such attribute %s in %s'%(key, self.name))
      a = self.attributes.get(key, self.DTD_ATTLIST[key](css_path))
      a.parse(value)
      self.attributes.update({key:a})

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
    if name in self.DTD_ATTLIST:
      a = self.attributes.get(name)
      if a:
        return a.get()
      elif self.DTD_ATTLIST[name].is_inherit():
        return getattr(self.parent, name)
    raise AttributeError('Element %s does not have such attribute "%s".'%(self.name, name))

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
  DTD_ELEMENT = ('#PCDATA')
Element.register(Action)

class Length(BaseElement):
  name = 'length'
  DTD_ELEMENT = ('#PCDATA')
Element.register(Length)


class Crawford(BaseElement):
  name = 'crawford'
  DTD_ELEMENT = ('#PCDATA')
Element.register(Crawford)


class Score(BaseElement):
  name = 'score'
  DTD_ELEMENT = ('#PCDATA')
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
  DTD_ATTLIST = dict(BaseElement.DTD_ATTLIST,
                     player=PlayerAttribute)
  #FIXME
  #<!ATTLIST field basic
  #                player (you|him) #REQUIRED
Element.register(Field)


class Die(BaseElement):
  name = 'die'
  DTD_ELEMENT = ('#PCDATA')
  DTD_ATTLIST = dict(BaseElement.DTD_ATTLIST,
                     x_offset=IntAttribute,
                     y_offset=IntAttribute)
Element.register(Die)


class Cube(BaseElement):
  name = 'cube'
  DTD_ELEMENT = ('#PCDATA')
Element.register(Cube)


class Chip(BaseElement):
  DTD_ATTLIST = dict(BaseElement.DTD_ATTLIST,
                     x_offset=IntAttribute,
                     y_offset=IntAttribute)
Element.register(Chip)


class Home(BaseElement):
  name = 'home'
  DTD_ELEMENT = ('EMPTY', 'cube', 'chequer')
  #FIXME <!ELEMENT home (EMPTY |  cube | chequer )>
  DTD_ATTLIST = dict(BaseElement.DTD_ATTLIST,
                     player=PlayerAttribute)
  #FIXME
  #<!ATTLIST home basic
  #                player (you|him) #REQUIRED
Element.register(Home)


class Chequer(BaseElement):
  name = 'chequer'
  DTD_ELEMENT = ('#PCDATA')
  DTD_ATTLIST = dict(BaseElement.DTD_ATTLIST,
                     player=PlayerAttribute)
  #FIXME
  #<!ATTLIST chequerbasic
  #                player (you|him) #REQUIRED
Element.register(Chequer)


class Bar(BaseElement):
  name = 'bar'
  DTD_ELEMENT = ('EMPTY', 'chequer')
  DTD_ATTLIST = dict(BaseElement.DTD_ATTLIST,
                     player=PlayerAttribute)
  #FIXME
  #<!ATTLIST bar basic
  #                player (you|him) #REQUIRED
Element.register(Bar)


class Point(BaseElement):
  name = 'point'
  DTD_ELEMENT = ('#PCDATA', 'chequer')
  DTD_ATTLIST = dict(BaseElement.DTD_ATTLIST,
                     parity=ParityAttribute)
  #FIXME
  #<!ATTLIST point basic
  #                parity (odd|even) #REQUIRED
Element.register(Point)



class ElementTree(object):
  def __init__(self):
    self.create_tree()

  def visit(self, callback, path, *args, **kw):
    callback(path, *args, **kw)
    for c in path[-1].children:
      if isinstance(c, bglib.image.base.BaseElement):
        path.append(c)
        self.visit(callback, path, *args, **kw)
        path.pop(-1)
  def css(self, fname):
    p = bglib.image.css.CSSParser()
    rules = list()
    f = file(fname)
    for no, line in enumerate(f.readlines()):
      r = p.rule(fname, no + 1, line)
      if r:
        rules.append(r)
    def apply(path):
      for r in rules:
        r.apply(path)
    self.visit(apply, [self.board])

  def create_tree(self):
    score = list()
    score.append(Element('score', player=you))
    score.append(Element('score',  player=him))
    self.score = score
    length = Element('length')
    self.length = length
    crawford = Element('crawford')
    self.crawford = crawford
    action = Element('action')
    self.action = action

    match = Element('match')
    match.append(action)
    match.append(crawford)
    match.append(length)
    match.append(score[bglib.model.constants.you])
    match.append(score[bglib.model.constants.him])
    self.match = match

    points = list()
    points.append(None)
    self.points = points
    home = list()
    home.append(Element('home', player=you))
    home.append(Element('home', player=him))
    self.home = home
    bar = list()
    bar.append(Element('bar', player=you))
    bar.append(Element('bar', player=him))
    self.bar = bar
    field = list()
    field.append(Element('field', player=you))
    field.append(Element('field', player=him))
    self.field = field
    cubeholder = CubeHolder()
    self.cubeholder = cubeholder

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
      self.points = points
    position.append(bar[bglib.model.constants.you])
    position.append(home[bglib.model.constants.him])
    position.append(field[bglib.model.constants.him])
    self.position = position

    board = Element('board')
    board.append(position)
    board.append(match)
    self.board = board

if __name__ == '__main__':
  t = ElementTree()
  print t.board.format(0)


