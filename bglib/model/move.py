#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2006-2008 Noriyuki Hosaka nori@backgammon.gr.jp
#

from bglib.model.constants import *
from bglib.model import util
from bglib.model import *


class AvailableToPlay(object):
  def __init__(self, rolled=None, copy_src=None):
    assert rolled is not None or copy_src is not None
    if rolled is not None:
      assert isinstance(rolled, tuple)
      assert len(rolled) == 2
      self._imp = {1:0, 2:0, 3:0, 4:0, 5:0, 6:0}
      if rolled[0] == 0:
        pass
      elif rolled[0]==rolled[1]:
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

  def __len__(self):
    count = 0
    for v in self._imp.values():
      count += v
    return count

  def consume(self, die):
    if die in self:
      assert self[die] > 0
      self[die] -= 1
    else:
      raise

  def add(self, die):
    assert(die in [1, 2, 3, 4, 5, 6])
    self._imp[die] += 1

  def items(self):
    return self._imp.items()

  def is_doubles(self):
    for value in self._imp.values():
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

  def __str__(self):
    s = 'Available to play:'
    for die, count in self.items():
      for i in range(count):
        s +='%i, '%die
    return s


class PartialMove(object):
  def __init__(self, die, src, dest, is_hitting):
    self.die = die
    self.src = src
    self.dest = dest
    self.is_hitting = is_hitting
  def __repr__(self):
    return "<PartialMove: " + str(self) + ">"
  def __str__(self):
    s = "%s/%s"%(util.move_ntop(self.src), util.move_ntop(self.dest))
    if self.is_hitting:
      s += '*'
    return s
    
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
  def __init__(self, src=None):
    if src is None:
      self._pms = list()
    else:
      assert isinstance(src, Move)
      self._pms = list(src._pms)

  def __repr__(self):
    return "<Move: %s>"%str(self._pms)

  def __str__(self):
    s = ''
    for pm in self:
      s += '%s, '%str(pm)
    return s

  def append(self, pm):
    assert isinstance(pm, PartialMove)
    for p in reversed(self._pms):
      if p.are_invertible_element(pm):
        self._pms.remove(p)
        return
    self._pms.append(pm)

  def add(self, mv):
    assert isinstance(mv, Move)
    for pm in mv._pms:
      self.append(pm)

  def find(self, dest):
    for pm in reversed(self._pms):
      if pm.dest == dest:
        yield pm

  def __iter__(self):
    for pm in self._pms:
      yield pm

  def __len__(self):
    return len(self._pms)

class MoveFactory(object):
  class Error(object):
    def __init__(self, s):
      self.s = s
    def __nonzero__(self):
      return False
    def __repr__(self):
      return "<MoveFactory.Error: %s>"%self.s
    __str__ = __repr__

  def __init__(self, b, move=None, available=None):
    #if not isinstance(b, board):
    #  raise TypeError('expected bglib.model.board.board but got %s'%type(b))
    self.board = b
    if move:
      assert isinstance(move, Move)
      self.move = Move(src=move)
    else:
      self.move = Move()
    if available:
      self.available = AvailableToPlay(copy_src=available)
    else:
      self.available = AvailableToPlay(self.board.rolled)

  def append(self, pm):
    assert(isinstance(pm, PartialMove))
    self.move.append(pm)
    if pm.is_undo():
      self.available.add(pm.die)
    else:
      self.available.consume(pm.die)
    self.board.make_partial_move(pm)

  def add(self, mv):
    for pm in mv:
      self.append(pm)
    
  def is_leagal_to_pickup_dice(self):
    assert self.board.rolled != (0, 0)
    if not self.available:
      return True
    bar = util.move_pton('bar')
    if self.board.has_chequer_to_move(bar):
      if not self.guess_your_single_pm_from_source(bar):
        return True #dance
    for pt in POINTS:
      if self.board.has_chequer_to_move(pt):
        if self.guess_your_single_pm_from_source(pt):
          return False
    #rewind all moves and check for blocked moves.
    mf = MoveFactory(self.board, self.move, self.available)
    for pm in mf.move:
      inverse = PartialMove(die=pm.die, src=pm.dest, dest=pm.src, is_hitting=pm.is_hitting)
      mf.append(inverse)
    assert len(mf.move) == 0

    # No need to check doubles.
    # care only about small-big use.
    # thus ...
    for src in POINTS:
      if mf.board.has_chequer_to_move(src):
        for dst in range(0, src):
          if mf.board.is_open_to_land(dst) or mf.board.is_hitting_to_land(dst):
            pms = mf.guess_your_multiple_pms(src, dst)
            if pms and len(pms) == 2:
              # all dice are used.
              # that means there is way to use all dice.
              return False
    # There is no way to use both dice
    # Make sure use big one
    # thus ... 
    if self.available.get_max() != mf.available.get_max():
      return True #max is used.

    die = mf.available.get_max()
    for src in POINTS:
      if mf.board.has_chequer_to_move(src):
        pm = mf.guess_your_single_pm_from_source(src, available=AvailableToPlay(rolled=(die, 0)))
        if pm:
          return False # There is way to use big one.
    return True

  def guess_your_single_pm_from_source(self, src, b=None, available=None):
    '''
    returns
    - acceptable: partial move
    - not acceptable: None
    '''
    assert isinstance(src, int)

    if b is None:
      b = self.board
    if available is None:
      available = AvailableToPlay(rolled=None, copy_src=self.available)
    assert isinstance(available, AvailableToPlay)

    die = available.get_max()
    if die is None:
      return self.Error('No die is available')
    if not b.has_chequer_to_move(src):
      return self.Error('No chequer to move')

    dest = src - die
    if dest < 0: #= constants.off:
      if not b.is_ok_to_bearoff_from(src, die):
        return self.Error('Not allowed to bear off from %i'%src)
      return PartialMove(die, src, OFF, False) 
    elif dest in POINTS:
      if b.is_open_to_land(dest):
        # some one is there, hit it
        return PartialMove(die, src, dest, b.is_hitting_to_land(dest))
      else:
        # then try another die.
        available = AvailableToPlay(rolled=None, copy_src=available)
        available.consume(die)
        return self.guess_your_single_pm_from_source(src, b, available)
    else:
      return self.Error('bad destination: %i'%dest)
    assert False

  def guess_your_single_pm_from_dest(self, dest, b=None, available=None):
    '''
    returns
    - acceptable: partial move
    - not acceptable: None
    '''
    assert isinstance(dest, int)

    if b is None:
      b = self.board
    #assert isinstance(b, board.board)
    if available is None:
      available = AvailableToPlay(rolled=None, copy_src=self.available)
    assert isinstance(available, AvailableToPlay)

    die = available.get_max()
    if not die:
      return self.Error('No die is available')

    if dest  == -1: 
      src = b.find_src_of_bearoff_with(die)
      if src is not None: # src== 0 is valid,as ace point
        return PartialMove(die, src, dest, False)
      else:
        available.consume(die)
        return self.guess_your_single_pm_from_dest(dest, b, available)
    elif dest in POINTS:
      if b.is_open_to_land(dest):
        if b.has_chequer_to_move(dest + die):
          return PartialMove(die, dest+die, dest, b.is_hitting_to_land(dest))
        else:
          # no source chequer, try another die.
          available = AvailableToPlay(rolled=None, copy_src=available)
          available.consume(die)
          return self.guess_your_single_pm_from_dest(dest, b, available)
      else:
        return self.Error("Can't land there")
    else:
      assert False

  def guess_your_multiple_pms(self, src, dest, b=None, available=None, mv=None):
    '''
    returns
    - accepted: list of partial move
    - not acceptable: None
    '''

    if b is None:
      b = self.board
    if available is None:
      available = AvailableToPlay(rolled=None, copy_src=self.available)
    if mv is None:
      mv = Move()

    assert isinstance(src, int)
    assert isinstance(dest, int)
    assert(src > dest)
    #if not isinstance(b, board):
    #  raise TypeError('expected bglib.model.board.board but got %s'%type(b))
    assert isinstance(available, AvailableToPlay)
    assert isinstance(mv, Move)

    pm = self.guess_your_single_pm_from_source(src, b, available)
    if not pm :
      return pm 

    assert pm.src == src
    if pm.dest == dest:
      mv.append(pm)
      return mv
    elif pm.dest > dest:
      # need to go further
      mv.append(pm)
      available.consume(pm.die)
      b.make_partial_move(pm)
      return self.guess_your_multiple_pms(pm.dest, dest, b, available, mv)
    else:
      # over run
      assert pm,dest < dest
      available.consume(pm.die)
      # retry with other die
      return self.guess_your_multiple_pms(src, dest, b, available, mv)
    assert False

  def guess_your_multiple_partial_undoes(self, src, dest, b=None, available=None, mv=None):
    if b is None:
      b = self.board
    if available is None:
      available = AvailableToPlay(rolled=None, copy_src=self.available)
    if mv is None:
      mv = Move()

    assert isinstance(src, int)
    assert isinstance(dest, int)
    assert(src < dest)

    for pm in self.move.find(src):
      inverse = PartialMove(die=pm.die, src=pm.dest, dest=pm.src, is_hitting=pm.is_hitting)
      mv.append(inverse)
      if inverse.dest == dest:
        return mv
      elif inverse.dest < dest:
        b.make_partial_move(inverse)
        available.add(inverse.die)
        return self.guess_your_multiple_partial_undoes(inverse.dest, dest, b, available, mv)
      else:
        assert(inverse.dest > dest)
        return self.Error('Overrun, bad (src, dest)=(%i, %i)'%(src, dest))
    return self.Error('Overrun, bad (src, dest)=(%i, %i)'%(src, dest))

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


if __name__ == '__main__':
  import doctest
  doctest.testfile('move.test')

