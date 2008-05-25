#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2006-2008 Noriyuki Hosaka nori@backgammon.gr.jp
#
import logging
import wx
import wx.lib.intctrl

import bglib.model.move
import bglib.model.util
import bglib.gui.viewer

class PlayerStatusBar(wx.StatusBar):
  def __init__(self, player):
    wx.StatusBar.__init__(self, player.GetParent(), -1)
    self.SetFieldsCount(2)
    self.player = player

  def Update(self):
    mf = self.player.mf
    self.SetStatusText(str(mf.available), 0)
    self.SetStatusText(str(mf.move), 1)


class Player(bglib.gui.viewer.Viewer):#bglib.gui.viewer.Viewer):
  '''
    It does high level works.
    such as:
    - determining leagality of move.
    - emitting board change event envoked by user action.
  '''
  def __init__(self, parent, model):
    self._statusbar = None
    self.mf = bglib.model.move.MoveFactory(model)
    bglib.gui.viewer.Viewer.__init__(self, parent, model)
    self.Bind(bglib.gui.viewer.EVT_REGION_LEFT_DRAG, self.OnRegionLeftDrag)
    self.Bind(bglib.gui.viewer.EVT_REGION_LEFT_CLICK, self.OnRegionLeftClick)
    self.Bind(bglib.gui.viewer.EVT_REGION_RIGHT_CLICK, self.OnRegionRightClick)
    self.MoveInputNotify()

  def MakeStatusBar(self):
    statusbar = PlayerStatusBar(self)
    self._statusbar = statusbar
    return statusbar

  def GetStatusBar(self):
    return self._statusbar

  def UpdateStatusBar(self):
    statusbar = self.GetStatusBar()
    if statusbar:
      statusbar.Update()

  def GetValue(self):
    return self.mf.move

  def Notify(self):
    bglib.gui.viewer.Viewer.Notify(self)
    self.mf = bglib.model.move.MoveFactory(self.model)
    self.UpdateStatusBar()

  def MoveInputNotify(self):
    bglib.gui.viewer.Viewer.Notify(self)
    self.UpdateStatusBar()

  def OnRegionLeftDrag(self, evt):
    down = evt.GetDown()
    up = evt.GetUp()
    if down.name == 'your field':
      print 'undefined action'
      return
    if up.name == 'your field':
      if down.name == 'your home' or down.name == 'center':
        print 'double!'
        return
      else:
        print 'undefined action'
        return 

    board = self.model
    down = bglib.model.util.position_pton(down.name, board.on_action)
    up = bglib.model.util.position_pton(up.name, board.on_action)
    print 'Board::OnRegionLeftDrag:  from ', down, 'to', up
    mf = self.mf
    if down > up:
      print 'forward'
      print mf.available
      print mf.move
      mv = mf.guess_your_multiple_pms(down, up)
    elif down < up:
      print 'backward'
      mv = mf.guess_your_multiple_partial_undoes(down, up)
    else:
      assert(up == donw)

    if mv:
      mf.add(mv)
      self.MoveInputNotify()
    else:
      print 'illeagal input'

  def OnRegionLeftClick(self, evt):
    region = evt.GetRegion()
    b = self.model
    mf = self.mf

    points = ['%i'%i for i in range(1, 25)]

    if region.name == 'your field':
      if b.is_leagal_to_double():
        print 'double!'
      else:
        print 'not allowed to double'
    elif region.name in points or region.name == 'your bar':
      src = bglib.model.util.position_pton(region.name, b.on_action)
      print 'moving from %s(%i)'%(region.name, src)
      pm = mf.guess_your_single_pm_from_source(src)
      if pm:
        print pm
        mf.append(pm)
        self.MoveInputNotify()
      else:
        print 'illeagal input'
    else:
      pass

  def OnRegionRightClick(self, evt):
    region = evt.GetRegion()
    board = self.model
    print 'Board::OnRegionRightClick:', region
    mf = self.mf
    dest = bglib.model.position_pton(region.name, board.on_action)
    print mf.guess_your_making_point(dest)
      


if __name__ == '__main__':
  import testframe
  app = wx.PySimpleApp()
  f = testframe.InteractiveTester(None)
  p = Player(f, f.get_model())
  st = p.MakeStatusBar()
  f.SetStatusBar(st)
  f.start([p])
  app.MainLoop()

