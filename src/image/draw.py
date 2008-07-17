#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2006-2008 Noriyuki Hosaka nori@backgammon.gr.jp
#

import bglib.image.base
import bglib.image.css

class Draw(object):
  def __init__(self, css):
    self.css = css
    self.cache = dict()
    self.dc = None
    self.mag = 1.0

  def calc_mag(self, xy):
    return int(xy[0] *self.mag), int(xy[1]*self.mag)

  def set_mag(self, bound, width, height):
    xmag = float(bound[0])/width
    ymag = float(bound[1])/height
    assert xmag > 0
    assert ymag > 0
    self.mag = min(xmag, ymag)

  def create_dc(self, size):
    assert self.dc is None
    self.dc = list()

  def delele_dc(self):
    self.dc = None

  def result_from_dc(self):
    assert self.dc
    return self.dc
    
  def make_tree(self, b):
    t = bglib.image.base.ElementTree(b)
    self.css.apply(t)
    return t

  def draw(self, b, size):
    if self.dc is not None:
      self.delele_dc()
    t = self.make_tree(b)
    self.set_mag(size, t.board.width, t.board.height)

    self.create_dc(size)
    assert self.dc is not None
    t.visit(self.draw_element, [t.board])
    result = self.result_from_dc()
    self.delele_dc()
    assert self.dc is None
    return result

  def draw_text(self, position, size, text, font_name, fill):
    assert self.dc is not None
    position=self.calc_mag(position)
    size=self.calc_mag(size)
    self.dc.append('draw_text "%s" in %s @ %s'%(text, size, position))

  def draw_ellipse(self, position, size, fill=None):
    assert self.dc is not None
    position=self.calc_mag(position)
    size=self.calc_mag(size)
    self.dc.append('draw_ellipse %s, fill=%s @ %s'%(size, bool(fill),  position))

  def draw_polygon(self, points, fill=None):
    assert self.dc is not None
    points = [self.calc_mag(pt) for pt in points]
    self.dc.append('draw_polygon %s fill=%s'%(points, bool(fill)))

  def draw_rect(self, position, size, fill=None):
    assert self.dc is not None
    position=self.calc_mag(position)
    size=self.calc_mag(size)
    self.dc.append('draw_rect %s, fill=%s @ %s'%(size, bool(fill),  position))

  def paste_image(self, src, position, size):
    assert self.dc is not None
    position=self.calc_mag(position)
    self.dc.append('paste_image %s @ %s'%(src, position))

  def load_image(self, uri, size, flip):
    size=self.calc_mag(size)
    return uri + ' size='+ str(size) + ' with flip=' + str(flip)

  def load_font(self, uri, size):
    #size=self.calc_mag(size)
    return uri + ' size=' + str(size)

  def draw_element(self, path):
    assert self.dc is not None
    e = path[-1]
    position = (e.x, e.y)
    size = (e.width, e.height)
    if hasattr(e, 'background'):
      bg = getattr(e, 'background')
      self.draw_rect(position, size, bg)
    if hasattr(e, 'image') or hasattr(e, 'color'):
      e.draw(self)

if __name__ == '__main__':
  import logging
  import bglib.model.board
  import bglib.image.base
  b = bglib.model.board.board()
  d = Draw(bglib.image.css.load("./bglib/image/resource/safari/default.css"))
  #d = Draw(bglib.image.css.load("./bglib/image/resource/minimal/default.css"))
  size = (400, 400)
  for line in d.draw(b, size):
    print line

