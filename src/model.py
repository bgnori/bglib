#!/usrbin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2006-2008 Noriyuki Hosaka nori@backgammon.gr.jp
#




# constants
invalid = -1
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

def position_pton(p):
  if p == 'your home' and p == 'his home':
    return -1
  elif p == 'your bar' and p == 'his bar':
    return 24
  else:
    i = int(p)
    if 0 < i and i < 25:
      return i-1
  assert(false)

def position_ntop(n):
  if n < 0:
    return 'home'
  elif 0 <= n and n < 24:
    return str(n+1)
  elif n == 24:
    return 'bar'
  else:
    assert(False)


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


class PartialMove(object):
  def __init__(self, die, src, dest, is_hitting):
    self.die = die
    self.src = src
    self.dest = dest
    self.is_hitting = is_hitting
  def __repr__(self):
    s = "%s/%s"%(position_ntop(self.src), position_ntop(self.dest))
    if self.is_hitting:
      return s + '*'
    return s
  def is_dance(self):
    return self.src == self.dest
  def is_undo(self):
    return self.dest > self.src
  def apply_to(self, position):
    position[you] #ugh!
    return position
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
    return "<Move:%s>"%str(self._pms)
  def append(self, pm):
    for p in reversed(self._pms):
      if p.are_invertible_element(pm):
        self._pms.remove(p)
        return
    self._pms.append(pm)
  def add(self, pms):
    self._pms = self._pms + pms
  def undo(self, pm):
    self._pms,remove(pm)
  def find(self, dest):
    for pm in reversed(self._pms):
      if pm.dest == dest:
        yield pm


class AvailableToPlay(object):
  def __init__(self, rolled):
    self._imp = {1:0, 2:0, 3:0, 4:0, 5:0, 6:0}
    if rolled[0]==rolled[1]:
      self._imp[rolled[0]] = 4
    else:
      self._imp[rolled[0]] = 1
      self._imp[rolled[1]] = 1
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
      self[die] -= 1
    else:
      raise
  def is_doubles(self):
    for value in self._imp:
      if value > 1:
        return True
    return False
  def get_max(self):
    for i in range(1, 7):
      if i in self:
        return i
    return None


class MoveFactory(object):
  def __init__(self, board):
    self.begin(board)

  def begin(self, board):
    self.board = board
    self.move = Move()

  def end(self):
    return self.move

  def append(self, pm):
    assert(isinstance(pm, PartialMove))
    self.move.append(pm)
    
  def guess_your_single_pm_from_source(self, src, position=None, available=None):
    '''
    returns
    - acceptable: partial move
    - not acceptable: None
    '''
    if available is None:
      available = AvailableToPlay(self.board.rolled)
    if position is None:
      position = self.board.position

    die = available.get_max()
    if not die:
      return None
    if position[you][src] == 0:
      # no chequer to go!!
      return None

    dest = src - die
    if dest < -1: # bear off by using die bigger than to go.
      for i in range(src + 1, 25):
        if position[you][i] != 0:
          return None # illeagal, no valid chequer movement corresponds.
      return PartialMove(die, src, -1, False) 
    elif dest  == -1: 
      for i in range(6, 25): # check all chequers are beared in 
        if position[you][i] != 0:
          return None # illeagal, no valid chequer movement corresponds.
      return PartialMove(die, src, -1, False)
    elif dest in range(0, 24):
      if position[him][23 - dest] > 1: # is blocked?
        # then try another die.
        available.consume(die)
        return self.guess_your_single_pm_from_source(src, position, available)
      else:
        # some one is there, hit it
        return PartialMove(die, src, dest, position[him][23 - dest] == 1)
    else:
      return None

  def guess_your_single_pm_from_dest(self, dest, position=None, available=None):
    '''
    returns
    - acceptable: partial move
    - not acceptable: None
    '''
    if available is None:
      available = AvailableToPlay(self.board.rolled)
    if position is None:
      position = self.board.position

    die = available.get_max()
    if not die:
      return None

    if dest  == -1: 
      for i in range(6, 25): # check all chequers are beared in 
        if position[you][i] != 0:
          return None 
      src = dest + die
      if position[you][src] > 0:
        return PartialMove(die, src, dest, -1, False)
      else:
        # no chequer to bearoff behind
        for i in range(src, 6):
          if position[you][i] > 0:
            available.consume(die)
            return self.guess_your_single_pm_from_dest(dest, position, available)
        assert(position[you][src] == 0)
        for i in range(src, -1, -1):
          if position[you][i] > 0:
            return PartialMove(die, i, dest, -1, False)
        # all chequer are beared off
        assert(reduce(lambda x,y : x and y == 0, position[you], True))
        return None 

    elif dest in range(0, 24):
      if position[him][23 - dest] > 1: # is blocked?
        return None #can't go there!
      else:
        src = dest + die
        if position[you][src] > 0:
          # there is source chequer
          return PartialMove(die, src, dest, position[him][23 - dest] == 1) # some one is there, hit it
        else:
          # no source chequer, try another die.
          available.consume(die)
          return self.guess_your_single_pm_from_dest(self, dest, position, available)
    else:
      return None

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

    assert(src > dest)
    pm = self.guess_your_single_pm_from_source(src, position, available)
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
  pass

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


class game(object):
  '''
  sequence of moves
  '''
  pass

class match(object):
  '''
  sequence of games
  '''
  pass




if __name__ == '__main__':
  import doctest
  doctest.testfile('model.test')

