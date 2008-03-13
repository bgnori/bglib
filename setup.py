#!/usrbin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2006-2008 Noriyuki Hosaka nori@backgammon.gr.jp
#

from setuptools import setup, Extension


__version__ = "0.0.1"

FIBSCookieMonster = Extension(
          name = 'FIBSCookieMonster', 
          include_dirs=['FCM'],
          sources=[
            'FCM/FIBSCookieMonster.c',
            'FCM/FIBSCookieMonster.i',
          ],
          extra_compile_args= [
            '-IFIBSCookieMonster.h',
            '-Iclip.h',
            #'-IFIBSCookies.h',
          ],
          depends=[
            'FCM/FIBSCookieMonster.h',
            'FCM/clip.h',
            #'FCM/FIBSCookies.h',
            'FCM/FIBSCookieMonster.c',
            'FCM/FIBSCookieMonster.i',
            'FCM/FIBSCookies.i',
            'FCM/CLIP.i',
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
  - FIBSCookieMonster Extension(wrapper generated with swig, originally written by Chris)
""",
  author="Noriyuki Hosaka",
  author_email="bgnori@gmail.com",
  py_modules=[
      'positionhash',
      ],
  headers=[
            'FCM/FIBSCookieMonster.h',
            'FCM/clip.h',
            #'FCM/FIBSCookies.h',
            ],
  ext_modules=[
              FIBSCookieMonster,
             ],
  url="http://www.backgammonbase.com",
  license="apache 2.0",
)
               #'FCM/FIBSCookieMonster.h', 'FCM/CLIP.h', 'FCM/FIBSCookies.h',
