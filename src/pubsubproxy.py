#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2006-2008 Noriyuki Hosaka nori@backgammon.gr.jp
#

class Proxy(object):
  def __init__(self, model):
    self.__dict__['_subscriber'] = list()
    self.__dict__['_model'] = model
  def register(self, notify):
    self._subscriber.append(notify)
  def unregister(self, notify):
    self._subscriber.remove(notify)
  def set_model(self, model):
    self.__dict__['_model'] = model
    self._notify()
  def __getattr__(self, name):
    return getattr(self._model, name)
  def __setattr__(self, name, value):
    setattr(self._model, name, value)
    self._notify()
  def _notify(self):
    for notify in self._subscriber:
      notify()

