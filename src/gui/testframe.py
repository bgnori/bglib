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

