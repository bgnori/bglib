#!/usr/bin/python

import socket
import select
import time
import os
import wx

def get_addr():
  return '127.0.0.1', 4321
  #return 'localhost', 20000

f = file('session.log')


'''
sock = socket.socket()
addr = get_addr()
sock.bind(addr)
sock.listen(1)
conn, address = sock.accept()
while True:
  line = f.readline()
  print line 

  conn.send(line)
  #time.sleep(1)
'''
sock = socket.socket()

class StreamWindow(wx.TextCtrl):
  def __init__(self, parent, **kw):
    wx.TextCtrl.__init__(self, parent, -1, '*** stream window ***', 
                style=wx.TE_MULTILINE|wx.TE_READONLY|wx.VSCROLL, 
                size=(400, 500),
                **kw
               )

class FileSelectionForm(wx.Panel):
  def __init__(self, parent, initial_value, **kw):
    wx.Panel.__init__(self, parent, -1)
    sizer = wx.BoxSizer(wx.HORIZONTAL)
    path = wx.TextCtrl(self, -1, initial_value, size=(600, 20))
    sizer.Add(path, 1, wx.EXPAND)
    start_selection = wx.Button(self, -1, '...')
    sizer.Add(start_selection)

    self.path = path
    self.SetSizer(sizer)
    self.Fit()

    self.Bind(wx.EVT_BUTTON, self.OnButton, start_selection)

  def GetValue(self):
    return self.path.GetValue()

  def OnButton(self, evt):
    dialog = wx.FileDialog(None, "Choose scenario file", os.getcwd(), '', "All files(*.*)|*.*",wx.OPEN)
    if dialog.ShowModal() == wx.ID_OK:
      self.path.SetValue(dialog.GetPath())
    dialog.Destroy()
    


class ScenarioWindow(wx.Panel):
  def __init__(self, parent, **kw):
    wx.Panel.__init__(self, parent, -1)
    sizer = wx.BoxSizer(wx.HORIZONTAL)
    stop = wx.Button(self, -1, 'stop')
    sizer.Add(stop)
    step = wx.Button(self, -1, 'step')
    sizer.Add(step)
    auto = wx.CheckBox(self, -1, 'auto')
    sizer.Add(auto)
    fileselection = FileSelectionForm(self,  '')
    sizer.Add(fileselection, 1, wx.EXPAND)

    self.SetSizer(sizer)
    self.Fit()
  

class AppFrame(wx.Frame):
  def __init__(self, **kw):
    wx.Frame.__init__(self, None, -1, 'networkplayer')
    sizer = wx.BoxSizer(wx.VERTICAL)

    stream = StreamWindow(self)
    sizer.Add(stream, 1, wx.EXPAND)
    self.stream = stream

    sw = ScenarioWindow(self)
    sizer.Add(sw, 0, wx.EXPAND)

    sw = ScenarioWindow(self)
    sizer.Add(sw, 0, wx.EXPAND)

    sw = ScenarioWindow(self)
    sizer.Add(sw, 0, wx.EXPAND)

    self.SetSizer(sizer)
    self.Fit()
    self.Show()

class MyApp(wx.App):
  """
  stream window
  -------------------------------
  > Wednesday, April 09 09:08:53 MEST   ( Wed Apr  9 07:08:53 2008 UTC )
  > login:
  < login client_name clip_version username password
  > 1 wxpygammon 1207724539 v113117.ppp.asahi-net.or.jp
  > 2 wxpygammon 1 1 0 0 0 0 1 1 0 0 0 0 1 1500.00 0 0 0 1 0 UTC'
  -------------------------------
  scenario window
  -------------------------------
  [add][stop all]
  stop step auto         scenario_one    ... trigger:
  stop step auto         scenario_two    ... trigger:
  stop step auto         scenario_three  ... trigger:
  stop step auto         scenario_four   ... trigger:

  """
  def __init__(self):
    wx.App.__init__(self)
    self.scenarios = dict()

  def add(self, filename):
    s = Scenario(filename)
    self.scenarios.update({filename:s})


class Scenario(object):
  def __init__(self, filename):
    self.f = file(filename)
    self.trigger = None
    self.is_fired = False
    self.auto_step = False
    self.interval = 0.0
    self.last = time.time()
    self.got_pulse = False

  def pulse(self):
    self.got_pulse = True

  def stop(self):
    self.auto_step = False

  def is_expired(self):
    if self.auto_step:
      delta = time.time() - self.last
      return self.interval > delta
    else:
      return self.got_pulse

  def get_line(self):
    if self.is_fired and self.is_expired():
      self.got_pulse = False
      return self.f.readline()

app = MyApp()
frame = AppFrame()
frame.Show()
app.MainLoop()
