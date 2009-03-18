#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2006-2008 Noriyuki Hosaka nori@backgammon.gr.jp
#
''' 
How to access is defined in class Proxy of this file.

What to access
  .cfg file access is implemented in cfg.py
  xml file access is implemented in xml.py
  csv file access is implemented in csv.py

'''

class Proxy(object):
  def __init__(self, cls, impl, access_path):
    assert(isinstance(access_path, list))
    self.__dict__['_cls'] = cls
    self.__dict__['_impl'] = impl
    self.__dict__['_apth'] = access_path
  # MUST

  def _is_in_(self, x):
    pass

  def _has_child_(self, x):
    # assert(self._is_in_(x))
    pass

  def _get_by_x_(self, x):
    assert(not self._has_child_(x))

  def _set_by_x_(self, x, value):
    assert(not self._has_child_(x))

  def __repr__(self):
    return "<Proxy for %s of  %s>"%(self._apth, str(self._impl))

  def __len__(self):
    pass

  def _get_node_(self, x):
    assert(self._has_child_(x))
    return self._cls(self._cls, self._impl, self._apth+[x])
    
  def _write_back_(self):
    pass

  # if possible to have node, spport this for inserting data
  def _mk_node_(self, x):
    pass

  # May, to support deletion
  def _del_by_x_(self, x):
    assert(not self._has_child_(x))

  def _rm_node_(self, x):
    assert(self._has_child_(x))


  # nested Dictionary emulation
  def __getitem__(self, key):
    if self._has_child_(key):
      return self._get_node_(key)
    else:
      return self._get_by_x_(key)

  def __contains__(self, key):
    return self._is_in_(key)

  def __setitem__(self, key, value):
    if not self._has_child_(key):
      return Proxy() #ugh!
    self._set_by_x_(key, value)

  def __delitem__(self, key):
    if not self._has_child_(key):
      return Proxy() #ugh!
    self._del_by_x_(key)

  def __iter__(self):
    pass


  # nested attribute emulation
  def __getattr__(self, name):
    if not self._is_in_(name):
      raise AttributeError("not such attribute %s in %s"%(name, str(self)))
    if self._has_child_(name):
      return self._get_node_(name)
    else:
      return self._get_by_x_(name)
    assert(False)

  def __setattr__(self, name, value):
    if not self._is_in_(name):
      raise AttributeError("not such attribute %s in %s"%(name, str(self)))
    if self._has_child_(name):
      pass
    else:
      self._set_by_x_(name, value)

  def __delattr__(self, name):
    if not self._is_in_(name):
      raise AttributeError("not such attribute %s in %s"%(name, str(self)))
    self._del_by_x_(name)

  def __eq__(self, x):
    return id(self) == id(x)
