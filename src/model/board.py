#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2006-2008 Noriyuki Hosaka nori@backgammon.gr.jp
#


import constants
import util

class board(object):
  defaults = dict(
                  position=constants.initial_position,
                  cube_in_logarithm=0,
                  cube_owner=constants.center,
                  on_action=constants.you,
                  crawford=False,
                  game_state=constants.not_started,
                  on_inner_action=constants.you,
                  doubled=False,
                  resign_offer=constants.resign_none,
                  rolled=(0, 0),
                  match_length=0,
                  score=(0, 0),
                  )

  def __init__(self, src=None, **kw):
    x = dict()
    if src is not None:
      #if not isinstance(src, board):
      #  raise TypeError('expected bglib.model.board.board but got %s'%type(src))
      x.update(src._data)
    else:
      x.update(self.defaults)
    x.update(kw)
    self.__dict__["_data"] = x

  def __getattr__(self, name):
    return self._data[name]

  def __setattr__(self, name, value):
    if name not in self._data:
      raise AttributeError
    self._data[name]=value

  def has_chequer_to_move(self, n):
    if self.on_action == constants.you:
      to_move, to_hit = self.position
    elif self.on_action == constants.him:
      to_hit, to_move = self.position
    if to_move[constants.bar] == 0:
      return to_move[n]
    elif n == constants.bar:
      return to_move[n]
    return False

  def is_ok_to_bearoff_from(self, n, die):
    if n +1 < die:
      for i in range(n + 1, constants.bar + 1):
        if self.has_chequer_to_move(i):
          return False
      return True
    elif n+1 == die:
      for i in constants.none_bearoff_points:
        if self.has_chequer_to_move(i):
          return False
      if self.has_chequer_to_move(n):
        return True
      return False
    else:
      assert die < n +1
      return False

  def find_src_of_bearoff_with(self, die):
    for i in constants.none_bearoff_points:
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


  def is_open_to_land(self, n):
    if self.on_action == constants.you:
      to_move, to_hit = self.position
    elif self.on_action == constants.him:
      to_hit, to_move = self.position
    if n in constants.points:
      return to_hit[util.flip_point(n)] < 2
    else:
      assert n == -1
      return True

  def is_hitting_to_land(self, n):
    if self.on_action == constants.you:
      to_move, to_hit = self.position
    elif self.on_action == constants.him:
      to_hit, to_move = self.position
    if n in constants.points:
      return to_hit[util.flip_point(n)] == 1
    else:
      assert n == -1
      return False

  def make_partial_move(self, pm):
    if self.on_action == constants.you:
      to_move, to_hit = self.position
    elif self.on_action == constants.him:
      to_hit, to_move = self.position
    else:
      assert False
    to_move = list(to_move)
    to_hit = list(to_hit)
    if pm.src > constants.off:
      to_move[pm.src] -=1
    if pm.dest > constants.off:
      to_move[pm.dest] +=1
    if pm.is_hitting:
      if pm.is_undo():
        to_hit[util.flip_point(pm.src)] +=1
        to_hit[constants.bar] -= 1
      else:
        to_hit[util.flip_point(pm.dest)] -=1
        to_hit[constants.bar] += 1
    if self.on_action == constants.you:
      self.position = (tuple(to_move), tuple(to_hit))
    elif self.on_action == constants.him:
      self.position = (tuple(to_hit), tuple(to_move))
    else:
      assert False

  def make(self, mv):
    for pm in mv._pms:
      self.make_partial_move(pm)

  def is_leagal_to_roll(self, who):
    return \
       self.game_state == constants.on_going and \
       self.resign_offer == constants.resign_none and \
       self.doubled == False and \
       self.rolled == (0, 0) and \
       self.on_action == who and \
       self.on_inner_action == who

  def is_leagal_to_move(self, who):
    '''
    verify leagality of the situation.
    i.e. you cant move on opponent turn, etc.
    '''
    return \
       self.game_state == constants.on_going and \
       self.on_action == who and \
       self.on_inner_action == who and \
       self.resign_offer == constants.resign_none and \
       self.doubled == False and \
       self.rolled != (0, 0) # already rolled something.


  def is_cube_take_or_pass(self, who):
    return self.doubled and self.on_inner_action != self.on_action and \
      self.on_inner_action == who
  
  def double(self, who):
    assert self.is_leagal_to_double(who) 
    self.on_inner_action = constants.get_opp(who)
    self.doubled = True

  def has_rolled(self):
    if self.rolled == (0, 0):
      return False
    return True

  def is_leagal_to_double(self, who):
    assert self.rolled == (0, 0)
    assert self.game_state == constants.on_going
    your_score, his_score = self.score
    if self.game_state != constants.on_going:
      return False
    if self.crawford:
      return False
    if self.on_action == constants.you:
      if who != constants.you:
        return False
      if self.on_inner_action == constants.you:
        if self.match_length == constants.money_game:
          return True
        if your_score <= self.match_length - pow(2, self.cube_in_logarithm):
          return True
      return False
    elif self.on_action == constants.him:
      if who != constants.him:
        return False
      if self.on_inner_action == constants.him:
        if self.match_length == constants.money_game:
          return True
        if his_score < self.match_length - pow(2, self.cube_in_logarithm):
          return True
      return False
    assert False

  def is_leagal_to_redouble(self):
    return self.is_cube_take_or_pass() and False # is allowed to beaver?

  def redouble(self):
    pass
  def take(self):
    pass
  def drop(self):
    pass
  def is_leagal_to_resign(self, who):
    return self.on_action == who
  def offer_resign(self):
    pass
  def accept_resign(self):
    pass

  def is_to_accept_resign(self, who):

    return self.resign_offer in (constants.resign_single, 
                                 constants.resign_gammon,
                                 constants.resign_backgammon
                                 ) \
           and self.on_inner_action == who

