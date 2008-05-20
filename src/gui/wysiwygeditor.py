#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2006-2008 Noriyuki Hosaka nori@backgammon.gr.jp
#
import logging

import wx
import wx.lib.intctrl
import bglib.gui.viewer


class WYSIWYGEditor(wx.Panel):
  def __init__(self, parent, model):
    wx.Panel.__init__(self, parent)
    board = bglib.gui.viewer.Viewer(self, model)

    self.Bind(bglib.gui.viewer.EVT_REGION_LEFT_DRAG, self.OnRegionLeftDrag)
    self.Bind(bglib.gui.viewer.EVT_REGION_LEFT_CLICK, self.OnRegionLeftClick)
    self.Bind(bglib.gui.viewer.EVT_REGION_RIGHT_CLICK, self.OnRegionRightClick)

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
        board, (0,0),
        label_length,   length,
        label_his_score, his_score,
        label_your_score, your_score,
        label_crawford, crawford,
        ])
    self.SetSizer(sizer)
    self.Fit()

  def Notify(self):
    pass

  def OnRegionLeftDrag(self, evt):
    print 'OnRegionLeftDrag'
  def OnRegionLeftClick(self, evt):
    print 'OnRegionLeftClick'
    region = evt.GetRegion()
  def OnRegionRightClick(self, evt):
    print 'OnRegionRightClick'
    
  def OnChangeLength(self, evt):
    print 'OnChangeLength', evt.GetString(), evt.GetEventObject()

  def OnChangeHisScore(self, evt):
    print 'OnChangeHisScore', evt.GetString(), evt.GetEventObject()

  def OnChangeYourScore(self, evt):
    print 'OnChangeYourScore', evt.GetString(), evt.GetEventObject()

  def OnChangeCrawford(self, evt):
    print 'OnChangeCrawford', evt.GetValue(), evt.GetEventObject()


if __name__ == '__main__':
  import testframe
  app = wx.PySimpleApp()
  f = testframe.InteractiveTester(None)
  w = WYSIWYGEditor(f, f.get_proxy())
  f.start([w])
  app.MainLoop()

