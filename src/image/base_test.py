#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2006-2008 Noriyuki Hosaka nori@backgammon.gr.jp
#

import unittest
import nose
import urllib

from bglib.image.base import Element
from bglib.image.base import BaseElement

class BaseTest(unittest.TestCase):
  def setUp(self):
    self.board = Element('board')
    self.match = Element('match')
    self.action = Element('action')
    self.length = Element('length')
    self.crawford = Element('crawford')
    self.score = Element('score')
    self.position = Element('position')
    self.cubeholder = Element('cubeholder')
    self.field = Element('field')
    self.die = Element('die')
    self.cube = Element('cube')
    self.chip = Element('chip')
    self.home = Element('home')
    self.chequer = Element('chequer')
    self.bar = Element('bar')
    self.point = Element('point')

  def tearDown(self):
    pass

  def _append(self, name, oks):
    e = self.__dict__[name]
    if 'str' in oks:
      try:
        e.append('str')
      except:
        self.assert_(False)
    else:
      try:
        e.append('str')
        self.assert_(False)
      except:
        self.assert_(True)
    for key, item in self.__dict__.items():
      if isinstance(item, BaseElement):
        if key in oks:
          try:
            e.append(item)
          except:
            self.assert_(False)
        else:
          try:
            e.append(item)
            self.assert_(False)
          except:
            self.assert_(True)

  def board_test(self):
    self._append('board', ['match', 'position'])

  def match_test(self):
    self._append('match', ['action', 'length', 'crawford', 'score'])

  def action_test(self):
    self._append('action', [])

  def length_test(self):
    self._append('length', [])

  def crawford_test(self):
    self._append('crawford', [])

  def score_test(self):
    self._append('score', [])

  def position_test(self):
    self._append('position', ['cubeholder', 'field', 'home', 'bar', 'point'])

  def cubeholder_test(self):
    self._append('cubeholder', ['cube'])

  def cube_test(self):
    self._append('cube', [])

  def field_test(self):
    self._append('field', ['cube', 'die', 'chip'])

  def home_test(self):
    self._append('home', ['cube', 'chequer'])

  def chequer_test(self):
    self._append('chequer', ['str'])

  def bar_test(self):
    self._append('bar', ['chequer'])

  def point_test(self):
    self._append('point', ['chequer'])

  def dtd_test(self):
    url = Element.dtd_url()
    try:
      obj = urllib.urlopen(url)
    except:
      self.assert_(False, 'failed to obtain dtd.')
      return
    self.assertEqual(obj.read(), Element.make_dtd(), 'dtd mismatch')



