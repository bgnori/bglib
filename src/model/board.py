#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2006-2008 Noriyuki Hosaka nori@backgammon.gr.jp
#


import constants

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
      if not isinstance(src, board):
        raise TypeError('expected bglib.model.board but got %s'%type(src))
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

  def make_partial_move(self, pm):
    if self.on_action == constants.you:
      to_move, to_hit = self.position
    elif self.on_action == constants.him:
      to_hit, to_move = self.position
    else:
      assert False
    assert not pm.is_undo()
    to_move = list(to_move)
    to_hit = list(to_hit)
    to_move[pm.src] -=1
    to_move[pm.dest] +=1
    if pm.is_hitting:
      to_hit[23 - pm.dest] -=1
      to_hit[25] += 1
    if self.on_action == constants.you:
      self.position = (tuple(to_move), tuple(to_hit))
    elif self.on_action == constants.him:
      self.position = (tuple(to_hit), tuple(to_move))
    else:
      assert False
  def make(self, mv):
    for pm in mv._pms:
      self.make_partial_move(pm)


if __name__ == '__main__':
  import doctest
  doctest.testfile('board.test')

