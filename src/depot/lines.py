#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2006-2008 Noriyuki Hosaka nori@backgammon.gr.jp
#


import bglib.depot.base

class Proxy(bglib.depot.base.Proxy):
  def __repr__(self):
    return "<lines.Proxy for %s of  %s>"%(self._apth, str(self._impl))

  def _is_in_(self, x):
    if len(self._apth) > 0:
      return x in self._impl[self._apth[0]]
    else:
      return x in self._impl

  def _has_child_(self, x):
    return len(self._apth) < 1

  def _get_by_x_(self, x):
    return self._impl[self._apth[0]][x]


def CRLFProxy(filename):
  config  = dict()
  f = file(filename)
  try:
    for line in f.readlines():
      x = line.split()
      if x:
        d = config.get(x[0], dict())
        try:
          e = (int(x[2]), int(x[3]))
        except:
          e = x[2]
        d.update({x[1]: e})
        config.update({x[0]: d})
      else:
        break
  finally:
    f.close()

  return Proxy(Proxy, config, [])

if __name__ == '__main__':
  proxy = CRLFProxy('./bglib/image/resource/align.txt')
  print proxy.point
  x = proxy.point
  print x
  print x[1]
  print proxy.bar
  print proxy.field

