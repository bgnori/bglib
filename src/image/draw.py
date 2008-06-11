#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2006-2008 Noriyuki Hosaka nori@backgammon.gr.jp
#

import bglib.image.base
import bglib.image.css

class Draw(object):
  def __init__(self, css_path):
    self.css = bglib.image.css.load(css_path)
    self.cache = dict()
    self.dc = None
    self.color = None

  def create_dc(self, size):
    return list()
  def delele_dc(self):
    pass
  def result_from_dc(self):
    return self.dc
    
  def make_tree(self, b):
    t = bglib.image.base.ElementTree(b)
    self.css.apply(t)
    return t

  def draw(self, b, size):
    t = self.make_tree(b)
    self.dc = self.create_dc(size)
    t.visit(self.draw_element, [t.board])
    result = self.result_from_dc()
    self.delele_dc()
    return result

  def draw_text(self, position, size, text):
    self.dc.append('draw_text "%s" in %s with %s  @ %s'%(text, size, self.color, position))

  def draw_ellipse(self, position, size, fill=None):
    self.dc.append('draw_ellipse %s with %s , fill=%s @ %s'%(size, self.color, bool(fill),  position))

  def draw_polygon(self, points, fill=None):
    self.dc.append('draw_polygon %s fill=%s'%(points, bool(fill)))

  def draw_rect(self, position, size, fill=None):
    self.dc.append('draw_rect %s with %s , fill=%s @ %s'%(size, self.color, bool(fill),  position))

  def paste_image(self, src, position):
    self.dc.append('paste_image %s @ %s'%(src, position))

  def load_image(self, uri, size, flip):
    return uri + ' with ' + str(flip)

  def draw_element(self, path):
    e = path[-1]
    position = (e.x, e.y)
    size = (e.width, e.height)
    if hasattr(e, 'background'):
      bg = getattr(e, 'background')
      self.draw_rect(position, size, bg)
    if hasattr(e, 'image'):
      loaded = self.load_image(e.image, size, hasattr(e, 'flip'))
      self.paste_image(loaded, position)
    if hasattr(e, 'color'):
      self.color = e.color
      e.draw(self)

if __name__ == '__main__':
  import logging
  import bglib.model.board
  import bglib.image.base
  b = bglib.model.board.board()
  #d = Draw("./bglib/image/resource/safari/default.css")
  d = Draw("./bglib/image/resource/minimal/default.css")
  size = (400, 400)
  for line in d.draw(b, size):
    print line

