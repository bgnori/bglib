#!/usr/bin/python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2006-2012 Noriyuki Hosaka bgnori@gmail.com
#

from setuptools import setup
import os.path


try:
    # add classifiers and download_url syntax to distutils
    from distutils.dist import DistributionMetadata
    DistributionMetadata.classifiers = None
    DistributionMetadata.download_url = None
except:
    pass

setup(
  name="python-bglib-library",
  version="0.0.10",
  zip_safe=False,
  description="""backgammon programming utilities for python""",
  long_description="""This package contains:
 * model
  provides model to all other modules in this library.

 * encoding
  gnubgid : provides gnubg postion id decoder/encoder
  FIBS : provides FIBS 'board:' responce  decoder
  asciiart : provides ascii art decoder/encoder.
  dbbyte : encoding for databasing position
  bearoff : encoding for bear off database

 * doc
  provides bgwiki formatting engine.

 * gui 
  provides some GUI widgets using wxpython.

 * image 
  board imaging functions using PIL.

 * protocol
  FIBS/session

 * record
  gnubg: gnubg python module support
  snowietxt: snowietxt format file support

 * stat
  rating: rating calculation
  tourney: tourney equity based on rating

""",
  author="Noriyuki Hosaka",
  author_email="bgnori@gmail.com",
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
  install_requires= ['BeautifulSoup==3.2.0\n', 'ClientForm==0.2.10\n', 'Markdown==2.1.1\n', 'decorator==3.3.2\n', 'distribute==0.6.19\n', 'docutils==0.8.1\n', 'elementtree==1.2.7-20070827-preview\n', 'feedparser==5.0.1\n', 'nose==1.1.2\n', 'python-memcached==1.47\n', 'python-tonic-library==0.0.16.rev\n', 'wsgiref==0.1.2\n'],
  provides=['bglib'],
  url="https://github.com/bgnori/bglib",
  license="proprietary",
)


