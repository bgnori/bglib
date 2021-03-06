
#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2006-2008 Noriyuki Hosaka nori@backgammon.gr.jp
#

from bglib.model.constants import *

def flip_point(n):
  return 23 - n

def position_pton(p, on_action):
  if p == 'your home' or p == 'his home':
    return -1
  elif p == 'your bar' or p == 'his bar':
    return 24
  else:
    i = int(p)
    if 0 < i and i < 25:
      if on_action == YOU:
        return i-1
      else:
        return 24 - i
  raise ValueError('Non-point numeric %s'%(p,))

def position_ntop(n, on_action):
  if n < 0:
    return OWNER_STRING[on_action] + ' home'
  elif 0 <= n and n < 24:
    if on_action == YOU:
      return str(n+1)
    elif on_action == HIM:
      return str(24-n)
    else:
      raise ValueError('Bad on action %s'%(on_action,))
  elif n == 24:
    return OWNER_STRING[on_action] + ' bar'
  else:
    raise ValueError('Non-point numeric %s'%(n,))

def move_ntop(n):
  if n < 0:
    return 'off'
  elif 0 <= n and n < 24:
    return str(n+1)
  elif n == 24:
    return 'bar'
  else:
    raise ValueError('Non-point numeric %s'%(n,))

def move_pton(p):
  if p == 'bar':
    return 24
  elif p == 'off':
    return -1
  else:
    i = int(p)
    if 0 <= i and i <= 25:
      #ugh! 25 is not well defined
      #ugh! 0 is not well defined
      return i-1
  raise ValueError('Non-point numeric %s'%(p,))

def get_opp(player):
  if player == HIM:
    return YOU
  elif player == YOU:
    return HIM
  raise ValueError('Non-player value %s'%(player,))
