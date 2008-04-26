#!/usrbin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2006-2008 Noriyuki Hosaka nori@backgammon.gr.jp
#
import logging
import wx
import wx.lib.intctrl

import bglib.encoding.gnubg
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


class BaseBoard(wx.Panel):
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
    self.Notify()

  def SetModel(self, model):
    self.model = model 
    self.Notify()
  
  def Notify(self):
    bglib.image.renderer.renderer.render(self.context, self.model)
    self.Refresh()
    self.Update()


class Board(BaseBoard):
  '''
    It does high level works.
    such as:
    - determining leagality of move.
    - emitting board change event envoked by user action.
  '''
  def __init__(self, parent, model):
    BaseBoard.__init__(self, parent, model)
    self.Bind(bglib.gui.wxpython.EVT_REGION_LEFT_DRAG, self.OnRegionLeftDrag)
    self.Bind(bglib.gui.wxpython.EVT_REGION_LEFT_CLICK, self.OnRegionLeftClick)
    self.Bind(bglib.gui.wxpython.EVT_REGION_RIGHT_CLICK, self.OnRegionRightClick)

  def OnRegionLeftDrag(self, evt):
    down = evt.GetDown()
    up = evt.GetUp()
    print 'Board::OnRegionLeftDrag:  from ', down, 'to', up
    down = bglib.model.position_pton(down.name)
    up = bglib.model.position_pton(up.name)
    mf = bglib.model.MoveFactory(self.model)
    if down > up:
      pms = mf.guess_your_multiple_partial_moves(down, up)
    elif down < up:
      pms = mf.guess_your_multiple_partial_undoes(down, up)
    else:
      assert(up == donw)

    if pms:
      for pm in pms:
        mf.append(pm)
      mv = mf.end()
      print mv
    else:
      print 'illeagal input'

  def OnRegionLeftClick(self, evt):
    region = evt.GetRegion()
    board = self.model
    mf = bglib.model.MoveFactory(self.model)

    points = ['%i'%i for i in range(1, 25)]

    print 'Board::OnRegionLeftClick:', region
    if region.name == 'your field':
      if board.is_leagal_to_double():
        print 'double!'
      else:
        print 'not allowed to double'
    elif region.name in points or region.name == 'your bar':
      print 'moving from ', region.name
      src = bglib.model.position_pton(region.name)
      print mf.guess_your_single_pm_from_source(src)
    else:
      pass

  def OnRegionRightClick(self, evt):
    region = evt.GetRegion()
    print 'Board::OnRegionRightClick:', region
    mf = bglib.model.MoveFactory(self.model)
    dest = bglib.model.position_pton(region.name)
    print mf.guess_your_making_point(dest)
      
  def SetModel(self, model):
    BaseBoard.SetModel(self, model)


class BoardEditor(wx.Panel):
  def __init__(self, parent, model):
    wx.Panel.__init__(self, parent)
    self.model = model

    label_position = wx.StaticText(self, -1, 'position id:')
    position_id = wx.TextCtrl(self, -1, 'jGfwATDg8+ABUA', 
                style=wx.TE_PROCESS_ENTER|wx.TE_NO_VSCROLL,
               )
    position_id.Bind(wx.EVT_TEXT_ENTER, self.OnChangePositionId)

    label_match = wx.StaticText(self, -1, 'match id:')
    match_id = wx.TextCtrl(self, -1, 'cIkWAAAAAAAA', 
                style=wx.TE_PROCESS_ENTER|wx.TE_NO_VSCROLL,
               )
    match_id.Bind(wx.EVT_TEXT_ENTER, self.OnChangeMatchId)

    label_length = wx.StaticText(self, -1, 'length:')
    length = wx.lib.intctrl.IntCtrl(self, -1, 0, 
                style=wx.TE_PROCESS_ENTER|wx.TE_NO_VSCROLL,
               )
    length.Bind(wx.EVT_TEXT_ENTER, self.OnChangeLength)

    label_your_score = wx.StaticText(self, -1, 'your score:')
    your_score = wx.lib.intctrl.IntCtrl(self, -1, 1,
                style=wx.TE_PROCESS_ENTER|wx.TE_NO_VSCROLL,
               )
    your_score.Bind(wx.EVT_TEXT_ENTER, self.OnChangeYourScore)

    label_his_score = wx.StaticText(self, -1, 'his score:')
    his_score = wx.lib.intctrl.IntCtrl(self, -1, 2, 
                style=wx.TE_PROCESS_ENTER|wx.TE_NO_VSCROLL,
               )
    his_score.Bind(wx.EVT_TEXT_ENTER, self.OnChangeHisScore)

    label_crawford = wx.StaticText(self, -1, 'crawford:')
    crawford = wx.CheckBox(self, -1, 'crawford')
    crawford.Bind(wx.EVT_CHECKBOX, self.OnChangeCrawford)

    space = 4
    sizer = wx.FlexGridSizer(cols=2, hgap=space, vgap=space)
    sizer.AddMany([
        label_position, position_id,
        label_match,    match_id,
        label_length,   length,
        label_his_score, his_score,
        label_your_score, your_score,
        label_crawford, crawford,
        ])
    self.SetSizer(sizer)
    self.Fit()

  def Notify(self):
    pass
    
  def OnChangePositionId(self, evt):
    print 'OnChangePositionId', evt.GetString(), evt.GetEventObject()
    p = bglib.encoding.gnubg.decode_position(evt.GetString())
    print p
    self.model.position = p

  def OnChangeMatchId(self, evt):
    print 'OnChangeMatchId', evt.GetString(), evt.GetEventObject()
    m = bglib.encoding.gnubg.decode_match(evt.GetString())

    print m.cube_in_logarithm
    print type(m.cube_in_logarithm)
    self.model.cube_value = (1 << m.cube_in_logarithm)
    self.model.cube_owner = m.cube_owner
    self.model.on_action = m.on_action
    self.model.crawford = m.crawford
    self.model.game_state = m.game_state
    self.model.on_inner_action = m.on_inner_action
    self.model.doubled = m.doubled
    self.model.resign_offer = m.resign_offer
    self.model.rolled = m.rolled
    self.model.match_length = m.match_length
    self.model.score = m.score

  def OnChangeLength(self, evt):
    print 'OnChangeLength', evt.GetString(), evt.GetEventObject()

  def OnChangeHisScore(self, evt):
    print 'OnChangeHisScore', evt.GetString(), evt.GetEventObject()

  def OnChangeYourScore(self, evt):
    print 'OnChangeYourScore', evt.GetString(), evt.GetEventObject()

  def OnChangeCrawford(self, evt):
    print 'OnChangeCrawford', evt.GetValue(), evt.GetEventObject()


if __name__ == '__main__':
  import bglib.pubsubproxy
  app = wx.PySimpleApp()
  frame = wx.Frame(None)
  model = bglib.model.board()
  proxy = bglib.pubsubproxy.Proxy(model)
  sizer = wx.BoxSizer(wx.VERTICAL)

  b = bglib.gui.wxpython.Board(frame, proxy)
  proxy.register(b.Notify)

  sizer.Add(b, proportion=1, flag=wx.SHAPED)
  be = BoardEditor(frame, proxy)
  proxy.register(be.Notify)

  sizer.Add(be, proportion=0, flag=wx.EXPAND)
  frame.SetSizer(sizer)

  frame.Fit()
  frame.Show()
  app.MainLoop()

