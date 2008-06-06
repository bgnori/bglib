#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2006-2008 Noriyuki Hosaka nori@backgammon.gr.jp
#
import logging

import bglib.model
import bglib.image.context

class Renderer(object):
  def draw_points(self, context, board):
    you, him = board.position
    for i in range(1, 25):
      if you[i-1]:
        context.draw_your_point_at(i, you[i-1])
      elif him[24-i]:
        context.draw_his_point_at(i, him[24-i])
      else:
        context.draw_empty_point_at(i)

  def draw_bar(self, context, board):
    you, him = board.position
    assert you[24] > -1
    assert him[24] > -1
    context.draw_your_bar(you[24])
    context.draw_his_bar(him[24])
    context.draw_center_bar()

  def draw_home(self, context, board):
    you, him = board.position
    context.draw_your_home(15 - reduce(lambda x, y: x+y, you))
    context.draw_his_home(15 - reduce(lambda x, y: x+y, him))
    context.draw_cubeholder()

  def draw_you_are_on_roll_cube_action(self, context, board):
    context.draw_you_to_play()
    context.draw_your_empty_field()
    context.draw_his_empty_field()
    if board.cube_owner == bglib.model.constants.you:
      context.draw_your_cube(board.cube_in_logarithm)
    elif board.cube_owner == bglib.model.constants.him:
      context.draw_his_cube(board.cube_in_logarithm)
    elif board.cube_owner == bglib.model.constants.center:
      context.draw_center_cube(board.cube_in_logarithm)
    else:
      assert(False)

  def draw_you_offered_resign(self, context, board):
    context.draw_him_to_play()
    context.draw_your_empty_field()
    context.draw_his_empty_field()
    assert board.resign_offer in bglib.model.constants.resign_types
    context.draw_you_offered_resign(board.resign_offer)
    if board.cube_owner == bglib.model.constants.you:
      context.draw_your_cube(board.cube_in_logarithm)
    elif board.cube_owner == bglib.model.constants.him:
      context.draw_his_cube(board.cube_in_logarithm)
    elif board.cube_owner == bglib.model.constants.center:
      context.draw_center_cube(board.cube_in_logarithm)
    pass

  def draw_you_doubled_he_is_on_take_or_pass(self, context, board):
    context.draw_him_to_play()
    context.draw_your_empty_field()
    context.draw_his_empty_field()
    context.draw_you_offered_double(board.cube_in_logarithm)
    context.draw_your_cube(0)
    context.draw_his_cube(0)

  def draw_you_doubled_he_took_you_are_on_roll(self, context, board):
    context.draw_you_to_play()
    context.draw_your_empty_field()
    context.draw_his_empty_field()
    context.draw_your_cube(0)
    context.draw_his_cube(board.cube_in_logarithm)

  def draw_you_rolled(self, context, board):
    context.draw_you_to_play()
    context.draw_your_empty_field()
    context.draw_his_empty_field()
    context.draw_your_dice_in_field(board.rolled)
    context.draw_his_dice_in_field((0, 0))
    if board.cube_owner == bglib.model.constants.you:
      context.draw_your_cube(board.cube_in_logarithm)
    elif board.cube_owner == bglib.model.constants.him:
      context.draw_his_cube(board.cube_in_logarithm)
    elif board.cube_owner == bglib.model.constants.center:
      context.draw_center_cube(board.cube_in_logarithm)
    else:
      assert(False)

  def draw_he_is_on_roll_cube_action(self, context, board):
    context.draw_him_to_play()
    context.draw_your_empty_field()
    context.draw_his_empty_field()
    if board.cube_owner == bglib.model.constants.you:
      context.draw_your_cube(board.cube_in_logarithm)
    elif board.cube_owner == bglib.model.constants.him:
      context.draw_his_cube(board.cube_in_logarithm)
    elif board.cube_owner == bglib.model.constants.center:
      context.draw_center_cube(board.cube_in_logarithm)
    else:
      assert(False)

  def draw_he_offered_resign(self, context, board):
    context.draw_you_to_play()
    context.draw_your_empty_field()
    context.draw_his_empty_field()
    assert board.resign_offer in bglib.model.constants.resign_types
    context.draw_he_offered_resign(board.resign_offer)
    if board.cube_owner == bglib.model.constants.you:
      context.draw_your_cube(board.cube_in_logarithm)
    elif board.cube_owner == bglib.model.constants.him:
      context.draw_his_cube(board.cube_in_logarithm)
    elif board.cube_owner == bglib.model.constants.center:
      context.draw_center_cube(board.cube_in_logarithm)
    else:
      assert(False)
    pass

  def draw_he_doubled_you_are_on_take_or_pass(self, context, board):
    context.draw_you_to_play()
    context.draw_your_empty_field()
    context.draw_his_empty_field()
    context.draw_he_offered_double(board.cube_in_logarithm)
    context.draw_your_cube(0)
    context.draw_his_cube(0)

  def draw_he_doubled_you_took_he_is_on_roll(self, context, board):
    context.draw_him_to_play()
    context.draw_your_empty_field()
    context.draw_his_empty_field()
    context.draw_your_cube(board.cube_in_logarithm)
    context.draw_his_cube(0)

  def draw_he_rolled(self, context, board):
    context.draw_him_to_play()
    context.draw_your_empty_field()
    context.draw_his_empty_field()
    context.draw_your_dice_in_field((0,0))
    context.draw_his_dice_in_field(board.rolled)
    if board.cube_owner == bglib.model.constants.you:
      context.draw_your_cube(board.cube_in_logarithm)
    elif board.cube_owner == bglib.model.constants.him:
      context.draw_his_cube(board.cube_in_logarithm)
    elif board.cube_owner == bglib.model.constants.center:
      context.draw_center_cube(board.cube_in_logarithm)
    else:
      assert(False)

  def draw_field(self, context, board):
    '''Following Cases with 
      - board.on_action
      - board.on_inner_action
    '''
    if board.on_action == bglib.model.constants.you and board.rolled == (0, 0):
      if not board.doubled and board.on_inner_action == bglib.model.constants.you:
        self.draw_you_are_on_roll_cube_action(context, board)
        return

      if not board.doubled and board.on_inner_action == bglib.model.constants.him and board.resign_offer in bglib.model.constants.resign_types:
        self.draw_you_offered_resign(context, board)
        return

      if board.doubled and board.on_inner_action == bglib.model.constants.him:
        self.draw_you_doubled_he_is_on_take_or_pass(context, board)
        return

      if board.doubled and board.on_inner_action == bglib.model.constants.you:
        self.draw_you_doubled_he_took_you_are_on_roll(context, board)
        return

    if board.on_action == bglib.model.constants.you and  board.rolled != (0, 0):
      self.draw_you_rolled(context, board)
      return

    if board.on_action == bglib.model.constants.him and board.rolled == (0, 0):
      if not board.doubled and board.on_inner_action == bglib.model.constants.him:
        self.draw_he_is_on_roll_cube_action(context, board)
        return
      if not board.doubled and board.on_inner_action == bglib.model.constants.you and board.resign_offer in bglib.model.constants.resign_types:
        self.draw_he_offered_resign(context, board)
        return

      if board.doubled and board.on_inner_action == bglib.model.constants.you:
        self.draw_he_doubled_you_are_on_take_or_pass(context, board)
        return

      if board.doubled and board.on_inner_action == bglib.model.constants.him:
        self.draw_he_doubled_you_took_he_is_on_roll(context, board)
        return

    if board.on_action == bglib.model.constants.him and  board.rolled !=(0, 0):
      self.draw_he_rolled(context, board)
      return

    #assert not board.doubled and board.on_inner_action == bglib.model.constants.him and board.resign_offer not in bglib.model.constants.resign_types

    raise AssertionError("""
    Bad field draw with
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

  def draw_frame(self, context):
    context.draw_frame()

  def draw_session_state(self, context, board):
    context.draw_your_score(board.score[0])
    context.draw_his_score(board.score[1])
    context.draw_match_length(board.match_length)
    context.draw_crawford_flag(board.crawford)

  def render(self, context, board):
    self.draw_frame(context)
    self.draw_session_state(context, board)
    self.draw_points(context, board)
    self.draw_bar(context, board)
    self.draw_home(context, board)
    self.draw_field(context, board)
    return context.result()

renderer = Renderer()
if __name__ == '__main__':
  import bglib.depot.dict
  import bglib.model.constants
  import bglib.model.board
  style = bglib.depot.dict.Proxy(hoge='piyo')
  context = bglib.image.context.context_factory.new_context('Null', style)
  board = bglib.model.board.board()
  image = renderer.render(context, board)

