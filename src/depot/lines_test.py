#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2006-2008 Noriyuki Hosaka nori@backgammon.gr.jp
#

import tempfile
import unittest
import nose

import bglib.depot.lines

class LinesTest(unittest.TestCase):
  def setUp(self):
    self.temp = tempfile.NamedTemporaryFile()
    self.lines_proxy = bglib.depot.lines.CRLFProxy('./bglib/depot/lines_test.txt')

  def tearDown(self):
    pass

  def creation_test(self):
    self.assertNotEqual(self.lines_proxy, None)
    self.assert_(isinstance(self.lines_proxy, bglib.depot.lines.Proxy))

  def secion_test(self):
    self.assert_('logging' in self.lines_proxy)
    self.assert_(hasattr(self.lines_proxy, 'logging'))
    self.assert_(hasattr(self.lines_proxy, 'CommandDebugger'))
    self.assert_(hasattr(self.lines_proxy, 'a'))
    self.assert_(hasattr(self.lines_proxy, 'b'))
    self.assert_(hasattr(self.lines_proxy, 'c'))

  def option_test(self):
    logging = self.lines_proxy.logging
    self.assert_(hasattr(logging, 'level'))
    self.assert_(hasattr(logging, 'format'))
    self.assert_(hasattr(logging, 'filename'))
    self.assert_(hasattr(logging, 'filemode'))

  def value_read_test(self):
    logging = self.lines_proxy.logging
    self.assertEqual(logging.level, '10')
    #self.assertEqual(logging.format, r"'%(asctime)s %(levelname)s %(message)s'")
    self.assertEqual(logging.filename, './wxPyGammon.log')
    self.assertEqual(logging.filemode, 'w')

  def value_write_test(self):
    c = self.lines_proxy.c
    self.assertEqual(c.port, '4321')
    c.port = '54321'
    #self.assertEqual(c.port, '54321')

    #bglib.depot.lines.write(self.lines_proxy, self.temp.name)

    #p = bglib.depot.cfg.CFGProxy([self.temp.name])
    #self.assertEqual(p.c.port, '54321')

