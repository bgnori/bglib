#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2006-2008 Noriyuki Hosaka nori@backgammon.gr.jp
#
import re
import os.path
import bglib.image.PIL
import bglib.image.css
from bglib.image.theme import themata

mypath = 'flower'
testdatapath = os.path.join(themata, mypath, 'test')

REVISION = re.compile(r"[0-9]+").search("$Revision: 1876 $").group()
css = bglib.image.css.load(os.path.join(themata, mypath, "default.css"))
draw = bglib.image.PIL.Draw(css)

if __name__ == '__main__':
  import bglib.image.testwriter
  w = bglib.image.testwriter.Writer()
  f = file(os.path.join(themata, 'flower_test.py'), 'w')
  w.write(f, 'flower')
  f.close()

