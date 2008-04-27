#!/usrbin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2006-2008 Noriyuki Hosaka nori@backgammon.gr.jp
#
import logging
import wx
import wx.lib.intctrl

import bglib.gui.wxpython

class Player(bglib.gui.wxpython.Viewer):
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
    View.SetModel(self, model)




if __name__ == '__main__':
  import bglib.pubsubproxy
  app = wx.PySimpleApp()
  frame = wx.Frame(None)
  model = bglib.model.board()
  proxy = bglib.pubsubproxy.Proxy(model)
  sizer = wx.BoxSizer(wx.VERTICAL)

  b = bglib.gui.wxpython.Viewer(frame, proxy)
  proxy.register(b.Notify)
  sizer.Add(b, proportion=1, flag=wx.SHAPED)
  
  frame.SetSizer(sizer)

  frame.Fit()
  frame.Show()
  app.MainLoop()


