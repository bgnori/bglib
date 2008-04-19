
#!/usrbin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2006-2008 Noriyuki Hosaka nori@backgammon.gr.jp
#

import wx
from wx.lib.colourchooser.canvas import Canvas

import bglib.depot.dict
import bglib.image.context
import bglib.image.renderer


class Region(object):
  def __init__(self, x, y, w, h):
    self.rect = wx.Rect(x, y ,w, h)
    self.wxbmp = None

  def set_image(self, image):
    self.wxbmp = image.ConvertToBitmap()
  
  def GetX(self):
    return self.rect.GetX()
  def GetY(self):
    return self.rect.GetY()

  def Inside(self, pt):
    return self.rect.Inside(pt)

  def InsideXY(self, x, y):
    return self.rect.InsideXY(x, y)

  def Draw(self, dc):
    if self.wxbmp:
      dc.DrawBitmap(self.wxbmp, self.GetX(), self.GetY())

  def __repr__(self):
    return  str(self.rect)

class BoardPanel(wx.Panel):
  def __init__(self, parent, id, **kw):
    wx.Panel.__init__(self, parent, **kw)
    self.reset_regions()

    self.board = bglib.model.board()

    style = bglib.depot.dict.Proxy(
                                  window = self,
                                  image=bglib.depot.lines.CRLFProxy('./bglib/image/resource/align.txt'),
                                )
    context_factory = bglib.image.context.context_factory
    self.context = context_factory.new_context('wx', style)

    self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
    self.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
    self.Bind(wx.EVT_PAINT, self.OnPaint)
    self.Bind(wx.EVT_SIZE, self.OnSize)
    
  def reset_regions(self):
    self.regions = list()

  def which(self, pt):
    for region in self.regions:
      if region.Inside(pt):
        return region
    return None

  def which_by_xy(self, x, y):
    for region in self.regions:
      if region.InsideXY(x, y):
        return region
    return None

  def append(self, region):
    assert(isinstance(region, bglib.image.wxpython.Region))
    self.regions.append(region)

  def OnPaint(self, evt):
    dc = wx.PaintDC(self)
    for region in self.regions:
      region.Draw(dc)

  def OnLeftDown(self, evt):
    print 'OnLeftDown'
    print 'GetPosition', evt.GetPosition()
    print 'at region ; ',  self.which(evt.GetPosition())

  def OnLeftUp(self, evt):
    print 'OnLeftUp'
    print 'GetPosition', evt.GetPosition()
    print 'at region ; ',  self.which(evt.GetPosition())

  def OnSize(self, evt):
    size = self.GetClientSize()
    print 'resized ', size
    self.reset_regions()
    bglib.image.renderer.renderer.render(self.context, self.board)
    self.Refresh()

  def SetBoard(self, board):
    self.board = board
    bglib.image.renderer.renderer.render(self.context, board)
    self.Refresh()


class Context(bglib.image.PIL.Context):
  name = 'wx'
  def __init__(self, style):
    bglib.image.PIL.Context.__init__(self, style.image)
    
    ix = style.image.size.board[0]
    self.window = style.window
    self.fn = None

  def apply_mag(self, t):
    ix = self.style().size.board[0]
    sx = self.window.GetSizeTuple()[0]
    return (
            t[0] *sx/ix,
            t[1] *sx/ix
            )

  def open_image(self, fn, size, upside_down=None):
    assert(len(size)==2)
    if upside_down is None:
      upside_down = False

    if (fn, size, upside_down) not in self.cache:
      i = wx.Image('./bglib/image/resource/'+fn, wx.BITMAP_TYPE_JPEG)
      j = i.Scale(size[0], size[1])
      if upside_down:
        j = j.Mirror(False)
      self.cache.update({(fn, size, upside_down): j})
    else:
      j = self.cache[(fn, size, upside_down)]
    return j

  def paste_image(self, image, position):
    x, y = position
    r = self.window.which_by_xy(x, y)
    if r:
      r.set_image(image)

  def result(self):
    return self.window

  def draw_your_point_at(self, point, checker_count):
    x, y = self.apply_mag(self.style().point[str(point)])
    w, h = self.apply_mag(self.style().size.point)
    r = Region(x, y, w, h)
    self.window.append(r)
    bglib.image.PIL.Context.draw_your_point_at(self, point, checker_count)
  
  def draw_his_point_at(self, point, checker_count):
    x, y = self.apply_mag(self.style().point[str(point)])
    w, h = self.apply_mag(self.style().size.point)
    r = Region(x, y, w, h)
    self.window.append(r)
    bglib.image.PIL.Context.draw_his_point_at(self, point, checker_count)

  def draw_empty_point_at(self, point):
    x, y = self.apply_mag(self.style().point[str(point)])
    w, h = self.apply_mag(self.style().size.point)
    r = Region(x, y, w, h)
    self.window.append(r)
    bglib.image.PIL.Context.draw_empty_point_at(self, point)

  def draw_your_bar(self, checker_count):
    x, y = self.apply_mag(self.style().bar.you)
    w, h = self.apply_mag(self.style().size.bar)
    r = Region(x, y, w, h)
    self.window.append(r)
    bglib.image.PIL.Context.draw_your_bar(self, checker_count)

  def draw_his_bar(self, checker_count):
    x, y = self.apply_mag(self.style().bar.him)
    w, h = self.apply_mag(self.style().size.bar)
    r = Region(x, y, w, h)
    self.window.append(r)
    bglib.image.PIL.Context.draw_his_bar(self, checker_count)

  def draw_center_bar(self):
    x, y = self.apply_mag(self.style().center.null)
    w, h = self.apply_mag(self.style().size.center)
    r = Region(x, y, w, h)
    self.window.append(r)
    bglib.image.PIL.Context.draw_center_bar(self)

  def draw_your_home(self, checker_count):pass
  def draw_his_home(self, checker_count):pass

  # cube holder
  def draw_your_cube(self, cube_value):pass
  def draw_his_cube(self, cube_value):pass
  def draw_center_cube(self, cube_value):pass

  # field
  def draw_you_offered_double(self, cube_value):
    x, y = self.apply_mag(self.style().field.you)
    w, h = self.apply_mag(self.style().size.field)
    r = Region(x, y, w, h)
    self.window.append(r)
    bglib.image.PIL.Context.draw_you_offered_double(self)

  def draw_he_offered_double(self, cube_value):
    x, y = self.apply_mag(self.style().field.him)
    w, h = self.apply_mag(self.style().size.field)
    r = Region(x, y, w, h)
    self.window.append(r)
    bglib.image.PIL.Context.draw_he_offered_double(self)

  def draw_your_dice_in_field(self, dice):
    x, y = self.apply_mag(self.style().field.you)
    w, h = self.apply_mag(self.style().size.field)
    r = Region(x, y, w, h)
    self.window.append(r)
    bglib.image.PIL.Context.draw_your_dice_in_field(self, dice)

  def draw_his_dice_in_field(self, dice):
    x, y = self.apply_mag(self.style().field.him)
    w, h = self.apply_mag(self.style().size.field)
    r = Region(x, y, w, h)
    self.window.append(r)
    bglib.image.PIL.Context.draw_his_dice_in_field(self, dice)

  # who is on action
  def draw_you_to_play(self):pass
  def draw_him_to_play(self):pass

  def draw_frame(self):pass

if __name__ == '__main__':
  app = wx.PySimpleApp()

  frame = wx.Frame(None)

  board = bglib.model.board()
  import bglib.depot.dict
  BoardPanel(frame, -1)
  frame.Show()
  app.MainLoop()


