#!/usrbin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2006-2008 Noriyuki Hosaka nori@backgammon.gr.jp
#




# constants
you = 0
him = 1
center = 2

#game state
not_started = 0
on_going = 1
finished = 2
resigned = 3

#resing type
resign_none = 0
resign_single=1
resign_gammon=2
resign_backgammon=3

initial_position = ((0, 0, 0, 0, 0, 5, 0, 3, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0), (0, 0, 0, 0, 0, 5, 0, 3, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0))


class board(object):
  defaults = dict(
                  position=initial_position,
                  cube_value=0,
                  cube_owner=center,
                  on_action=you,
                  crawford=False,
                  game_state=not_started,
                  on_inner_action=you,
                  doubled=False,
                  resign_offer=resign_none,
                  rolled=(0, 0),
                  match_length=0,
                  score=(0, 0),
                  )

  def __init__(self, **kw):
    x = dict()
    for key in self.defaults:
      if key in kw:
        x.update({key:kw[key]})
        del kw[key]
      else:
        x.update({key:self.defaults[key]})
    if kw:
      raise
    self.__dict__["_data"] = x

  def __getattr__(self, name):
    return self._data[name]

  def __setattr__(self, name, value):
    if name not in self._data:
      raise AttributeError
    self._data[name]=value





if __name__ == '__main__':
  import doctest
  doctest.testfile('model.test')

