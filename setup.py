#!/usrbin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2006-2008 Noriyuki Hosaka nori@backgammon.gr.jp
#

from distutils.core import setup
#from setuptools import setup
import os.path


NAME = 'python-bglib-library'
AUTHOR = "Noriyuki Hosaka", "bgnori@gmail.com"
VERSION = open("VERSION").read().strip()
DESCRIPTION = "backgammon programming utilities for python"
LONG_DESCRIPTION="""\
This package contains:
  * model 
   this module provides model to all other modules in this library.
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
"""
HOMEPAGE="http://www.backgammonbase.com"

try:
    # add classifiers and download_url syntax to distutils
    from distutils.dist import DistributionMetadata
    DistributionMetadata.classifiers = None
    DistributionMetadata.download_url = None
except:
    pass

setup(
  name=NAME,
  version=VERSION,
  zip_safe=False,
  description=DESCRIPTION,
  long_description=LONG_DESCRIPTION,
  author=AUTHOR[0],
  author_email=AUTHOR[1],
  package_dir = {
                 'bglib':'bglib', #root
                 },
  packages = ['bglib', 
              'bglib.doc', 
              'bglib.encoding', 
              'bglib.gui', 
              'bglib.image', 
              'bglib.image.resource', 
              'bglib.model',
              'bglib.protocol'
              ],
  package_data = {
      'bglib.image.resource':[os.path.join('matrix','default.css'),
                              os.path.join('matrix','*.png'),
                              os.path.join('minimal','*.ttf'),
                              os.path.join('minimal','default.css'),
                              os.path.join('kotobuki','*.ttf'),
                              os.path.join('kotobuki','default.css'),
                              os.path.join('nature','*.ttf'),
                              os.path.join('nature','default.css'),
                              os.path.join('flower','*.ttf'),
                              os.path.join('flower','default.css'),
                              os.path.join('neon','*.ttf'),
                              os.path.join('neon','default.css'),
                              os.path.join('deutsche','*.ttf'),
                              os.path.join('deutsche','default.css'),
                              os.path.join('safari','default.css'),
                              os.path.join('safari','*.jpg'),
                              os.path.join('safari','*.png'),
                             ],
      },
  py_modules=[],
  install_requires=[
      #FIXME! packages installed via RPM do not have egg.
      #"python-imaging >= 1.1.6", 
      #"wxPython >= 2.8.7.1",
  ],
  requires=[
    'python-imageing >=1.1.6',
    'python-tonic-library>=0.0.13',
    'wxPython >=2.8.7.1',
  ],
  provides=['bglib'],
  url=HOMEPAGE,
  license="proprietary",
)

