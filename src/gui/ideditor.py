#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2006-2008 Noriyuki Hosaka nori@backgammon.gr.jp
#
import logging
import wx
import wx.lib.intctrl

import bglib.encoding.gnubg

import bglib.gui.viewer

class IDEditor(wx.Panel):
  def __init__(self, parent, model):
    wx.Panel.__init__(self, parent)
    self.model = model
    label_position = wx.StaticText(self, -1, 'position id:')
    pid, mid = bglib.encoding.gnubg.encode(model)
    position_id = wx.TextCtrl(self, -1, pid,
                style=wx.TE_PROCESS_ENTER|wx.TE_NO_VSCROLL,
               )
    position_id.Bind(wx.EVT_TEXT_ENTER, self.OnChangePositionId)
    self.position_id = position_id

    label_match = wx.StaticText(self, -1, 'match id:')
    match_id = wx.TextCtrl(self, -1, mid,
                style=wx.TE_PROCESS_ENTER|wx.TE_NO_VSCROLL,
               )
    match_id.Bind(wx.EVT_TEXT_ENTER, self.OnChangeMatchId)
    self.match_id = match_id

    space = 4
    sizer = wx.FlexGridSizer(cols=2, hgap=space, vgap=space)
    sizer.AddMany([
        label_position, position_id,
        label_match,    match_id,
        ])
    self.SetSizer(sizer)
    self.Fit()

  def Notify(self):
    pid, mid = bglib.encoding.gnubg.encode(self.model)
    self.position_id.SetValue(pid)
    self.match_id.SetValue(mid)

  def OnChangePositionId(self, evt):
    logging.debug('OnChangePositionId', evt.GetString(), evt.GetEventObject())
    p = bglib.encoding.gnubg.decode_position(evt.GetString())
    self.model.position = p

  def OnChangeMatchId(self, evt):
    logging.debug('OnChangeMatchId', evt.GetString(), evt.GetEventObject())
    m = bglib.encoding.gnubg.decode_match(evt.GetString())

    self.model.cube_in_logarithm = (1 << m.cube_in_logarithm)
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

if __name__ == '__main__':
  import testframe
  app = wx.PySimpleApp()
  f = testframe.InteractiveTester(None)

  v = bglib.gui.viewer.Viewer(f, f.get_model())
  ie = IDEditor(f, f.get_model())
  f.start([v, ie])
  app.MainLoop()

