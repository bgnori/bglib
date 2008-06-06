#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2006-2008 Noriyuki Hosaka nori@backgammon.gr.jp
#

import bglib.model.constants
import bglib.image.context
import bglib.image.base

you = bglib.model.constants.player_string[bglib.model.constants.you]
him = bglib.model.constants.player_string[bglib.model.constants.him]

class Context(bglib.image.context.Context):
  name = 'XML'
  def __init__(self, style):
    bglib.image.context.Context.__init__(self, style)
    self.stack = list()
    self.tree = bglib.image.base.ElementTree()
    self.tree_root = self.tree.board
    self.points = self.tree.points
    self.home = self.tree.home
    self.bar = self.tree.bar
    self.field = self.tree.field

  def draw_your_point_at(self, point, chequer_count):
    chequer = bglib.image.base.Element('chequer', player=you)
    chequer.append(str(chequer_count))
    self.points[point].append(chequer)

  def draw_his_point_at(self, point, chequer_count):
    chequer = bglib.image.base.Element('chequer', player=him)
    chequer.append(str(chequer_count))
    self.points[point].append(chequer)

  def draw_empty_point_at(self, point):pass

  def draw_your_bar(self, chequer_count):
    chequer = bglib.image.base.Element('chequer', player=you)
    chequer.append(str(chequer_count))
    self.bar[bglib.model.constants.you].append(chequer)

  def draw_his_bar(self, chequer_count):
    chequer = bglib.image.base.Element('chequer', player=him)
    chequer.append(str(chequer_count))
    self.bar[bglib.model.constants.him].append(chequer)

  def draw_center_bar(self):pass

  def draw_your_home(self, chequer_count):
    chequer = bglib.image.base.Element('chequer', player=you)
    chequer.append(str(chequer_count))
    self.home[bglib.model.constants.you].append(chequer)

  def draw_his_home(self, chequer_count):
    chequer = bglib.image.base.Element('chequer', player=him)
    chequer.append(str(chequer_count))
    self.home[bglib.model.constants.him].append(chequer)

  def draw_cubeholder(self):pass

  # cube holder
  def draw_your_cube(self, cube_in_logarithm):
    cube = bglib.image.base.Element('cube')
    cube.append(str(pow(2, cube_in_logarithm)))
    self.home[bglib.model.constants.you].append(cube)

  def draw_his_cube(self, cube_in_logarithm):
    cube = bglib.image.base.Element('cube')
    cube.append(str(pow(2, cube_in_logarithm)))
    self.home[bglib.model.constants.him].append(cube)

  def draw_center_cube(self, cube_in_logarithm):
    cube = bglib.image.base.Element('cube')
    cube.append("1")
    #FIXME no cubeholder element in empty tree

  # field
  def draw_your_empty_field(self):pass
  def draw_his_empty_field(self):pass

  def draw_you_offered_double(self, cube_in_logarithm):
    cube = bglib.image.base.Element('cube')
    cube.append(str(pow(2, cube_in_logarithm)))
    self.field[bglib.model.constants.him].append(cube)

  def draw_he_offered_double(self, cube_in_logarithm):
    cube = bglib.image.base.Element('cube')
    cube.append(str(pow(2, cube_in_logarithm)))
    self.home[bglib.model.constants.you].append(cube)

  def draw_you_offered_resign(sefl, rtype):
    chip = bglib.image.base.Element('chip')
    chip.append(str(rtype))
    self.home[bglib.model.constants.you].append(chip)

  def draw_he_offered_resign(self, rtype):
    chip = bglib.image.base.Element('chip')
    chip.append(str(rtype))
    self.home[bglib.model.constants.you].append(chip)

  def draw_your_dice_in_field(self, dice):
    die = bglib.image.base.Element('die')
    die.append(str(dice[0]))
    self.field[bglib.model.constants.you].append(die)
    die = bglib.image.base.Element('die')
    die.append(str(dice[1]))
    self.field[bglib.model.constants.you].append(die)

  def draw_his_dice_in_field(self, dice):
    die = bglib.image.base.Element('die')
    die.append(str(dice[0]))
    self.field[bglib.model.constants.him].append(die)
    die = bglib.image.base.Element('die')
    die.append(str(dice[1]))
    self.field[bglib.model.constants.him].append(die)

  # who is on action
  def draw_you_to_play(self):pass
  def draw_him_to_play(self):pass

  def draw_frame(self):pass

  def draw_your_score(self, score):
    score = bglib.image.base.Element('score')
    score.append(str(score))
    #self.field[bglib.model.constants.you].append(score)

  def draw_his_score(self, score):
    score = bglib.image.base.Element('score')
    score.append(str(score))

  def draw_match_length(self, length):
    e = bglib.image.base.Element('length')
    e.append(str(length))

  def draw_crawford_flag(self, flag):
    pass

  def result(self):
    return self.tree

def TextRender(path):
  e = path[-1]
  print e.name, e.width, e.height, '@', e.x, e.y, 'with', e.image, 'by', e.css_lineno


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
  style = bglib.depot.lines.CRLFProxy('./bglib/image/resource/original/align.txt')
  context_factory = bglib.image.context.context_factory
  context = context_factory.new_context('XML', style)
  xml = renderer.render(context, board)
  xml.css("./bglib/image/resource/safari/default.css")
  v = xml.visit(TextRender, [xml.board])




