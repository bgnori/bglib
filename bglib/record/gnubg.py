#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2006-2008 Noriyuki Hosaka nori@backgammon.gr.jp
#

from bglib.model import *
from bglib.model.constants import *
import bglib.encoding
from bglib.encoding.gnubgid import decode, encode


class Tracer(object):
  def __init__(self, gnubgid=None, board=None):
    if board is not None:
      assert isinstance(board, Board)
      self.board = BoardEditor(board)
    elif gnubgid is not None:
      self.board = BoardEditor()
      pid, mid = gnubgid.split(':')
      decode(self.board, pid, mid)
    else:
      self.board = BoardEditor()
    self.action = None

  def set_action(self, d):
    assert self.action is None
    assert isinstance(d, dict)
    assert d.has_key('action')
    assert d['action'] in ['resign', 'move', 'take', 'drop', 'double']
    assert d.has_key('player')
    assert d.has_key('board')
    if d['player'] == 'X':
      assert self.board.on_action == YOU
    elif d['player'] == 'O':
      assert self.board.on_action == HIM
    else:
      assert False

  def on_roll_or_double(self):
    assert self.action

  def on_offering_double(self):
    assert self.action
    pass

  def on_take_or_pass(self):
    assert self.action
    pass

  def on_move(self):
    assert self.action
    b = self.board.freeze()
    return b

  def on_pickup_dice(self):
    assert self.action
    b = self.board.freeze()
    d = bglib.model.board.board(self.board)
    assert d
    action = d.action
    if action == 'resign':
      pass
    elif action == 'move':
      self.board.rolled = d['dice']
    elif action == 'take':
      pass
    elif action == 'drop':
      pass
    elif action == 'double':
      pass
    else:
      assert False
    #self.board.make(mv
    return self.board

  def pickup_dice(self):
    assert self.action
    self.board = self.get_on_done()

