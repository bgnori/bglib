#!/usrbin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2006-2008 Noriyuki Hosaka nori@backgammon.gr.jp
#
import os.path
import csv

import Image
import ImageDraw

import bglib.image.context
import bglib.image.renderer
import bglib.depot.lines

debug_color = 'blue'

class Context(bglib.image.context.Context):
  name = 'PIL'
  def __init__(self, style):
    bglib.image.context.Context.__init__(self, style)
    x, y = style.size.board
    self.image = Image.new("RGB", (x, y), debug_color)
    self.cache = dict()

  def open_image(self, fn, size):
    assert(len(size)==2)
    if (fn, size) not in self.cache:
      i = Image.open('./bglib/image/resource/'+fn)
      j = i.resize(size, resample=1)
      self.cache.update({(fn, size): j})
    else:
      j = self.cache[(fn, size)]
    return j
    
  # points + home +  bar
  def draw_your_point_at(self, point, checker_count):
    x, y = self.style().point[str(point)]
    if point  % 2:
      fn = "odd-"
    else:
      fn = "even-"
    fn += self.style().color.you + '-' + str(checker_count) + ".jpg"
    pt = self.open_image(fn, self.style().size.point)
    if point > 12:
      pt = pt.rotate(180)
    self.image.paste(pt, (x, y))
    
  def draw_his_point_at(self, point, checker_count):
    x, y = self.style().point[str(point)]
    if point % 2:
      fn = "odd-"
    else:
      fn = "even-"
    fn += self.style().color.him + '-' + str(checker_count) + ".jpg"
    pt = self.open_image(fn, self.style().size.point)
    if point > 12:
      pt = pt.rotate(180)
    self.image.paste(pt, (x, y))

  def draw_empty_point_at(self, point):
    x, y = self.style().point[str(point)]
    if point % 2:
      fn = "odd-"
    else:
      fn = "even-"
    fn += "none.jpg"
    pt = self.open_image(fn, self.style().size.point)
    if point > 12:
      pt = pt.rotate(180)
    self.image.paste(pt, (x, y))
  
  def draw_your_bar(self, checker_count):
    x, y = self.style().bar.you
    if checker_count:
      res = self.open_image("bar-"+self.style().color.you + "-%i.jpg"%(checker_count),
                            self.style().size.bar)
    else:
      res = self.open_image("bar-none.jpg",
                            self.style().size.bar
                            )
    self.image.paste(res, (x, y))

  def draw_his_bar(self, checker_count):
    x, y = self.style().bar.him
    if checker_count:
      res = self.open_image("bar-"+self.style().color.him+"-%i.jpg"%(checker_count),
                            self.style().size.bar
                            )
    else:
      res = self.open_image("bar-none.jpg",
                            self.style().size.bar
                            )
    self.image.paste(res, (x, y))

  def draw_center_bar(self):
    x, y = self.style().center.null
    image = self.open_image("center.jpg",
                            self.style().size.bar
                           )
    self.image.paste(image, (x, y))

  def draw_your_home(self, checker_count):pass
  def draw_his_home(self, checker_count):pass

  # cube holder
  def draw_your_cube(self, cube_value):pass
  def draw_his_cube(self, cube_value):pass
  def draw_center_cube(self, cube_value):pass

  # field
  def draw_you_offered_double(self, cube_value):
    x, y = self.style().field.you
    image = self.open_image("field.jpg",
                            self.style().size.field
                            )
    self.image.paste(image, (x, y))

  def draw_he_offered_double(self, cube_value):
    x, y = self.style().field.him
    image = self.open_image("field.jpg",
                            self.style().size.field
                            )
    self.image.paste(image, (x, y))

  def draw_your_dice_in_field(self, dice):
    x, y = self.style().field.you
    image = self.open_image("field.jpg",
                            self.style().size.field
                            )
    self.image.paste(image, (x, y))

  def draw_his_dice_in_field(self, dice):
    x, y = self.style().field.him
    image = self.open_image("field.jpg",
                            self.style().size.field
                            )
    self.image.paste(image, (x, y))

  # who is on action
  def draw_you_to_play(self):pass
  def draw_him_to_play(self):pass
  def draw_frame(self):pass

  def result(self):
    return self.image


if __name__ == '__main__':
  board = bglib.model.board()
  style = bglib.depot.lines.CRLFProxy('./bglib/image/resource/align.txt')
  renderer = bglib.image.renderer.renderer
  context_factory = bglib.image.context.context_factory
  context = context_factory.new_context('PIL', style)
  image = renderer.render(context, board)
  image.show()
  

