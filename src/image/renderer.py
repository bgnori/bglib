#!/usrbin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2006-2008 Noriyuki Hosaka nori@backgammon.gr.jp
#
import logging

import bglib.model
import bglib.image.context
#import bglib.image.style
import bglib.image.PIL
bglib.image.context.context_factory.register(bglib.image.PIL.Context)

import bglib.image.wxpython
bglib.image.context.context_factory.register(bglib.image.wxpython.Context)

class Renderer(object):
  def context(self):
    return self._context

  def draw_points(self, board):
    context = self.context()
    you, him = board.position
    for i in range(1, 25):
      if you[i-1]:
        context.draw_your_point_at(i, you[i-1])
      elif him[24-i]:
        context.draw_his_point_at(i, him[24-i])
      else:
        context.draw_empty_point_at(i)

  def draw_bar(self, board):
    context = self.context()
    you, him = board.position
    context.draw_your_bar(you[24])
    context.draw_his_bar(him[24])
    context.draw_center_bar()

  def draw_home(self, board):
    context = self.context()
    you, him = board.position
    context.draw_your_home(15 - reduce(lambda x, y: x+y, you))
    context.draw_his_home(15 - reduce(lambda x, y: x+y, him))

  def draw_you_are_on_roll_cube_action(self, board):
    context = self.context()
    context.draw_you_to_play()
    context.draw_he_offered_double(0)
    context.draw_you_offered_double(0)
    context.draw_your_cube(board.cube_owner == bglib.model.you and board.cube_value or 0)
    context.draw_his_cube(board.cube_owner == bglib.model.him and board.cube_value or 0)
    context.draw_center_cube(board.cube_owner == bglib.model.center and board.cube_value or 0)

  def draw_you_doubled_he_is_on_take_or_pass(self, board):
    context = self.context()
    context.draw_him_to_play()
    context.draw_you_offered_double(board.cube_value)
    context.draw_he_offered_double(0)
    context.draw_your_cube(0)
    context.draw_his_cube(0)
    context.draw_center_cube(0)

  def draw_you_doubled_he_took_you_are_on_roll(self, board):
    context = self.context()
    context.draw_you_to_play()
    context.draw_you_offered_double(0)
    context.draw_he_offered_double(0)
    context.draw_your_cube(0)
    context.draw_his_cube(board.cube_value)
    context.draw_center_cube(0)

  def draw_you_rolled(self, board):
    context = self.context()
    context.draw_you_to_play()
    context.draw_your_dice_in_field(board.rolled)
    context.draw_his_dice_in_field(0)
    context.draw_your_cube(board.cube_owner == bglib.model.you and board.cube_value or 0)
    context.draw_his_cube(board.cube_owner == bglib.model.him and board.cube_value or 0)
    context.draw_center_cube(board.cube_owner == bglib.model.center and board.cube_value or 0)

  def draw_he_is_on_roll_cube_action(self, board):
    context = self.context()
    context.draw_him_to_play()
    context.draw_he_offered_double(0)
    context.draw_you_offered_double(0)
    context.draw_your_cube(board.cube_owner == bglib.model.you and board.cube_value or 0)
    context.draw_his_cube(board.cube_owner == bglib.model.him and board.cube_value or 0)
    context.draw_center_cube(board.cube_owner == bglib.model.center and board.cube_value or 0)


  def draw_he_doubled_you_are_on_take_or_pass(self, board):
    context = self.context()
    context.draw_you_to_play()
    context.draw_you_offered_double(0)
    context.draw_he_offered_double(board.cube_value)
    context.draw_your_cube(0)
    context.draw_his_cube(0)
    context.draw_center_cube(0)

  def draw_he_doubled_you_took_he_is_on_roll(self, board):
    context = self.context()
    context.draw_him_to_play()
    context.draw_you_offered_double(0)
    context.draw_he_offered_double(0)
    context.draw_your_cube(board.cube_value)
    context.draw_his_cube(0)
    context.draw_center_cube(0)

  def draw_he_rolled(self, board):
    context = self.context()
    context.draw_him_to_play()
    context.draw_your_dice_in_field(board.rolled)
    context.draw_his_dice_in_field(board.rolled)
    context.draw_your_cube(board.cube_owner == bglib.model.you and board.cube_value or 0)
    context.draw_his_cube(board.cube_owner == bglib.model.him and board.cube_value or 0)
    context.draw_center_cube(board.cube_owner == bglib.model.center and board.cube_value or 0)

  def draw_field(self, board):
    '''Following Cases with 
      - board.on_action
      - board.on_inner_action
    '''
    context = self.context()

    if board.on_action == bglib.model.you and not board.rolled:
      if not board.doubled and board.on_inner_action == bglib.model.you:
        self.draw_you_are_on_roll_cube_action(board)

      if board.doubled and board.on_inner_action == bglib.model.him:
        self.draw_you_doubled_he_is_on_take_or_pass(board)

      if board.doubled and board.on_inner_action == bglib.model.you:
        self.draw_you_doubled_he_took_you_are_on_roll(board)

    if board.on_action == bglib.model.you and  board.rolled:
      self.draw_you_rolled(board)

    if board.on_action == bglib.model.him and not board.rolled:
      if not board.doubled and board.on_inner_action == bglib.model.him:
        self.draw_he_is_on_roll_cube_action(board)

      if board.doubled and board.on_inner_action == bglib.model.you:
        self.draw_he_doubled_you_are_on_take_or_pass(board)

      if board.doubled and board.on_inner_action == bglib.model.him:
        self.draw_he_doubled_you_took_he_is_on_roll(board)

    if board.on_action == bglib.model.him and  board.rolled:
      self.draw_he_rolled(board)

  def draw_frame(self):
    context = self.context()
    context.draw_frame()

  def render(self, context, board):
    self._context = context

    self.draw_frame()
    self.draw_points(board)
    self.draw_bar(board)
    self.draw_home(board)
    self.draw_field(board)
    return context.result()

renderer = Renderer()
if __name__ == '__main__':
  style = bglib.image.style.Style(hoge='piyo')
  context = bglib.image.context.context_factory.new_context('Null', style)
  board = bglib.model.board()
  image = renderer.render(context, board)


