#!/usr/bin/python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2006-2012 Noriyuki Hosaka bgnori@gmail.com
#


d = dict(
  NAME='python-bglib-library',
  AUTHOR="Noriyuki Hosaka",
  AUTHOR_EMAIL= "bgnori@gmail.com",
  VERSION=open("VERSION").read().strip(),
  HOMEPAGE="https://github.com/bgnori/bglib",
  DESCRIPTION = "backgammon programming utilities for python",
  LONG_DESCRIPTION=open("DESCRIPTION").read(),
  install_requires=open("freeze.txt").readlines(),
)



setup_str = '''\
#!/usr/bin/python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2006-2012 Noriyuki Hosaka bgnori@gmail.com
#

from setuptools import setup


try:
    # add classifiers and download_url syntax to distutils
    from distutils.dist import DistributionMetadata
    DistributionMetadata.classifiers = None
    DistributionMetadata.download_url = None
except:
    pass

setup(
  name="{NAME}",
  version="{VERSION}",
  zip_safe=False,
  description="""{DESCRIPTION}""",
  long_description="""{LONG_DESCRIPTION}""",
  author="{AUTHOR}",
  author_email="{AUTHOR_EMAIL}",
  package_dir = {{
                 'bglib':'bglib', #root
                 }},
  packages = ['bglib', 
              'bglib.doc', 
              'bglib.encoding', 
              'bglib.gui', 
              'bglib.image', 
              'bglib.image.resource', 
              'bglib.model',
              'bglib.protocol'
              ],
  package_data = {{
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
      }},
  py_modules=[],
  install_requires= {install_requires},
  provides=['bglib'],
  url="{HOMEPAGE}",
  license="proprietary",
)

'''

print setup_str.format(**d)
