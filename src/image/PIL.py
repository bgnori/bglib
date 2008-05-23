#!/usr/bin/env python
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
    x, y = style.size.table
    self.image = Image.new("RGB", (x, y), debug_color)
    self.cache = dict()

    self.mag_numer  = 1
    self.mag_denom  = 1

  def apply_mag(self, t):
    return (
            t[0] *self.mag_numer/ self.mag_denom,
            t[1] *self.mag_numer/ self.mag_denom
            )

  def open_image(self, fn, size, upside_down=None):
    assert(len(size)==2)
    if upside_down is None:
      upside_down = False

    if (fn, size, upside_down) not in self.cache:
      i = Image.open('./bglib/image/resource/'+fn)
      j = i.resize(size, resample=1)
      if upside_down:
        j = j.rotate(180)
      self.cache.update({(fn, size, upside_down): j})
    else:
      j = self.cache[(fn, size, upside_down)]
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

    pt = self.open_image(fn, size, point > 12)

    x, y = self.apply_mag(self.style().point[str(point)])
    self.paste_image(pt, (x, y))
    
  def draw_his_point_at(self, point, checker_count):
    if point % 2:
      fn = "odd-"
    else:
      fn = "even-"
    fn += self.style().color.him + '-' + str(checker_count) + ".jpg"

    size = self.apply_mag(self.style().size.point)
    pt = self.open_image(fn, size, point > 12)

    x, y = self.apply_mag(self.style().point[str(point)])
    self.paste_image(pt, (x, y))

  def draw_empty_point_at(self, point):
    if point % 2:
      fn = "odd-"
    else:
      fn = "even-"
    fn += "none.jpg"

    size = self.apply_mag(self.style().size.point)
    pt = self.open_image(fn, size, point > 12)

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
  def draw_your_cube(self, cube_in_logarithm):
    if cube_in_logarithm > 0:
      size = self.apply_mag(self.style().size.cube)
      image = self.open_image("cube_"+str(cube_in_logarithm)+".jpg",
                              size
                             )
      x, y = self.apply_mag(self.style().cube.yours)
      self.paste_image(image, (x, y))

  def draw_his_cube(self, cube_in_logarithm):
    if cube_in_logarithm > 0:
      size = self.apply_mag(self.style().size.cube)
      image = self.open_image("cube_"+str(cube_in_logarithm)+".jpg",
                              size
                             )
      x, y = self.apply_mag(self.style().cube.his)
      self.paste_image(image, (x, y))

  def draw_center_cube(self, cube_in_logarithm):
    if cube_in_logarithm == 0:
      size = self.apply_mag(self.style().size.cube)
      image = self.open_image("cube_0.jpg",
                            size
                           )
      x, y = self.apply_mag(self.style().cube.center)
      self.paste_image(image, (x, y))

  # field
  def draw_you_offered_double(self, cube_in_logarithm):
    size = self.apply_mag(self.style().size.field)
    image = self.open_image("field.jpg",
                            size
                            )
    x, y = self.apply_mag(self.style().field.you)
    self.paste_image(image, (x, y))

    if cube_in_logarithm > 0:
      size = self.apply_mag(self.style().size.cube)
      image = self.open_image("cube_"+str(cube_in_logarithm)+".jpg",
                              size
                              )
      x, y = self.apply_mag(self.style().cube.you)
      self.paste_image(image, (x, y))

  def draw_he_offered_double(self, cube_in_logarithm):
    size = self.apply_mag(self.style().size.field)
    image = self.open_image("field.jpg",
                            size
                            )
    x, y = self.apply_mag(self.style().field.him)
    self.paste_image(image, (x, y))

    if cube_in_logarithm > 0:
      size = self.apply_mag(self.style().size.cube)
      image = self.open_image("cube_"+str(cube_in_logarithm)+".jpg",
                              size
                              )
      x, y = self.apply_mag(self.style().cube.him)
      self.paste_image(image, (x, y))

  def draw_your_dice_in_field(self, dice):
    size = self.apply_mag(self.style().size.field)
    image = self.open_image("field.jpg",
                            size
                            )
    x, y = self.apply_mag(self.style().field.you)
    self.paste_image(image, (x, y))

    if dice[0]:
      size = self.apply_mag(self.style().size.dice)
      image = self.open_image('die_' + str(dice[0]) + '.jpg',
                              size
                              )
      x, y = self.apply_mag(self.style().die_a.you)
      self.paste_image(image, (x, y))

    if dice[1]:
      size = self.apply_mag(self.style().size.dice)
      image = self.open_image('die_' + str(dice[1]) + '.jpg',
                              size
                              )
      x, y = self.apply_mag(self.style().die_b.you)
      self.paste_image(image, (x, y))

  def draw_his_dice_in_field(self, dice):
    size = self.apply_mag(self.style().size.field)
    image = self.open_image("field.jpg",
                            size
                            )
    x, y = self.apply_mag(self.style().field.him)
    self.paste_image(image, (x, y))

    if dice[0]:
      size = self.apply_mag(self.style().size.dice)
      image = self.open_image('die_' + str(dice[0]) + '.jpg',
                              size
                              )
      x, y = self.apply_mag(self.style().die_a.him)
      self.paste_image(image, (x, y))

    if dice[1]:
      size = self.apply_mag(self.style().size.dice)
      image = self.open_image('die_' + str(dice[1]) + '.jpg',
                              size
                              )
      x, y = self.apply_mag(self.style().die_b.him)
      self.paste_image(image, (x, y))

  # who is on action
  def draw_you_to_play(self):
    size = self.apply_mag(self.style().size.action)
    image = self.open_image("action_white.jpg",
                            size
                            )
    x, y = self.apply_mag(self.style().action.you)
    self.paste_image(image, (x, y))

  def draw_him_to_play(self):
    size = self.apply_mag(self.style().size.action)
    image = self.open_image("action_green.jpg",
                            size
                            )
    x, y = self.apply_mag(self.style().action.him)
    self.paste_image(image, (x, y))

  def draw_frame(self):
    size = self.apply_mag(self.style().size.edge)
    image = self.open_image("empty-edge.jpg",
                            size
                            )
    x, y = self.apply_mag(self.style().edge.null)
    self.paste_image(image, (x, y))

    size = self.apply_mag(self.style().size.home)
    image = self.open_image("empty-home.jpg",
                            size
                            )
    x, y = self.apply_mag(self.style().home.null)
    self.paste_image(image, (x, y))

    size = self.apply_mag(self.style().size.frame)
    image = self.open_image("frame.jpg",
                            size
                            )
    x, y = self.apply_mag(self.style().frame.top)
    self.paste_image(image, (x, y))
    x, y = self.apply_mag(self.style().frame.bottom)
    self.paste_image(image, (x, y))

  def draw_your_score(self, score):
    size = self.apply_mag(self.style().size.score)
    image = self.open_image("score_" + str(score)  + ".jpg",
                            size
                            )
    x, y = self.apply_mag(self.style().score.yours)
    self.paste_image(image, (x, y))

  def draw_his_score(self, score):
    size = self.apply_mag(self.style().size.score)
    image = self.open_image("score_" + str(score)  + ".jpg",
                            size
                            )
    x, y = self.apply_mag(self.style().score.his)
    self.paste_image(image, (x, y))

  def draw_match_length(self, length):
    size = self.apply_mag(self.style().size.matchlength)
    image = self.open_image("score_" + str(length)  + ".jpg",
                            size
                            )
    x, y = self.apply_mag(self.style().matchlength.null)
    self.paste_image(image, (x, y))

  def draw_crawford_flag(self, flag):
    size = self.apply_mag(self.style().size.matchcrawford)
    if flag:
      image = self.open_image("crawford.jpg", size)
    else:
      image = self.open_image("non-crawford.jpg", size)

    x, y = self.apply_mag(self.style().matchcrawford.null)
    self.paste_image(image, (x, y))

  def result(self):
    return self.image

bglib.image.context.context_factory.register(Context)


if __name__ == '__main__':
  import bglib.model.board
  board = bglib.model.board.board()
  style = bglib.depot.lines.CRLFProxy('./bglib/image/resource/align.txt')
  renderer = bglib.image.renderer.renderer
  context_factory = bglib.image.context.context_factory
  context = context_factory.new_context('PIL', style)
  image = renderer.render(context, board)
  image.show()
  

