#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2006-2008 Noriyuki Hosaka nori@backgammon.gr.jp
#

import os.path

import bglib.image.css
import bglib.model.constants

from bglib.model.constants import you, him

class  ElementFactory(object):
  def __init__(self):
    self.ec = dict()

  def __call__(self, name, *args, **kw):
    kls = self.ec[name]
    return kls(*args, **kw)

  def register(self, kls):
    self.ec.update({kls.name: kls})

  def make_dtd(self):
    CRLF = '\n'
    r = ''
    for elemclass in self.ec.values():
      r+= elemclass.make_DTD_ELEMENT() + CRLF
      r+= "<!ATTLIST %s \n"%elemclass.name  
      r+= CRLF.join(list(elemclass. make_DTD_ATTLIST())) + CRLF
      r+= ">\n"
    return r

  def dtd_url(self):
    return 'http://dtd.wxpygammon.org/backgammon.dtd'
    

Element = ElementFactory()


class BaseAttribute(object):
  def __init__(self, css_path=None, value=None):
    self.css_path = css_path
    self._value = value
  def parse(self, s):
    return s
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
  def is_match(self, value):
    return self.parse(value) == self.get()


class InheritMixIn(object):
  @classmethod
  def is_inherit(cls):
    return True

class IntAttribute(BaseAttribute):
  def parse(self, s):
    return int(s)

class InheritIntAttribute(InheritMixIn, IntAttribute):
  pass

class StringAttribute(BaseAttribute):
  pass

class ColorAttribute(StringAttribute):
  def parse(self, s):
    #FIXME validation is needed
    return s

class URIAttribute(StringAttribute):
  def parse(self, s):
    dir = os.path.dirname(self.css_path)
    fn = s.split('"')[1]
    return os.path.join(dir, fn)
  
class FlipAttribute(InheritMixIn, StringAttribute):
  pass

class HideCountAttribute(StringAttribute):
  pass

class FontAttribute(InheritMixIn, URIAttribute):
  pass

class ParityAttribute(StringAttribute):
  pass

class ParityAttributeEven(StringAttribute):
  def __init__(self, css_path=None):
    self.css_path = css_path
    self._value = 'even'
class ParityAttributeOdd(StringAttribute):
  def __init__(self, css_path=None):
    self.css_path = css_path
    self._value = 'odd'

class PlayerAttribute(StringAttribute):
  pass
class PlayerAttributeYou(PlayerAttribute):
  def __init__(self, css_path=None):
    self.css_path = css_path
    self._value = bglib.model.constants.player_string[you]

class PlayerAttributeHim(PlayerAttribute):
  def __init__(self, css_path=None):
    self.css_path = css_path
    self._value = bglib.model.constants.player_string[him]


class BaseElement(object):
  name = None
  DTD_ELEMENT = None
  DTD_ATTLIST = {'x':InheritIntAttribute, 'y':InheritIntAttribute,
                  'width':InheritIntAttribute, 'height':InheritIntAttribute,
                 'image':URIAttribute, 'flip': FlipAttribute,
                 'background': ColorAttribute, 'color':ColorAttribute, 
                 'font':FontAttribute}

  def __init__(self,  **kw):
    self.__dict__['children'] = list()
    self.__dict__['attributes'] = dict(kw)
    self.__dict__['parent'] = None
    self.__dict__['css_lineno'] = list()

  def __str__(self):
    s = "<%s"%self.name
    for name, value in self.attributes.items():
      s += ' %s="%s"'%(name, value)
    s += ">"
    for c in self.children:
      if not isinstance(c, BaseElement):
        s += "%s"%str(c)
    s += "</%s>"%self.name
    return s
  __repr__ = __str__

  def append(self, e):
    if isinstance(e, BaseElement):
      if self.DTD_ELEMENT is not None and e.name not in self.DTD_ELEMENT:
        raise TypeError("can't append %s to %s", e.name, self)
      e.parent = self
      self.children.append(e)
    elif isinstance(e, str):
      if '#PCDATA' not in self.DTD_ELEMENT:
        raise TypeError("can't append %s to %s", e, self)
      self.children.append(e)
    else:
      assert False

  def apply(self, css_path, d):
    for name, value in d.items():
      if name not in self.DTD_ATTLIST:
        raise KeyError('no such attribute %s in %s'%(name, self.name))
      a = self.attributes.get(name, self.DTD_ATTLIST[name](css_path=css_path))
      a.set(a.parse(value))
      setattr(self, name, a)

  def format(self, indent):
    s = ' '*indent + "<%s"%(self.name)
    for n, v in self.attributes.items():
      s+= ' %s="%s"'%(n, str(v))
    s+=">\n"
    for c in self.children:
      if isinstance(c, BaseElement):
        s += c.format(indent+2)
      else:
        s += ' '*(indent +2) + str(c) + '\n'
    s+= ' '*indent + "</%s>\n"%(self.name)
    return s

  def draw(self, context):
    if hasattr(self, 'image'):
      size = context.calc_mag((self.width, self.height))
      position = context.calc_mag((self.x, self.y))
      loaded = context.load_image(self.image, size, hasattr(self, 'flip'))
      context.paste_image(loaded, position, size)

  def __setattr__(self, name, attr):
    if name in self.DTD_ATTLIST:
      self.attributes.update({name:attr})
      return
    else:
      if name not in self.__dict__:
        raise KeyError('no such attribute %s in %s'%(name, self.name))
      if isinstance(attr, BaseAttribute):
        self.attributes[name] = attr
        return
      else:
        self.__dict__[name] = attr
      return

  def __getattr__(self, name):
    if name in self.DTD_ATTLIST:
      a = self.attributes.get(name, None)
      if a:
        return a.get()
      elif self.DTD_ATTLIST[name].is_inherit() and self.parent is not None:
        return getattr(self.parent, name)
      raise ValueError('Element %s is not assigned a value of attribute "%s".'%(self.name, name))
    raise AttributeError('Element %s does not have such attribute "%s".'%(self.name, name))

  @classmethod
  def make_DTD_ELEMENT(cls):
    if not cls.DTD_ELEMENT:
      raise TypeError('Bad class %s'%cls)
    return "<!ELEMENT %s (%s)* >"%(cls.name, '|'.join(cls.DTD_ELEMENT))

  @classmethod
  def make_DTD_ATTLIST(cls):
    for key, value in cls.DTD_ATTLIST.items():
      yield '   %s CDATA #IMPLIED'%(key)


class Board(BaseElement):
  name = 'board'
  DTD_ELEMENT = ('match', 'position')
Element.register(Board)


class Match(BaseElement):
  name = 'match'
  DTD_ELEMENT = ('action', 'length', 'crawford', 'score')
Element.register(Match)

class Action(BaseElement):
  name = 'action'
  DTD_ELEMENT = ('#PCDATA', )
  DTD_ATTLIST = dict(BaseElement.DTD_ATTLIST,
                     player=PlayerAttribute)
Element.register(Action)

class Length(BaseElement):
  name = 'length'
  DTD_ELEMENT = ('#PCDATA', )
  def draw(self, context):
    position = [self.x, self.y]
    size = [self.width, self.height]
    image = getattr(self, 'image', None)
    color = getattr(self, 'color', 'white')
    font = getattr(self, 'font', None)
    if image:
      loaded = context.load_image(image, size, hasattr(self, 'flip'))
      context.paste_image(loaded, position, size)
    elif font:
      context.draw_text((self.x, self.y), (self.width, self.height), self.children[0], self.font, self.color)
Element.register(Length)

class Crawford(BaseElement):
  name = 'crawford'
  DTD_ELEMENT = ('#PCDATA', )
  def draw(self, context):
    position = [self.x, self.y]
    size = [self.width, self.height]
    image = getattr(self, 'image', None)
    color = getattr(self, 'color', 'white')
    font = getattr(self, 'font', None)
    if image:
      loaded = context.load_image(image, size, hasattr(self, 'flip'))
      context.paste_image(loaded, position, size)
    elif font:
      if self.children[0] == 'True':
        context.draw_text((self.x, self.y), (self.width, self.height), '*', self.font, self.color)
    pass
Element.register(Crawford)

class Score(BaseElement):
  name = 'score'
  DTD_ELEMENT = ('#PCDATA', )
  DTD_ATTLIST = dict(BaseElement.DTD_ATTLIST,
                     player=PlayerAttribute)
  def draw(self, context):
    position = [self.x, self.y]
    size = [self.width, self.height]
    image = getattr(self, 'image', None)
    color = getattr(self, 'color', 'white')
    font = getattr(self, 'font', None)
    if image:
      loaded = context.load_image(image, size, hasattr(self, 'flip'))
      context.paste_image(loaded, position, size)
    elif font:
      context.draw_text((self.x, self.y), (self.width, self.height), self.children[0], self.font, self.color)
Element.register(Score)

class Position(BaseElement):
  name = 'position'
  DTD_ELEMENT =('cubeholder', 'field', 'home', 'bar', 'point',)
Element.register(Position)


class CubeHolder(BaseElement):
  name = 'cubeholder'
  DTD_ELEMENT = ('#PCDATA', 'cube', 'chip' )
Element.register(CubeHolder)


class Field(BaseElement):
  name = 'field'
  DTD_ELEMENT = ('#PCDATA', 'die', 'cube', 'chip' )
  #FIXME <!ELEMENT field (EMPTY | (die, die) | cube | chip )>
  DTD_ATTLIST = dict(BaseElement.DTD_ATTLIST,
                     player=PlayerAttribute)
  #FIXME
  #<!ATTLIST field basic
  #                player (you|him) #REQUIRED
Element.register(Field)


class Die(BaseElement):
  name = 'die'
  DTD_ELEMENT = ('#PCDATA', )
  DTD_ATTLIST = dict(BaseElement.DTD_ATTLIST,
                     x_offset=IntAttribute,
                     y_offset=IntAttribute)
  def draw(self, context):
    pass

Element.register(Die)


class Cube(BaseElement):
  name = 'cube'
  DTD_ELEMENT = ('#PCDATA', )
  def draw(self, context):
    position = [self.x, self.y]
    size = [self.width, self.height]
    image = getattr(self, 'image', None)
    color = getattr(self, 'color', 'white')
    font = getattr(self, 'font', None)
    if image:
      loaded = context.load_image(image, size, hasattr(self, 'flip'))
      context.paste_image(loaded, position, size)
    elif font:
      log = int(self.children[0])
      v = pow(2, log)
      context.draw_text((self.x, self.y), (self.width, self.height), str(v), self.font, self.color)
    else:
      assert False

Element.register(Cube)


class Chip(BaseElement):
  name = 'chip'
  DTD_ELEMENT = ('#PCDATA', )
  DTD_ATTLIST = dict(BaseElement.DTD_ATTLIST,
                     x_offset=IntAttribute,
                     y_offset=IntAttribute)
Element.register(Chip)


class Home(BaseElement):
  name = 'home'
  DTD_ELEMENT = ('#PCDATA', 'cube', 'chequer')
  #FIXME <!ELEMENT home (EMPTY |  cube | chequer )>
  DTD_ATTLIST = dict(BaseElement.DTD_ATTLIST,
                     player=PlayerAttribute)
  #FIXME
  #<!ATTLIST home basic
  #                player (you|him) #REQUIRED
Element.register(Home)


class Chequer(BaseElement):
  name = 'chequer'
  DTD_ELEMENT = ('#PCDATA', )
  DTD_ATTLIST = dict(BaseElement.DTD_ATTLIST,
                     player=PlayerAttribute,
                     x_offset=IntAttribute, 
                     y_offset=IntAttribute,
                     x_offset2=IntAttribute, 
                     y_offset2=IntAttribute,
                     hide_count=HideCountAttribute,
                     max_count=IntAttribute
                    )
  #FIXME
  #<!ATTLIST chequerbasic
  #                player (you|him) #REQUIRED
  def draw(self, context):
    count = int(self.children[0])
    position = [self.x, self.y]
    size = [self.width, self.height]
    xoff = getattr(self, 'x_offset', 0)
    yoff = getattr(self, 'y_offset', 0)
    image = getattr(self, 'image', None)
    color = getattr(self, 'color', 'white')
    font = getattr(self, 'font', None)
    hide = getattr(self, 'hide_count', None)

    for i in range(min(count, self.max_count)):
      if image:
        loaded = context.load_image(image, size, hasattr(self, 'flip'))
        context.paste_image(loaded, position, size)
      else:
        context.draw_ellipse(position, size,fill=color)
      position[0] += xoff
      position[1] += yoff
      if position[0] + self.width > self.parent.x + self.parent.width or\
         position[1] + self.height > self.parent.y + self.parent.height:
        position[0] += getattr(self, 'x_offset2', 0)
        position[1] += getattr(self, 'y_offset2', 0)

    if font is not None and hide is None and count > self.max_count:
      context.draw_text(position, size, str(count), self.font, color)
Element.register(Chequer)


class Bar(BaseElement):
  name = 'bar'
  DTD_ELEMENT = ('#PCDATA', 'chequer')
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
  def draw(self, context):
    position = [self.x, self.y]
    size = [self.width, self.height]
    image = getattr(self, 'image', None)
    color = getattr(self, 'color', 'white')
    if image:
      loaded = context.load_image(image, size, hasattr(self, 'flip'))
      context.paste_image(loaded, position, size)
    elif color:
      if hasattr(self, 'flip'):
        pinacle = self.x + self.width/2, self.y+self.height
        rbase = self.x, self.y
        lbase = self.x + self.width, self.y
      else:
        pinacle = self.x + self.width/2, self.y
        rbase = self.x, self.y+self.height
        lbase = self.x + self.width, self.y+self.height
      context.draw_polygon([rbase, pinacle, lbase], fill=color)
    else:
      assert False
Element.register(Point)


class ElementTree(object):
  def __init__(self, board=None):
    self.create_tree()
    if board: 
      self.set(board)

  def __str__(self):
    return self.board.format(0)

  def dec_xml(self):
    return '<?xml version="1.0" encoding="us-ascii" ?>\n'

  def dec_doctype(self):
    return '<!DOCTYPE board SYSTEM "%s" >\n'%(Element.dtd_url())
    
  def xml(self):
    return self.dec_xml() + self.dec_doctype() + str(self)

  def visit(self, callback, path=None, *args, **kw):
    if path is None:
      path = [self.board]
    #print 'visiting', path[-1]
    callback(path, *args, **kw)
    for c in path[-1].children:
      if isinstance(c, BaseElement):
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

  def set(self, board):
    self.score[you].append(str(board.score[you]))
    self.score[him].append(str(board.score[him]))
    self.length.append(str(board.match_length))
    self.crawford.append(str(board.crawford))

    for i in range(1, 25):
      chequer_count = board.position[you][i-1]
      if chequer_count:
        chequer = Element('chequer',player=PlayerAttributeYou())
        chequer.append(str(chequer_count))
        self.points[i].append(chequer)

      chequer_count = board.position[him][i-1]
      if chequer_count:
        chequer = Element('chequer', player=PlayerAttributeHim())
        chequer.append(str(chequer_count))
        self.points[25-i].append(chequer)

    chequer_count = board.position[you][24]
    if chequer_count:
      chequer = Element('chequer', player=PlayerAttributeYou())
      chequer.append(str(chequer_count))
      self.bar[you].append(chequer)

    chequer_count = board.position[him][24]
    if chequer_count:
      chequer = Element('chequer', player=PlayerAttributeHim())
      chequer.append(str(chequer_count))
      self.bar[him].append(chequer)

    chequer_count = 15 - reduce(lambda x, y: x+y, board.position[you])
    if chequer_count:
      chequer = Element('chequer', player=PlayerAttributeYou())
      chequer.append(str(chequer_count))
      self.home[you].append(chequer)

    chequer_count = 15 - reduce(lambda x, y: x+y, board.position[him])
    if chequer_count:
      chequer = Element('chequer', player=PlayerAttributeHim())
      chequer.append(str(chequer_count))
      self.home[him].append(chequer)

    if not board.doubled or board.on_inner_action == board.on_action:
      if board.cube_owner == you:
        cube = Element('cube')
        cube.append(str(board.cube_in_logarithm))
        self.home[you].append(cube)
      elif board.cube_owner == him:
        cube = Element('cube')
        cube.append(str(board.cube_in_logarithm))
        self.home[him].append(cube)
      elif board.cube_owner == bglib.model.constants.center:
        cube = Element('cube')
        cube.append(str(board.cube_in_logarithm))
        self.cubeholder.append(cube)
      else:
        assert False

    if board.on_action == you and board.rolled == (0, 0):
      if not board.doubled and board.on_inner_action == you:
        self.action.player = PlayerAttributeYou()
        return

      if not board.doubled and board.on_inner_action == him and board.resign_offer in bglib.model.constants.resign_types:
        self.action.player = PlayerAttributeHim()
        return

      if board.doubled and board.on_inner_action == him:
        cube = Element('cube')
        cube.append(str(board.cube_in_logarithm+1))
        self.field[him].append(cube)
        self.action.player = PlayerAttributeYou()
        return

      if board.doubled and board.on_inner_action == you:
        self.action.player = PlayerAttributeYou()
        return

    if board.on_action == you and  board.rolled != (0, 0):
      self.action.player = PlayerAttributeYou()
      return

    if board.on_action == him and board.rolled == (0, 0):
      if not board.doubled and board.on_inner_action == him:
        self.action.player = PlayerAttributeHim()
        return
      if not board.doubled and board.on_inner_action == you and board.resign_offer in bglib.model.constants.resign_types:
        self.action.player = PlayerAttributeYou()
        return

      if board.doubled and board.on_inner_action == you:
        self.action.player = PlayerAttributeYou()
        cube = Element('cube')
        cube.append(str(board.cube_in_logarithm+1))
        self.field[you].append(cube)
        return

      if board.doubled and board.on_inner_action == him:
        self.action.player = PlayerAttributeHim()
        return

    if board.on_action == him and  board.rolled !=(0, 0):
      self.action.player = PlayerAttributeHim()
      return

    #assert not board.doubled and board.on_inner_action == him and board.resign_offer not in bglib.model.constants.resign_types

    raise AssertionError("""
    Bad element tree with
    board.rolled = %s
    board.on_action = %i
    board.doubled = %i
    board.on_inner_action = %i
    board.cube_in_logarithm = %i
    board.resign_offer = %i
    """%(
    str(board.rolled),
    board.on_action,
    board.doubled,
    board.on_inner_action,
    board.cube_in_logarithm,
    board.resign_offer
    ))



  def create_tree(self):
    score = list()
    score.append(Element('score', player=PlayerAttributeYou()))
    score.append(Element('score',  player=PlayerAttributeHim()))
    self.score = score
    length = Element('length')
    self.length = length
    crawford = Element('crawford')
    self.crawford = crawford
    action = Element('action')
    self.action = action

    match = Element('match')
    match.append(action)
    match.append(length)
    match.append(crawford)
    match.append(score[you])
    match.append(score[him])
    self.match = match

    points = list()
    points.append(None)
    self.points = points
    home = list()
    home.append(Element('home', player=PlayerAttributeYou()))
    home.append(Element('home', player=PlayerAttributeHim()))
    self.home = home
    bar = list()
    bar.append(Element('bar', player=PlayerAttributeYou()))
    bar.append(Element('bar', player=PlayerAttributeHim()))
    self.bar = bar
    field = list()
    field.append(Element('field', player=PlayerAttributeYou()))
    field.append(Element('field', player=PlayerAttributeHim()))
    self.field = field
    cubeholder = CubeHolder()
    self.cubeholder = cubeholder

    position = Element('position')
    position.append(cubeholder)
    position.append(field[you])
    position.append(home[you])
    position.append(bar[him])
    for i in range(1, 25):
      if i%2:
        pt = Element('point', parity=ParityAttributeOdd())
      else:
        pt = Element('point', parity=ParityAttributeEven())
      pt.append(str(i))
      position.append(pt)
      points.append(pt)
      self.points = points
    position.append(bar[you])
    position.append(home[him])
    position.append(field[him])
    self.position = position

    board = Element('board')
    board.append(match)
    board.append(position)
    self.board = board

if __name__ == '__main__':
  print Element.make_dtd()



