#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2006-2008 Noriyuki Hosaka nori@backgammon.gr.jp
#

import wx
import bglib.image.draw


class Draw(bglib.image.draw.Draw):
  def create_dc(self, size):
    assert self.dc is None
    wxbmp = wx.EmptyBitmap(size[0], size[1])
    dc = wx.MemoryDC()
    dc.SelectObject(wxbmp)
    self.dc = [wxbmp, dc]

  def delele_dc(self):
    del self.dc[1]
    self.dc = None

  def result_from_dc(self):
    return self.dc[0]

  def calc_font_size(self, font_name, size, text):
    fsize = size[1]
    font = self.load_font(font_name, fsize)
    w, h = font.getsize(text)
    while w >= size[0] or h >= size[1]:
      fsize = fsize - 1
      font = self.load_font(font_name, fsize)
      w, h = font.getsize(text)
    return fsize, w, h

  def calc_em(self, font_name, fsize):
    font = self.load_font(font_name, fsize)
    w, h = font.getsize('m')
    return w

  def draw_text(self, position, size, text, font_name, fill):
    ''' places text in center of rect, rect is specified by size and position.'''
    position = self.calc_mag(position)
    size = self.calc_mag(size)
    x, y = position
    fsize, w, h = self.calc_font_size(font_name, size, text)
    font = self.load_font(font_name, fsize)
    draw = self.dc[1]
    xoff = (size[0] - w)/2
    yoff = (size[1] - h)/2
    draw.text((x+xoff, y+yoff), text, font=font, fill=fill)


  def load_font(self, uri, size):
    if (uri, size)  in self.cache:
      return self.cache[(uri, size)]

    font = ImageFont.truetype(uri, size)
    self.cache.update({(uri, size): font})
    return font

  def load_image(self, uri, size, flip):
    size=self.calc_mag(size)
    if (uri, size, flip) in self.cache:
      return self.cache[(uri, size, flip)]

    if uri.endswith(".jpg"):
      bitmap_type = wx.BITMAP_TYPE_JPEG
    elif uri.endswith(".png"):
      bitmap_type = wx.BITMAP_TYPE_PNG
    else:
      #FIXME 
      assert False

    image = wx.Image(uri, bitmap_type)
    if flip:
      image = image.transpose(Image.FLIP_TOP_BOTTOM)
      image = image.Scale(size[0], size[1])
    image = image.resize(size)
    self.cache.update({(uri, size, flip): image})
    return image

  def paste_image(self, src, position, size):
    position=self.calc_mag(position)
    size=self.calc_mag(size)
    x1, y1 = position
    #x2 = x1 + size[0]
    #y2 = y1 + size[1]
    #self.dc[0].paste(src, [x1, y1, x2, y2])

    wximage =self.dc[0]
    dc = self.dc[1]
    assert isinstance(wximage, wx.Image)
    dc.DrawBitmap(wximage.ConvertToBitmap(), x1, y1)
    #FIXME size is gone!

  def draw_ellipse(self, position, size, fill=None):
    draw = self.dc[1]
    x1, y1 = position
    x2 = x1 + size[0]
    y2 = y1 + size[1]
    x1, y1 = self.calc_mag((x1, y1))
    x2, y2 = self.calc_mag((x2, y2))
    draw.ellipse([x1, y1, x2, y2], fill=fill)

  def draw_polygon(self, points, fill=None):
    points = [self.calc_mag(pt) for pt in points]
    draw = self.dc[1]
    draw.polygon(points, fill=fill)

  def draw_rect(self, position, size, fill=None):
    position=self.calc_mag(position)
    size=self.calc_mag(size)
    draw = self.dc[1]
    x2, y2 = position
    x2 += size[0]
    y2 += size[1]
    draw.rectangle([position, (x2-1, y2-1)], fill=fill)

if __name__ == '__main__':
  import bglib.model.board
  b = bglib.model.board.board()
  d = Draw("./bglib/image/resource/minimal/default.css")
  image = d.draw(b, (400, 400))
  image.show()

