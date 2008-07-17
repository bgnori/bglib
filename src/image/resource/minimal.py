#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2006-2008 Noriyuki Hosaka nori@backgammon.gr.jp
#
import os.path
import bglib.image.PIL
import bglib.image.css
from bglib.image.theme import themata

mypath = 'minimal'
testdatapath = os.path.join(themata, mypath, 'testdata')

css = bglib.image.css.load(os.path.join(themata, mypath, "default.css"))
draw = bglib.image.PIL.Draw(css)

if __name__ == '__main__':
  import bglib.image.writer
  w = bglib.image.writer.Writer()
  f = file(os.path.join(themata, mypath, 'test.py'), 'w')
  w.write(f, 'minimal')
  f.close()


