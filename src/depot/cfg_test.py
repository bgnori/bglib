#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2006-2008 Noriyuki Hosaka nori@backgammon.gr.jp
#

import tempfile
import unittest
import nose

import bglib.depot.cfg

class CFGTest(unittest.TestCase):
  def setUp(self):
    self.temp = tempfile.NamedTemporaryFile()
    self.cfg_proxy = bglib.depot.cfg.CFGProxy(['./bglib/depot/cfg_test.cfg'])

  def tearDown(self):
    pass

  def creation_test(self):
    self.assertNotEqual(self.cfg_proxy, None)
    assert isinstance(self.cfg_proxy, bglib.depot.cfg.Proxy)

  def secion_test(self):
    self.assert_( hasattr(self.cfg_proxy, 'logging'))
    self.assert_(hasattr(self.cfg_proxy, 'CommandDebugger'))
    self.assert_(hasattr(self.cfg_proxy, 'a'))
    self.assert_(hasattr(self.cfg_proxy, 'b'))
    self.assert_(hasattr(self.cfg_proxy, 'c'))

  def option_test(self):
    logging = self.cfg_proxy.logging
    self.assert_(hasattr(logging, 'level'))
    self.assert_(hasattr(logging, 'format'))
    self.assert_(hasattr(logging, 'filename'))
    self.assert_(hasattr(logging, 'filemode'))

  def value_read_test(self):
    logging = self.cfg_proxy.logging
    self.assertEqual(logging.level, '10')
    self.assertEqual(logging.format, r"'%(asctime)s %(levelname)s %(message)s'")
    self.assertEqual(logging.filename, './wxPyGammon.log')
    self.assertEqual(logging.filemode, 'w')

  def value_write_test(self):
    c = self.cfg_proxy.c
    self.assertEqual(c.port, '4321')
    c.port = '54321'
    self.assertEqual(c.port, '54321')

    bglib.depot.cfg.write(self.cfg_proxy, self.temp.name)

    p = bglib.depot.cfg.CFGProxy([self.temp.name])
    self.assertEqual(p.c.port, '54321')

