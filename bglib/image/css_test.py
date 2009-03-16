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
import bglib.image.css

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
    self.resign = Element('resign')
    self.home = Element('home')
    self.chequer = Element('chequer')
    self.bar = Element('bar')
    self.point = Element('point')

  def tearDown(self):
    pass

  def selector_1_test(self):
    s = bglib.image.css.Selector('point')
    self.assertEqual(str(s), "<point></point>")

  def selector_2_test(self):
    s = bglib.image.css.Selector('point', 'x', '42')
    self.assertEqual(str(s), '''<point x="42"></point>''')

  def selector_3_test(self):
    s = bglib.image.css.Selector('point', 'x', '42', "2")
    self.assertEqual(str(s), '''<point x="42">2</point>''')

  def selector_4_test(self):
    s = bglib.image.css.Selector('point', 'x', '42', "2")
    self.assertEqual(str(s), '''<point x="42">2</point>''')

  def selector_match_test(self):
    s = bglib.image.css.Selector('point', 'x', '42', "2")
    self.assertEqual(str(s), '''<point x="42">2</point>''')
    e = bglib.image.base.Element('point', x=42)
    e.append("2")
    self.assertEqual(repr(e.x), '''42''')
    self.assert_(s.is_match(e))

  def selector_mismatch_attr_test(self):
    s = bglib.image.css.Selector('point', 'x', '42', "2")
    e = bglib.image.base.Element('point', x=43)
    e.append("2")
    self.assertFalse(s.is_match(e))

  def selector_mismatch_elem_test(self):
    s = bglib.image.css.Selector('point', 'x', '42', "2")
    e = bglib.image.base.Element('die', x=42)
    e.append("2")
    self.assertFalse(s.is_match(e))


  def selector_mismatch_child_1_test(self):
    s = bglib.image.css.Selector('point', 'x', '42', "2")
    e = bglib.image.base.Element('point', x=42)
    self.assertFalse(s.is_match(e))

  def selector_mismatch_child_2_test(self):
    s = bglib.image.css.Selector('point', 'x', '42', "2")
    e = bglib.image.base.Element('point', x=42)
    e.append("3")
    self.assertFalse(s.is_match(e))

  def selector_match_extra_attr_test(self):
    s = bglib.image.css.Selector('point', 'x', '42', "2")
    e = bglib.image.base.Element('point', x=42, y=22)
    e.append("2")
    self.assert_(s.is_match(e))

  def Rule_test(self):
    s = bglib.image.css.Selector('point', 'x', '42', "2")
    r = bglib.image.css.Rule('~/defaule.css', 0)
    self.assertEqual(r.lineno, 0)
    r.add(s)
    self.assertEqual(repr(r), '''in line: 0
pattern: <point x="42">2</point>
block: {}''')

    r.update({'image': 'uri("board.jpg")'})
    self.assertEqual(repr(r), '''in line: 0
pattern: <point x="42">2</point>
block: {'image': 'uri("board.jpg")'}''')

    r.update({'image': 'uri("backgammon.jpg")'})
    self.assertEqual(repr(r), '''in line: 0
pattern: <point x="42">2</point>
block: {'image': 'uri("backgammon.jpg")'}''')

  def selector_and_element_test(self):
    s = bglib.image.css.Selector('point', 'x', '42', "2")
    r = bglib.image.css.Rule('~/defaule.css', 0)
    r.add(s)
    r.update({'image': 'uri("backgammon.jpg")'})
    s = bglib.image.css.Selector('point', 'x', '42', "2")
    e = bglib.image.base.Element('point', x=42)
    self.assertEqual(repr(e), '''<point x="42"></point>''')

    e = bglib.image.base.Element('point', x=42)
    e.append("2")
    self.assertEqual(repr(e), '''<point x="42">2</point>''')

    self.assert_(s.is_match(e))
    self.assert_(r.is_match([e]))

    r.apply([e])
    self.assertEqual(repr(e), '''<point x="42" image="~/backgammon.jpg">2</point>''')

    e = bglib.image.base.Element('point',  x=42)
    self.assertEqual(repr(e), '''<point x="42"></point>''')
    r.apply([e])
    self.assertEqual(repr(e), '''<point x="42"></point>''')

  def parser_test(self):
    parser = bglib.image.css.CSSParser()
    r = parser.rule('~/defaule.css', 0, """point:data(1) { x: 249 ; y: 139 }""")
    self.assertEqual(repr(r), '''in line: 0
pattern: <point>1</point>
block: {'y': '139', 'x': '249'}''')

    r = parser.rule('~/defaule.css', 0, """point:data(1) { x: 249}""")
    self.assertEqual(repr(r), '''in line: 0
pattern: <point>1</point>
block: {'x': '249'}''')

    r = parser.rule('~/defaule.css', 0, """point {x: 0; y: 0; width: 341; height: 232}""")
    self.assertEqual(repr(r), '''in line: 0
pattern: <point></point>
block: {'y': '0', 'x': '0', 'height': '232', 'width': '341'}''')

    r = parser.rule('~/defaule.css', 0, """die:data(1) {image}""")
    self.assertEqual(repr(r), '''in line: 0
pattern: <die>1</die>
block: {}''')

    r = parser.rule('~/defaule.css', 0, """home[player=you] cube{x: 266; y: 197;}""")
    self.assertEqual(repr(r), '''in line: 0
pattern: <home player="you"></home> <cube></cube>
block: {'y': '197', 'x': '266'}''')

  def css_apply_test(self):
    parser = bglib.image.css.CSSParser()
    b = bglib.image.base.Element('board')
    p = bglib.image.base.Element('point', parity='even')
    c = bglib.image.base.Element('chequer', player='him')
    c.append('1')
    self.assertEqual(repr(c), '''<chequer player="him">1</chequer>''')

    r = parser.rule('~/defaule.css', 0, """point[parity=even] chequer[player=him]:data(2)  {image: uri("even-green-2.jpg")} """)
    self.assertEqual(repr(r), '''in line: 0
pattern: <point parity="even"></point> <chequer player="him">2</chequer>
block: {'image': 'uri("even-green-2.jpg")'}''')
    self.assertEqual(repr(r.pattern[-1]), '''<chequer player="him">2</chequer>''')

    self.assertFalse(r.pattern[-1].is_match(c))
    self.assertFalse(r.is_match([b, p, c]))

    r.apply([b, p, c])
    self.assertEqual(repr(c), '''<chequer player="him">1</chequer>''')

    r = parser.rule('~/defaule.css', 0, """point[parity=even] chequer[player=him]:data(1)  {image: uri("even-green-1.jpg")} """)

    self.assertEqual(repr(r), '''in line: 0
pattern: <point parity="even"></point> <chequer player="him">1</chequer>
block: {'image': 'uri("even-green-1.jpg")'}''')
    self.assertEqual(repr(r.pattern[-1]), '''<chequer player="him">1</chequer>''')
    self.assert_(r.pattern[-1].is_match(c))
    self.assert_(r.is_match([b, p, c]))
    r.apply([b, p, c])
    self.assertEqual(repr(c), '''<chequer player="him" image="~/even-green-1.jpg">1</chequer>''')


