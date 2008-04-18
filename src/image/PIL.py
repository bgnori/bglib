#!/usrbin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2006-2008 Noriyuki Hosaka nori@backgammon.gr.jp
#
import os.path

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

    self.mag_numer  = 1
    self.mag_denom  = 1

  def apply_mag(self, t):
    return (
            t[0] *self.mag_numer/ self.mag_denom,
            t[1] *self.mag_numer/ self.mag_denom
            )

  def open_image(self, fn, size):
    assert(len(size)==2)
    if (fn, size) not in self.cache:
      i = Image.open('./bglib/image/resource/'+fn)
      j = i.resize(size, resample=1)
      self.cache.update({(fn, size): j})
    else:
      j = self.cache[(fn, size)]
    return j

  def paste_image(self, image, position):
    self.image.paste(image, position)

    
  # points + home +  bar
  def draw_your_point_at(self, point, checker_count):
    if point  % 2:
      fn = "odd-"
    else:
      fn = "even-"
    fn += self.style().color.you + '-' + str(checker_count) + ".jpg"
    size = self.apply_mag(self.style().size.point)

    pt = self.open_image(fn, size)
    if point > 12:
      pt = pt.rotate(180)

    x, y = self.apply_mag(self.style().point[str(point)])
    self.paste_image(pt, (x, y))
    
  def draw_his_point_at(self, point, checker_count):
    if point % 2:
      fn = "odd-"
    else:
      fn = "even-"
    fn += self.style().color.him + '-' + str(checker_count) + ".jpg"

    size = self.apply_mag(self.style().size.point)
    pt = self.open_image(fn, size)
    if point > 12:
      pt = pt.rotate(180)

    x, y = self.apply_mag(self.style().point[str(point)])
    self.paste_image(pt, (x, y))

  def draw_empty_point_at(self, point):
    if point % 2:
      fn = "odd-"
    else:
      fn = "even-"
    fn += "none.jpg"

    size = self.apply_mag(self.style().size.point)
    pt = self.open_image(fn, size)
    if point > 12:
      pt = pt.rotate(180)

    x, y = self.apply_mag(self.style().point[str(point)])
    self.paste_image(pt, (x, y))
  
  def draw_your_bar(self, checker_count):
    size = self.apply_mag(self.style().size.bar)
    if checker_count:
      res = self.open_image("bar-"+self.style().color.you + "-%i.jpg"%(checker_count),
                            size)
    else:
      res = self.open_image("bar-none.jpg",
                            size
                            )
    x, y = self.apply_mag(self.style().bar.you)
    self.paste_image(res, (x, y))

  def draw_his_bar(self, checker_count):
    size = self.apply_mag(self.style().size.bar)
    if checker_count:
      res = self.open_image("bar-"+self.style().color.him+"-%i.jpg"%(checker_count),
                            size
                            )
    else:
      res = self.open_image("bar-none.jpg",
                            size
                           )
    x, y = self.apply_mag(self.style().bar.him)
    self.paste_image(res, (x, y))

  def draw_center_bar(self):
    size = self.apply_mag(self.style().size.center)
    image = self.open_image("center.jpg",
                            size
                           )
    x, y = self.apply_mag(self.style().center.null)
    self.paste_image(image, (x, y))

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
    self.paste_image(image, (x, y))

  def draw_he_offered_double(self, cube_value):
    x, y = self.style().field.him
    image = self.open_image("field.jpg",
                            self.style().size.field
                            )
    self.paste_image(image, (x, y))

  def draw_your_dice_in_field(self, dice):
    x, y = self.style().field.you
    image = self.open_image("field.jpg",
                            self.style().size.field
                            )
    self.paste_image(image, (x, y))

  def draw_his_dice_in_field(self, dice):
    x, y = self.style().field.him
    image = self.open_image("field.jpg",
                            self.style().size.field
                            )
    self.paste_image(image, (x, y))

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
  

