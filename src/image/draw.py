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
  def set_pen(self, color):
    self.color = color

  def draw(self, b, size):
    t = self.make_tree(b)
    self.dc = self.create_dc(size)
    t.visit(self.draw_element, [t.board])
    result = self.result_from_dc()
    self.delele_dc()
    return result

  def draw_text(self, text):
    pass

  def fill_polygon(self, points):
    self.canvas.append('draw_polygon %s'%(points))

  def fill_rect(self, position, size):
    self.canvas.append('fill_rect %s with %s @ %s'%(size, self.color, position))

  def paste_image(self, src, position):
    self.canvas.append('paste_image %s @ %s'%(src, position))

  def load_image(self, uri, size, flip):
    return uri + ' with ' + str(flip)

  def draw_element(self, path):
    e = path[-1]
    position = (e.x, e.y)
    size = (e.width, e.height)
    if hasattr(e, 'background'):
      bg = getattr(e, 'background')
      self.set_pen(bg)
      self.fill_rect(position, size)
    if hasattr(e, 'image'):
      loaded = self.load_image(e.image, size, hasattr(e, 'flip'))
      self.paste_image(loaded, position)
    if hasattr(e, 'color'):
      self.set_pen(e.color)
      e.draw(self)

if __name__ == '__main__':
  import logging
  import bglib.model.board
  import bglib.image.base
  b = bglib.model.board.board()
  d = Draw("./bglib/image/resource/safari/default.css")
  size = (400, 400)
  for line in d.draw(b, size):
    print line

