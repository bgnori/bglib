#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2006-2008 Noriyuki Hosaka nori@backgammon.gr.jp
#
import re

from bglib.model import BoardEditor
from bglib.model.constants import *

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

  assert isinstance(m, BoardEditor)
     
  fibs = _FIBSBoardState(s)
  m.position = fibs.position()
  m.cube_in_logarithm = log(fibs.doubling_cube)

  if fibs.you_may_double and fibs.he_may_double:
    m.cube_owner = CENTER
    m.crawford = False
  elif fibs.you_may_double and not fibs.he_may_double:
    m.cube_owner = YOU
    m.crawford = False
  elif not fibs.you_may_double and fibs.he_may_double:
    m.cube_owner = HIM
    m.crawford = False
  else:
    m.cube_owner = CENTER
    m.crawford = True

  if fibs.turn == fibs.your_colour:
    m.on_action = YOU
    m.on_inner_action = YOU
    m.rolled = fibs.your_dice
    m.game_state = ON_GOING
  elif fibs.turn == fibs.your_colour * -1: #opposite colour
    m.rolled = fibs.his_dice
    m.on_action = HIM
    m.on_inner_action = HIM
    m.game_state = bglib.model.constants.on_going
  else:
    m.rolled=(0, 0)
    m.on_action = INVALID
    m.game_state = FINISHED
    #m.game_state = bglib.model.constants.resigned
    #ugh! There is no way to define it
    #may be we need to add some thing.

  if fibs.was_doubled:
    m.doubled = True
    if m.on_action == YOU:
      m.on_inner_action = HIM
    elif m.on_action == HIM:
      m.on_inner_action = YOU

  m.resign_offer = RESIGN_NONE
  # can't define!

  m.match_length = fibs.matchlength
  m.score = (fibs.your_score, fibs.his_score)

def encode(s):
  '''currently no use.'''
  raise NotImplemented

die_expr = re.compile("[1-6]")
def get_dice(got):
  die_a, die_b = die_expr.findall(got)
  return int(die_a), int(die_b)

name_expr = re.compile("^[a-zA-Z_<>]+")
def get_name(got):
  m = name_expr.search(got)
  if m is None:
    return None
  return got[m.start():m.end()]

taker_name_expr = re.compile("(?P<name>^[a-zA-Z_<>]+) accpets")
def get_taker_name(got):
  m = name_expr.search(got)
  if m is None:
    return None
  try:
    return got[m.start('name'):m.end('name')]
  except IndexError:
    return None

def get_move(got, who):
  '''got = gBOTworldclass moves 22-off 24-off .'''
  mv = bglib.model.move.Move()
  for m in got.split(' ')[2:-1]:
    src, dest = m.split('-')
    is_hitting = dest.endswith('*')
    if is_hitting:
      dest = dest[:-1]
    if who == bglib.model.constants.you:
      src = bglib.model.util.move_pton(src)
      dest = bglib.model.util.move_pton(dest)
      pm = bglib.model.move.PartialMove(src-dest, src, dest, is_hitting)
    elif who == bglib.model.constants.him:
      src = bglib.model.util.move_pton(src)
      dest = bglib.model.util.move_pton(dest)
      pm = bglib.model.move.PartialMove(dest-src, src, dest, is_hitting)
    else:
      continue
    mv.append(pm)
  return mv

score_expr = re.compile("[0-9]+")
def get_score(got):
  score = score_expr.findall(got)
  return int(score)

match_score_expr = re.compile("[0-9]+")
def get_match_scores(got):
  you, him, matchlength = match_score_expr.findall(got)
  return int(you), int(him), int(matchlength)

def get_resign_score(got):
  score = score_expr.findall(got)[0]
  return int(score)


if __name__ == '__main__':
  import doctest
  doctest.testfile('FIBS.test')


