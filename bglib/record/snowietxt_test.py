#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2006-2009 Noriyuki Hosaka bgnori@gmail.com
#

import unittest
import StringIO
from bglib.record.snowietxt import Validator, chop 

class SnowietxtValidatorTest(unittest.TestCase):
  def test_1857680(self):
    f = open('bglib/record/snowietxt/1857680.txt')
    v = Validator()
    h = v.validate(f)
    self.assertEqual(h.hexdigest(),
                     'a1d23325d0c8a614756529de960e4e7bdc1f6737')
  def test_bad(self):
    f = StringIO.StringIO('hogehoge\nzooba\n')
    v = Validator()
    try:
      h= v.validate(f)
      self.assert_(False)
    except ValueError:
      pass

  def test_too_long(self):
    f = StringIO.StringIO('hoge\n'*10)
    v = Validator(max_size=10)
    try:
      v.validate(f)
      self.assert_(False)
    except ValueError:
      pass


class SnowietxtChopTest(unittest.TestCase):
  def test_chop_1857680(self):
    f = open('bglib/record/snowietxt/1857680.txt')
    xs = [x for x in chop(f.read())]
    print xs[0][20]
    s = '''\
 5 point match

 Game 1
 DianaIN : 0                         bgnori : 0
  1) 31: 8/5 6/5                     41: 24/23 13/9
'''
    self.assert_(xs[0].startswith(s))

    s = '''\
 24) 64: 25/19 19/15                 66: 4/0 3/0 3/0 3/0
 25) 62: 15/9 9/7                    51: 2/0 1/0
 26) 63: 7/1 3/0                     Wins 2 points
'''
    self.assert_(xs[0].endswith(s))

    s = '''\
 5 point match

 Game 2
 DianaIN : 0                         bgnori : 2
  1) 61: 13/7 8/7                    21: 24/23 13/11
'''
    self.assert_(xs[1].startswith(s))

    s = '''\
 22) 44: 4/0 3/0 3/0 2/0             11: 2/1 1/0 1/0 1/0
 23) 51: 2/0 1/0                     62: 3/0 2/0
 24) 32: 1/0 1/0                     Wins 2 points
'''
    print len(s)
    print repr(xs[1][-len(s):])
    print repr(s)
    self.assertEqual(xs[1][-len(s):], s)
    self.assert_(xs[1].endswith(s))


    s = '''\
 5 point match

 Game 3
 DianaIN : 0                         bgnori : 4
  1) 43: 13/9 13/10                  32: 24/22 13/10
  2) 42: 8/4 6/4                     22: 22/20 20/18 18/16* 16/14
'''
    self.assert_(xs[2].startswith(s))
    s = '''\
 19) 52: 22/17 17/15                 64: 4/0 4/0
 20) 52: 15/10 10/8                  53: 4/0 2/0
                                      Wins 1 point and the match
'''
    self.assert_(xs[2].endswith(s))


  def test_chop_zoonk_nori_2009Jan151857(self):
    f = open('bglib/record/snowietxt/zoonk-nori-2009Jan151857.txt')
    xs = [x for x in chop(f.read())]
    self.assertEqual(len(xs),1)
    print xs[0][20]
    s = '''\
 3 point match

 Game 1
 zoonk,1666 : 0                   nori,1699 : 0
  1)                             26: 24/18 13/11
'''
    self.assert_(xs[0].startswith(s))
