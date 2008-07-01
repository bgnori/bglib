#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2006-2008 Noriyuki Hosaka nori@backgammon.gr.jp
#

import logging
import bglib.model.board
import bglib.encoding.gnubg
import bglib.image.base
import bglib.image.draw

tests = [
     ('4Dl4ADqwt4MDIA', 'MBmgAAAAAAAA'),

     ('4Dl4ADqwt4MDIA', 'AQGgAAAAAAAA'),
     ('22wqECCw8+ABYA', 'UQmgAAAAAAAA'),
     ('4HPiASHgc/ABMA', 'UQn1AAAAAAAA'),
     ('4HPKATDgc/ABMA', 'cAngAAAAAAAA'),
     ('mGfwATDgc/ABMA', 'cCOgAAAAAAAA'),
     ('mGfwATDgc/ABMA', 'cEOgAAAAAAAA'),
     ('mGfwATDgc/ABMA', 'cGOgAAAAAAAA'),

     ('PwkAACoBAAAAAA', 'cAn2AAAAAAAA'),
     ('FwAA4CcBAAAAAA', 'MAH2AAAAAAAA'),
     ('4HPiASHgc/ABMA', 'UQn1AAAAAAAA'),
     ('NgAAACAEAAAAAA', 'cAnyAAAAAAAA'),
     ('4PPIQRCYc4sBMA', '8Am1AEAAAAAA'),
     ('284lIADf7QAAYA', '8Im1AEAAAAAA'),
     ('AAAAgAAAAAAAAA', 'cAqgAFAAAAAA'),
     ('2ObIAEpDu5EBKA', 'cInsAFAAIAAA'),
     ('AAAAAAAAAAAAAA', 'AAAAAAAAAAAA'),
    ]
#tests = [
#     ('AAAAAAAAAAAAAA', 'AAAAAAAAAAAA'),
#  ]

b = bglib.model.board.board()
css = bglib.image.css.load("./bglib/image/resource/minimal/default.css")

for test in tests:
  bglib.encoding.gnubg.decode(b, test[0], test[1])
  tree = bglib.image.base.ElementTree(b)
  css.apply(tree)
  print tree
