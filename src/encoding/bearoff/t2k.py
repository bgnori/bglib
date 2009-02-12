#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2006-2009 Noriyuki Hosaka bgnori@gmail.com
#


def writetest(c):
  n, t = c
  us, them = t

  name = "t2k_"\
         + ''.join([str(i) for i in us]) \
         + ''.join([str(i) for i in them]) \
         + "_test"

  print '  def %s(self):'%name
  print '    self.assertEqual(t2k('
  print '        ', t, ','
  print '        ', n, ')'
  print '    )'


dat = '''\
1 0 0
2 1 0
3 1 1
4 0 1
5 0,1 0,0
6 0,1 1,0
7 0,1 0,1
8 1,0 0,1
9 0,0 0,1
10 0,0,1 0,0,0
11 0,0,1 1,0,0
12 0,0,1 0,1,0
13 0,0,1 0,0,1
14 0,1,0 0,0,1
15 1,0,0 0,0,1
16 0,0,0 0,0,1
17 0,0,0,1 0,0,0,0
18 0,0,0,1 1,0,0,0
19 0,0,0,1 0,1,0,0
20 0,0,0,1 0,0,1,0
21 0,0,0,1 0,0,0,1
22 0,0,1,0 0,0,0,1
23 0,1,0,0 0,0,0,1
24 1,0,0,0 0,0,0,1
25 0,0,0,0 0,0,0,1 
49 0,0,0,0,0,0 0,0,0,0,0,1
50 2 0
51 2 1
65 1,1 0
'''

def s2t(s):
  xs = [int(n) for n in s.split(',')]
  return tuple(xs + [0 for i in range(6 - len(xs))])

def dat2case(s):
  ret = list()
  for line in s.splitlines():
    n, us, them = line.split()
    ret.append((int(n), ((s2t(us), s2t(them)))))
  return tuple(ret)

selftest = (
  ( 1 , ((0,0,0,0,0,0), (0,0,0,0,0,0))),
  ( 2 , ((1,0,0,0,0,0), (0,0,0,0,0,0))),
  ( 3 , ((1,0,0,0,0,0), (1,0,0,0,0,0))),
  ( 4 , ((0,0,0,0,0,0), (1,0,0,0,0,0))),
  ( 5 , ((0,1,0,0,0,0), (0,0,0,0,0,0))),
  ( 6 , ((0,1,0,0,0,0), (1,0,0,0,0,0))),
  ( 7 , ((0,1,0,0,0,0), (0,1,0,0,0,0))),
  ( 8 , ((1,0,0,0,0,0), (0,1,0,0,0,0))),
  ( 9 , ((0,0,0,0,0,0), (0,1,0,0,0,0))),
  (10 , ((0,0,1,0,0,0), (0,0,0,0,0,0))),
  (11 , ((0,0,1,0,0,0), (1,0,0,0,0,0))),
  (25 , ((0,0,0,0,0,0), (0,0,0,1,0,0))),
  (49 , ((0,0,0,0,0,0), (0,0,0,0,0,1))),
  (50 , ((2,0,0,0,0,0), (0,0,0,0,0,0))),
  (51 , ((2,0,0,0,0,0), (1,0,0,0,0,0))),
  (65 , ((1,1,0,0,0,0), (0,0,0,0,0,0))),
)

cases = dat2case(dat)
d = dict(cases)
for n, t in selftest:
  assert d[n] == t


if __name__ == '__main__':
  print '''#!/usr/bin/env python'''
  print '''# -*- coding: us-ascii -*-'''
  print '''# vim: syntax=python'''
  print '''#'''
  print '''# DO NOT EDIT'''
  print '''# this test file is generated by t2k.py'''
  print 
  print '''import unittest'''
  print '''from bglib.encoding.bearoff.trice import *'''
  print 
  print 
  print '''class ConvTest(unittest.TestCase):'''
  for c in cases:
    writetest(c)

