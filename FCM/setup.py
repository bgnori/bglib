#!/usr/bin/env python

from distutils.core import setup, Extension

FIBSCookieMonster_module = Extension('_FIBSCookieMonster',
                                     sources=['FIBSCookieMonster_wrap.c',
                                              'FIBSCookieMonster.c'],
                                    )

setup(name='FIBSCookieMonster',
      version='1.0',
      author='Paul Ferguson',
      description='''a CLIP parsing module for FIBS client''',
      ext_modules=[FIBSCookieMonster_module, ],
      py_modules=["FIBSCookieMonster", ],
      packager='Noriyuki Hosaka, nori@gmail.com',
  )


