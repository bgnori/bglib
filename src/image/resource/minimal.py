#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2006-2008 Noriyuki Hosaka nori@backgammon.gr.jp
#
import bglib.image.PIL
import bglib.image.css
css = bglib.image.css.load("./bglib/image/resource/minimal/default.css")
draw = bglib.image.PIL.Draw(css)

if __name__ == '__main__':
  import bglib.image.writer
  w = bglib.image.writer.Writer()
  f = file('minimal_test.py', 'w')
  w.write(f, 'minimal')
  f.close()



