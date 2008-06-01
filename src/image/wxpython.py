#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2006-2008 Noriyuki Hosaka nori@backgammon.gr.jp
#
import wx

import bglib.image.PIL

class Region(object):
  def __init__(self, x, y, w, h, name=None):
    if name is None:
      name = str(id(self))
    self.name = name
    self.rect = wx.Rect(x, y ,w, h)
    self.wxbmp = wx.EmptyBitmap(w, h)
    dc = wx.MemoryDC()
    dc.SelectObject(self.wxbmp)
    self.dc = dc

  def window_to_region(self, x, y):
    return x - self.GetX(), y - self.GetY()

  def paste_image(self, wximage, x, y):
    assert isinstance(wximage, wx.Image)
    self.dc.DrawBitmap(wximage.ConvertToBitmap(), x, y)

  def __hash__(self):
    return hash(self.name)
  
  def GetX(self):
    return self.rect.GetX()

  def GetY(self):
    return self.rect.GetY()

  def Inside(self, pt):
    return self.rect.Inside(pt)

  def InsideXY(self, x, y):
    return self.rect.InsideXY(x, y)

  def Draw(self, dc):
    dc.DrawBitmap(self.wxbmp, self.GetX(), self.GetY())

  def __repr__(self):
    return  self.name + ' @ ' + str(self.rect)


class Context(bglib.image.PIL.Context):
  name = 'wx'
  def __init__(self, style):
    bglib.image.PIL.Context.__init__(self, style.image)
    self.window = style.window

  def apply_mag(self, t):
    table_size = self.style().size.table[0]
    window_size = self.window.GetSizeTuple()[0]
    return (t[0] *window_size/table_size, t[1] *window_size/table_size)

  def open_image(self, fn, size, upside_down=None):
    assert(len(size)==2)
    if upside_down is None:
      upside_down = False

    if fn.endswith(".jpg"):
      bitmap_type = wx.BITMAP_TYPE_JPEG
    else:
      bitmap_type = wx.BITMAP_TYPE_PNG

    if (fn, size, upside_down) not in self.cache:
      i = wx.Image('./bglib/image/resource/'+fn, bitmap_type)
      j = i.Scale(size[0], size[1])
      if upside_down:
        j = j.Mirror(False)
      self.cache.update({(fn, size, upside_down): j})
    else:
      j = self.cache[(fn, size, upside_down)]
    return j

  def paste_image(self, wximage, position):
    x, y = position
    r = self.window.which_by_xy(x, y)
    if r:
      x, y = r.window_to_region(x, y)
      r.paste_image(wximage, x, y)
    else:
      self.window.paste_image(wximage, x, y)

  def result(self):
    return self.window

  def draw_your_point_at(self, point, checker_count):
    x, y = self.apply_mag(self.style().point[str(point)])
    w, h = self.apply_mag(self.style().size.point)
    r = Region(x, y, w, h, str(point))
    self.window.append(r)
    bglib.image.PIL.Context.draw_your_point_at(self, point, checker_count)
  
  def draw_his_point_at(self, point, checker_count):
    x, y = self.apply_mag(self.style().point[str(point)])
    w, h = self.apply_mag(self.style().size.point)
    r = Region(x, y, w, h, str(point))
    self.window.append(r)
    bglib.image.PIL.Context.draw_his_point_at(self, point, checker_count)

  def draw_empty_point_at(self, point):
    x, y = self.apply_mag(self.style().point[str(point)])
    w, h = self.apply_mag(self.style().size.point)
    r = Region(x, y, w, h, str(point))
    self.window.append(r)
    bglib.image.PIL.Context.draw_empty_point_at(self, point)

  def draw_your_bar(self, checker_count):
    x, y = self.apply_mag(self.style().bar.you)
    w, h = self.apply_mag(self.style().size.bar)
    r = Region(x, y, w, h, 'your bar')
    self.window.append(r)
    bglib.image.PIL.Context.draw_your_bar(self, checker_count)

  def draw_his_bar(self, checker_count):
    x, y = self.apply_mag(self.style().bar.him)
    w, h = self.apply_mag(self.style().size.bar)
    r = Region(x, y, w, h, 'his bar')
    self.window.append(r)
    bglib.image.PIL.Context.draw_his_bar(self, checker_count)

  def draw_center_bar(self):
    x, y = self.apply_mag(self.style().center.null)
    w, h = self.apply_mag(self.style().size.center)
    r = Region(x, y, w, h, 'center bar')
    self.window.append(r)
    bglib.image.PIL.Context.draw_center_bar(self)

  def draw_your_home(self, checker_count):
    x, y = self.apply_mag(self.style().home.you)
    w, h = self.apply_mag(self.style().size.home)
    r = Region(x, y, w, h, str('your home'))
    self.window.append(r)
    bglib.image.PIL.Context.draw_your_home(self, checker_count)

  def draw_his_home(self, checker_count):
    x, y = self.apply_mag(self.style().home.him)
    w, h = self.apply_mag(self.style().size.home)
    r = Region(x, y, w, h, str('his home'))
    self.window.append(r)
    bglib.image.PIL.Context.draw_his_home(self, checker_count)

  def draw_cubeholder(self):
    x, y = self.apply_mag(self.style().cubeholder.null)
    w, h = self.apply_mag(self.style().size.cubeholder)
    r = Region(x, y, w, h, str('cubeholder'))
    self.window.append(r)
    bglib.image.PIL.Context.draw_cubeholder(self)

  # cube holder
  def draw_your_cube(self, cube_in_logarithm):
    bglib.image.PIL.Context.draw_your_cube(self, cube_in_logarithm)

  def draw_his_cube(self, cube_in_logarithm):
    bglib.image.PIL.Context.draw_his_cube(self, cube_in_logarithm)

  def draw_center_cube(self, cube_in_logarithm):
    bglib.image.PIL.Context.draw_center_cube(self, cube_in_logarithm)

  # field
  def draw_your_empty_field(self):
    x, y = self.apply_mag(self.style().field.you)
    w, h = self.apply_mag(self.style().size.field)
    r = Region(x, y, w, h, 'your field')
    self.window.append(r)
    bglib.image.PIL.Context.draw_your_empty_field(self)

  def draw_his_empty_field(self):
    x, y = self.apply_mag(self.style().field.him)
    w, h = self.apply_mag(self.style().size.field)
    r = Region(x, y, w, h, 'his field')
    self.window.append(r)
    bglib.image.PIL.Context.draw_his_empty_field(self)

  # who is on action
  def draw_you_to_play(self):
    bglib.image.PIL.Context.draw_you_to_play(self)

  def draw_him_to_play(self):
    bglib.image.PIL.Context.draw_him_to_play(self)

  def draw_frame(self):
    w, h  = self.apply_mag(self.style().size.table)
    self.window.set_wxbmp(wx.EmptyImage(w, h))
    bglib.image.PIL.Context.draw_frame(self)
  def draw_your_score(self, score):
    x, y = self.apply_mag(self.style().score.yours)
    w, h = self.apply_mag(self.style().size.score)
    r = Region(x, y, w, h, 'your score')
    self.window.append(r)
    bglib.image.PIL.Context.draw_your_score(self, score)

  def draw_his_score(self, score):
    x, y = self.apply_mag(self.style().score.his)
    w, h = self.apply_mag(self.style().size.score)
    r = Region(x, y, w, h, 'his score')
    self.window.append(r)
    bglib.image.PIL.Context.draw_his_score(self, score)

bglib.image.context.context_factory.register(Context)

if __name__ == '__main__':
  print 'test code is in bglib/gui/viewer,py'
