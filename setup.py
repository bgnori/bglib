#!/usrbin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2006-2008 Noriyuki Hosaka nori@backgammon.gr.jp
#

from setuptools import setup, Extension


__version__ = "0.0.1"

name = 'FIBSCookieMonster'

soFIBSCookieMonster = Extension(
          name='_FIBSCookieMonster',
          sources=[
            'FCM/FIBSCookieMonster.i',
          ],
         )

setup(
  name='backgammonbase-bgutil',
  version=__version__,
  zip_safe=False,
  description="backgammon programming utilities",
  long_description=
"""This package contains:
  - gnubg postion id decoder/decoder
  - FIBS board: decoder
  - FIBSCookieMonster Extension(wrapper generated with swig, originally written by Paul Ferguson)
""",
  author="Noriyuki Hosaka",
  author_email="bgnori@gmail.com",
  packages = ['bgutil',],
  package_dir = {'bgutil': 'FCM'},
  py_modules=[
      '__init__',
      'positionhash',
      'FIBSCookieMonster',
      ],
  ext_modules=[
              soFIBSCookieMonster,
             ],
  url="http://www.backgammonbase.com",
  license="apache 2.0",
)

