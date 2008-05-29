#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2006-2008 Noriyuki Hosaka nori@backgammon.gr.jp
#

import sys
import wx

import bglib.model.board
import bglib.encoding.gnubg

import bglib.gui.viewer
import bglib.gui.player


class InteractiveTester(wx.Frame):
  def __init__(self, parent):
    wx.Frame.__init__(self, parent)
    self.model = bglib.model.board.board()
    self.targets = list()
    self.tests = list()
    self.nth = 0
    self.results = list()

    ok = wx.Button(self, -1, 'OK')
    self.Bind(wx.EVT_BUTTON, self.OnOK, ok)
    fail = wx.Button(self, -1, 'Fail')
    self.Bind(wx.EVT_BUTTON, self.OnFail, fail)

    self.info = wx.TextCtrl(self, -1, style=wx.TE_READONLY | wx.TE_NO_VSCROLL)
    sizer = wx.BoxSizer(wx.HORIZONTAL)
    sizer.Add(ok)
    sizer.Add(fail)
    sizer.Add(self.info, proportion=1, flag=wx.EXPAND)
    self.buttons = sizer

    self.Bind(bglib.gui.viewer.EVT_REGION_LEFT_DRAG, self.OnRegionLeftDrag)
    self.Bind(bglib.gui.viewer.EVT_REGION_LEFT_CLICK, self.OnRegionLeftClick)
    self.Bind(bglib.gui.viewer.EVT_REGION_RIGHT_CLICK, self.OnRegionRightClick)
    self.Bind(bglib.gui.player.EVT_ROLL_REQUESTED, self.OnRollRequested)
    self.Bind(bglib.gui.player.EVT_DOUBLE_REQUESTED, self.OnDoubleRequested)
    self.Bind(bglib.gui.player.EVT_CUBE_TAKE, self.OnCubeTake)
    self.Bind(bglib.gui.player.EVT_CUBE_PASS, self.OnCubePass)
    self.Bind(bglib.gui.player.EVT_MOVE_DONE, self.OnMoveDone)

    evt = bglib.gui.viewer.LeftClick(self.GetId(), None)
    self.GetEventHandler().ProcessEvent(evt)

    evt = bglib.gui.player.RollRequest(self.GetId())
    self.GetEventHandler().ProcessEvent(evt)

  def OnRegionLeftDrag(self ,evt):
    down = evt.GetDown()
    up = evt.GetUp()
    print 'OnRegionLeftDrag:  from ', down, 'to', up
  def OnRegionLeftClick(self, evt):
    print 'OnRegionLeftClick:', evt.GetRegion()
  def OnRegionRightClick(self, evt):
    print 'OnRegionRightClick:', evt.GetRegion()
  def OnRollRequested(self, evt):
    print 'RollRequested'
  def OnDoubleRequested(self, evt):
    print 'DoubleRequested'
  def OnCubeTake(self, evt):
    print 'CubeTake'
  def OnCubePass(self, evt):
    print 'CubePass'
  def OnMoveDone(self, evt):
    print 'MoveDone', evt.move

  def get_model(self):
    return self.model

  def next(self):
    if len(self.tests) <= self.nth + 1:
      sys.exit()
    self.nth += 1
    self.sync()

  def sync(self):
    test = self.tests[self.nth]
    model = bglib.model.board.board()
    bglib.encoding.gnubg.decode(model, test[0], test[1])
    self.info.SetValue("pid=%s,  mid=%s"%(test[0], test[1]))

    for target in self.targets:
      target.SetModel(model)
      target.Notify()

  def OnOK(self, evt):
    print 'ok :', self.tests[self.nth]
    self.next()

  def OnFail(self, evt):
    print 'fail:', self.tests[self.nth]
    self.next()

  def start(self, targets, tests=None):
    if tests is None:
      tests = [
           ('22wqECCw8+ABYA', 'UQmgAAAAAAAA'),
           ('4HPiASHgc/ABMA', 'UQn1AAAAAAAA'),
           ('4HPKATDgc/ABMA', 'cAngAAAAAAAA'),
           ('PwkAACoBAAAAAA', 'cAn2AAAAAAAA'),
           ('FwAA4CcBAAAAAA', 'MAH2AAAAAAAA'),
           ('4HPiASHgc/ABMA', 'UQn1AAAAAAAA'),
           ('NgAAACAEAAAAAA', 'cAnyAAAAAAAA'),
           ('4PPIQRCYc4sBMA', '8Am1AEAAAAAA'),
           ('284lIADf7QAAYA', '8Im1AEAAAAAA'),
           ('AAAAgAAAAAAAAA', 'cAqgAFAAAAAA'),
          ]
    self.tests = tests
    self.targets = targets

    sizer = wx.BoxSizer(wx.VERTICAL)
    print 'adding... ', str(targets[0])
    sizer.Add(targets[0], proportion=1, flag=wx.SHAPED)
    for target in targets[1:]:
      print 'adding... ', str(target)
      sizer.Add(target, proportion=0, flag=wx.EXPAND)
    sizer.Add(self.buttons, proportion=0, flag=wx.EXPAND)
    self.SetSizer(sizer)
    self.Fit()

    self.sync()
    self.Show()

