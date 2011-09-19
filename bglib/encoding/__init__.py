#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2006-2011 Noriyuki Hosaka bgnori@gmail.com
#

import exceptions

class DecodeError(exceptions.Exception):
  pass

class InconsistentData(exceptions.Exception):
  pass
