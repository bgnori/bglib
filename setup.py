#!/usrbin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2006-2008 Noriyuki Hosaka nori@backgammon.gr.jp
#

from distutils.core import setup
import os.path


__version__ = "0.0.2"


setup(
  name='backgammonbase-bgutil',
  version=__version__,
  #zip_safe=False,
  description="backgammon programming utilities",
  long_description=
"""This package contains:
  encoding subpackage
  - base module is basic component for encoding subpackage
  - gnubg module is gnubg postion id decoder/decoder
  - urlsafe module is urlsafe version of gnubg position decoder/encoder
  - FIBS module is FIBS 'board:' responce  decoder
""",
  author="Noriyuki Hosaka",
  author_email="bgnori@gmail.com",
  package_dir = {'bglib':'src',},
  packages = ['bglib', 'bglib.encoding'],
  package_data = {'bglib':[os.path.join('resource','*.jpg'),], },
  py_modules=[
      'bglib.model',
      'bglib.image',
      'bglib.helper',
      'bglib.encoding.base',
      'bglib.encoding.gnubg',
      'bglib.encoding.urlsafe',
      'bglib.encoding.FIBS',
      ],
  url="http://www.backgammonbase.com",
  license="proprietary",
)

