#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2006-2011 Noriyuki Hosaka bgnori@gmail.com
#

import exceptions

class EncodingError(exceptions.Exception):
  pass

class DecodeError(EncodingError):
  pass

class InconsistentData(EncodingError):
  pass

class UndefinedTurn(EncodingError):
  pass
