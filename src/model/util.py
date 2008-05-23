
#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2006-2008 Noriyuki Hosaka nori@backgammon.gr.jp
#

import constants

def position_pton(p, on_action):
  if p == 'your home' or p == 'his home':
    return -1
  elif p == 'your bar' or p == 'his bar':
    return 24
  else:
    i = int(p)
    if 0 < i and i < 25:
      if on_action == constants.you:
        return i-1
      else:
        return 24 - i
  assert(false)

def position_ntop(n, on_action):
  if n < 0:
    return constants.owner_string[on_action] + ' home'
  elif 0 <= n and n < 24:
    if on_action == constants.you:
      return str(n+1)
    elif on_action == constants.him:
      return str(24-n)
    else:
      assert False
  elif n == 24:
    return constants.owner_string[on_action] + ' bar'
  else:
    assert False

def move_ntop(n):
  if n < 0:
    return 'off'
  elif 0 <= n and n < 24:
    return str(n+1)
  elif n == 24:
    return 'bar'
  else:
    assert False

if __name__ == '__main__':
  import doctest
  doctest.testfile('util.test')

