#!/usrbin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2006-2008 Noriyuki Hosaka nori@backgammon.gr.jp
#
import Image
import ImageDraw
import logging

import config
import model

debug_color = config.active.image.debug_color
rpath = config.active.image.resource

def draw_point(im, i, O, X):
    fn = rpath + ''
    xoffset = 0
    yoffset = 0
    rotate = False

    if i > 11:
      if i < 18:
        xoffset = 18 * (i-12) + 25
      else:
        xoffset = 18 * (i-12) + 50
      yoffset = 18
    else:
      rotate = True
      if i < 6:
        xoffset = 18 * (11 - i) + 50
      else:
        xoffset = 18 * (11 - i) + 25
      yoffset = 88 + 38

    if i % 2:
      fn += "even-"
    else:
      fn += "odd-"

    if O[i] == 0 and X[23-i] ==0:
      fn += "none.jpg"
    elif X[23-i]:
      logging.debug("X x %i @ %i"%(X[23-i],i))
      fn += "green-"+ str(X[23-i]) + ".jpg"
    elif O[i]:
      logging.debug("O x %i @ %i"%(O[i],i))
      fn += "white-" + str(O[i]) + ".jpg"
    else:
      raise Exception

    pt = Image.open(fn)
    if rotate:
      pt = pt.rotate(180)
    print i, xoffset, yoffset
    im.paste(pt, (xoffset, yoffset))


def draw_bar(im, O, X ):
  if O[24]:
    logging.debug("%i"%(O[24]))
    res = Image.open(rpath+"bar-white-%i.jpg"%(O[24]))
    logging.debug("%s"%(str(res)))
  else:
    res = Image.open(rpath+"bar-none.jpg")
  im.paste(res , (133, 126))
  print "O[24]", 133, 126

  if X[24]:
    res = Image.open(rpath+"bar-green-%i.jpg"%(X[24]))
  else:
    res = Image.open(rpath+"bar-none.jpg")
  im.paste(res, (133, 18))
  print "X[24]", 133, 18


def generate(board):
  X, O = board.position
  im = Image.new("RGB",(291, 232), debug_color)
  for i in range(0,24):
    draw_point(im, i, O, X)
  draw_bar(im, O, X)

  im.paste(Image.open(rpath+"center.jpg"), (133, 106))
  im.paste(Image.open(rpath+"field.jpg"), (25, 106))
  im.paste(Image.open(rpath+"field.jpg"), (158, 106))

  return im

if __name__ == '__main__':
  import doctest
  doctest.testfile('image.test')

