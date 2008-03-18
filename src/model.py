#!/usrbin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2006-2008 Noriyuki Hosaka nori@backgammon.gr.jp
#



you = 0
him = 1


class board(object):
  def __init__(self, 
                  chequers=None
                  cube_value,
                  cube_owner=
                  on_action=
                  crawford=None
                  game_state = (8, 11, single_int),
                  on_inner_action = (11, 12, single_int),
                  doubled = (12, 13, single_boolean),
                  resign_offer = (13, 15, single_int),
                  rolled = (15, 21, double_int_tuple),
                  match_length = (21, 36, single_int),
                  score = (36, 66, double_int_tuple),
              )




if __name__ == '__main__':
  import doctest
  doctest.testfile('base.test')
