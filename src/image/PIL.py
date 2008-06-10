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
  def load_image(self, uri, size, flip):
    if (uri, size, flip) in self.cache:
      return self.cache[(uri, size, flip)]
    image = Image.open(uri)
    if flip:
      image = image.transpose(Image.FLIP_TOP_BOTTOM)
    image = image.resize(size)
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

  def draw(self, b, size):
    t = bglib.image.base.ElementTree(b)
    t.visit(self.apply, [t.board])
    result = Image.new('RGB', size)
    t.visit(self.draw_element, [t.board], result)
    return result


if __name__ == '__main__':
  import bglib.model.board
  b = bglib.model.board.board()
  d = Draw("./bglib/image/resource/safari/default.css")
  image = d.draw(b, (500, 500))
  image.show()
  

