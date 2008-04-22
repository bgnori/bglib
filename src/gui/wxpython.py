#!/usrbin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2006-2008 Noriyuki Hosaka nori@backgammon.gr.jp
#
import logging
import wx
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
  '''
    It does low level works.
    such as:
    - converting mouse up/down to command event.
    - drawing.
  '''
  def __init__(self, parent):
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

    self.SetBoard(bglib.model.board())

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
    assert(isinstance(region, bglib.gui.wxpython.Region))
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
    bglib.image.renderer.renderer.render(self.context, self.board)
    self.Refresh()
    self.Update()

  def SetBoard(self, board):
    self.board = board
    bglib.image.renderer.renderer.render(self.context, board)
    self.Refresh()
    self.Update()



class Board(BoardPanel):
  '''
    It does high level works.
    such as:
    - determining leagality of move.
    - emitting board change event envoked by user action.
  '''
  def __init__(self, parent):
    BoardPanel.__init__(self, parent)
    self.Bind(bglib.gui.wxpython.EVT_REGION_LEFT_DRAG, self.OnRegionLeftDrag)
    self.Bind(bglib.gui.wxpython.EVT_REGION_LEFT_CLICK, self.OnRegionLeftClick)
    self.Bind(bglib.gui.wxpython.EVT_REGION_RIGHT_CLICK, self.OnRegionRightClick)

  def OnRegionLeftDrag(self, evt):
    down = evt.GetDown()
    up = evt.GetUp()
    print 'Board::OnRegionLeftDrag:  from ', down, 'to', up

  def OnRegionLeftClick(self, evt):
    r = evt.GetRegion()
    print 'Board::OnRegionLeftClick:', r

  def OnRegionRightClick(self, evt):
    r = evt.GetRegion()
    print 'Board::OnRegionRightClick:', r

  def SetBoard(self, board):
    BoardPanel.SetBoard(self, board)

if __name__ == '__main__':
  app = wx.PySimpleApp()
  frame = wx.Frame(None)
  board = bglib.model.board()
  bglib.gui.wxpython.Board(frame)
  frame.Show()
  app.MainLoop()
