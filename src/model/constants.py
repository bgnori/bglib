#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2006-2008 Noriyuki Hosaka nori@backgammon.gr.jp
#

# constants
you = 0
him = 1
center = 3 # in gnubg 11
player_string = ('you', 'him')
owner_string = ('your', 'his')

off = -1
bar = 24
points = range(0, 24)
none_bearoff_points =range(6, 25)
points_strings = ['%i'%i for i in range(1, 25)]

#game state
not_started = 0
on_going = 1
finished = 2
resigned = 3
doubled_out = 4

# for match length
money_game = 0

#resing type
resign_none = 0
resign_single=1
resign_gammon=2
resign_backgammon=3
resign_types = (resign_single, resign_gammon, resign_backgammon)
resign_strings = ('none', 'single', 'gammon', 'backgammon')

initial_position = ((0, 0, 0, 0, 0, 5, 0, 3, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0), (0, 0, 0, 0, 0, 5, 0, 3, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0))


def get_opp(player):
  if player == him:
    return you
  elif player == you:
    return him
  else:
    pass
  assert False

