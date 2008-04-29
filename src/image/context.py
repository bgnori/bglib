#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2006-2008 Noriyuki Hosaka nori@backgammon.gr.jp
#
import logging

class ContextFactroy(object):
  def __init__(self):
    self._cls = dict()
  def register(self, context_class):
    self._cls.update({context_class.name:context_class})
  def new_context(self, name, style):
    # ContextFactroy needs size of picture, which is in style
    # Rendering process DOES NOT depend on style
    # thus Renderer object does not have style.
    return self._cls[name](style)

context_factory = ContextFactroy()


class Context(object):
  name = 'base'
  def __init__(self, style):
    self._style = style
    self._result = None
  def style(self):
    return self._style
  def result(self):
    return self._result

  # points + home +  bar
  def draw_your_point_at(self, point, checker_count):raise NotImplemented('')
  def draw_his_point_at(self, point, checker_count):raise NotImplemented('')
  def draw_empty_point_at(self, point):raise NotImplemented('')
  def draw_your_bar(self, checker_count):raise NotImplemented('')
  def draw_his_bar(self, checker_count):raise NotImplemented('')
  def draw_center_bar(self):raise NotImplemented('')
  def draw_your_home(self, checker_count):raise NotImplemented('')
  def draw_his_home(self, checker_count):raise NotImplemented('')

  # cube holder
  def draw_your_cube(self, cube_in_logarithm):raise NotImplemented('')
  def draw_his_cube(self, cube_in_logarithm):raise NotImplemented('')
  def draw_center_cube(self, cube_in_logarithm):raise NotImplemented('')

  # field
  def draw_you_offered_double(self, cube_in_logarithm):raise NotImplemented('')
  def draw_he_offered_double(self, cube_in_logarithm):raise NotImplemented('')
  def draw_your_dice_in_field(self, dice):raise NotImplemented('')
  def draw_his_dice_in_field(self, dice):raise NotImplemented('')

  # who is on action
  def draw_you_to_play(self):raise NotImplemented('')
  def draw_him_to_play(self):raise NotImplemented('')

  def draw_frame(self):raise NotImplemented('')

class NullContext(Context):
  name = 'Null'

  # points + home +  bar
  def draw_your_point_at(self, point, checker_count):pass
  def draw_his_point_at(self, point, checker_count):pass
  def draw_empty_point_at(self, point):pass
  def draw_your_bar(self, checker_count):pass
  def draw_his_bar(self, checker_count):pass
  def draw_center_bar(self):pass
  def draw_your_home(self, checker_count):pass
  def draw_his_home(self, checker_count):pass

  # cube holder
  def draw_your_cube(self, cube_in_logarithm):pass
  def draw_his_cube(self, cube_in_logarithm):pass
  def draw_center_cube(self, cube_in_logarithm):pass

  # field
  def draw_you_offered_double(self, cube_in_logarithm):pass
  def draw_he_offered_double(self, cube_in_logarithm):pass
  def draw_your_dice_in_field(self, dice):pass
  def draw_his_dice_in_field(self, dice):pass

  # who is on action
  def draw_you_to_play(self):pass
  def draw_him_to_play(self):pass

  def draw_frame(self):pass

context_factory.register(NullContext)

