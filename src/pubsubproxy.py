#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2006-2008 Noriyuki Hosaka nori@backgammon.gr.jp
#

class Proxy(object):
  def __init__(self, model):
    self.__dict__['_notify'] = list()
    self.__dict__['_model'] = model
  def register(self, notify):
    self._notify.append(notify)
  def unregister(self, notify):
    self._notify.remove(notify)
  def set_model(self, model):
    self.__dict__['_model'] = model
  def __getattr__(self, name):
    return getattr(self._model, name)
  def __setattr__(self, name, value):
    setattr(self._model, name, value)
    for notify in self._notify:
      notify()

