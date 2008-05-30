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

def acitons_whose(board):
  if board.on_action==bglib.model.constants.you:
    if board.on_inner_action == bglib.model.constants.you:
      return 'your ', 'his '
    elif board.on_inner_action == bglib.model.constants.him:
      return 'his ', 'your '
    else:
      assert False
  elif board.on_action==bglib.model.constants.him:
    if board.on_inner_action == bglib.model.constants.you:
      return 'your ', 'his '
    elif board.on_inner_action == bglib.model.constants.him:
      return 'his ', 'your '
    else:
      assert False
  else:
    return 'xxxx ', 'yyyy '

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

EVT_RESIGN_REQUESTED_TYPE = wx.NewEventType()
EVT_RESIGN_REQUESTED = wx.PyEventBinder(EVT_RESIGN_REQUESTED_TYPE, 1)
class ResignRequest(wx.PyCommandEvent):
  def __init__(self, id, t):
    assert t in [bglib.model.constants.resign_single, 
                 bglib.model.constants.resign_gammon, 
                 bglib.model.constants.resign_backgammon, 
                 ]
    wx.PyCommandEvent.__init__(self, EVT_RESIGN_REQUESTED_TYPE, id)
    self.t = t
  def GetResignType(self):
    return self.t

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

  def StatusBarMessage(self, message):
    self.message = message
    self.UpdateStatusBar()

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
    evt.Skip()
    down = evt.GetDown()
    up = evt.GetUp()
    board = self.model
    mf = self.mf

    on_action_plyars, opps = acitons_whose(board)

    if down.name == on_action_plyars+'field':
      if up.name == on_action_plyars+'home':
        if board.has_rolled():
          if mf.is_leagal_to_pickup_dice():
            evt = MoveDone(self.GetId(), mf.move)
            self.GetEventHandler().ProcessEvent(evt)
            return 
          elif mf.available:
            self.StatusBarMessage('Need to move more')
            return 
        elif board.doubled:
          evt = CubeTake(self.GetId())
          self.GetEventHandler().ProcessEvent(evt)
          return
        else:
          self.StatusBarMessage('undefined action')
          return
      elif up.name == 'cubeholder':
        if not board.has_rolled():
          evt = CubePass(self.GetId())
          self.GetEventHandler().ProcessEvent(evt)
          return
        else:
          self.StatusBarMessage('undefined action')
          return
      else:
        self.StatusBarMessage('undefined action')
        return

    if up.name == on_action_plyars +'field':
      if down.name == 'cubeholder':
        if board.is_leagal_to_double():
          evt = DoubleRequest(self.GetId())
          self.GetEventHandler().ProcessEvent(evt)
        else:
          self.StatusBarMessage('doubling is not allowed here')
          return 
      elif down.name == on_action_plyars + 'home':
        if board.is_leagal_to_double():
          evt = DoubleRequest(self.GetId())
          self.GetEventHandler().ProcessEvent(evt)
          return 
        else:
          self.StatusBarMessage('doubling is not allowed here')
          return 
      elif down.name == on_action_plyars + 'score':
        evt = ResignRequest(self.GetId(), 1)
        self.GetEventHandler().ProcessEvent(evt)
        return
      else:
        self.StatusBarMessage('undefined action')
        return 

    try:
      down = bglib.model.util.position_pton(down.name, board.on_action)
      up = bglib.model.util.position_pton(up.name, board.on_action)
    except:
      self.StatusBarMessage("can't move to there")
      return

    if down > up:
      mv = mf.guess_your_multiple_pms(down, up)
    elif down < up:
      mv = mf.guess_your_multiple_partial_undoes(down, up)
    else:
      assert(up == donw)

    if mv:
      mf.add(mv)
      self.MoveInputNotify()
    else:
      self.StatusBarMessage('illeagal input')

  def OnRegionLeftClick(self, evt):
    evt.Skip()
    region = evt.GetRegion()
    b = self.model
    mf = self.mf

    points = ['%i'%i for i in range(1, 25)]

    on_action_plyars, opps = acitons_whose(b)

    if region.name == opps + 'field':
      self.StatusBarMessage('not your field!')
      return
    print 'is_leagal_to_roll:', b.is_leagal_to_roll()
      
    if region.name == on_action_plyars + 'field':
      if b.has_rolled():
        if mf.available:
          self.StatusBarMessage('move your checker')
          return
        elif mf.is_leagal_to_pickup_dice():
          evt = MoveDone(self.GetId(), mf.move)
          self.GetEventHandler().ProcessEvent(evt)
          self.StatusBarMessage('picking up dice ... ')
          return
        else:
          assert False
      elif b.is_leagal_to_roll():
        evt = RollRequest(self.GetId())
        self.GetEventHandler().ProcessEvent(evt)
        self.StatusBarMessage('rolling ...')
        return
      elif b.is_cube_take_or_pass():
        evt = CubeTake(self.GetId())
        self.GetEventHandler().ProcessEvent(evt)
        self.StatusBarMessage('take!')
        return
      else:
        self.StatusBarMessage('undefined action')
        return

    elif region.name == on_action_plyars + 'home':
      if b.is_leagal_to_double():
        evt = DoubleRequest(self.GetId())
        self.GetEventHandler().ProcessEvent(evt)
        self.StatusBarMessage('doubling ...')
        return
      else:
        self.StatusBarMessage("can't double.")
        return

    elif region.name == 'cubeholder':
      if b.is_cube_take_or_pass():
        evt = CubePass(self.GetId())
        self.GetEventHandler().ProcessEvent(evt)
        return
      elif b.is_leagal_to_double():
        evt = DoubleRequest(self.GetId())
        self.GetEventHandler().ProcessEvent(evt)
        self.StatusBarMessage('doubling ...')
        return
      else:
        self.StatusBarMessage("It's not time for cube action.")
        return

    elif region.name == 'score':
      evt = ResignRequest(self.GetId(), 1)
      self.GetEventHandler().ProcessEvent(evt)
      self.StatusBarMessage('resign ...')

    elif region.name in points or region.name == on_action_plyars + 'bar':
      src = bglib.model.util.position_pton(region.name, b.on_action)
      pm = mf.guess_your_single_pm_from_source(src)
      if pm:
        mf.append(pm)
        self.MoveInputNotify()
      else:
        self.StatusBarMessage('illeagal move')
    else:
      pass

  def OnRegionRightClick(self, evt):
    evt.Skip()
    region = evt.GetRegion()
    board = self.model
    mf = self.mf

    if region == 'your field':
      evt = CubePass(self.GetId())
      self.GetEventHandler().ProcessEvent(evt)
      return

    dest = bglib.model.position_pton(region.name, board.on_action)
    print mf.guess_your_making_point(dest)
    self.StatusBarMessage('illeagal move')
      


if __name__ == '__main__':
  import testframe
  app = wx.PySimpleApp()
  f = testframe.InteractiveTester(None)
  p = Player(f, f.get_model())
  st = p.MakeStatusBar()
  f.SetStatusBar(st)
  f.start([p])
  app.MainLoop()

