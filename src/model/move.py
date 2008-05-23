#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2006-2008 Noriyuki Hosaka nori@backgammon.gr.jp
#

import constants
import util
import board



class AvailableToPlay(object):
  def __init__(self, rolled=None, copy_src=None):
    assert rolled is not None or copy_src is not None
    if rolled is not None:
      assert isinstance(rolled, tuple)
      assert len(rolled) == 2
      self._imp = {1:0, 2:0, 3:0, 4:0, 5:0, 6:0}
      if rolled[0]==rolled[1]:
        self._imp[rolled[0]] = 4
      else:
        self._imp[rolled[0]] = 1
        self._imp[rolled[1]] = 1
    if copy_src is not None:
      # copy constructor
      assert isinstance(copy_src, AvailableToPlay)
      self._imp = dict(copy_src._imp)

  def __getitem__(self, key):
    assert(key in [1, 2, 3, 4, 5, 6])
    return self._imp[key]
  def __contains__(self, key):
    assert(key in [1, 2, 3, 4, 5, 6])
    return self._imp[key] > 0
  def __setitem__(self, key, value):
    assert(key in [1, 2, 3, 4, 5, 6])
    self._imp[key] = value
  def consume(self, die):
    if die in self:
      assert self[die] > 0
      self[die] -= 1
    else:
      raise
  def items(self):
    return self._imp.items()
  def is_doubles(self):
    for value in self._imp:
      if value > 1:
        return True
    return False
  def get_max(self):
    for i in range(6, 0, -1):
      if i in self:
        return i
    return None
  def __repr__(self):
    return '<AvailableToPlay: ' + str(self.items()) + '>'
  __str__ = __repr__

class PartialMove(object):
  def __init__(self, die, src, dest, is_hitting):
    self.die = die
    self.src = src
    self.dest = dest
    self.is_hitting = is_hitting
  def __repr__(self):
    s = "%s/%s"%(util.move_ntop(self.src), util.move_ntop(self.dest))
    if self.is_hitting:
      s += '*'
    return "<PartialMove: " + s + ">"
  def is_dance(self):
    return self.src == self.dest
  def is_undo(self):
    return self.dest > self.src
  def are_invertible_element(self, pm):
    assert(isinstance(pm, PartialMove))
    return ( self.die == pm.die 
             and
             self.src == pm.dest 
             and 
             self.dest == pm.src
             and
             self.is_hitting == pm.is_hitting
           )


class Move(object):
  def __init__(self):
    self._pms = list()
  def __repr__(self):
    return "<Move: %s>"%str(self._pms)
  def append(self, pm):
    for p in reversed(self._pms):
      if p.are_invertible_element(pm):
        self._pms.remove(p)
        return
    self._pms.append(pm)
  def find(self, dest):
    for pm in reversed(self._pms):
      if pm.dest == dest:
        yield pm


class MoveFactory(object):
  def __init__(self, b):
    #if not isinstance(b, board):
    #  raise TypeError('expected bglib.model.board.board but got %s'%type(b))
    self.board = b
    self.move = Move()
    self.available = AvailableToPlay(self.board.rolled)

  def append(self, pm):
    assert(isinstance(pm, PartialMove))
    self.move.append(pm)
    self.available.consume(pm.die)
    self.board.make_partial_move(pm)
    
  def guess_your_single_pm_from_source(self, src, b=None, available=None):
    '''
    returns
    - acceptable: partial move
    - not acceptable: None
    '''
    assert isinstance(src, int)

    if available is None:
      available = AvailableToPlay(rolled=None, copy_src=self.available)
    assert isinstance(available, AvailableToPlay)
    if b is None:
      b = board.board(src=self.board)
    #assert isinstance(b, board.board)

    die = available.get_max()
    if not die:
      return None
    if not b.has_chequer_to_move(src):
      return None

    dest = src - die
    if dest <= constants.off:
      if b.is_ok_to_bearoff_from(src):
        return None # illeagal, no valid chequer movement corresponds.
      return PartialMove(die, src, constants.off, False) 
    elif dest in constants.points:
      if b.is_open_to_land(dest):
        # some one is there, hit it
        return PartialMove(die, src, dest, b.is_hitting_to_land(dest))
      else:
        # then try another die.
        available.consume(die)
        return self.guess_your_single_pm_from_source(src, b, available)
    else:
      return None

  def guess_your_single_pm_from_dest(self, dest, b=None, available=None):
    '''
    returns
    - acceptable: partial move
    - not acceptable: None
    '''
    assert isinstance(dest, int)

    if available is None:
      available = AvailableToPlay(rolled=None, copy_src=self.available)
    assert isinstance(available, AvailableToPlay)
    if b is None:
      b = board.board(src=self.board)

    die = available.get_max()
    if not die:
      return None

    if dest  == -1: 
      src = b.find_src_of_bearoff_with(die)
      if src is not None: # src== 0 is valid,as ace point
        return PartialMove(die, src, dest, -1, False)
      else:
        available.consume(die)
        return self.guess_your_single_pm_from_dest(dest, b, available)
    elif dest in constants.points:
      if b.is_open_to_land(dest):
        if b.has_chequer_to_move(dest + die):
          return PartialMove(die, dest+die, dest, b.is_hitting_to_land(dest))
        else:
          # no source chequer, try another die.
          available.consume(die)
          return self.guess_your_single_pm_from_dest(dest, b, available)
      else:
        return None #can't go there!
    else:
      assert False

  def guess_your_multiple_partial_moves(self, src, dest, position=None, available=None, pms=None):
    '''
    returns
    - accepted: list of partial move
    - not acceptable: None
    '''
    if available is None:
      available = AvailableToPlay(self.board.rolled)
    if position is None:
      position = self.board.position
    if pms is None:
      pms = []

    if not isinstance(position, tuple):
      raise TypeError('expected tuple but got %s'%str(type(position)))
    assert isinstance(available, AvailableToPlay)

    assert(src > dest)
    pm = self.guess_your_single_pm_from_source(src, position=position, available=available)
    if pm is None:
      return pm
    print pm

    if pm.dest == dest:
      pms.append(pm)
      return pms
    elif pm.dest > dest:
      available.consume(pm.die)
      pms.append(pm)
      return self.guess_your_multiple_partial_moves(pm.dest, dest, 
                    pm.apply_to(position), available, pms)
    else:
      assert(pm,dest < dest)
      return None

  def guess_your_multiple_partial_undoes(self, src, dest, position=None, pms=None):
    assert(src < dest)
    if position is None:
      position = self.board.position
    if pms is None:
      pms = []
    for pm in self.move.find(src):
      inverse = PartialMove(die=pm.die, src=pm.dest, dest=pm.src, is_hitting=pm.is_hitting)
      if inverse is None:
        return None
      pms.append(inverse)
      if pm.src == dest:
        return pms
      elif pm.src < dest:
        pms.append(pm)
        return self.guess_your_multiple_partial_undoes(self, pm.src, dest, inverse.apply_to(position), pms=pms)
      else:
        assert(pm.src > dest)
        return None
    return None

  def guess_your_making_point(self, dest, position=None, available=None, pms=None):
    if available is None:
      available = AvailableToPlay(self.board.rolled)
    if position is None:
      position = self.board.position
    if pms is None:
      pms = []

    pm = self.guess_your_single_pm_from_dest(dest)
    if pm:
      pms.append(pm)
      available = available.consume(pm)
      pm = self.guess_your_single_pm_from_dest(dest, position=pm.apply_to(position), available=available)
      if pm:
        pms.append(pm)
        return pms
    return None


class ViewerInputHelperMixin(object):
  # dice / roll related actions
  def roll(self):
    '''
    need to send command to server.
    '''
  def is_leagal_to_roll(self):
    return \
       self.game_state == bglib.model.on_going and \
       self.on_action == bglib.model.you and \
       self.on_inner_action == bglib.model.you and \
       self.resign_offer == bglib.model.resign_none and \
       self.doubled == False and \
       self.rolled == (0, 0) # already rolled nothing.

  def is_leagal_to_move(self):
    '''
    verify leagality of the situation.
    i.e. you cant move on opponent turn, etc.
    '''
    return \
       self.game_state == bglib.model.on_going and \
       self.on_action == bglib.model.you and \
       self.on_inner_action == bglib.model.you and \
       self.resign_offer == bglib.model.resign_none and \
       self.doubled == False and \
       self.rolled != (0, 0) # already rolled something.

  def is_leagal_partial_move(self):
    '''
    verify leagality of the move.
    '''
    pass

  def is_leagal_move(self, src, dst):
    '''
    verify leagality of the move.
    '''
    pass



class PlayInputHelperMixin(object):
  def guess_input(self):pass

  def put_chequier_movement(self):
    pass
  def pickup_dice(self):
    pass

  def make_move(self):
    '''
    generates board with position according to move, even it is illeagal.
    '''
    return board()

  # cube related actions
  def is_leagal_to_double(self):
    return not self.crawford and self.is_leagal_to_roll() 

  def double(self):pass

  def is_cube_take_or_pass(self):
    return self.doubled and self.on_inner_action == bglib.model.you

  def is_leagal_to_redouble(self):
    return self.is_cube_take_or_pass() and False # is allowed to beaver?

  def redouble(self):pass
  def take(self):pass
  def drop(self):pass

  def is_leagal_to_resign(self):
    return self.on_action == bglib.model.you
  def offer_resign(self):pass
  def is_to_accept_resign(self):
    #  and self.on_inner_action == bglib.model.you
    return self.resign_offer in (bglib.model.resign_single, 
                                 bglib.model.resign_gammon,
                                 bglib.model.resign_backgammon
                                 ) 
  def accept_resign(self):pass

  def who_to_play(self):
    pass


if __name__ == '__main__':
  import doctest
  doctest.testfile('move.test')

