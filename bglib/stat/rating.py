#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2006-2009 Noriyuki Hosaka bgnori@gmain.com
#
import math

'''\
based on http://www.backgammon.gr.jp/rating/about_rating.html
'''

def upset_chance(high, low, length):
  assert high >= low
  return 1/(pow(10, ( high - low ) * math.sqrt(length)/2000) +1)


def winning_chance(high, low, length):
  return 1.0 - upset_chance(high, low, length)
  

def gain_on_win(player, opp, length):
  if player >= opp:
    return length * upset_chance(player, opp, length)
  if player < opp:
    return length * (1.0 - upset_chance(opp, player, length))

