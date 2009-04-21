#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2006-2009 Noriyuki Hosaka bgnori@gmail.com
#

import unittest
import StringIO
from bglib.record.snowietxt import Validator

class SnowietxtTest(unittest.TestCase):
  def test1857680(self):
    f = open('bglib/record/snowietxt/1857680.txt')
    v = Validator(f)
    h = v.validate()
    self.assertEqual(h.hexdigest(),
                     'a1d23325d0c8a614756529de960e4e7bdc1f6737')
  def testbad(self):
    f = StringIO.StringIO('hogehoge\nzooba\n')
    v = Validator(f)
    try:
      h = v.validate()
      self.assert_(False)
    except ValueError:
      pass
