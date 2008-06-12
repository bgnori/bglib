#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2006-2008 Noriyuki Hosaka nori@backgammon.gr.jp
#

import logging
import bglib.model.board
import bglib.image.base
import bglib.image.draw

b = bglib.model.board.board()
tree = bglib.image.base.ElementTree(b)
css = bglib.image.css.load("./bglib/image/resource/minimal/default.css")
css.apply(tree)

print tree
