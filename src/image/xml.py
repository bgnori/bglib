#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2006-2008 Noriyuki Hosaka nori@backgammon.gr.jp
#

import bglib.image.context

class Context(bglib.image.context.Context):
  name = 'XML'
  def __init__(self, style):
    bglib.image.context.Context.__init__(self, style)
  def draw_your_point_at(self, point, checker_count):pass
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

