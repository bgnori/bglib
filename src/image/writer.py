#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2006-2008 Noriyuki Hosaka nori@backgammon.gr.jp
#
import string
import StringIO
import unittest

tests = {
     'a':('4Dl4ADqwt4MDIA', 'MBmgAAAAAAAA'),

     'b':('4Dl4ADqwt4MDIA', 'AQGgAAAAAAAA'),
     'c':('22wqECCw8+ABYA', 'UQmgAAAAAAAA'),
     'd':('4HPiASHgc/ABMA', 'UQn1AAAAAAAA'),
     'e':('4HPKATDgc/ABMA', 'cAngAAAAAAAA'),
     'f':('mGfwATDgc/ABMA', 'cCOgAAAAAAAA'),
     'g':('mGfwATDgc/ABMA', 'cEOgAAAAAAAA'),
     'h':('mGfwATDgc/ABMA', 'cGOgAAAAAAAA'),

     'i':('PwkAACoBAAAAAA', 'cAn2AAAAAAAA'),
     'j':('FwAA4CcBAAAAAA', 'MAH2AAAAAAAA'),
     'k':('4HPiASHgc/ABMA', 'UQn1AAAAAAAA'),
     'l':('NgAAACAEAAAAAA', 'cAnyAAAAAAAA'),
     'm':('4PPIQRCYc4sBMA', '8Am1AEAAAAAA'),
     'n':('284lIADf7QAAYA', '8Im1AEAAAAAA'),
     'o':('AAAAgAAAAAAAAA', 'cAqgAFAAAAAA'),
     'q':('2ObIAEpDu5EBKA', 'cInsAFAAIAAA'),
     'r':('AAAAAAAAAAAAAA', 'AAAAAAAAAAAA'),
    }

class Writer(object):
  def make_header(self, css):
    header = (
      '''import os.path\n'''
      '''import unittest\n'''
      '''import Image\n'''
      '''import bglib.model.board\n'''
      '''import bglib.encoding.gnubg\n'''
      '''import bglib.image.css\n'''
      '''from bglib.image.resource.${css} import css\n'''
      '''from bglib.image.resource.${css} import draw\n'''
      '''\n'''
    )
    t = string.Template(header)
    return t.substitute(css=css)

  def make_class(self, css):
    klass = (
      '''class theTest(unittest.TestCase):\n'''
      '''  def setUp(self):\n'''
      '''    self.b = bglib.model.board.board()\n'''
      '''    \n'''
      '''  def tearDown(self):\n'''
      '''    pass\n'''
    )
    t = string.Template(klass)
    return t.substitute(css=css)
    
  def make_helper(self, css):
    helper = (
      '''\n'''
      '''def load(b, mid, pid):\n'''
      '''  bglib.encoding.gnubg.decode(b, mid, pid)\n'''
      '''\n'''
      '''def get_image(self, name):\n'''
      '''  return Image.open(os.path.join(testdatapath, name + '.png'))\n'''
      '''\n'''
      '''def make_image(name, pid, mid):\n'''
      '''  b = bglib.model.board.board()\n'''
      '''  load(b, pid, mid)\n'''
      '''  image = draw.draw(b, (1000, 800))\n'''
      '''  image.save('./bglib/image/tests/${css}/%s.png'%name)\n'''
      '''\n'''
      '''def get_xml(self, name):\n'''
      '''  f = file(os.path.join(testdatapath, name+'.xml'))\n'''
      '''  try:\n'''
      '''    return f.read()\n'''
      '''  finally:\n'''
      '''    f.close()\n'''
      '''\n'''
      '''def make_tree(b):\n'''
      '''  tree = bglib.image.base.ElementTree(b)\n'''
      '''  css.apply(tree)\n'''
      '''  return tree\n'''
      '''  \n'''
      '''def make_xml(name, pid, mid):\n'''
      '''  b = bglib.model.board.board()\n'''
      '''  load(b, pid, mid)\n'''
      '''  tree = make_tree(b)\n'''
      '''  f = file('./bglib/image/tests/${css}/%s.xml'%name, 'w')\n'''
      '''  f.write(str(tree))\n'''
      '''  f.close()\n'''
      '''\n'''
    )
    t = string.Template(helper)
    return t.substitute(css=css)

  def make_method(self, name, pid, mid):
    method = (
      '''  def ${name}_tree_test(self):\n'''
      '''    """ tree test for ${name} pid='${pid}', mid='${mid}'"""\n'''
      '''    load(self.b, pid='${pid}', mid='${mid}')\n'''
      '''    tree = make_tree(self.b)\n'''
      '''    self.assertEqual(str(tree), get_xml('${name}'))\n'''
      '''    \n'''
      '''  def ${name}_image_test(self):\n'''
      '''    """ image test for ${name} pid='${pid}', mid='${mid}'"""\n'''
      '''    load(self.b, pid='${pid}', mid='${mid}')\n'''
      '''    image = draw.draw(self.b, (1000, 800))\n'''
      '''    ans = get_image('${name}')\n'''
      '''    self.assertEqual(image.tostring(), ans.tostring())\n'''
      '''    \n'''
    )
    t = string.Template(method)
    return t.substitute(name=name, pid=pid, mid=mid)

  def make_footer(self, css):
    footer = (
      '''if __name__ == '__main__':\n'''
      '''  from bglib.image.writer import tests\n'''
      '''  try:\n'''
      '''    os.makedirs('./bglib/image/tests/${css}')\n'''
      '''  except OSError:\n'''
      '''    pass\n'''
      '''  for name, (pid, mid) in tests.items():\n'''
      '''    make_xml(name, pid, mid)\n'''
      '''    make_image(name, pid, mid)\n'''
      '''  pass\n'''
    )
    t = string.Template(footer)
    return t.substitute(css=css)

  def write(self, fobj, css):
    header = self.make_header(css)
    helper = self.make_helper(css)
    klass = self.make_class(css)
    methods = ''.join([self.make_method(test, pid, mid) for test, (pid, mid) in tests.items()])
    footer = self.make_footer(css)
    assert header + helper+ klass + methods + footer
    fobj.write(header + helper+ klass + methods + footer)
    fobj.flush()


class WriterTest(unittest.TestCase):
  def setUp(self):
    self.writer = Writer()
  def tearDown(self):
    pass

  def assertLinesEqual(self, xs, ys):
    ys = ys.split('\n')
    for i, x in enumerate(xs.split('\n')):
      self.assertEqual(x, ys[i], 'mismatch at %i th line.'%(i+1) )

  def grammer_validity_test(self):
    f = StringIO.StringIO()
    self.writer.write(f, 'matrix')
    f.seek(0)
    read = f.read()
    self.assert_(f.tell())
    self.assert_(read)
    o = compile(read, '<string>', 'exec')
    self.assert_(o)
    f.close()
    
  def method_test(self):
    method_code = self.writer.make_method('initial_position', '4HPwATDgc/ABMA', 'MAAAAAAAAAAA')
    self.assertLinesEqual(method_code, (
      '''  def initial_position_tree_test(self):\n'''
      '''    """ tree test for initial_position pid='4HPwATDgc/ABMA', mid='MAAAAAAAAAAA'"""\n'''
      '''    load(self.b, pid='4HPwATDgc/ABMA', mid='MAAAAAAAAAAA')\n'''
      '''    tree = make_tree(self.b)\n'''
      '''    self.assertEqual(str(tree), get_xml('initial_position'))\n'''
      '''    \n'''
      '''  def initial_position_image_test(self):\n'''
      '''    """ image test for initial_position pid='4HPwATDgc/ABMA', mid='MAAAAAAAAAAA'"""\n'''
      '''    load(self.b, pid='4HPwATDgc/ABMA', mid='MAAAAAAAAAAA')\n'''
      '''    image = draw.draw(self.b, (1000, 800))\n'''
      '''    ans = get_image('initial_position')\n'''
      '''    self.assertEqual(image.tostring(), ans.tostring())\n'''
      '''    \n'''
      ))

  def class_test(self):
    class_code = self.writer.make_class('matrix')
    self.assertLinesEqual(class_code,(
      '''class theTest(unittest.TestCase):\n'''
      '''  def setUp(self):\n'''
      '''    self.b = bglib.model.board.board()\n'''
      '''    \n'''
      '''  def tearDown(self):\n'''
      '''    pass\n'''
      ))

  def helper_test(self):
    helper_code = self.writer.make_helper('matrix')
    self.assertLinesEqual(helper_code, (
      '''\n'''
      '''def load(b, mid, pid):\n'''
      '''  bglib.encoding.gnubg.decode(b, mid, pid)\n'''
      '''\n'''
      '''def get_image(self, name):\n'''
      '''  return Image.open(os.path.join(testdatapath, name + '.png'))\n'''
      '''\n'''
      '''def make_image(name, pid, mid):\n'''
      '''  b = bglib.model.board.board()\n'''
      '''  load(b, pid, mid)\n'''
      '''  image = draw.draw(b, (1000, 800))\n'''
      '''  image.save('./bglib/image/tests/matrix/%s.png'%name)\n'''
      '''\n'''
      '''def get_xml(self, name):\n'''
      '''  f = file(os.path.join(testdatapath, name+'.xml'))\n'''
      '''  try:\n'''
      '''    return f.read()\n'''
      '''  finally:\n'''
      '''    f.close()\n'''
      '''\n'''
      '''def make_tree(b):\n'''
      '''  tree = bglib.image.base.ElementTree(b)\n'''
      '''  css.apply(tree)\n'''
      '''  return tree\n'''
      '''  \n'''
      '''def make_xml(name, pid, mid):\n'''
      '''  b = bglib.model.board.board()\n'''
      '''  load(b, pid, mid)\n'''
      '''  tree = make_tree(b)\n'''
      '''  f = file('./bglib/image/tests/matrix/%s.xml'%name, 'w')\n'''
      '''  f.write(str(tree))\n'''
      '''  f.close()\n'''
      '''\n'''
      ))

  def header_test(self):
    header_code = self.writer.make_header('matrix')
    self.assertLinesEqual(header_code,(
      '''import os.path\n'''
      '''import unittest\n'''
      '''import Image\n'''
      '''import bglib.model.board\n'''
      '''import bglib.encoding.gnubg\n'''
      '''import bglib.image.css\n'''
      '''from bglib.image.resource.matrix import css\n'''
      '''from bglib.image.resource.matrix import draw\n'''
      '''\n'''
      ))

  def footer_test(self):
    footer_code = self.writer.make_footer('matrix')
    ans = (
      '''if __name__ == '__main__':\n'''
      '''  from bglib.image.writer import tests\n'''
      '''  try:\n'''
      '''    os.makedirs('./bglib/image/tests/matrix')\n'''
      '''  except OSError:\n'''
      '''    pass\n'''
      '''  for name, (pid, mid) in tests.items():\n'''
      '''    make_xml(name, pid, mid)\n'''
      '''    make_image(name, pid, mid)\n'''
      '''  pass\n'''
      )
    self.assertLinesEqual(ans, footer_code)
