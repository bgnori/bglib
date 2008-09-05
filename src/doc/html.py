#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2006-2008 Noriyuki Hosaka nori@backgammon.gr.jp
#
import re
import unittest
import pprint
import difflib
import xml.parsers.expat

UNSAFE_LETTERS = '(?P<lt>[<])|(?P<gt>[>])|(?P<amp>[&])'
def escape(s):
  def handler(matchobj):
    d = matchobj.groupdict()
    if d['lt']:
      return '&lt;'
    if d['gt']:
      return '&gt;'
    if d['amp']:
      return '&amp;'
  return re.sub(UNSAFE_LETTERS, handler, s)

crlf = re.compile(r'\n')
gt = re.compile(r'>')
def nomalize(html):
  crlfless = re.sub(crlf, '', html)
  return re.sub(gt, '>\n', crlfless)


ELEMENT = r'(?P<element>[a-zA-Z]+)'
ATTRNAME = r'(?P<attrname>[a-zA-Z]+)'
ATTRVALUE = r'(?P<attrvalue>[a-zA-Z0-9:;./\-]+)'
ATTRIBUTE = r'(?P<attribute>' + ATTRNAME + '="' + ATTRVALUE + '")'
ATTRIBUTE_LIST = '(?P<attribute_list>(' + ATTRIBUTE + '[ ]*)*)'
TAG = '(?P<tag></?' + ELEMENT + '( ' +  ATTRIBUTE_LIST + ')?>)'

r_attribute =re.compile(ATTRIBUTE)
r_tag = re.compile(TAG)

def tuplify_attr(attr):
  r = list()
  for matchobj in r_attribute.finditer(attr):
    d = matchobj.groupdict('')
    r.append((d['attrname'], d['attrvalue']))
  return tuple(r)

def dictify_attr(attr):
  r = dict()
  for matchobj in r_attribute.finditer(attr):
    d = matchobj.groupdict('')
    r.update({d['attrname']:d['attrvalue']})
  return r

def tuplify(normalized):
  r = list()
  for matchobj in r_tag.finditer(normalized):
    d = matchobj.groupdict('')
    r.append((d['element'], tuplify_attr(d['attribute_list'])))
  return tuple(r)

def tupdict(normalized):
  r = list()
  for matchobj in r_tag.finditer(normalized):
    d = matchobj.groupdict('')
    r.append((d['element'], dictify_attr(d['attribute_list'])))
  return tuple(r)

def cmp_tuple(html_a, html_b):
  if html_a == html_b:
    return []
  a = tuplify(nomalize(html_a))
  b = tuplify(nomalize(html_b))
  s = difflib.SequenceMatcher(lambda x: len(x) == 0, a, b)
  for opcode in s.get_opcodes():
    if opcode[0] != 'equal':
      print "%6s a[%d:%d] b[%d:%d]"%opcode,
      print a[opcode[1]: opcode[2]], b[opcode[3]: opcode[4]]


def cmp(html_a, html_b):
  if html_a == html_b:
    return []
  na = nomalize(html_a)
  nb = nomalize(html_b)
  g = difflib.unified_diff(na, nb)
  return list(g)

class HtmlTestCase(unittest.TestCase):
  def assertHtmlEqual(self, html_a, html_b, message=None):
    r = cmp_tuple(html_a, html_b)
    pprint.pprint(r)
    self.assertFalse(r, message)

def validate(html_fragment):
  p = xml.parsers.expat.ParserCreate()
  p.Parse(
  '''<?xml version="1.0" encoding="us-ascii"?>\n''')
  p.Parse(
  '''<!DOCTYPE html PUBLIC "'''
  '''-//W3C//DTD XHTML 1.0 Strict//EN"\n'''
  '''"http://www.w3.org/TR/xhtml1'''
  '''/DTD/xhtml1-strict.dtd">\n''')
  p.Parse(
  '''<html xmlns="http://www.w3.org/\n'''
  '''1999/xhtml" xml:lang="en">\n''')
  #'''lang="en">\n''')
  p.Parse(
  '''<head><title>test</title></head>\n''')
  p.Parse('''<body>\n''')

  p.Parse(html_fragment)
  p.Parse('''</body></html>\n''', True)

