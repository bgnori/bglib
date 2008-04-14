#!/usrbin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2006-2008 Noriyuki Hosaka nori@backgammon.gr.jp
#
import logging
import model


class ContextFactroy(object):
  def __init__(self):
    self._cls = dict()
  def register(self, context_class):
    self._context_classes.update({context_class.name:context_class})
  def new_context(self, name, style):
    # ContextFactroy needs size of picture, which is in style
    # Rendering process DOES NOT depend on style
    # thus Renderer object does not have style.
    return self._context_classes[name](style)

context_factory = ContextFactroy()


class Style(object):
  def __init__(self, **kw):
    self.__dict__['_d'] = dict()
    for key, value in kw.items():
      self._d.update({key:value})

  def __getattr__(self, name):
    return self._d[name]

  def __setattr__(self, name, value):
    self._d[name] = value

class Contenxt(object):
  name = 'base'
  def __init__(self, style):
    self._style = style
    self._result = None
  def style(self):
    return self._style
  def result(self):
    return self._result
  def draw_your_point_at(self, point, checker_count):
    raise NotImplemented('')
  def draw_his_point_at(self, point, checker_count):
    raise NotImplemented('')
  def draw_empty_point_at(self, point):
    raise NotImplemented('')
  def draw_your_bar(self, checker_count):
    raise NotImplemented('')
  def draw_his_bar(self, checker_count):
    raise NotImplemented('')
  def draw_center_bar(self):
    raise NotImplemented('')
  def draw_your_home(self, checker_count);
    raise NotImplemented('')
  def draw_his_home(self. checker_count):
    raise NotImplemented('')

  def draw_cube(self):
    raise NotImplemented('')
  def draw_home(self):
    raise NotImplemented('')
  def draw_field(self):
    raise NotImplemented('')
  def draw_who_to_play(self):
    raise NotImplemented('')
  def draw_dice(self):
    raise NotImplemented('')
  def draw_center(self):
    raise NotImplemented('')

import bglib.image.PIL
_factory.register(bglib.image.PIL.Context)

class Renderer(object):
  def context(self):
    return self._context()

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
    contect.draw_your_home(15 - reduce(lambda x, y: x+y, you))
    contect.draw_his_home(15 - reduce(lambda x, y: x+y, him))

  def draw_field(self. board):
    '''Following Cases with 
      - board.on_action
      - board.on_inner_action
    '''
    context = self.context()

    """ you are on roll cube action. """
    """ you doubled. he is on take or pass. """
    """ you double, he took. you are on roll. """
    """ you rolled x, y. """
    if board.on_action == model.you and not board.rolled:
      if not board.doubled and board.on_inner_action == model.you:
        context.draw_empty_field()
      if board.doubled and board.on_inner_action == model.him:
        context.draw_you_offered_double(board.cube_value)
        context.draw_your_cube(0)
        context.draw_his_cube(0)
      if board.doubled and board.on_inner_action == model.you:
        context.draw_empty_field()
        context.draw_your_cube(0)
        context.draw_his_cube(board.cube_value)

    if board.on_action == model.you and  board.rolled:
      context.draw_your_dice_in_field(board.rolled())

    """ he is  on roll cube action. """
    """ he doubled. you are on take or pass. """
    """ he doubled. you took. he is on roll. """
    """ he rolled x, y. """
    if board.on_action == model.him and not board.rolled:
      if not board.doubled and board.on_inner_action == model.him:
        context.draw_center()
        pass
      if board.doubled and board.on_inner_action == model.you:
        pass
      if board.doubled and board.on_inner_action == model.him:
        pass
    if board.on_action == model.him and  board.rolled:
      context.draw_his_dice(board.rolled())

  def self.draw_frame(self):
    context = self.context()
    context.draw_frame()

  def render(context, board):
    self._context = context

    self.draw_points(board)
    self.draw_bar(board)
    self.draw_home(board)
    self.draw_field(board)
    self.draw_frame()
    return context.result()

