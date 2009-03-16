#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2006-2008 Noriyuki Hosaka nori@backgammon.gr.jp
#
import unittest
import nose

from bglib.image.draw import Draw


class MethodTest(unittest.TestCase):
  def setUp(self):
    self.draw = Draw(None)

  def tearDown(self):
    pass

  def dc_test(self):
    self.draw.create_dc([1,1])
    self.assert_(self.draw.dc is not None)
    self.draw.delele_dc()
    self.assertFalse(self.draw.dc)

  def draw_text_test(self):
    self.draw.create_dc([1, 1])
    self.draw.draw_text([0,0], [10, 10], 'draw text', 'ariel', fill=False)
    self.assertEqual(self.draw.dc[0], '''draw_text "draw text" in [10, 10] @ [0, 0]''')

  def draw_ellipse_test(self):
    self.draw.create_dc([1, 1])
    self.draw.draw_ellipse([0,0], [10, 10], fill=False)
    self.assertEqual(self.draw.dc[0], '''draw_ellipse [10, 10], fill=False @ [0, 0]''')

  def draw_polygon_test(self):
    self.draw.create_dc([1, 1])
    self.draw.draw_polygon([[0,0], [1, 1], [1,0]], fill=False)
    self.assertEqual(self.draw.dc[0], '''draw_polygon [[0, 0], [1, 1], [1, 0]] fill=False''')

  def draw_rect_test(self):
    self.draw.create_dc([1, 1])
    self.draw.draw_rect([0,0], [10, 10], fill=False)
    self.assertEqual(self.draw.dc[0], '''draw_rect [10, 10], fill=False @ [0, 0]''')

  def draw_image_test(self):
    self.draw.create_dc([1, 1])
    self.draw.paste_image('image.jpg', [0,0], [10, 10])
    self.assertEqual(self.draw.dc[0], '''paste_image image.jpg @ [0, 0]''')

  def load_image_test(self):
    r = self.draw.load_image('image.jpg', (10,10), False)
    self.assertEqual(r, '''image.jpg size=(10, 10) with flip=False''')

  def load_font_test(self):
    r = self.draw.load_font('bg.ttf', 10)
    self.assertEqual(r, '''bg.ttf size=10''')

  #def draw_element_test(self):
  #    self.draw.draw_element(path)


