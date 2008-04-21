#!/usrbin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2006-2008 Noriyuki Hosaka nori@backgammon.gr.jp
#
import logging
import time

import wx
from wx.lib.colourchooser.canvas import Canvas

import bglib.depot.dict
import bglib.image.context
import bglib.image.renderer


class Region(object):
  def __init__(self, x, y, w, h, name=None):
    if name is None:
      name = str(id(self))
    self.name = name
    self.rect = wx.Rect(x, y ,w, h)
    self.wxbmp = None

  def set_image(self, image):
    self.wxbmp = wx.BitmapFromImage(image)
    #self.wxbmp = image.ConvertToBitmap()

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
    if self.wxbmp:
      dc.DrawBitmap(self.wxbmp, self.GetX(), self.GetY())

  def __repr__(self):
    return  self.name + ' @ ' + str(self.rect)



class LeftDrag(wx.PyCommandEvent):
  def __init__(self, evtType, id):
    wx.PyCommandEvent.__init__(self, evtType, id)
    self.up = None
    self.down= None

  def GetUp(self):
    return self.up
  def SetUp(self, up):
    self.up = up
  def GetDown(self):
    return self.down
  def SetDown(self, down):
    self.down = down

class RegionClick(wx.PyCommandEvent):
  def __init__(self, evtType, id):
    wx.PyCommandEvent.__init__(self, evtType, id)
    self.region = None
  def GetRegion(self):
    return self.region
  def SetRegion(self, r):
    self.region = r

class LeftClick(RegionClick):
  pass
class RightClick(RegionClick):
  pass

EVT_REGION_LEFT_DRAG_TYPE = wx.NewEventType()
EVT_REGION_LEFT_DRAG = wx.PyEventBinder(EVT_REGION_LEFT_DRAG_TYPE, 1)

EVT_REGION_LEFT_CLICK_TYPE = wx.NewEventType()
EVT_REGION_LEFT_CLICK = wx.PyEventBinder(EVT_REGION_LEFT_CLICK_TYPE, 1)

EVT_REGION_RIGHT_CLICK_TYPE = wx.NewEventType()
EVT_REGION_RIGHT_CLICK = wx.PyEventBinder(EVT_REGION_RIGHT_CLICK_TYPE, 1)

class BoardPanel(wx.Panel):
  def __init__(self, parent, id):
    wx.Panel.__init__(self, parent, style=wx.FULL_REPAINT_ON_RESIZE)
    self.reset_regions()
    self.left_q = list()


    style = bglib.depot.dict.Proxy(
                                  window = self,
                                  image=bglib.depot.lines.CRLFProxy('./bglib/image/resource/align.txt'),
                                )
    context_factory = bglib.image.context.context_factory
    self.context = context_factory.new_context('wx', style)

    self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
    self.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
    self.Bind(wx.EVT_RIGHT_DOWN, self.OnRightClick)

    self.Bind(wx.EVT_PAINT, self.OnPaint)
    self.Bind(wx.EVT_SIZE, self.OnSize)

    self.SetBoard(bglib.model.board())

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
    # debug fill
    dc.SetBackground(wx.Brush('sky blue'))
    dc.Clear()

    for region in self.regions:
      region.Draw(dc)

  def OnRightClick(self, evt):
    region = self.which(evt.GetPosition())
    if region:
      evt = RightClick(EVT_REGION_RIGHT_CLICK_TYPE, self.GetId())
      evt.SetRegion(region)
      self.GetEventHandler().ProcessEvent(evt)

  def OnLeftDown(self, evt):
    down = self.which(evt.GetPosition())
    assert(not self.left_q)
    self.left_q.append(down)

  def OnLeftUp(self, evt):
    up = self.which(evt.GetPosition())
    if not up:
      # drag out to out of region. ignore.

      # consume down
      try:
        self.left_q.pop()
      except:
        pass
      return

    if not self.left_q:
      # ignores double click
      # double click comes with down-up-up
      return

    down = self.left_q.pop()
    if down is None:
      # drag from out of region. ignore.
      return

    if down == up:
      evt = LeftClick(EVT_REGION_LEFT_CLICK_TYPE, self.GetId())
      evt.SetRegion(up)
    else:
      evt = LeftDrag(EVT_REGION_LEFT_DRAG_TYPE, self.GetId())
      evt.SetUp(up)
      evt.SetDown(down)
    self.GetEventHandler().ProcessEvent(evt)

  def OnSize(self, evt):
    size = self.GetClientSize()
    logging.debug('resized %s', str(size))
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
    r = Region(x, y, w, h, 'your field')
    self.window.append(r)
    bglib.image.PIL.Context.draw_you_offered_double(self)

  def draw_he_offered_double(self, cube_value):
    x, y = self.apply_mag(self.style().field.him)
    w, h = self.apply_mag(self.style().size.field)
    r = Region(x, y, w, h, 'his field')
    self.window.append(r)
    bglib.image.PIL.Context.draw_he_offered_double(self)

  def draw_your_dice_in_field(self, dice):
    x, y = self.apply_mag(self.style().field.you)
    w, h = self.apply_mag(self.style().size.field)
    r = Region(x, y, w, h, 'your field')
    self.window.append(r)
    bglib.image.PIL.Context.draw_your_dice_in_field(self, dice)

  def draw_his_dice_in_field(self, dice):
    x, y = self.apply_mag(self.style().field.him)
    w, h = self.apply_mag(self.style().size.field)
    r = Region(x, y, w, h, 'his field')
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


