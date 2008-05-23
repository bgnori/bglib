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

#game state
not_started = 0
on_going = 1
finished = 2
resigned = 3
doubled_out = 4


#resing type
resign_none = 0
resign_single=1
resign_gammon=2
resign_backgammon=3

initial_position = ((0, 0, 0, 0, 0, 5, 0, 3, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0), (0, 0, 0, 0, 0, 5, 0, 3, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0))

