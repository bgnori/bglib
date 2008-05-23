#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2006-2008 Noriyuki Hosaka nori@backgammon.gr.jp
#

import bglib.model.constants
import bglib.model.board

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
    '''returns (you, him)'''
    def your_chequers(x):
      if self.your_colour * x > 0:
        return abs(x)
      return 0
    def his_chequers(x):
      if self.your_colour * x < 0:
        return abs(x)
      return 0
      
    if self.your_direction < 0:
      you = self.board[1:25] + (self.board[25], )
      him = (self.board[0], )+ self.board[1:25]
      him= list(him)
      him.reverse()
    else:
      you = (self.board[0], ) + self.board[1:25]
      him = self.board[1:25] + (self.board[25],)
      you = list(you)
      you.reverse()

    you = map(your_chequers, you)
    him = map(his_chequers, him)
    return tuple(you), tuple(him)


def decode(m, s):
  def log(power_of_two):
    r = 0
    while power_of_two > 1:
      power_of_two = power_of_two >> 1
      r+=1
    return r

  assert isinstance(m, bglib.model.board.board)
     
  fibs = _FIBSBoardState(s)
  m.position = fibs.position()
  m.cube_in_logarithm = log(fibs.doubling_cube)

  if fibs.you_may_double and fibs.he_may_double:
    m.cube_owner = bglib.model.constants.center
    m.crawford = False
  elif fibs.you_may_double and not fibs.he_may_double:
    m.cube_owner = bglib.model.constants.you
    m.crawford = False
  elif not fibs.you_may_double and fibs.he_may_double:
    m.cube_owner = bglib.model.constants.him
    m.crawford = False
  else:
    m.cube_owner = bglib.model.constants.center
    m.crawford = True

  if fibs.turn == fibs.your_colour:
    m.on_action = bglib.model.constants.you
    m.rolled = fibs.your_dice
    m.game_state = bglib.model.constants.on_going
  elif fibs.turn == fibs.your_colour * -1: #opposite colour
    m.rolled = fibs.his_dice
    m.on_action = bglib.model.constants.him
    m.game_state = bglib.model.constants.on_going
  else:
    m.rolled=(0, 0)
    m.on_action = bglib.model.constants.invalid
    m.game_state = bglib.model.constants.finished
    #m.game_state = bglib.model.constants.resigned
    #ugh! There is no way to define it
    #may be we need to add some thing.

  if fibs.was_doubled:
    m.on_inner_action=bglib.model.constants.you
    m.doubled = True

  m.resign_offer = bglib.model.constants.resign_none
  # can't define!

  m.match_length = fibs.matchlength
  m.score = (fibs.your_score, fibs.his_score)

def encode(s):
  '''currently no use.'''
  raise NotImplemented

if __name__ == '__main__':
  import doctest
  doctest.testfile('FIBS.test')


