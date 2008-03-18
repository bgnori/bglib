#!/usrbin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2006-2008 Noriyuki Hosaka nori@backgammon.gr.jp
#
import logging
import csv

import Image
import ImageDraw

import config
import model

debug_color = config.active.image.debug_color

def parse_align():
  f = file('./resource/align.txt', 'r')
  for line in f.readlines():
    x = line.split()
    if x:
      yield line.split()
    else:
      raise StopIteration
    

class Painter(object):
  def __init__(self, board):
    self.image = Image.new("RGB",(291, 232), debug_color)
    self.board = board
    self.rpath = config.active.image.resource
    self.colormap = {model.him:"green-", model.you:"white-"}
    
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
    if param == 'Him':
      if him[24]:
        res = Image.open(self.rpath+"bar-"+self.colormap[model.him]+"%i.jpg"%(him[24]))
      else:
        res = Image.open(self.rpath+"bar-none.jpg")
      
    self.image.paste(res , (x, y))

  def field(self, param, x, y):
    self.image.paste(Image.open(self.rpath+"field.jpg"), (x, y))

  def center(self, param, x, y):
    self.image.paste(Image.open(self.rpath+"center.jpg"), (133, 106))

  def handle(self, name, param, x, y):
    f = getattr(self, name)
    f(param, int(x), int(y))


def generate(board):
  p = Painter(board)
  for name, param, x, y in parse_align():
    p.handle(name, param, int(x), int(y))
  return p.image


if __name__ == '__main__':
  import doctest
  doctest.testfile('image.test')

