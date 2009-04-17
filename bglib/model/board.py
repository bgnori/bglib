#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2006-2008 Noriyuki Hosaka nori@backgammon.gr.jp
#

from bglib.model import *
from bglib.model.constants import *
import util

class AbstractBoard(object):
  defaults = dict(
                  position=INITIAL_POSITION,
                  cube_in_logarithm=0,
                  cube_owner=CENTER,
                  on_action=YOU,
                  crawford=False,
                  game_state=NOT_STARTED,
                  on_inner_action=YOU,
                  doubled=False,
                  resign_offer=RESIGN_NONE,
                  rolled=(0, 0),
                  match_length=0,
                  score=(0, 0),
                  )
  def __repr__(self):
    return '\n'.join(['='*5 + 'start of board dump' + '='*5] + \
                     ['%s: %s'%(key, getattr(self, key)) for key in self.defaults.keys()] + \
                     ['='*5 + 'end of board dump' + '='*5]
                     )
  def __eq__(self, other):
    if not isinstance(other, AbstractBoard):
      raise TypeError
    for key in AbstractBoard.defaults:
      if getattr(self, key) != getattr(other, key):
        return False
    return True

  def is_open_to_land(self, n):
    if self.on_action == YOU:
      to_move, to_hit = self.position
    elif self.on_action == HIM:
      to_hit, to_move = self.position
    if n in POINTS:
      return to_hit[util.flip_point(n)] < 2
    else:
      assert n == -1
      return True

  def has_chequer_to_move(self, n):
    if self.on_action == YOU:
      to_move, to_hit = self.position
    elif self.on_action == HIM:
      to_hit, to_move = self.position
    else:
      assert False
    if to_move[BAR] == 0:
      return to_move[n]
    elif n == BAR:
      return to_move[n]
    return False

  def is_hitting_to_land(self, n):
    if self.on_action == YOU:
      to_move, to_hit = self.position
    elif self.on_action == HIM:
      to_hit, to_move = self.position
    if n in POINTS:
      return to_hit[util.flip_point(n)] == 1
    else:
      assert n == -1
      return False

  def is_ok_to_bearoff_from(self, n, die):
    if n +1 < die:
      for i in range(n + 1, BAR + 1):
        if self.has_chequer_to_move(i):
          return False
      return True
    elif n+1 == die:
      for i in NONE_BEAROFF_POINTS:
        if self.has_chequer_to_move(i):
          return False
      if self.has_chequer_to_move(n):
        return True
      return False
    else:
      assert die < n +1
      return False

  def is_leagal_to_roll(self, who):
    return \
       self.game_state == ON_GOING and \
       self.resign_offer == RESIGN_NONE and \
       self.rolled == (0, 0) and \
       self.on_action == who and \
       self.on_inner_action == who
       #self.doubled == False and \

  def is_leagal_to_move(self, who):
    '''
    verify leagality of the situation.
    i.e. you cant move on opponent turn, etc.
    '''
    return \
       self.game_state == ON_GOING and \
       self.on_action == who and \
       self.on_inner_action == who and \
       self.resign_offer == RESIGN_NONE and \
       self.rolled != (0, 0) # already rolled something.
       #self.doubled == False and \

  def has_rolled(self):
    if self.rolled == (0, 0):
      return False
    return True

  def is_cube_take_or_pass(self, who):
    return self.doubled and self.on_inner_action != self.on_action and \
      self.on_inner_action == who
  
  def find_src_of_bearoff_with(self, die):
    for i in NONE_BEAROFF_POINTS:
      if self.has_chequer_to_move(i):
        return None
    if self.has_chequer_to_move(die - 1):
      return die - 1
    for i in range(die - 1, 6):
      if self.has_chequer_to_move(i):
        return None
    for i in range(die, 0, -1):
      if self.has_chequer_to_move(i):
        return i
    return None# no chequer on board!

  def is_leagal_to_double(self, who):
    assert self.rolled == (0, 0)
    assert self.game_state == ON_GOING
    your_score, his_score = self.score
    if self.game_state != ON_GOING:
      return False
    if self.crawford:
      return False
    if self.doubled:
      return False
    if self.on_action == YOU:
      if who != YOU:
        return False
      if self.on_inner_action == YOU:
        if self.match_length == MONEY_GAME:
          return True
        if your_score <= self.match_length - pow(2, self.cube_in_logarithm):
          return True
      return False
    elif self.on_action == HIM:
      if who != HIM:
        return False
      if self.on_inner_action == HIM:
        if self.match_length == MONEY_GAME:
          return True
        if his_score < self.match_length - pow(2, self.cube_in_logarithm):
          return True
      return False
    assert False

  def is_leagal_to_redouble(self, who):
    """is allowed to beaver?"""
    return self.is_cube_take_or_pass(who) and \
           self.match_length == MONEY_GAME 

  def is_leagal_to_resign(self, who):
    return self.on_action == who and self.on_inner_action == who

  def is_to_accept_resign(self, who):
    return self.resign_offer in (RESIGN_SINGLE, 
                                 RESIGN_GAMMON,
                                 RESIGN_BACKGAMMON
                                 ) \
           and self.on_inner_action == who
  

class Board(AbstractBoard):
  __slots__ = AbstractBoard.defaults.keys()
  # immutable! immutable! immutable!

  def __new__(cls, **kw):
    self = object.__new__(cls)
    x = dict(self.defaults)
    for key, value in kw.items():
      assert key in x
      x[key] = value
    setter = object.__setattr__
    for key, value in x.items():
      setter(self, key, value)
    return self

  def __setattr__(self, name, value):
    raise TypeError('Tried to mutate immutable object attr of "%s" with %s'%(name, value))

  def __hash__(self):
    pass

  def __copy__(self):
    return self #immutable


