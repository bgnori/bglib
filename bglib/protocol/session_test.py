#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2006-2008 Noriyuki Hosaka nori@backgammon.gr.jp
#

import subprocess
import signal
import os
import time

import unittest
import nose

from bglib.protocol.session import Session
from bglib.protocol.session import Subscriber
from bglib.protocol.session import Transport
from bglib.protocol.session import synchronized_with

class SessionTest(unittest.TestCase):
  def setUp(self):
    self.serverps = subprocess.Popen(('python',
                                     './bglib/protocol/server.py',
                                     './bglib/protocol/fibs_test.in',),
                                     )
                                     #stdin=None, stdout=None, stderr=None,)
    time.sleep(.5)
    self.session = Session()
    assert not self.session.is_active()

  def tearDown(self):
    if self.session.is_active():
      self.session.close()
    assert not self.session.is_active()
    os.kill(self.serverps.pid, signal.SIGKILL)
    time.sleep(.2)
    self.serverps.wait()
    time.sleep(.2)

  def subscriber_1_test(self):
    sub = Subscriber()
    self.session.register(sub)
    self.session.open('localhost', 4321)
    self.session.unregister(sub)

  def subscriber_2_test(self):
    sub = Subscriber()
    self.session.open('localhost', 4321)
    self.session.register(sub)
    self.session.unregister(sub)

  def subscriber_3_test(self):
    class PreLogin(Subscriber):
      flag = False
      def CLIP_MOTD_END(self, got):pass
      def CLIP_OWN_INFO(self, got):pass
      def CLIP_WELCOME(self, got):pass
      def CLIP_MOTD_BEGIN(self, got):pass
      def FIBS_MOTD(self, got):pass
      def FIBS_PreLogin(self, got):
        self.flag = True
    sub = PreLogin()
    self.assertFalse(sub.flag)
    self.session.register(sub)
    self.session.open('localhost', 4321)
    time.sleep(2)
    self.assert_(sub.flag)
    self.session.unregister(sub)

