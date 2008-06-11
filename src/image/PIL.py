#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2006-2008 Noriyuki Hosaka nori@backgammon.gr.jp
#
import Image
import ImageDraw

import bglib.image.draw


class Draw(bglib.image.draw.Draw):
  def create_dc(self, size):
    img = Image.new('RGB', size)
    draw = ImageDraw.Draw(img)
    return [img, draw]

  def delele_dc(self):
    del self.dc[1]

  def result_from_dc(self):
    return self.dc[0]

  def load_image(self, uri, size, flip):
    if (uri, size, flip) in self.cache:
      return self.cache[(uri, size, flip)]
    image = Image.open(uri)
    if flip:
      image = image.transpose(Image.FLIP_TOP_BOTTOM)
    image = image.resize(size)
    self.cache.update({(uri, size, flip): image})
    return image

  def paste_image(self, src, position):
    self.dc[0].paste(src, position)

  def fill_polygon(self, points):
    draw = self.dc[1]
    draw.polygon(points, fill=self.color)

  def fill_rect(self, position, size):
    draw = self.dc[1]
    x2, y2 = position
    x2 += size[0]
    y2 += size[1]
    draw.rectangle([position, (x2-1, y2-1)], fill=self.color)

if __name__ == '__main__':
  import bglib.model.board
  b = bglib.model.board.board()
  #d = Draw("./bglib/image/resource/safari/default.css")
  d = Draw("./bglib/image/resource/minimal/default.css")
  image = d.draw(b, (400, 400))
  image.show()

