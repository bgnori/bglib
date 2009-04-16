#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2006-2009 Noriyuki Hosaka bgnori@gmail.com
#

from bglib.model import *
from bglib.model.constants import *
import util

from bglib.model.board import AbstractBoard

class BoardEditor(AbstractBoard):
  def __init__(self, b=None, **kw):
    if isinstance(b, Board):
      d = dict(AbstractBoard.defaults)
      for key in AbstractBoard.defaults:
        d.update({key: getattr(b, key)})
    elif isinstance(b, BoardEditor):
      d = dict(b._d)
    elif b is None:
      d = dict(AbstractBoard.defaults)
    else:
      assert False
    for key in AbstractBoard.defaults:
      v = kw.get(key, None)
      if v is not None:
        d.update({key: v})
    self.__dict__['_d'] = d

  def __getattr__(self, name):
    return self.__dict__['_d'].get(name)

  def __setattr__(self, name, value):
    print '%s:%s'%(name, value)
    self.__dict__['_d'][name] = value

  def freeze(self):
    return Board(self._d)

  def flip(self):
    if self.cube_owner == YOU:
      self.cube_owner = HIM
    elif self.cube_owner == HIM:
      self.cube_owner = YOU
    else:
      assert self.cube_owner == CENTER

    self.score = (self.score[1], self.score[0])
    self.position = (self.position[1], self.position[0])

    if self.on_inner_action == YOU:
      self.on_inner_action = HIM
    elif self.on_inner_action == HIM:
      self.on_inner_action = YOU
    else:
      assert self.on_inner_action == CENTER

    if self.on_action == YOU:
      self.on_action = HIM
    elif self.on_action == HIM:
      self.on_action = YOU
    else:
      assert self.on_action == CENTER

  def make_partial_move(self, pm):
    if self.on_action == YOU:
      to_move, to_hit = self.position
    elif self.on_action == HIM:
      to_hit, to_move = self.position
    else:
      assert False
    to_move = list(to_move)
    to_hit = list(to_hit)
    if pm.src > OFF:
      to_move[pm.src] -=1
    if pm.dest > OFF:
      to_move[pm.dest] +=1
    if pm.is_hitting:
      if pm.is_undo():
        to_hit[util.flip_point(pm.src)] +=1
        to_hit[BAR] -= 1
      else:
        to_hit[util.flip_point(pm.dest)] -=1
        to_hit[BAR] += 1
    if self.on_action == YOU:
      self.position = (tuple(to_move), tuple(to_hit))
    elif self.on_action == HIM:
      self.position = (tuple(to_hit), tuple(to_move))
    else:
      assert False

  def make(self, mv):
    for pm in mv._pms:
      self.make_partial_move(pm)

  def double(self, who):
    assert self.is_leagal_to_double(who) 
    self.on_inner_action = util.get_opp(who)
    self.doubled = True

  def redouble(self):
    pass

  def take(self, who):
    assert self.is_cube_take_or_pass(who)
    self.on_inner_action = self.on_action
    #self.doubled = False

  def drop(self, who):
    assert self.is_cube_take_or_pass(who)
    new = [0, 0]
    self.game_state = DOUBLED_OUT
    new[who] = self.score[who]
    new[util.get_opp(who)] = self.score[util.get_opp(who)] + pow(2, self.cube_in_logarithm)
    self.score = tuple(new)

  def offer_resign(self, who, how_much):
    assert self.is_leagal_to_resign(who)
    assert how_much in (RESIGN_SINGLE, 
                                 RESIGN_GAMMON,
                                 RESIGN_BACKGAMMON
                                 )
    self.resign_offer = how_much
    self.on_inner_action = util.get_opp(who)

  def accept_resign(self, who):
    assert self.is_to_accept_resign(who)
    new = [0, 0]
    self.game_state = RESIGNED
    new[who] = self.score[who] + self.resign_offer * pow(2, self.cube_in_logarithm)
    new[util.get_opp(who)] = self.score[util.get_opp(who)]
    self.score = tuple(new)

  def reject_resign(self, who):
    assert self.is_to_accept_resign(who)
    self.on_inner_action = util.get_opp(who)
    self.resign_offer = RESIGN_NONE




