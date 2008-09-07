#!/usrbin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2006-2008 Noriyuki Hosaka nori@backgammon.gr.jp
#

#from distutils.core import setup
from setuptools import setup
import os.path


__version__ = "0.0.3"


setup(
  name='python-bglib-library',
  version=__version__,
  #zip_safe=False,
  description="backgammon programming utilities for python",
  long_description=
"""This package contains:
  * model 
   this module provides model to all other modules in this library.
  * depot
   this module provides config loader in various formats.
  * encoding 
   - base module provides basic operations to other modules in this subpackage
   - gnubg module is gnubg postion id decoder/decoder
   - urlsafe module is urlsafe version of gnubg position decoder/encoder
   - FIBS module is FIBS 'board:' responce  decoder
  * image 
   this module provides board imagin functions using PIL.
  * gui 
   this module provides some GUI widgets using wxpython.
  * doc
   this  module provides bgwiki formatting engine.
""",
  author="Noriyuki Hosaka",
  author_email="bgnori@gmail.com",
  package_dir = {
                 'bglib':'src', #root
                 },
  packages = ['bglib', 
              'bglib.depot', 
              'bglib.doc', 
              'bglib.encoding', 
              'bglib.gui', 
              'bglib.image', 
              'bglib.model',
              'bglib.protocol'
              ],
  package_data = {
      'bglib.image.resource.matrix':[os.path.join('image','resource','matrix','default.css'),
                                     os.path.join('image','resource','matrix','*.png'),
                                    ],
      'bglib.image.resource.minimal':[os.path.join('image','resource','matrix','default.css'),
                                    ],
      'bglib.image.resource.safari':[os.path.join('image','resource','safari','default.css'),
                                     os.path.join('image','resource','safari','*.jpg'),
                                    ],
      },
  py_modules=[],
  url="http://www.backgammonbase.com",
  license="proprietary",
)

