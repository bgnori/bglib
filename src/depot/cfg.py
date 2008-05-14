#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2006-2008 Noriyuki Hosaka nori@backgammon.gr.jp
#
import ConfigParser

if __name__ == "__main__":
  # for module test
  import base
  baseclass = base.Proxy
else:
  import bglib.depot.base
  baseclass = bglib.depot.base.Proxy

class Proxy(baseclass):
  def __repr__(self):
    return "<cfg.Proxy for %s of  %s>"%(self._apth, str(self._impl))

  def _is_in_(self, x):
    #print 'cfg.Proxy._is_in_', self._apth, x
    if self._apth:
      return self._impl.has_option(self._apth[0], x)
    else:
      return x in self._impl.sections()

  def _has_child_(self, x):
    return not bool(self._apth)

  def _get_by_x_(self, x):
    return self._impl.get(self._apth[0], x)

  def _set_by_x_(self, x, value):
    self._impl.set(self._apth[0], x, value)

  def __iter__(self):
    if not self._apth:
      for section in self._impl.sections():
        yield self[section]
    elif len(self._apth) == 1:
      section = self._apth[0]
      for option in self._impl.options(section):
        yield self._impl.get(section, option)
      #for item in self._impl.items(section):
      #  yield item
    else:
      raise

def CFGProxy(filenames):
  config = ConfigParser.SafeConfigParser()
  config.read(filenames)
  return  Proxy(Proxy, config, [])

if __name__ == '__main__':
  proxy = CFGProxy(['./connection.cfg'])
  print proxy.a
  x = proxy.a
  print x
  print x.name
  print proxy.a.port
  proxy.a.port = '100'
  print proxy.a.port
  for section in proxy:
    for option in section:
      print option

