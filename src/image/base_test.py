#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2006-2008 Noriyuki Hosaka nori@backgammon.gr.jp
#
import os
import os.path

import StringIO

import urllib
from urllib2 import urlopen

import unittest

import nose
import ClientForm

import bglib.model.board

from bglib.image.base import Element
from bglib.image.base import BaseElement
from bglib.image.base import IntAttribute
from bglib.image.base import StringAttribute
from bglib.image.base import ColorAttribute
from bglib.image.base import URIAttribute
from bglib.image.base import FlipAttribute
from bglib.image.base import ParityAttribute

from bglib.image.base import  ElementTree


class ElementTest(unittest.TestCase):
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


class AttributeTest(unittest.TestCase):
  def hasattr_x_test(self):
    base = BaseElement()
    try:
      base.x
      self.assert_(False)
    except ValueError:
      return 
    self.assert_(False)

  def hasattr_y_test(self):
    base = BaseElement()
    try:
      base.y
      self.assert_(False)
    except ValueError:
      return
    self.assert_(False)

  def hasattr_width_test(self):
    base = BaseElement()
    try:
      base.width
      self.assert_(False)
    except ValueError:
      return
    self.assert_(False)

  def hasattr_height_test(self):
    base = BaseElement()
    try:
      base.height
      self.assert_(False)
    except ValueError:
      return
    self.assert_(False)

  def hasattr_image_test(self):
    base = BaseElement()
    try:
      base.image
      self.assert_(False)
    except ValueError:
      return
    self.assert_(False)

  def hasattr_flip_test(self):
    base = BaseElement()
    try:
      base.flip
      self.assert_(False)
    except ValueError:
      return
    self.assert_(False)

  def hasattr_background_test(self):
    base = BaseElement()
    try:
      base.background
      self.assert_(False)
    except ValueError:
      return

  def hasattr_color_test(self):
    base = BaseElement()
    try:
      base.color
      self.assert_(False)
    except ValueError:
      return
    self.assert_(False)

  def hasattr_font_test(self):
    base = BaseElement()
    try:
      base.font
      self.assert_(False)
    except ValueError:
      return
    self.assert_(False)

  def attr_inherit_test(self):
    parent = BaseElement()
    child = BaseElement()
    parent.append(child)
    parent.x = 10
    self.assertEqual(child.x, 10)

  def attr_string_test(self):
    base = BaseElement()
    base.image = 'hoge'
    self.assertEqual(base.image, 'hoge')

  def attr_int_test(self):
    base = BaseElement()
    base.x = 10
    self.assertEqual(base.x, 10)
    try:
      base.x = 'hoge'
      self.assert_(False)
    except TypeError:
      return
    self.assert_(False)

  def attr_uri_test(self):
    base = BaseElement()
    base.image = './bglib/image/base_test.py'
    self.assert_(os.path.exists(base.image))

  def attr_flip_test(self):
    base = BaseElement()
    base.flip = True

  def attr_parity_test(self):
    point= Element('point')
    point.parity= 'even'

  def attr_player_test(self):
    home = Element('home')
    home.player = 'you'
    home.player = 'him'
    try:
      home.player = 'hoge'
      self.assert_(False)
    except TypeError:
      return
    self.assert_(False)

  def facotry_test(self):
    score = Element('score', player='you')
    self.assertEqual(score.player, 'you')

class TreeTest(unittest.TestCase):
  def setUp(self):
    self.buf = StringIO.StringIO()
    self.tree = ElementTree()
  def dtd_test(self):
    url = Element.dtd_url()
    try:
      obj = urllib.urlopen(url)
    except:
      self.assert_(False, 'failed to obtain dtd.')
      return
    self.assertEqual(obj.read(), Element.make_dtd(), 'dtd mismatch')

  def validity_test(self):
    res = urlopen('http://validator.w3.org/#validate_by_upload')
    forms = ClientForm.ParseResponse(res, backwards_compat=False)
    form = forms[1]

    self.tree.set(bglib.model.board.board())
    self.buf.write(self.tree.xml())
    self.buf.flush()
    self.buf.seek(0)

    form.add_file(self.buf, 
                  content_type='text/xml; charset=us-ascii',
                  name='uploaded_file', filename='test.xml')
    req = form.click()
    res = urlopen(req)
    self.assertEqual(res.info()['X-W3C-Validator-Status'], 'Valid')
    self.assertEqual(res.info()['X-W3C-Validator-Errors'], '0')



