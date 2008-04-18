
#!/usrbin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2006-2008 Noriyuki Hosaka nori@backgammon.gr.jp
#

import Image
import wx
from wx.lib.colourchooser.canvas import Canvas

import bglib.image.context
import bglib.image.renderer


class Region(object):
  def __init__(self, image, x, y):
    assert(isinstance(image, Image.Image))
    w, h = image.size
    self.rect = wx.Rect(x, y ,w, h)
    wximage = wx.EmptyImage(image.size[0], image.size[1])
    wximage.SetData(image.convert('RGB').tostring())
    self.wxbmp = wximage.ConvertToBitmap()
  
  def GetX(self):
    return self.rect.GetX()
  def GetY(self):
    return self.rect.GetY()

  def Inside(self, pt):
    return self.rect.Inside(pt)

  def Draw(self, dc):
    dc.DrawBitmap(self.wxbmp, self.GetX(), self.GetY())

class BoardPanel(wx.Panel):
  def __init__(self, parent, id, **kw):
    wx.Panel.__init__(self, parent, **kw)
    self.regions = list()

    self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
    self.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
    self.Bind(wx.EVT_PAINT, self.OnPaint)
    self.Bind(wx.EVT_SIZE, self.OnSize)
    
  def which(self, pt):
    for region in self.regions:
      if region.Inside(pt):
        return region
    return None

  def append(self, region):
    #print region
    assert(isinstance(region, bglib.image.wxpython.Region))
    self.regions.append(region)

  def OnPaint(self, evt):
    dc = wx.PaintDC(self)
    for region in self.regions:
      region.Draw(dc)

  def OnLeftDown(self, evt):
    pass
  def OnLeftUp(self, evt):
    pass

  def OnSize(self, evt):
    size = self.GetClientSize()
    print 'resized ', size
    self.regions = list()
    style = bglib.depot.dict.Proxy(
                                  window = self,
                                  image=bglib.depot.lines.CRLFProxy('./bglib/image/resource/align.txt'),
                                )
    context_factory = bglib.image.context.context_factory
    context = context_factory.new_context('wx', style)
    board = bglib.model.board()
    renderer.render(context, board)

class Context(bglib.image.PIL.Context):
  name = 'wx'

  def __init__(self, style):
    bglib.image.PIL.Context.__init__(self, style.image)
    
    ix = style.image.size.board[0]
    print ix
    self.window = style.window
    sx = self.window.GetSizeTuple()[0]
    print sx

    self.mag_numer  = sx
    self.mag_denom  = ix

  def paste_image(self, image, position):
    position = self.apply_mag(position)
    x, y = position
    r = Region(image, x, y)
    self.window.append(r)

  def result(self):
    return self.window


if __name__ == '__main__':
  app = wx.PySimpleApp()

  frame = wx.Frame(None)

  board = bglib.model.board()
  import bglib.depot.dict
  style = bglib.depot.dict.Proxy(
                                  window = BoardPanel(frame, id=-1, 
                                                      pos=wx.DefaultPosition,
                                                     ),
                                  image=bglib.depot.lines.CRLFProxy('./bglib/image/resource/align.txt'),
                                  size=(100, 200)
                                )
  renderer = bglib.image.renderer.renderer
  context_factory = bglib.image.context.context_factory
  context = context_factory.new_context('wx', style)
  renderer.render(context, board)
  frame.Show()
  app.MainLoop()


