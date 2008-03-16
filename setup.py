#!/usrbin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2006-2008 Noriyuki Hosaka nori@backgammon.gr.jp
#

from distutils.core import setup
#from setuptools import setup


__version__ = "0.0.2"


setup(
  name='backgammonbase-bgutil',
  version=__version__,
  #zip_safe=False,
  description="backgammon programming utilities",
  long_description=
"""This package contains:
  board subpackage
  - base module is basic component for board subpackage
  - gnubg module is gnubg postion id decoder/decoder
  - urlsafe module is urlsafe version of gnubg position decoder/encoder
  - FIBS module is FIBS 'board:' decoder
""",
  author="Noriyuki Hosaka",
  author_email="bgnori@gmail.com",
  packages = ['bgutil.board','bgutil'],
  package_dir = {'bgutil.board': 'board', 'bgutil':''},
  py_modules=[
      'board.base',
      'board.gnubg',
      'board.urlsafe',
      'board.FIBS',
      ],
  url="http://www.backgammonbase.com",
  license="apache 2.0",
)

