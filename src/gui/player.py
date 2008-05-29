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


EVT_ROLL_REQUESTED_TYPE = wx.NewEventType()
EVT_ROLL_REQUESTED = wx.PyEventBinder(EVT_ROLL_REQUESTED_TYPE, 1)
class RollRequest(wx.PyCommandEvent):
  def __init__(self, id):
    wx.PyCommandEvent.__init__(self, EVT_ROLL_REQUESTED_TYPE, id)

EVT_DOUBLE_REQUESTED_TYPE = wx.NewEventType()
EVT_DOUBLE_REQUESTED = wx.PyEventBinder(EVT_DOUBLE_REQUESTED_TYPE, 1)
class DoubleRequest(wx.PyCommandEvent):
  def __init__(self, id):
    wx.PyCommandEvent.__init__(self, EVT_DOUBLE_REQUESTED_TYPE, id)

EVT_CUBE_TAKE_TYPE = wx.NewEventType()
EVT_CUBE_TAKE = wx.PyEventBinder(EVT_CUBE_TAKE_TYPE, 1)
class CubeTake(wx.PyCommandEvent):
  def __init__(self, id):
    wx.PyCommandEvent.__init__(self, EVT_CUBE_TAKE_TYPE, id)

EVT_CUBE_PASS_TYPE = wx.NewEventType()
EVT_CUBE_PASS = wx.PyEventBinder(EVT_CUBE_PASS_TYPE, 1)
class CubePass(wx.PyCommandEvent):
  def __init__(self, id):
    wx.PyCommandEvent.__init__(self, EVT_CUBE_PASS_TYPE, id)

EVT_MOVE_DONE_TYPE = wx.NewEventType()
EVT_MOVE_DONE = wx.PyEventBinder(EVT_MOVE_DONE_TYPE, 1)
class MoveDone(wx.PyCommandEvent):
  def __init__(self, id, move):
    wx.PyCommandEvent.__init__(self, EVT_MOVE_DONE_TYPE, id)
    self.move = bglib.model.move.Move(src=move)

  def GetMove(self):
    return self.move

class PlayerStatusBar(wx.StatusBar):
  def __init__(self, player):
    wx.StatusBar.__init__(self, player.GetParent(), -1)
    self.SetFieldsCount(3)
    self.player = player

  def Update(self):
    mf = self.player.mf
    self.SetStatusText(str(mf.available), 0)
    self.SetStatusText('Moved: ' +str(mf.move), 1)
    self.SetStatusText(str(self.player.message), 2)


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
    self.message = ''
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

  def SetModel(self, model):
    bglib.gui.viewer.Viewer.SetModel(self, model)
    self.mf = bglib.model.move.MoveFactory(model)
    self.UpdateStatusBar()

  def MoveInputNotify(self):
    bglib.gui.viewer.Viewer.Notify(self)
    self.UpdateStatusBar()

  def OnRegionLeftDrag(self, evt):
    down = evt.GetDown()
    up = evt.GetUp()
    board = self.model
    mf = self.mf
    #print 'Board::OnRegionLeftDrag:  from ', down, 'to', up

    if down.name == 'your field':
      if up.name == 'your home':
        if board.on_action == bglib.model.constants.you:
          if mf.is_leagal_to_pickup_dice():
            evt = MoveDone(self.GetId(), mf.move)
            self.GetEventHandler().ProcessEvent(evt)
            return 
          else:
            self.message = 'Need to move more'
            self.UpdateStatusBar()
            return 
        elif board.on_inner_action == bglib.model.constants.you and board.doubled:
          evt = CubeTake(self.GetId())
          self.GetEventHandler().ProcessEvent(evt)
          return
        else:
          print 'undefined action'
      elif up.name == 'cubeholder':
        evt = CubePass(self.GetId())
        self.GetEventHandler().ProcessEvent(evt)
        return
      else:
        print 'undefined action'
        return

    if up.name == 'your field':
      if down.name == 'your home' or down.name == 'cubeholder':
        if board.is_leagal_to_double():
          evt = DoubleRequest(self.GetId())
          self.GetEventHandler().ProcessEvent(evt)
          return 
        else:
          self.message = 'Need to move more'
          self.UpdateStatusBar()
          return 
      else:
        print 'undefined action'
        return 

    down = bglib.model.util.position_pton(down.name, board.on_action)
    up = bglib.model.util.position_pton(up.name, board.on_action)

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
      if b.on_action != bglib.model.constants.you:
        self.message = 'not your turn'
        self.UpdateStatusBar()
      elif b.is_leagal_to_roll():
        if b.is_leagal_to_double():
          evt = DoubleRequest(self.GetId())
          self.GetEventHandler().ProcessEvent(evt)
          return
        else:
          evt = RollRequest(self.GetId())
          self.GetEventHandler().ProcessEvent(evt)
          return
      elif mf.is_leagal_to_pickup_dice():
        evt = RollRequest(self.GetId())
        self.GetEventHandler().ProcessEvent(evt)
        return
      else:
        self.message = 'move your checker'
        self.UpdateStatusBar()
        return

    elif region.name in points or region.name == 'your bar':
      src = bglib.model.util.position_pton(region.name, b.on_action)
      print 'moving from %s(%i)'%(region.name, src)
      pm = mf.guess_your_single_pm_from_source(src)
      if pm:
        mf.append(pm)
        self.MoveInputNotify()
      else:
        self.message = 'illeagal move'
        self.UpdateStatusBar()
    else:
      print region.name

  def OnRegionRightClick(self, evt):
    region = evt.GetRegion()
    board = self.model
    print 'Board::OnRegionRightClick:', region
    mf = self.mf

    if region == 'your field':
      evt = CubePass(self.GetId())
      self.GetEventHandler().ProcessEvent(evt)
      return

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

