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

  def open_image(self, fn):
    return Image.open('./bglib/image/resource/'+fn)
    
  # points + home +  bar
  def draw_your_point_at(self, point, checker_count):
    x, y = self.style().point[str(point)]
    if point  % 2:
      fn = "odd-"
    else:
      fn = "even-"
    fn += self.style().color.you + '-' + str(checker_count) + ".jpg"
    pt = self.open_image(fn)
    if point < 13:
      pt = pt.rotate(180)
    self.image.paste(pt, (x, y))
    
  def draw_his_point_at(self, point, checker_count):
    x, y = self.style().point[str(point)]
    if point % 2:
      fn = "odd-"
    else:
      fn = "even-"
    fn += self.style().color.him + '-' + str(checker_count) + ".jpg"
    pt = self.open_image(fn)
    if point < 13:
      pt = pt.rotate(180)
    self.image.paste(pt, (x, y))

  def draw_empty_point_at(self, point):
    x, y = self.style().point[str(point)]
    if point % 2:
      fn = "odd-"
    else:
      fn = "even-"
    fn += "none.jpg"
    pt = self.open_image(fn)
    if point < 13:
      pt = pt.rotate(180)
    self.image.paste(pt, (x, y))
  
  def draw_your_bar(self, checker_count):
    x, y = self.style().bar.you
    if checker_count:
      res = self.open_image("bar-"+self.style().color.you + "-%i.jpg"%(checker_count))
    else:
      res = self.open_image("bar-none.jpg")
    self.image.paste(res, (x, y))

  def draw_his_bar(self, checker_count):
    x, y = self.style().bar.him
    if checker_count:
      res = self.open_image("bar-"+self.style().color.him+"-%i.jpg"%(checker_count))
    else:
      res = self.open_image("bar-none.jpg")
    self.image.paste(res, (x, y))

  def draw_center_bar(self):
    x, y = self.style().center.null
    self.image.paste(self.open_image("center.jpg"), (x, y))

  def draw_your_home(self, checker_count):pass
  def draw_his_home(self, checker_count):pass

  # cube holder
  def draw_your_cube(self, cube_value):pass
  def draw_his_cube(self, cube_value):pass
  def draw_center_cube(self, cube_value):pass

  # field
  def draw_you_offered_double(self, cube_value):
    x, y = self.style().field.you
    self.image.paste(self.open_image("field.jpg"), (x, y))

  def draw_he_offered_double(self, cube_value):
    x, y = self.style().field.him
    self.image.paste(self.open_image("field.jpg"), (x, y))

  def draw_your_dice_in_field(self, dice):
    x, y = self.style().field.you
    self.image.paste(self.open_image("field.jpg"), (x, y))

  def draw_his_dice_in_field(self, dice):
    x, y = self.style().field.him
    self.image.paste(self.open_image("field.jpg"), (x, y))

  # who is on action
  def draw_you_to_play(self):pass
  def draw_him_to_play(self):pass
  def draw_frame(self):pass

  def result(self):
    return self.image


def parse_align(f):
  for line in f.readlines():
    x = line.split()
    if x:
      yield line.split()
    else:
      raise StopIteration



class Painter(object):
  def __init__(self, board, rpath):
    self.board = board
    self.rpath = rpath
    self.colormap = dict()
    
  def size(self, param, x, y):
    self.image = Image.new("RGB",(x, y), debug_color)
    
  def you(self, param, x, y):
    self.colormap.update({model.you:param})

  def him(self, param, x, y):
    self.colormap.update({model.him:param})

  def point(self, param, x, y):
    you, him = self.board.position
    i = int(param) - 1
    fn = self.rpath

    if i % 2:
      fn += "even-"
    else:
      fn += "odd-"

    assert(you[i] >=0 and him[i] >=0)

    if you[i]:
      fn += self.colormap[model.you] + '-' + str(you[i]) + ".jpg"
    elif him[23-i]:
      fn += self.colormap[model.him] + '-' + str(him[23-i]) + ".jpg"
    else:
      fn += "none.jpg"

    pt = Image.open(fn)
    if i < 12:
      pt = pt.rotate(180)
    self.image.paste(pt, (x, y))

  def bar(self, param, x, y):
    you, him = self.board.position
    if param == 'You':
      if you[24]:
        res = Image.open(self.rpath+"bar-"+self.colormap[model.you]+"-%i.jpg"%(you[24]))
      else:
        res = Image.open(self.rpath+"bar-none.jpg")
    elif param == 'Him':
      if him[24]:
        res = Image.open(self.rpath+"bar-"+self.colormap[model.him]+"-%i.jpg"%(him[24]))
      else:
        res = Image.open(self.rpath+"bar-none.jpg")
    else:
      raise TypeError("bad parameter for bar: %s"%param)
      
    self.image.paste(res , (x, y))

  def field(self, param, x, y):
    self.image.paste(Image.open(self.rpath+"field.jpg"), (x, y))

  def center(self, param, x, y):
    self.image.paste(Image.open(self.rpath+"center.jpg"), (x, y))


def generate(board):
  #rpath = config.active.image.resource
  rpath = './bglib/resource/'
  p = Painter(board, rpath)
  f = file(os.path.join(rpath, 'align.txt'))
  try:
    for name, param, x, y in parse_align(f):
      m = getattr(p, name)
      if m and callable(m):
        m(param, int(x), int(y))
      else:
        raise
    return p.image
  finally:
    f.close()


if __name__ == '__main__':
  board = bglib.model.board()
  style = bglib.depot.lines.CRLFProxy('./bglib/image/resource/align.txt')
  renderer = bglib.image.renderer.renderer
  context_factory = bglib.image.context.context_factory
  context = context_factory.new_context('PIL', style)
  image = renderer.render(context, board)
  image.show()
  

