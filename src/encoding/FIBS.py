#!/usrbin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2006-2008 Noriyuki Hosaka nori@backgammon.gr.jp
#

import tito.smuggle
tito.smuggle.module('../..', 'bglib.model', locals())

import bglib.model

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
      # your_bar = his_home
      # your_home = his_bar
      you = self.board[self.your_home+1:self.your_bar+1]
      him = list(self.board[self.your_home:self.your_bar-1+1])
    else:
      you = self.board[self.your_bar:self.your_home-1+1]
      him = list(self.board[self.your_bar+1:self.your_home+1])

    him.reverse()
    you = map(your_chequers, you)
    him = map(his_chequers, him)
    return tuple(you), tuple(him)


def decode(s):
  fibs = _FIBSBoardState(s)
  m = bglib.model.board()
  m.position = fibs.position()
  m.cube_value=fibs.doubling_cube

  if fibs.you_may_double and fibs.he_may_double:
    m.cube_owner = bglib.model.center
    m.crawford = False
  elif fibs.you_may_double and not fibs.he_may_double:
    m.cube_owner = bglib.model.you
    m.crawford = False
  elif not fibs.you_may_double and fibs.he_may_double:
    m.cube_owner = bglib.model.him
    m.crawford = False
  else:
    m.cube_owner = bglib.model.center
    m.crawford = True

  if fibs.turn == fibs.your_colour:
    m.on_action = bglib.model.you
    m.rolled = fibs.your_dice
    m.game_state = bglib.model.on_going
  elif fibs.turn == fibs.your_colour * -1: #opposite colour
    m.rolled = fibs.his_dice
    m.on_action = bglib.model.him
    m.game_state = bglib.model.on_going
  else:
    m.rolled=(0, 0)
    m.on_action = bglib.model.invalid
    m.game_state = bglib.model.finished
    #m.game_state = bglib.model.resigned
    #ugh! There is no way to define it
    #may be we need to add some thing.

  if fibs.was_doubled:
    m.on_inner_action=bglib.model.you
    m.doubled = True

  m.resign_offer = bglib.model.resign_none
  # can't define!

  m.match_length = fibs.matchlength
  m.score = (fibs.your_score, fibs.his_score)
  return m

def encode(s):
  '''currently no use.'''
  raise NotImplemented

if __name__ == '__main__':
  import doctest
  doctest.testfile('FIBS.test')


