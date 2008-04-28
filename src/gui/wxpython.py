#!/usrbin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2006-2008 Noriyuki Hosaka nori@backgammon.gr.jp
#
import logging
import wx
import wx.lib.intctrl

import bglib.model
import bglib.encoding.gnubg
import bglib.depot.dict
import bglib.depot.lines
import bglib.image.context
import bglib.image.renderer
import bglib.image.wxpython


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

    self.reset_regions()
    self.left_q = list()

    style = bglib.depot.dict.Proxy(
                                  window = self,
                                  image=bglib.depot.lines.CRLFProxy('./bglib/image/resource/align.txt'),
                                )
    self.SetSize(style.image.size.board) # MINIMUM SIZE
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
    self.bgimage = None

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

  def set_bgimage(self, image):
    self.bgimage = image

  def paste_image(self, image, x, y):
    self.bgimage.Paste(image, x, y)

  def OnEraseBackground(self, evt):
    pass

  def OnPaint(self, evt):
    dc = wx.PaintDC(self)
    # debug fill
    dc.SetBackground(wx.Brush('sky blue'))
    dc.Clear()

    bgbmp = wx.BitmapFromImage(self.bgimage)
    dc.DrawBitmap(bgbmp, 0, 0)
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
    logging.debug('resized %s', str(self.GetClientSize()))
    self.reset_regions()
    self.Notify()

  def SetModel(self, model):
    self.model = model 
    self.Notify()
  
  def Notify(self):
    bglib.image.renderer.renderer.render(self.context, self.model)
    self.Refresh()
    self.Update()


if __name__ == '__main__':
  import bglib.pubsubproxy
  app = wx.PySimpleApp()
  frame = wx.Frame(None)
  model = bglib.model.board()
  proxy = bglib.pubsubproxy.Proxy(model)
  sizer = wx.BoxSizer(wx.VERTICAL)

  #b = bglib.gui.wxpython.Viewer(frame, proxy)
  b = Viewer(frame, proxy)
  proxy.register(b.Notify)
  sizer.Add(b, proportion=1, flag=wx.SHAPED)
  
  frame.SetSizer(sizer)

  frame.Fit()
  frame.Show()
  app.MainLoop()

