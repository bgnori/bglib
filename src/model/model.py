#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2006-2008 Noriyuki Hosaka nori@backgammon.gr.jp
#



class game(object):
  '''
  sequence of moves
  '''
  pass

class match(object):
  '''
  sequence of games
  '''
  pass


if __name__ == '__main__':
  import doctest
  doctest.testfile('model.test')

