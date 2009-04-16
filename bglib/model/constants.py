#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2006-2008 Noriyuki Hosaka nori@backgammon.gr.jp
#

# constants
YOU = 0
HIM = 1
CENTER = 3 # in gnubg 11
player_string = ('you', 'him')
owner_string = ('your', 'his', None, 'center')

OFF = -1
BAR = 24
POINTS = range(0, 24)
NONE_BEAROFF_POINTS =range(6, 25)
POINTS_STRINGS = ('%i'%i for i in range(1, 25))

#game state
NOT_STARTED = 0
ON_GOING = 1
FINISHED = 2
RESIGNED = 3
DOUBLED_OUT = 4

# for match length
MONEY_GAME = 0

#resing type
RESIGN_NONE = 0
RESIGN_SINGLE = 1
RESIGN_GAMMON = 2
RESIGN_BACKGAMMON = 3
RESIGN_TYPES = (RESIGN_SINGLE, RESIGN_GAMMON, RESIGN_BACKGAMMON)
RESIGN_STRINGS = ('none', 'single', 'gammon', 'backgammon')

INITIAL_POSITION = ((0, 0, 0, 0, 0, 5, 0, 3, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0), (0, 0, 0, 0, 0, 5, 0, 3, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0))


NO_DOUBLE = 0
DOUBLE_TAKE = 1
DOUBLE_PASS = 2
TOO_GOOD_TO_DOUBLE = 3
CUBEACTION_TYPES = (NO_DOUBLE, DOUBLE_TAKE, DOUBLE_PASS, TOO_GOOD_TO_DOUBLE)
CUBEACTION_STRINGS = ('No double', 'Double, take', 'Double, pass', 'Too good to double')

