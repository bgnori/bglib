#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2006-2008 Noriyuki Hosaka nori@backgammon.gr.jp
#

import os.path

import bglib.image.css
import bglib.model.constants

from bglib.model.constants import YOU, HIM

class  ElementFactory(object):
  def __init__(self):
    self.ec = dict()

  def __call__(self, name, *args, **kw):
    kls = self.ec[name]
    return kls(*args, **kw)

  def register(self, kls):
    assert kls.name
    self.ec.update({kls.name: kls})

  def make_dtd(self):
    CRLF = '\n'
    r = ''
    for elemclass in self.ec.values():
      r+= elemclass.make_DTD_ELEMENT() + CRLF
      r+= "<!ATTLIST %s "%elemclass.name + CRLF
      r+= CRLF.join(list(elemclass. make_DTD_ATTLIST())) + CRLF
      r+= ">" + CRLF
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
    if not self.is_acceptable(value):
      raise TypeError('%s got bad value %s'%(self.name, str(value)))
    self._value = value
    
  def get(self):
    return self._value
  def __hash__(self):
    return hash(self.value)
  def __str__(self):
    return str(self.get())
  def is_match(self, value):
    return self.parse(value) == self.get()
  def is_acceptable(self, v):
    return False
  __repr__ = __str__

class InheritMixIn(object):
  @classmethod
  def is_inherit(cls):
    return True

class IntAttribute(BaseAttribute):
  name = 'int'
  def is_acceptable(self, v):
    return isinstance(v, int)
  def parse(self, s):
    return int(s)

class IntWithDefaultZeroAttribute(IntAttribute):
  name = 'intDefaultZero'
  default = 0

class FloatAttribute(BaseAttribute):
  name = 'float'
  def is_acceptable(self, v):
    return isinstance(v, float)
  def parse(self, s):
    return float(s)
class InheritFloatAttribute(InheritMixIn, FloatAttribute):
  name = 'inheritFloat'

class InheritIntAttribute(InheritMixIn, IntAttribute):
  pass

class StringAttribute(BaseAttribute):
  name = 'string'
  def is_acceptable(self, v):
    return isinstance(v, str)

class IdAttribute(StringAttribute):
  name = 'id'

class DieStyleAttribute(StringAttribute):
  name='die_style'
  default='dot'
  def is_acceptable(self, v):
    #FIXME
    return isinstance(v, str) and v in ['dot', 'numeric']
  def parse(self, s):
    #FIXME validation is needed
    return s

class ColorAttribute(StringAttribute):
  name = 'color'
  def is_acceptable(self, v):
    #FIXME
    return isinstance(v, str)
  def parse(self, s):
    #FIXME validation is needed
    return s

class URIAttribute(StringAttribute):
  def is_acceptable(self, v):
    #FIXME
    return isinstance(v, str)
  def parse(self, s):
    dir = os.path.dirname(self.css_path)
    fn = s.split('"')[1]
    return os.path.join(dir, fn)
  
class BoolAttribute(BaseAttribute):
  def parse(self, s):
    return bool(s)
  def is_acceptable(self, v):
    return isinstance(v, bool)

class FlipAttribute(InheritMixIn, BoolAttribute):
  default = False
  name = 'flip'

class FillAttribute(InheritMixIn, BoolAttribute):
  default = True 
  name = 'fill'

class HideCountAttribute(BoolAttribute):
  default = False
  name = 'hide_count'
  def parse(self, s):
    return bool(s)
  def is_acceptable(self, v):
    return isinstance(v, bool)

class FontAttribute(InheritMixIn, URIAttribute):
  name = 'font'
  def is_acceptable(self, v):
    return isinstance(v, str)

class ParityAttribute(StringAttribute):
  name = 'parity'
  def is_acceptable(self, v):
    return isinstance(v, str) and v in ['even', 'odd']

class PlayerAttribute(StringAttribute):
  name='player'
  def is_acceptable(self, v):
    return isinstance(v, str) and v in bglib.model.constants.PLAYER_STRING

class InitialCubeString(StringAttribute):
  name='initialCube'


class BaseElement(object):
  name = None
  DTD_ELEMENT = None
  DTD_ATTLIST = dict(x=InheritIntAttribute, 
                     y=InheritIntAttribute,
                     width=InheritIntAttribute,
                     height=InheritIntAttribute,
                     image=URIAttribute, 
                     flip=FlipAttribute,
                     background=ColorAttribute,
                     color=ColorAttribute, 
                     font=FontAttribute,
                     mag=InheritFloatAttribute,
                     )

  def __init__(self,  **kw):
    self.__dict__['children'] = list()
    self.__dict__['attributes'] = dict([[key, self.DTD_ATTLIST[key](value=value)] for key, value in kw.items()])
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

  def calc_mag(self, xy):
    return [self.apply_mag(xy[0]), self.apply_mag(xy[1])]

  def apply_mag(self, x):
    return int(x *self.mag)

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
      assert a
      v = a.parse(value)
      setattr(self, name, v)

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

  def bg_draw(self, context):
    assert hasattr(self, 'background')
    size = self.calc_mag((self.width, self.height))
    position = self.calc_mag((self.x, self.y))
    context.draw_rect(tuple(position), tuple(size), self.background)

  def draw(self, context):
    size = self.calc_mag((self.width, self.height))
    position = self.calc_mag((self.x, self.y))
    if hasattr(self, 'image'):
      loaded = context.load_image(self.image, size, getattr(self, 'flip'))
      context.paste_image(loaded, position, size)

  def __setattr__(self, name, value):
    if name in self.DTD_ATTLIST:
      if name in self.attributes:
        if isinstance(value, BaseAttribute):
          self.attributes[name] = value
        else:
          self.attributes[name].set(value)
      else:
        ac = self.DTD_ATTLIST[name]
        a = ac()
        a.set(value)
        self.attributes.update({name:a})
        
    else:
      self.__dict__[name] = value

  def __getattr__(self, name):
    if name in self.__dict__:
      return self.__dict__[nane]
    if name in self.DTD_ATTLIST:
      a = self.attributes.get(name, None)
      if a:
        return a.get()
      elif self.DTD_ATTLIST[name].is_inherit() and self.parent is not None:
        return getattr(self.parent, name)
      else:
        try:
          return self.DTD_ATTLIST[name].default
        except AttributeError:
          raise AttributeError('Element %s is not assigned a value of attribute "%s".'%(self.name, name))
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

  def set_mag(self, bound):
    xmag = float(bound[0])/self.width
    ymag = float(bound[1])/self.height
    assert xmag > 0.0
    assert ymag > 0.0
    self.mag = min(xmag, ymag)
    assert self.width * self.mag <= bound[0]
    assert self.height * self.mag <= bound[1]

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
  def draw(self, context):
    size = self.calc_mag((self.width, self.height))
    position = self.calc_mag((self.x, self.y))
    image = getattr(self, 'image', None)
    color = getattr(self, 'color', 'white')
    font = getattr(self, 'font', None)
    if image:
      loaded = context.load_image(image, size, self.flip)
      context.paste_image(loaded, position, size)
    elif font:
      context.draw_text(
                position, size, self.children[0], self.font, self.color)

Element.register(Action)

class Length(BaseElement):
  name = 'length'
  DTD_ELEMENT = ('#PCDATA', )
  def draw(self, context):
    size = self.calc_mag((self.width, self.height))
    position = self.calc_mag((self.x, self.y))
    image = getattr(self, 'image', None)
    color = getattr(self, 'color', 'white')
    font = getattr(self, 'font', None)
    if image:
      loaded = context.load_image(image, size, self.flip)
      context.paste_image(loaded, position, size)
    elif font:
      context.draw_text(
                position, size, self.children[0], self.font, self.color)

Element.register(Length)

class Crawford(BaseElement):
  name = 'crawford'
  DTD_ELEMENT = ('#PCDATA', )
  def draw(self, context):
    size = self.calc_mag((self.width, self.height))
    position = self.calc_mag((self.x, self.y))
    image = getattr(self, 'image', None)
    color = getattr(self, 'color', 'white')
    font = getattr(self, 'font', None)
    if image:
      loaded = context.load_image(image, size, getattr(self, 'flip'))
      context.paste_image(loaded, position, size)
    elif font:
      if self.children[0] == 'True':
        context.draw_text(position, size, '*', self.font, self.color)
Element.register(Crawford)

class Score(BaseElement):
  name = 'score'
  DTD_ELEMENT = ('#PCDATA', )
  DTD_ATTLIST = dict(BaseElement.DTD_ATTLIST,
                     player=PlayerAttribute)
  def draw(self, context):
    size = self.calc_mag((self.width, self.height))
    position = self.calc_mag((self.x, self.y))
    image = getattr(self, 'image', None)
    color = getattr(self, 'color', 'white')
    font = getattr(self, 'font', None)
    if image:
      loaded = context.load_image(image, size, getattr(self, 'flip'))
      context.paste_image(loaded, position, size)
    elif font:
      context.draw_text(position, size, self.children[0], self.font, self.color)
Element.register(Score)

class Position(BaseElement):
  name = 'position'
  DTD_ELEMENT =('cubeholder', 'field', 'home', 'bar', 'point', 'top_frame', 'bottom_frame')
Element.register(Position)

class TopFrame(BaseElement):
  name = 'top_frame'
  DTD_ELEMENT = ('#PCDATA', )
Element.register(TopFrame)

class BottomFrame(BaseElement):
  name = 'bottom_frame'
  DTD_ELEMENT = ('#PCDATA', )
Element.register(BottomFrame)

class CubeHolder(BaseElement):
  name = 'cubeholder'
  DTD_ELEMENT = ('#PCDATA', 'cube')
Element.register(CubeHolder)


class Field(BaseElement):
  name = 'field'
  DTD_ELEMENT = ('#PCDATA', 'die', 'cube', 'resign' )
  #FIXME <!ELEMENT field (EMPTY | (die, die) | cube | resign )>
  DTD_ATTLIST = dict(BaseElement.DTD_ATTLIST,
                     player=PlayerAttribute,
                     text=StringAttribute)

  def draw(self, context):
    size = self.calc_mag((self.width, self.height))
    position = self.calc_mag((self.x, self.y))
    image = getattr(self, 'image', None)
    color = getattr(self, 'color', 'black')
    font = getattr(self, 'font', None)
    text = getattr(self, 'text', '')
    flip = getattr(self, 'flip', None)
    if image:
      loaded = context.load_image(image, size, flip)
      context.paste_image(loaded, position, size)
    elif text and font:
      context.draw_text(position, size, text, self.font, color)
  #FIXME
  #<!ATTLIST field basic
  #                player (YOU|HIM) #REQUIRED
Element.register(Field)


class Die(BaseElement):
  name = 'die'
  DTD_ELEMENT = ('#PCDATA', )
  DTD_ATTLIST = dict(BaseElement.DTD_ATTLIST,
                     backgammon=ColorAttribute,
                     diestyle=DieStyleAttribute,
                     eyesize=IntAttribute,
                     id=IdAttribute)

  def draw(self, context):
    size = self.calc_mag((self.width, self.height))
    position = self.calc_mag((self.x, self.y))
    image = getattr(self, 'image', None)
    color = getattr(self, 'color', 'black')
    font = getattr(self, 'font', None)
    style = self.diestyle
    if image:
      loaded = context.load_image(image, size, getattr(self, 'flip'))
      context.paste_image(loaded, position, size)
    elif style == 'numeric' and font:
      context.draw_text(position, size, self.children[0], self.font, color)
    elif style == 'dot':
      dotsize = self.calc_mag((self.eyesize, self.eyesize))
      center = (position[0] + size[0]/2 - dotsize[0]/2, position[1] + size[1]/2 -dotsize[1]/2)
      ltop = (position[0] + size[0]*1/4 - dotsize[0]/2, position[1] + size[1]*1/4 - dotsize[1]/2)
      lmid = (position[0] + size[0]*1/4 - dotsize[0]/2, position[1] + size[1]*2/4 - dotsize[1]/2)
      lbot = (position[0] + size[0]*1/4 - dotsize[0]/2, position[1] + size[1]*3/4 - dotsize[1]/2)
      rtop = (position[0] + size[0]*3/4 - dotsize[0]/2, position[1] + size[1]*1/4 - dotsize[1]/2)
      rmid = (position[0] + size[0]*3/4 - dotsize[0]/2, position[1] + size[1]*2/4 - dotsize[1]/2)
      rbot = (position[0] + size[0]*3/4 - dotsize[0]/2, position[1] + size[1]*3/4 - dotsize[1]/2)
      if self.children[0] == '1':
        context.draw_ellipse(center, dotsize, fill=color)
      elif self.children[0] == '2':
        context.draw_ellipse(rtop, dotsize, fill=color)
        context.draw_ellipse(lbot, dotsize, fill=color)
      elif self.children[0] == '3':
        context.draw_ellipse(rtop, dotsize, fill=color)
        context.draw_ellipse(center, dotsize, fill=color)
        context.draw_ellipse(lbot, dotsize, fill=color)
      elif self.children[0] == '4':
        context.draw_ellipse(rtop, dotsize, fill=color)
        context.draw_ellipse(rbot, dotsize, fill=color)
        context.draw_ellipse(ltop, dotsize, fill=color)
        context.draw_ellipse(lbot, dotsize, fill=color)
      elif self.children[0] == '5':
        context.draw_ellipse(rtop, dotsize, fill=color)
        context.draw_ellipse(rbot, dotsize, fill=color)
        context.draw_ellipse(ltop, dotsize, fill=color)
        context.draw_ellipse(lbot, dotsize, fill=color)
        context.draw_ellipse(center, dotsize, fill=color)

      elif self.children[0] == '6':
        context.draw_ellipse(rtop, dotsize, fill=color)
        context.draw_ellipse(rmid, dotsize, fill=color)
        context.draw_ellipse(rbot, dotsize, fill=color)
        context.draw_ellipse(ltop, dotsize, fill=color)
        context.draw_ellipse(lmid, dotsize, fill=color)
        context.draw_ellipse(lbot, dotsize, fill=color)
      else:
        assert False
    else:
      assert False
Element.register(Die)


class Cube(BaseElement):
  name = 'cube'
  DTD_ELEMENT = ('#PCDATA', )
  DTD_ATTLIST = dict(BaseElement.DTD_ATTLIST,
                     initialCube=InitialCubeString)
  def draw(self, context):
    size = self.calc_mag((self.width, self.height))
    position = self.calc_mag((self.x, self.y))
    image = getattr(self, 'image', None)
    color = getattr(self, 'color', 'white')
    font = getattr(self, 'font', None)
    if image:
      loaded = context.load_image(image, size, getattr(self, 'flip'))
      context.paste_image(loaded, position, size)
    elif font:
      log = int(self.children[0])
      v = pow(2, log)
      if v == 1 and hasattr(self, 'initialCube'):
        context.draw_text(position, size, str(self.initialCube), self.font, color)
      else:
        context.draw_text(position, size, str(v), self.font, color)
    else:
      assert False

Element.register(Cube)


class Resign(BaseElement):
  name = 'resign'
  DTD_ELEMENT = ('#PCDATA', )
  DTD_ATTLIST = dict(BaseElement.DTD_ATTLIST,
                     player=PlayerAttribute,
                     x_offset=IntWithDefaultZeroAttribute,
                     y_offset=IntWithDefaultZeroAttribute)
  def draw(self, context):
    size = self.calc_mag((self.width, self.height))
    position = self.calc_mag((self.x, self.y))
    image = getattr(self, 'image', None)
    color = getattr(self, 'color', 'white')
    font = getattr(self, 'font', None)
    x_offset = self.apply_mag(self.x_offset)
    y_offset = self.apply_mag(self.y_offset)
    if image:
      loaded = context.load_image(image, size, False)
      for i in range(int(self.children[0])):
        position = (position[0] + x_offset, position[1] + y_offset)
        context.paste_image(loaded, position, size)
    elif font:
      s = bglib.model.constants.RESIGN_STRINGS[int(self.children[0])]
      context.draw_text(position, size, s, self.font, color)
    else:
      assert False
Element.register(Resign)


class Home(BaseElement):
  name = 'home'
  DTD_ELEMENT = ('#PCDATA', 'cube', 'chequer')
  #FIXME <!ELEMENT home (EMPTY |  cube | chequer )>
  DTD_ATTLIST = dict(BaseElement.DTD_ATTLIST,
                     fill=FillAttribute,
                     player=PlayerAttribute)
  #FIXME
  #<!ATTLIST home basic
  #                player (YOU|HIM) #REQUIRED
Element.register(Home)


class Chequer(BaseElement):
  name = 'chequer'
  DTD_ELEMENT = ('#PCDATA', )
  DTD_ATTLIST = dict(BaseElement.DTD_ATTLIST,
                     player=PlayerAttribute,
                     x_offset=IntWithDefaultZeroAttribute, 
                     y_offset=IntWithDefaultZeroAttribute,
                     x_offset2=IntWithDefaultZeroAttribute, 
                     y_offset2=IntWithDefaultZeroAttribute,
                     hide_count=HideCountAttribute,
                     max_count=IntAttribute
                    )
  #FIXME
  #<!ATTLIST chequerbasic
  #                player (YOU|HIM) #REQUIRED
  def draw(self, context):
    count = int(self.children[0]) #FIXME
    height = self.apply_mag(self.height)
    width = self.apply_mag(self.width)
    size = (width, height)
    
    position = self.calc_mag((self.x, self.y))
    xoff = self.apply_mag(getattr(self, 'x_offset', 0))
    yoff = self.apply_mag(getattr(self, 'y_offset', 0))
    image = getattr(self, 'image', None)
    color = getattr(self, 'color', 'white')
    font = getattr(self, 'font', None)
    hide = getattr(self, 'hide_count', None)
    fill = getattr(self, 'fill', True)

    for i in range(min(count, self.max_count)):
      if image:
        loaded = context.load_image(image, size, getattr(self, 'flip'))
        context.paste_image(loaded, position, size)
      else:
        if fill:
          context.draw_ellipse(position, size, fill=color)
        else:
          context.draw_ellipse(position, size, fill)
      position[0] += xoff
      position[1] += yoff
      if position[0] + width > self.apply_mag(self.parent.x) + self.apply_mag(self.parent.width) or\
         position[1] + height > self.apply_mag(self.parent.y) + self.apply_mag(self.parent.height):
        position[0] += self.apply_mag(getattr(self, 'x_offset2', 0))
        position[1] += self.apply_mag(getattr(self, 'y_offset2', 0))

    if font is not None and not hide and count > self.max_count:
      context.draw_text(position, size, str(count), self.font, color)
Element.register(Chequer)


class Bar(BaseElement):
  name = 'bar'
  DTD_ELEMENT = ('#PCDATA', 'chequer')
  DTD_ATTLIST = dict(BaseElement.DTD_ATTLIST,
                     player=PlayerAttribute)
  #FIXME
  #<!ATTLIST bar basic
  #                player (YOU|HIM) #REQUIRED
Element.register(Bar)


class Point(BaseElement):
  name = 'point'
  DTD_ELEMENT = ('#PCDATA', 'chequer')
  DTD_ATTLIST = dict(BaseElement.DTD_ATTLIST,
                     fill=FillAttribute,
                     parity=ParityAttribute)
  #FIXME
  #<!ATTLIST point basic
  #                parity (odd|even) #REQUIRED
  def draw(self, context):
    x = self.apply_mag(self.x)
    y = self.apply_mag(self.y)
    position = (x, y)
    width = self.apply_mag(self.width) 
    height = self.apply_mag(self.height)
    size = (width, height)
    image = getattr(self, 'image', None)
    color = getattr(self, 'color', 'white')
    fill = getattr(self, 'fill', True)
    if image:
      loaded = context.load_image(image, size, getattr(self, 'flip'))
      context.paste_image(loaded, position, size)
    elif color:
      if getattr(self, 'flip'):
        pinacle = x + width/2, y + height
        rbase = x, y
        lbase = x + width, y
      else:
        pinacle = x + width/2, y
        rbase = x, y + height
        lbase = x + width, y+height
      if fill:
        context.draw_polygon([rbase, pinacle, lbase], fill=color)
      else:
        context.draw_polygon([rbase, pinacle, lbase])
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
    self.score[YOU].append(str(board.score[YOU]))
    self.score[HIM].append(str(board.score[HIM]))
    self.length.append(str(board.match_length))
    self.crawford.append(str(board.crawford))

    for i in range(1, 25):
      chequer_count = board.position[YOU][i-1]
      if chequer_count:
        chequer = Element('chequer',player=bglib.model.constants.PLAYER_STRING[YOU])
        chequer.append(str(chequer_count))
        self.points[i].append(chequer)

      chequer_count = board.position[HIM][i-1]
      if chequer_count:
        chequer = Element('chequer', player=bglib.model.constants.PLAYER_STRING[HIM])
        chequer.append(str(chequer_count))
        self.points[25-i].append(chequer)

    chequer_count = board.position[YOU][24]
    if chequer_count:
      chequer = Element('chequer', player=bglib.model.constants.PLAYER_STRING[YOU])
      chequer.append(str(chequer_count))
      self.bar[YOU].append(chequer)

    chequer_count = board.position[HIM][24]
    if chequer_count:
      chequer = Element('chequer', player=bglib.model.constants.PLAYER_STRING[HIM])
      chequer.append(str(chequer_count))
      self.bar[HIM].append(chequer)

    chequer_count = 15 - reduce(lambda x, y: x+y, board.position[YOU])
    if chequer_count:
      chequer = Element('chequer', player=bglib.model.constants.PLAYER_STRING[YOU])
      chequer.append(str(chequer_count))
      self.home[YOU].append(chequer)

    chequer_count = 15 - reduce(lambda x, y: x+y, board.position[HIM])
    if chequer_count:
      chequer = Element('chequer', player=bglib.model.constants.PLAYER_STRING[HIM])
      chequer.append(str(chequer_count))
      self.home[HIM].append(chequer)

    if not board.doubled or board.on_inner_action == board.on_action:
      if board.cube_owner == YOU:
        cube = Element('cube')
        cube.append(str(board.cube_in_logarithm))
        self.home[YOU].append(cube)
      elif board.cube_owner == HIM:
        cube = Element('cube')
        cube.append(str(board.cube_in_logarithm))
        self.home[HIM].append(cube)
      elif board.cube_owner == bglib.model.constants.CENTER:
        cube = Element('cube')
        cube.append(str(board.cube_in_logarithm))
        self.cubeholder.append(cube)
      else:
        assert False

    if board.on_action == YOU and board.rolled == (0, 0):
      if not board.doubled and board.on_inner_action == YOU:
        self.action.player = bglib.model.constants.PLAYER_STRING[YOU]
        self.action.append('you to roll or double.')
        return

      if not board.doubled and board.on_inner_action == HIM and board.resign_offer in bglib.model.constants.RESIGN_TYPES:
        self.action.player = bglib.model.constants.PLAYER_STRING[HIM]
        self.action.append('him to accept your resignation or not.')
        resign = Element('resign')
        resign.append(str(board.resign_offer))
        self.field[HIM].append(resign)
        return

      if board.doubled and board.on_inner_action == HIM:
        cube = Element('cube')
        cube.append(str(board.cube_in_logarithm+1))
        self.field[HIM].append(cube)
        self.action.player = bglib.model.constants.PLAYER_STRING[YOU]
        self.action.append('you doubled. him to take or drop.')
        return

      if board.doubled and board.on_inner_action == YOU:
        self.action.player = bglib.model.constants.PLAYER_STRING[YOU]
        self.action.append('you doubled. he took. you to roll.')
        return

    if board.on_action == YOU and  board.rolled != (0, 0):
      self.action.player = bglib.model.constants.PLAYER_STRING[YOU]
      self.action.append('you to move.')
      die = Element('die', id='right')
      die.append(str(board.rolled[0]))
      self.field[YOU].append(die)
      die = Element('die', id='left')
      die.append(str(board.rolled[1]))
      self.field[YOU].append(die)
      return

    if board.on_action == HIM and board.rolled == (0, 0):
      if not board.doubled and board.on_inner_action == HIM:
        self.action.player = bglib.model.constants.PLAYER_STRING[HIM]
        self.action.append('him to roll or double.')
        return
      if not board.doubled and board.on_inner_action == YOU and board.resign_offer in bglib.model.constants.RESIGN_TYPES:
        self.action.player = bglib.model.constants.PLAYER_STRING[YOU]
        self.action.append('you to accept his resignation or not.')
        resign = Element('resign')
        resign.append(str(board.resign_offer))
        self.field[YOU].append(resign)
        return

      if board.doubled and board.on_inner_action == YOU:
        self.action.player = bglib.model.constants.PLAYER_STRING[YOU]
        cube = Element('cube')
        cube.append(str(board.cube_in_logarithm+1))
        self.field[YOU].append(cube)
        self.action.append('he doubled. you to take or drop.')
        return

      if board.doubled and board.on_inner_action == HIM:
        self.action.player = bglib.model.constants.PLAYER_STRING[HIM]
        self.action.append('he doubled. you took. him to roll.')
        return

    if board.on_action == HIM and  board.rolled !=(0, 0):
      self.action.player = bglib.model.constants.PLAYER_STRING[HIM]
      self.action.append('him to move.')
      die = Element('die', id='right')
      die.append( str(board.rolled[0]))
      self.field[HIM].append(die)
      die = Element('die', id='left')
      die.append(str(board.rolled[1]))
      self.field[HIM].append(die)
      return

    #assert not board.doubled and board.on_inner_action == HIM and board.resign_offer not in bglib.model.constants.resign_types

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
    score.append(Element('score', player=bglib.model.constants.PLAYER_STRING[YOU]))
    score.append(Element('score',  player=bglib.model.constants.PLAYER_STRING[HIM]))
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
    match.append(score[YOU])
    match.append(score[HIM])
    self.match = match

    points = list()
    points.append(None)
    self.points = points
    home = list()
    home.append(Element('home', player=bglib.model.constants.PLAYER_STRING[YOU]))
    home.append(Element('home', player=bglib.model.constants.PLAYER_STRING[HIM]))
    self.home = home
    bar = list()
    bar.append(Element('bar', player=bglib.model.constants.PLAYER_STRING[YOU]))
    bar.append(Element('bar', player=bglib.model.constants.PLAYER_STRING[HIM]))
    self.bar = bar
    field = list()
    field.append(Element('field', player=bglib.model.constants.PLAYER_STRING[YOU]))
    field.append(Element('field', player=bglib.model.constants.PLAYER_STRING[HIM]))
    self.field = field
    cubeholder = CubeHolder()
    self.cubeholder = cubeholder

    position = Element('position')
    position.append(TopFrame())
    position.append(BottomFrame())
    position.append(cubeholder)
    position.append(field[YOU])
    position.append(home[YOU])
    position.append(bar[HIM])
    for i in range(1, 25):
      if i%2:
        pt = Element('point', parity='odd')
      else:
        pt = Element('point', parity='even')
      pt.append(str(i))
      position.append(pt)
      points.append(pt)
      self.points = points
    position.append(bar[YOU])
    position.append(home[HIM])
    position.append(field[HIM])
    self.position = position

    board = Element('board')
    board.append(match)
    board.append(position)
    self.board = board

if __name__ == '__main__':
  print Element.make_dtd()


