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

  def make_tree(self, b):
    t = bglib.image.base.ElementTree(b)
    self.css.apply(t)
    return t
  def draw(self, b, size):
    t = self.make_tree(b)
    result = list()
    t.visit(self.draw_element, [t.board], result)
    return result

  def fill_rect(self, canvas, position, size, color):
    canvas.append('fill_rect %s with %s @ %s'%(size, color, position))

  def paste_image(self, canvas, src, position):
    canvas.append('paste_image %s @ %s'%(src, position))

  def load_image(self, uri, size, flip):
    return uri + ' with ' + str(flip)

  def draw_element(self, path, canvas):
    e = path[-1]
    position = (e.x, e.y)
    size = (e.width, e.height)
    if hasattr(e, 'background'):
      bg = getattr(e, 'background')
      self.fill_rect(canvas, position, size, bg)
    if hasattr(e, 'color'):
      pass #fill rect here
    if hasattr(e, 'image'):
      loaded = self.load_image(e.image, size, hasattr(e, 'flip'))
      self.paste_image(canvas, loaded, position)
    else:
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

