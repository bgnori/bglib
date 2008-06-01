#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2006-2008 Noriyuki Hosaka nori@backgammon.gr.jp
#
import logging
import wx
import wx.lib.intctrl

import bglib.model
import bglib.depot.dict
import bglib.depot.lines
import bglib.image.context
import bglib.image.renderer
import bglib.image.wxpython


EVT_REGION_LEFT_DRAG_TYPE = wx.NewEventType()
EVT_REGION_LEFT_DRAG = wx.PyEventBinder(EVT_REGION_LEFT_DRAG_TYPE, 1)
class LeftDrag(wx.PyCommandEvent):
  def __init__(self, id, up, down):
    wx.PyCommandEvent.__init__(self, EVT_REGION_LEFT_DRAG_TYPE, id)
    self.up = up
    self.down= down
  def GetUp(self):
    return self.up
  def GetDown(self):
    return self.down


class RegionClick(wx.PyCommandEvent):
  def __init__(self, evtType, id, region):
    wx.PyCommandEvent.__init__(self, evtType, id)
    self.region = region
  def GetRegion(self):
    return self.region


EVT_REGION_LEFT_CLICK_TYPE = wx.NewEventType()
EVT_REGION_LEFT_CLICK = wx.PyEventBinder(EVT_REGION_LEFT_CLICK_TYPE, 1)
class LeftClick(RegionClick):
  def __init__(self, id, region):
    RegionClick.__init__(self, EVT_REGION_LEFT_CLICK_TYPE, id, region)


EVT_REGION_RIGHT_CLICK_TYPE = wx.NewEventType()
EVT_REGION_RIGHT_CLICK = wx.PyEventBinder(EVT_REGION_RIGHT_CLICK_TYPE, 1)
class RightClick(RegionClick):
  def __init__(self, id, region):
    RegionClick.__init__(self, EVT_REGION_RIGHT_CLICK_TYPE, id, region)


class Viewer(wx.Panel):
  '''
    It does low level works.
    such as:
    - converting mouse up/down to command event.
    - drawing.
  '''
  def __init__(self, parent, model):
    wx.Panel.__init__(self, parent, style=wx.FULL_REPAINT_ON_RESIZE)
    self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)


    style = bglib.depot.dict.Proxy(
                                   window = self,
                                   image=bglib.depot.lines.CRLFProxy(
                                     './bglib/image/resource/align.txt'),
                                  )
    self.SetSize(style.image.size.table) # MINIMUM SIZE
    self.reset_regions()
    self.left_q = list()
    context_factory = bglib.image.context.context_factory
    self.context = context_factory.new_context('wx', style)

    self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
    self.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
    self.Bind(wx.EVT_RIGHT_DOWN, self.OnRightClick)

    self.Bind(wx.EVT_PAINT, self.OnPaint)
    self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)
    self.Bind(wx.EVT_SIZE, self.OnSize)

    self.SetModel(model)

  def reset_regions(self):
    self.regions = list()
    w, h = self.GetSize()
    self.wxbmp = wx.EmptyBitmap(w, h)

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

  def set_wxbmp(self, wximage):
    assert isinstance(wximage, wx.Image)
    dc = wx.MemoryDC()
    dc.SelectObject(self.wxbmp)
    dc.DrawBitmap(wximage.ConvertToBitmap(), 0, 0)
    #del dc

  def paste_image(self, wximage, x, y):
    dc = wx.MemoryDC()
    dc.SelectObject(self.wxbmp)
    dc.DrawBitmap(wximage.ConvertToBitmap(), x, y)
    #del dc

  def OnEraseBackground(self, evt):
    pass

  def OnPaint(self, evt):
    dc = wx.BufferedPaintDC(self)
    # debug fill
    dc.SetBackground(wx.Brush('sky blue'))
    dc.Clear()

    dc.DrawBitmap(self.wxbmp, 0, 0)
    for region in self.regions:
      region.Draw(dc)

  def OnRightClick(self, evt):
    region = self.which(evt.GetPosition())
    if region:
      new_evt = RightClick(self.GetId(), region)
      self.GetEventHandler().ProcessEvent(new_evt)

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
      new_evt = LeftClick(self.GetId(), up)
    else:
      new_evt = LeftDrag(self.GetId(), up, down)
    self.GetEventHandler().ProcessEvent(new_evt)

  def OnSize(self, evt):
    logging.debug('resized %s', str(self.GetClientSize()))
    self.Notify()

  def SetModel(self, model):
    assert isinstance(model, bglib.model.board.board)
    self.model = model 
    self.Notify()
  
  def Notify(self):
    self.reset_regions()
    bglib.image.renderer.renderer.render(self.context, self.model)
    self.Refresh()
    self.Update()


if __name__ == '__main__':
  import testframe
  app = wx.PySimpleApp()
  f = testframe.InteractiveTester(None)
  v = Viewer(f, f.get_model())
  f.start([v])
  app.MainLoop()


