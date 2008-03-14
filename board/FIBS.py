#!/usrbin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2006-2008 Noriyuki Hosaka nori@backgammon.gr.jp
#

class _FIBSBoardState(object):
  '''
  http://www.fibs.com/fibs_interface.html#board_state
  '''
  index = dict(
      you=(1, 2), 
      him=(2, 3),
      matchlength=(3, 4),
      your_score=(4, 5),
      his_score=(5, 6),
      board=(6, 32),
      turn=(32, 33),
      your_dice=(33, 35),
      his_dice=(35, 37),
      doubling_cube=(37, 38),
      you_may_double=(38, 39),
      he_may_double=(39, 40),
      was_doubled=(40, 41), # maybe not used ?
      your_colour=(41, 42),
      your_direction=(42, 43),
      your_home=(43, 44), #obsolete
      your_bar=(44, 45), 
      your_chequers_on_home=(45, 46),
      his_chequers_on_home=(46, 47),
      your_chequers_on_bar=(47, 48),
      his_chequers_on_bar=(48, 49),
      your_chequers_to_play=(49, 50),
      forced_move_and_did_crawford=(50, 52),# Not USED! 
      redoubles=(52, 53),
    )

  def __init__(self, s):
    self.data = s.split(':')

  def __getattr__(self, name):
    def cast_if_possible(x):
      try:
        return int(x)
      except:
        return x
    L = map(cast_if_possible, self.data[self.index[name][0]:self.index[name][1]])
    if len(L) == 1:
      return L[0]
    else:
      return tuple(L)

  def position(self):
    return ((0, 0, 0, 0, 0, 5, 0, 3, 0, 0, 0, 0,\
 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0),\
 (0, 0, 0, 0, 0, 5, 0, 3, 0, 0, 0, 0,\
 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0))


def FIBSDecode(s):
  return _FIBSBoardState(s)

def FIBSEncode(s):
  '''currently no use.'''
  raise NotImplemented

if __name__ == '__main__':
  import doctest
  doctest.testfile('FIBS.test')

