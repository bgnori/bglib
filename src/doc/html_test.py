#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2006-2008 Noriyuki Hosaka nori@backgammon.gr.jp
#
import unittest
import pprint
import bglib.doc.html

class HTMLEscapeTest(unittest.TestCase):
  def test_escape_lt(self):
    self.assertEqual(
      bglib.doc.html.escape('<'),
      '&lt;')

  def test_escape_gt(self):
    self.assertEqual(
      bglib.doc.html.escape('>'),
      '&gt;')

  def test_escape_amp(self):
    self.assertEqual(
      bglib.doc.html.escape('&'),
      '&amp;')

  def test_escape_combined(self):
    self.assertEqual(
      bglib.doc.html.escape('&<>'),
      '&amp;&lt;&gt;')

  def test_escape_combined(self):
    self.assertEqual(
      bglib.doc.html.escape('!&<>'),
      '!&amp;&lt;&gt;')

  def test_cmp_empty_string(self):
    r = bglib.doc.html.cmp('', '')
    self.assertFalse(r)

  def test_cmp_somthing(self):
    r = bglib.doc.html.cmp('a', 'b')
    self.assert_(r)
    self.assertEqual(r, 
      ['---  \n',
       '+++  \n',
       '@@ -1,1 +1,1 @@\n',
       '-a',
       '+b']
       )
  def test_normalize(self):
    a = ('''<blockquote class="citation">\n'''
    '''<blockquote class="citation">\n'''
    '''<p>\n'''
    '''Someone\'s original text</p>\n'''
    '''</blockquote>\n'''
    '''<p>\n'''
    '''Someone else\'s reply text</p>\n'''
    '''</blockquote>\n'''
    '''My reply text''')
    
    b = ('''<blockquote class="citation">\n'''
    '''<blockquote class="citation">\n'''
    '''<p>\n'''
    '''Someone\'s original text\n'''
    '''</p>\n'''
    '''</blockquote>\n'''
    '''<p>\n'''
    '''Someone else\'s reply text\n'''
    '''</p>\n'''
    '''</blockquote>\n'''
    '''My reply text''')
    z = bglib.doc.html.nomalize(b)
    pprint.pprint(z)
    self.assertEqual(z, a)


  def test_cmp_htmlthing(self):
    a = ('''<blockquote class="citation">\n'''
    '''<blockquote class="citation">\n'''
    '''<p>\n'''
    '''Someone\'s original text</p>\n'''
    '''</blockquote>\n'''
    '''<p>\n'''
    '''Someone else\'s reply text</p>\n'''
    '''</blockquote>\n'''
    '''My reply text''')
    
    b = ('''<blockquote class="citation">\n'''
    '''<blockquote class="citation">\n'''
    '''<p>\n'''
    '''Someone\'s original text\n'''
    '''</p>\n'''
    '''</blockquote>\n'''
    '''<p>\n'''
    '''Someone else\'s reply text\n'''
    '''</p>\n'''
    '''</blockquote>\n'''
    '''My reply text''')

    r = bglib.doc.html.cmp(a, b)
    pprint.pprint(r)
    self.assertFalse(r)


class TestForTestHelpter(bglib.doc.html.HtmlTestCase):
  def test_it(self):
    a = ('''<blockquote class="citation">\n'''
    '''<blockquote class="citation">\n'''
    '''<p>\n'''
    '''Someone\'s original text</p>\n'''
    '''</blockquote>\n'''
    '''<p>\n'''
    '''Someone else\'s reply text</p>\n'''
    '''</blockquote>\n'''
    '''My reply text''')
    
    b = ('''<blockquote class="citation">\n'''
    '''<blockquote class="citation">\n'''
    '''<p>\n'''
    '''Someone\'s original text\n'''
    '''</p>\n'''
    '''</blockquote>\n'''
    '''<p>\n'''
    '''Someone else\'s reply text\n'''
    '''</p>\n'''
    '''</blockquote>\n'''
    '''My reply text''')
    self.assertHtmlEqual(a, b)


