#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2006-2008 Noriyuki Hosaka nori@backgammon.gr.jp
#
import bglib.depot

class DictProxy(bglib.depot.Proxy):
  def __repr__(self):
    return "<dict.Proxy for %s of  %s>"%(self._apth, str(self._impl))

  def _is_in_(self, x):
    names = self._apth + []
    d = self._impl
    while names:
      d = d[names.pop(0)]
    return x in d

  def _has_child_(self, x):
    item = self._get_by_x_(x)
    return isinstance(item, dict)

  def _get_by_x_(self, x):
    names = self._apth + [x]
    d = self._impl
    while names:
      d = d[names.pop(0)]
    return d

def Proxy(**kw):
  impl = dict(kw)
  return DictProxy(DictProxy, impl, [])

if __name__ == '__main__':
  proxy = Proxy(hoge='hoge',
                piyo='piyo',
                one=1,
                double=dict(child='this is a child'),
                triple=dict(
                  double=dict(child='this is a grand child'),
                  )
                )
  print proxy.hoge
  print proxy.piyo
  print proxy.one
  print proxy.double.child
  print proxy.triple.double.child

