#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2006-2008 Noriyuki Hosaka nori@backgammon.gr.jp
#

import bglib.model.constants
import bglib.image.context



class Element(object):
  def __init__(self, name, **kw):
    self.name = name
    self.children = list()
    self.attributes = dict(kw)

  def append(self, e):
    self.children.append(e)
  

  def format(self, indent):
    s = ' '*indent + "<%s"%(self.name)
    for n, v in self.attributes.items():
      s+= '%s=%s'%(n, str(v))
    s+=">\n"
    for c in self.children:
      if isinstance(c, Element):
        s += c.format(indent+2)
      else:
        s += ' '*(indent +2) + str(c) + '\n'
    s+= ' '*indent + "</%s>\n"%(self.name)
    return s

you = "'"+bglib.model.constants.player_string[bglib.model.constants.you]+"'"
him = "'"+bglib.model.constants.player_string[bglib.model.constants.him]+"'"

def make_empty_tree():
  b = Element('board')
  b.append(Element('field', player=you))
  b.append(Element('home', player=you))
  b.append(Element('bar', player=him))
  for i in range(1, 25):
    if i%2:
      pt = Element('point', parity='odd')
    else:
      pt = Element('point', parity='even')
    pt.append(i)
    b.append(pt)
  b.append(Element('bar', player=you))
  b.append(Element('home', player=him))
  b.append(Element('field', player=him))
  return b


class Context(bglib.image.context.Context):
  name = 'XML'
  def __init__(self, style):
    bglib.image.context.Context.__init__(self, style)
    self.stack = list()
    self.xml = make_empty_tree()

  def draw_your_point_at(self, point, checker_count):
    chequer = Element('chequer', player=you)
    chequer.append(str(checker_count))
    for c in self.xml.children:
      for pt in c.children:
        if isinstance(pt, int):
          if pt == point:
            c.append(chequer)
            return
    return

  def draw_his_point_at(self, point, checker_count):pass
  def draw_empty_point_at(self, point):pass
  def draw_your_bar(self, checker_count):pass
  def draw_his_bar(self, checker_count):pass
  def draw_center_bar(self):pass
  def draw_your_home(self, checker_count):pass
  def draw_his_home(self, checker_count):pass
  def draw_cubeholder(self):pass

  # cube holder
  def draw_your_cube(self, cube_in_logarithm):pass
  def draw_his_cube(self, cube_in_logarithm):pass
  def draw_center_cube(self, cube_in_logarithm):pass

  # field
  def draw_your_empty_field(self):pass
  def draw_his_empty_field(self):pass
  def draw_you_offered_double(self, cube_in_logarithm):pass
  def draw_he_offered_double(self, cube_in_logarithm):pass
  def draw_you_offered_resign(sefl, rtype):pass
  def draw_he_offered_resign(self, rtype):pass
  def draw_your_dice_in_field(self, dice):pass
  def draw_his_dice_in_field(self, dice):pass

  # who is on action
  def draw_you_to_play(self):pass
  def draw_him_to_play(self):pass

  def draw_frame(self):pass

  def draw_your_score(self, score):pass
  def draw_his_score(self, score):pass
  def draw_match_length(self, length):pass
  def draw_crawford_flag(self, flag):pass
  def result(self):
    return self.xml.format(0)

bglib.image.context.context_factory.register(Context)


if __name__ == '__main__':
  import bglib.model.board
  import bglib.image.renderer
  import bglib.depot.lines
  board = bglib.model.board.board()
  renderer = bglib.image.renderer.renderer
  style = bglib.depot.lines.CRLFProxy('./bglib/image/resource/align.txt')
  context_factory = bglib.image.context.context_factory
  context = context_factory.new_context('XML', style)
  xml = renderer.render(context, board)
  print xml

