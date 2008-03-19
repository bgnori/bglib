#!/usrbin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2006-2008 Noriyuki Hosaka nori@backgammon.gr.jp
#
import os.path
import logging
import csv

import Image
import ImageDraw

import config
import model

debug_color = config.active.image.debug_color

def parse_align(f):
  for line in f.readlines():
    x = line.split()
    if x:
      yield line.split()
    else:
      raise StopIteration

class Painter(object):
  def __init__(self, board, rpath):
    self.board = board
    self.rpath = rpath
    self.colormap = dict()
    
  def size(self, param, x, y):
    self.image = Image.new("RGB",(x, y), debug_color)
    
  def you(self, param, x, y):
    self.colormap.update({model.you:param})

  def him(self, param, x, y):
    self.colormap.update({model.him:param})

  def point(self, param, x, y):
    you, him = self.board.position
    i = int(param) - 1
    fn = self.rpath

    if i % 2:
      fn += "even-"
    else:
      fn += "odd-"

    if you[i]:
      fn += self.colormap[model.you]+ str(you[i]) + ".jpg"
    elif him[23-i]:
      fn += self.colormap[model.him] + str(him[23-i]) + ".jpg"
    else:
      fn += "none.jpg"

    pt = Image.open(fn)
    if i < 12:
      pt = pt.rotate(180)
    self.image.paste(pt, (x, y))

  def bar(self, param, x, y):
    you, him = self.board.position
    if param == 'You':
      if you[24]:
        res = Image.open(self.rpath+"bar-"+self.colormap[model.you]+"%i.jpg"%(you[24]))
      else:
        res = Image.open(self.rpath+"bar-none.jpg")
    elif param == 'Him':
      if him[24]:
        res = Image.open(self.rpath+"bar-"+self.colormap[model.him]+"%i.jpg"%(him[24]))
      else:
        res = Image.open(self.rpath+"bar-none.jpg")
    else:
      raise TypeError("bad parameter for bar: %s"%param)
      
    self.image.paste(res , (x, y))

  def field(self, param, x, y):
    self.image.paste(Image.open(self.rpath+"field.jpg"), (x, y))

  def center(self, param, x, y):
    self.image.paste(Image.open(self.rpath+"center.jpg"), (x, y))


def generate(board):
  rpath = config.active.image.resource
  p = Painter(board, rpath)
  f = file(os.path.join(rpath, 'align.txt'))
  try:
    for name, param, x, y in parse_align(f):
      m = getattr(p, name)
      if m and callable(m):
        m(param, int(x), int(y))
      else:
        raise
    return p.image
  finally:
    f.close()


if __name__ == '__main__':
  import doctest
  doctest.testfile('image.test')

