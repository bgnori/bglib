#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2006-2008 Noriyuki Hosaka nori@backgammon.gr.jp
#
import Image
import ImageDraw
import ImageFont

import bglib.image.draw


class Draw(bglib.image.draw.Draw):
  def create_dc(self, size):
    assert self.dc is None
    img = Image.new('RGBA', size)
    assert img
    draw = ImageDraw.Draw(img)
    assert draw
    self.dc = [img, draw]

  def delele_dc(self):
    assert self.dc
    self.dc = None

  def result_from_dc(self):
    assert self.dc
    return self.dc[0]

  def calc_font_size(self, font_name, size, text):
    fsize = size[1]
    font = self.load_font(font_name, fsize)
    w, h = font.getsize(text)
    while w >= size[0] or h >= size[1]:
      fsize = fsize - 1
      if fsize < 8: # FIXME
        return None, w, h
      font = self.load_font(font_name, fsize)
      w, h = font.getsize(text)
    return fsize, w, h

  def calc_em(self, font_name, fsize):
    font = self.load_font(font_name, fsize)
    w, h = font.getsize('m')
    return w

  def draw_text(self, position, size, text, font_name, fill):
    ''' places text in center of rect, rect is specified by size and position.'''
    x, y = position
    fsize, w, h = self.calc_font_size(font_name, size, text)
    if fsize is None: #FIXME
      return
    font = self.load_font(font_name, fsize)
    draw = self.dc[1]
    xoff = (size[0] - w)/2
    yoff = (size[1] - h)/2
    draw.text((x+xoff, y+yoff), text, font=font, fill=fill)

  def load_font(self, uri, size):
    if (uri, size)  in self.cache:
      return self.cache[(uri, size)]
    assert uri
    font = ImageFont.truetype(uri, size)
    self.cache.update({(uri, size): font})
    return font

  def load_image(self, uri, size, flip):
    size = tuple(size)
    if (uri, size, flip) in self.cache:
      return self.cache[(uri, size, flip)]
    image = Image.open(uri)
    if flip:
      image = image.transpose(Image.FLIP_TOP_BOTTOM)
    image = image.resize(size)
    self.cache.update({(uri, size, flip): image})
    return image

  def paste_image(self, to_paste, position, size):
    assert self.dc
    assert to_paste.size[0] == size[0]
    assert to_paste.size[1] == size[1]
    x1, y1 = position
    x2 = x1 + size[0]
    y2 = y1 + size[1]
    self.dc[0].paste(to_paste, (x1, y1, x2, y2))

  def draw_ellipse(self, position, size, fill=None):
    assert self.dc
    draw = self.dc[1]
    x1, y1 = position
    x2 = x1 + size[0]
    y2 = y1 + size[1]
    draw.ellipse([x1, y1, x2, y2], fill=fill)

  def draw_polygon(self, points, fill=None):
    assert self.dc
    draw = self.dc[1]
    draw.polygon(points, fill=fill)

  def draw_rect(self, position, size, fill=None):
    assert self.dc is not None
    draw = self.dc[1]
    x2, y2 = position
    x2 += size[0]
    y2 += size[1]
    draw.rectangle([position, (x2-1, y2-1)], fill=fill)

if __name__ == '__main__':
  import bglib.model.board
  from bglib.image.css import load
  b = bglib.model.board.board()
  d = Draw(load("./bglib/image/resource/safari/default.css"))
  image = d.draw(b, (400, 400))
  image.show()

