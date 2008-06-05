#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2006-2008 Noriyuki Hosaka nori@backgammon.gr.jp
#

import bglib.model.constants
import bglib.image.context
import bglib.image.css



class Element(object):
  def __init__(self, name, **kw):
    self.name = name
    self.children = list()
    self.attributes = dict(kw)

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

you = bglib.model.constants.player_string[bglib.model.constants.you]
him = bglib.model.constants.player_string[bglib.model.constants.him]

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


class Context(bglib.image.context.Context):
  name = 'XML'
  def __init__(self, style):
    bglib.image.context.Context.__init__(self, style)
    self.stack = list()
    root, points, home, bar, field = make_empty_tree()
    self.tree_root = root
    self.points = points
    self.home = home
    self.bar = bar
    self.field = field

  def draw_your_point_at(self, point, chequer_count):
    chequer = Element('chequer', player=you)
    chequer.append(str(chequer_count))
    self.points[point].append(chequer)

  def draw_his_point_at(self, point, chequer_count):
    chequer = Element('chequer', player=him)
    chequer.append(str(chequer_count))
    self.points[point].append(chequer)

  def draw_empty_point_at(self, point):pass

  def draw_your_bar(self, chequer_count):
    chequer = Element('chequer', player=you)
    chequer.append(str(chequer_count))
    self.bar[bglib.model.constants.you].append(chequer)

  def draw_his_bar(self, chequer_count):
    chequer = Element('chequer', player=him)
    chequer.append(str(chequer_count))
    self.bar[bglib.model.constants.him].append(chequer)

  def draw_center_bar(self):pass

  def draw_your_home(self, chequer_count):
    chequer = Element('chequer', player=you)
    chequer.append(str(chequer_count))
    self.home[bglib.model.constants.you].append(chequer)

  def draw_his_home(self, chequer_count):
    chequer = Element('chequer', player=him)
    chequer.append(str(chequer_count))
    self.home[bglib.model.constants.him].append(chequer)

  def draw_cubeholder(self):pass

  # cube holder
  def draw_your_cube(self, cube_in_logarithm):
    cube = Element('cube')
    cube.append(str(pow(2, cube_in_logarithm)))
    self.home[bglib.model.constants.you].append(cube)

  def draw_his_cube(self, cube_in_logarithm):
    cube = Element('cube')
    cube.append(str(pow(2, cube_in_logarithm)))
    self.home[bglib.model.constants.him].append(cube)

  def draw_center_cube(self, cube_in_logarithm):
    cube = Element('cube')
    cube.append("1")
    #FIXME no cubeholder element in empty tree

  # field
  def draw_your_empty_field(self):pass
  def draw_his_empty_field(self):pass

  def draw_you_offered_double(self, cube_in_logarithm):
    cube = Element('cube')
    cube.append(str(pow(2, cube_in_logarithm)))
    self.field[bglib.model.constants.him].append(cube)

  def draw_he_offered_double(self, cube_in_logarithm):
    cube = Element('cube')
    cube.append(str(pow(2, cube_in_logarithm)))
    self.home[bglib.model.constants.you].append(cube)

  def draw_you_offered_resign(sefl, rtype):
    chip = Element('chip')
    chip.append(str(rtype))
    self.home[bglib.model.constants.you].append(chip)

  def draw_he_offered_resign(self, rtype):
    chip = Element('chip')
    chip.append(str(rtype))
    self.home[bglib.model.constants.you].append(chip)

  def draw_your_dice_in_field(self, dice):
    die = Element('die')
    die.append(str(dice[0]))
    self.field[bglib.model.constants.you].append(die)
    die = Element('die')
    die.append(str(dice[1]))
    self.field[bglib.model.constants.you].append(die)

  def draw_his_dice_in_field(self, dice):
    die = Element('die')
    die.append(str(dice[0]))
    self.field[bglib.model.constants.him].append(die)
    die = Element('die')
    die.append(str(dice[1]))
    self.field[bglib.model.constants.him].append(die)

  # who is on action
  def draw_you_to_play(self):pass
  def draw_him_to_play(self):pass

  def draw_frame(self):pass

  def draw_your_score(self, score):
    score = Element('score')
    score.append(str(score))
    #self.field[bglib.model.constants.you].append(score)

  def draw_his_score(self, score):
    score = Element('score')
    score.append(str(score))

  def draw_match_length(self, length):
    e = Element('length')
    e.append(str(length))

  def draw_crawford_flag(self, flag):
    pass


  def apply(self, path, css_rules):
    for r in css_rules:
      r.apply(path)
    for c in path[-1].children:
      if isinstance(c, Element):
        path.append(c)
        self.apply(path, css_rules)
        path.pop(-1)
    
  def result(self):
    p = bglib.image.css.CSSParser()
    rules = list()
    f = file("./bglib/image/safari.css")
    for no, line in enumerate(f.readlines()):
      r = p.rule(no, line)
      if r:
        rules.append(r)
    self.apply([self.tree_root], rules)

    return self.tree_root.format(0)

bglib.image.context.context_factory.register(Context)


if __name__ == '__main__':
  import logging
  import bglib.model.board
  import bglib.image.renderer
  import bglib.depot.lines
  logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s',
                    filename="xml.log",
                    filemode="w"
                    )
  board = bglib.model.board.board()
  renderer = bglib.image.renderer.renderer
  style = bglib.depot.lines.CRLFProxy('./bglib/image/resource/align.txt')
  context_factory = bglib.image.context.context_factory
  context = context_factory.new_context('XML', style)
  xml = renderer.render(context, board)
  print xml


