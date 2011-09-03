#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2006-2008 Noriyuki Hosaka nori@backgammon.gr.jp
#
import re
import os.path

#import tonic.moduleid 

import bglib.image.PIL
import bglib.image.css
from bglib.image.theme import themata

mypath = 'nature'
__moduleid_deps__ = [
    mypath+'/DejaVuLGCSans-Bold.ttf',
    mypath+'/default.css']

#tonic.moduleid.register(globals())

testdatapath = os.path.join(themata, mypath, 'test')

css = bglib.image.css.load(os.path.join(themata, mypath, "default.css"))
draw = bglib.image.PIL.Draw(css)

if __name__ == '__main__':
  import bglib.image.testwriter
  w = bglib.image.testwriter.Writer()
  f = file(os.path.join(themata, 'nature_test.py'), 'w')
  w.write(f, 'nature')
  f.close()

