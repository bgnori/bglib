#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2006-2008 Noriyuki Hosaka nori@backgammon.gr.jp
#
import os.path

import Image
import ImageDraw

import bglib.image.context
import bglib.image.renderer
import bglib.depot.lines

debug_color = 'blue'

class Context(bglib.image.context.Context):
  name = 'PIL'
  def __init__(self, style):
    bglib.image.context.Context.__init__(self, style)
    x, y = style.size.table
    self.image = Image.new("RGB", (x, y), debug_color)
    self.cache = dict()

    self.mag_numer  = 1
    self.mag_denom  = 1

  def apply_mag(self, t):
    return (
            t[0] *self.mag_numer/ self.mag_denom,
            t[1] *self.mag_numer/ self.mag_denom
            )


  def paste_image(self, image, position):
    self.image.paste(image, position)


import bglib.image.xml
class Context(bglib.image.xml.Context):
  name = 'xmlPIL'
  def __init__(self, style):
    bglib.image.xml.Context.__init__(self, style)
    self.cache = dict()

  def load_image(self, uri, size, flip):
    if (uri, size, flip) in self.cache:
      return self.cache[(uri, size, flip)]
    image = Image.open(uri)
    if flip:
      image = image.transpose(Image.FLIP_TOP_BOTTOM)
    self.cache.update({(uri, size, flip): image})
    return image

  def paste_image(self, dest, src, position):
    dest.paste(src, position)

  def fill_rect(self, image, position, size, color):
    draw = ImageDraw.Draw(image)
    x2, y2 = position
    x2 += size[0]
    y2 += size[1]
    draw.rectangle([position, (x2, y2)], fill=color)

  def xmlrender(self, path, image):
    e = path[-1]
    position = (int(e.x), int(e.y))
    size = (int(e.width), int(e.height))
    if hasattr(e, 'background'):
      bg = getattr(e, 'background')
      self.fill_rect(image, position, size, bg)
    if hasattr(e, 'color'):
      pass #fill rect here
    if hasattr(e, 'image'):
      loaded = self.load_image(e.image.get(), size, hasattr(e, 'flip'))
      self.paste_image(image, loaded, position)

  def result(self):
    x, y = style.size.table
    image = Image.new("RGB", (x, y), debug_color)
    self.tree.css("./bglib/image/resource/safari/default.css")
    self.tree.visit(self.xmlrender, [self.tree.board], image)
    return image

bglib.image.context.context_factory.register(Context)

if __name__ == '__main__':
  import bglib.model.board
  board = bglib.model.board.board()
  style = bglib.depot.lines.CRLFProxy('./bglib/image/resource/original/align.txt')
  renderer = bglib.image.renderer.renderer
  context_factory = bglib.image.context.context_factory
  context = context_factory.new_context('xmlPIL', style)
  image = renderer.render(context, board)
  image.show()
  

