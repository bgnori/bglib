#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2006-2008 Noriyuki Hosaka nori@backgammon.gr.jp
#
import unittest
import bglib.doc.doctree

class NodeTest(unittest.TestCase):
  def setUp(self):
    self.root = bglib.doc.doctree.Root()

  def test_is_acceptable_of_Span(self):
    b = bglib.doc.doctree.BoldElement(self.root)
    i = bglib.doc.doctree.ItalicElement(self.root)
    isinstance(b, bglib.doc.doctree.SpanElement)
    isinstance(i, bglib.doc.doctree.SpanElement)
    self.assert_(i.is_acceptable(b))
    self.assert_(b.is_acceptable(i))

    self.root.append(b)
    self.root.append(i)
    d = bglib.doc.doctree.DebugVisitor()
    self.root.accept(d)

    self.assertEqual(
      d.buf,
      ('Root\n'
      'BoldElement\n'
      'ItalicElement\n')
    )
    
  def test_is_acceptable_of_itemize(self):
    b = bglib.doc.doctree.BoldElement(self.root)
    i = bglib.doc.doctree.ItemizeElement(self.root)
    o = bglib.doc.doctree.ListElement(self.root)
    isinstance(i, bglib.doc.doctree.LineElement)
    isinstance(o, bglib.doc.doctree.BoxElement)
    self.assert_(i.is_acceptable(b))
    self.assert_(o.is_acceptable(i))
    self.assert_(o.is_acceptable(b))

    self.assertFalse(b.is_acceptable(o))
    self.assertFalse(b.is_acceptable(i))

  def test_is_acceptable_of_Definition(self):
    dl = bglib.doc.doctree.DefinitionListElement(self.root)
    dd = bglib.doc.doctree.DefinitionBodyElement(dl)
    a = bglib.doc.doctree.AnchorElement(dd)
    print dl.acceptables()
    print dd.acceptables()
    self.assert_(dd.is_acceptable(a))


class EditorTest(unittest.TestCase):
  def setUp(self):
    self.root = bglib.doc.doctree.BgWikiElementRoot()
    self.editor = bglib.doc.doctree.Editor()

  def test_start_done(self):
    editor = self.editor
    editor.start(self.root)
    t = editor.done()
    self.assertEqual(t, self.root)

  def test_enter(self):
    editor = self.editor
    editor.start(self.root)
    editor.enter(bglib.doc.doctree.Node)
    self.assertNotEqual(self.root, self.editor.current)
    t = editor.done()
    self.assertEqual(t, self.root)
  
  def test_leave(self):
    editor = self.editor
    editor.start(self.root)
    editor.enter(bglib.doc.doctree.BgWikiElementNode)
    editor.enter(bglib.doc.doctree.Node)
    editor.leave(bglib.doc.doctree.BgWikiElementNode)
    self.assertEqual(editor.current, self.root)
    t = editor.done()
    self.assertEqual(t, self.root)

  def test_append_text(self):
    #FIXME move append_text method to HtmlEditor.
    editor = self.editor
    editor.start(self.root)
    editor.append_text('ho')
    editor.append_text('ge')
    editor.enter(bglib.doc.doctree.BgWikiElementNode)
    self.assertEqual(len(editor.current.children), 0)
    editor.append_text('pi')
    self.assertEqual(len(editor.current.children), 1)
    editor.append_text('yo')
    self.assertEqual(len(editor.current.children), 1)
    editor.leave(bglib.doc.doctree.BgWikiElementNode)
    editor.append_text('foo')
    editor.append_text('bar')
    t = editor.done()
    d = bglib.doc.doctree.DebugVisitor()
    self.root.accept(d)
    self.assertEqual(
      d.buf,
      ('Root\n'
      'Text:hoge\n'
      'BgWikiElementNode\n'
      'Text:piyo\n'
      'Text:foobar\n'
      )
    )
    self.assertEqual(len(t.children), 3)# Text, BgWikiElementNode, Text

class BgWikiElementNodeTest(unittest.TestCase):
  def setUp(self):
    self.root = bglib.doc.doctree.BgWikiElementRoot()
    self.editor = bglib.doc.doctree.Editor()
    self.writer = bglib.doc.doctree.HtmlWriter()

  def test_append_text(self):
    editor = self.editor
    editor.start(self.root)
    editor.append_text('ho')
    editor.append_text('ge')
    editor.enter(bglib.doc.doctree.BoldElement)
    self.assertEqual(len(editor.current.children), 0)
    editor.append_text('pi')
    self.assertEqual(len(editor.current.children), 1)
    editor.append_text('yo')
    self.assertEqual(len(editor.current.children), 1)
    editor.leave(bglib.doc.doctree.BoldElement)
    editor.append_text('foo')
    editor.append_text('bar')
    t = editor.done()
    d = bglib.doc.doctree.DebugVisitor()
    self.root.accept(d)
    self.assertEqual(
      d.buf,
      ('Root\n'
      'Text:hoge\n'
      'BoldElement\n'
      'Text:piyo\n'
      'Text:foobar\n'
      )
    )
    self.assertEqual(len(t.children), 3)# Text, BgWikiElementNode, Text

    self.root.accept(self.writer)
    self.assertHtmlEqual(
      self.writer.html(),
      ('hoge'
       '<strong>piyo</strong>'
       'foobar')
    )


