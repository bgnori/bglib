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

class Player(bglib.gui.viewer.Viewer):
  '''
    It does high level works.
    such as:
    - determining leagality of move.
    - emitting board change event envoked by user action.
  '''
  def __init__(self, parent, model):
    bglib.gui.viewer.Viewer.__init__(self, parent, model)
    self.mf = bglib.model.move.MoveFactory(model)
    self.Bind(bglib.gui.viewer.EVT_REGION_LEFT_DRAG, self.OnRegionLeftDrag)
    self.Bind(bglib.gui.viewer.EVT_REGION_LEFT_CLICK, self.OnRegionLeftClick)
    self.Bind(bglib.gui.viewer.EVT_REGION_RIGHT_CLICK, self.OnRegionRightClick)

  def GetValue(self):
    return self.mf.move

  def Notify(self):
    bglib.gui.viewer.Viewer.Notify(self)
    self.mf = bglib.model.move.MoveFactory(self.model)

  def MoveInputNotify(self):
    bglib.gui.viewer.Viewer.Notify(self)

  def OnRegionLeftDrag(self, evt):
    down = evt.GetDown()
    up = evt.GetUp()
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
    b= self.model
    mf = self.mf

    points = ['%i'%i for i in range(1, 25)]

    print 'Board::OnRegionLeftClick:', region
    print mf.available
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
  f.start([p])
  app.MainLoop()


