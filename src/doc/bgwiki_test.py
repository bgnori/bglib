#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2006-2008 Noriyuki Hosaka nori@backgammon.gr.jp
#
import re
import unittest

import bglib.doc.macro
import bglib.doc.bgwiki
import bglib.doc.mock
import bglib.doc.viewer_type


class ElementTest(unittest.TestCase):
  def setUp(self):
    self.stack = bglib.doc.bgwiki.ElementStack()

  def test_is_acceptable_of_Span(self):
    b = bglib.doc.bgwiki.BoldElement()
    i = bglib.doc.bgwiki.ItalicElement()
    isinstance(b, bglib.doc.bgwiki.SpanElement)
    isinstance(i, bglib.doc.bgwiki.SpanElement)
    self.assert_(i.is_acceptable(b))
    self.assert_(b.is_acceptable(i))

    self.assertEqual(
      self.stack.push(b),
      '<strong>'
    )
    self.assertEqual(
      self.stack.push(i),
      '<i>'
    )
    self.assertEqual(
      self.stack.empty(),
      '</i></strong>'
    )
    
  def test_is_acceptable_of_itemize(self):
    b = bglib.doc.bgwiki.BoldElement()
    i = bglib.doc.bgwiki.ItemizeElement()
    o = bglib.doc.bgwiki.ListElement()
    isinstance(i, bglib.doc.bgwiki.LineElement)
    isinstance(o, bglib.doc.bgwiki.BoxElement)
    self.assert_(i.is_acceptable(b))
    self.assert_(o.is_acceptable(i))
    self.assert_(o.is_acceptable(b))

    self.assertFalse(b.is_acceptable(o))
    self.assertFalse(b.is_acceptable(i))


class RegexpTest(unittest.TestCase):
  def setUp(self):
    pass
  def test_regexp(self):
    for p in bglib.doc.bgwiki.LineFormatter.patterns():
      print p
      r = re.compile(p)

class FormatterDuckTypeTest(bglib.doc.viewer_type.FormatterDuckTypeTest):
  def setUp(self):
    db = bglib.doc.mock.DataBaseMock()
    self.target = bglib.doc.bgwiki.Formatter(db)

class FormatterTest(unittest.TestCase):
  def setUp(self):
    db = bglib.doc.mock.DataBaseMock()
    stack = bglib.doc.bgwiki.ElementStack()
    macroprocessor = bglib.doc.macro.Processor(db)
    self.line = bglib.doc.bgwiki.LineFormatter(stack, macroprocessor)
    self.wiki = bglib.doc.bgwiki.Formatter(db)

  def test_bold(self):
    self.assertEqual(
      self.line.make_html(r"'''bold''', '''!''' can be bold too''', and '''! '''"),
      r"<strong>bold</strong>, <strong>''' can be bold too</strong>, and <strong>! </strong>")

  def test_italic(self):
    self.assertEqual(
      self.line.make_html(r"''italic''"),
      r"<i>italic</i>")

  def test_bolditalic(self):
    self.assertEqual(
      self.line.make_html(r"'''''bold italic'''''"),
      r"<strong><i>bold italic</i></strong>")

  def test_underline(self):
    self.assertEqual(
      self.line.make_html(r"__underline__"),
      r'<span class="underline">underline</span>')

  def test_monospace_1(self):
    self.assertEqual(
      self.line.make_html(r"`monospace`"),
      r'''<span class="monospace">monospace</span>''')

  def test_monospace_2(self):
    self.assertEqual(
      self.line.make_html(r"{{{monospace}}}"),
      r'''<span class="monospace">monospace</span>''')

  def test_strike(self):
    self.assertEqual(
      self.line.make_html(r"~~strike-through~~"),
      r"<del>strike-through</del>")

  def test_superscript(self):
    self.assertEqual(
      self.line.make_html(r"^superscript^"),
      r"<sup>superscript</sup> ")

  def test_superscript(self):
    self.assertEqual(
      self.line.make_html(r",,subscript,,"),
      r"<sub>subscript</sub>")

  def test_forced_br(self):
    self.assertEqual(
      self.line.make_html("Line 1[[BR]]Line 2\n"),
      'Line 1<br />Line 2\n')

  def test_itemize_style_unorder(self):
    self.assertEqual(
      self.wiki.make_html(" * Item 1\n"
                      "  * Item 1.1\n"
                      " * Item 2\n"),
      ('<ul>\n'
       '<li>Item 1\n'
       '<ul>\n'
       '<li>Item 1.1\n'
       '</li></ul>\n'
       '</li><li>Item 2\n'
       '</li></ul>\n'
       ))
  def test_itemize_style_order_numeric(self):
    self.assertEqual(
      self.wiki.make_html(" 1. Item 1\n"
                      "  1. Item 1.1\n"
                      " 1. Item 2\n"),
      ('<ol>\n'
       '<li>Item 1\n'
       '<ol>\n'
       '<li>Item 1.1\n'
       '</li></ol>\n'
       '</li><li>Item 2\n'
       '</li></ol>\n'
       ))

  def test_itemize_style_order_alpha(self):
    self.assertEqual(
      self.wiki.make_html(" a. Item 1\n"
                      "  1. Item 1.1\n"
                      " a. Item 2\n"),
      ('<ol class="loweralpha">\n'
       '<li>Item 1\n'
       '<ol>\n'
       '<li>Item 1.1\n'
       '</li></ol>\n'
       '</li><li>Item 2\n'
       '</li></ol>\n'
       ))

  def test_itemize_style_order_alpha_maxmin(self):
    self.assertEqual(
      self.wiki.make_html(" a. Item a\n"
                      " b. Item b\n"
                      " c. Item c\n"
                      " d. Item d\n"
                      " e. Item e\n"
                      " f. Item f\n"
                      " g. Item g\n"
                      " h. Item h\n"),
      ('<ol class="loweralpha">\n'
       '<li>Item a\n'
       '</li><li>Item b\n'
       '</li><li>Item c\n'
       '</li><li>Item d\n'
       '</li><li>Item e\n'
       '</li><li>Item f\n'
       '</li><li>Item g\n'
       '</li><li>Item h\n'
       '</li></ol>\n'
       ))

  def test_itemize_style_order_roman(self):
    self.assertEqual(
      self.wiki.make_html(" i. Item 1\n"
                      "  1. Item 1.1\n"
                      " i. Item 2\n"),
      ('<ol class="lowerroman">\n'
       '<li>Item 1\n'
       '<ol>\n'
       '<li>Item 1.1\n'
       '</li></ol>\n'
       '</li><li>Item 2\n'
       '</li></ol>\n'
       ))

  def test_itemize_style_order_roman_maxmin(self):
    self.assertEqual(
      self.wiki.make_html(" i. Item i\n"
                      " ii. Item ii\n"
                      " iii. Item iii\n"
                      " iv. Item iv\n"
                      " v. Item v\n"
                      " vi. Item vi\n"
                      " vii. Item vii\n"
                      " viii. Item viii\n"),
      ('<ol class="lowerroman">\n'
       '<li>Item i\n'
       '</li><li>Item ii\n'
       '</li><li>Item iii\n'
       '</li><li>Item iv\n'
       '</li><li>Item v\n'
       '</li><li>Item vi\n'
       '</li><li>Item vii\n'
       '</li><li>Item viii\n'
       '</li></ol>\n'
       ))


  def test_itemize_full(self):
    self.assertEqual(
      self.wiki.make_html(" * Item 1\n"
                      "  * Item 1.1\n"
                      " * Item 2\n"
                      "\n"
                      " 1. Item 1\n"
                      "  a. Item 1.a\n"
                      "  a. Item 1.b\n"
                      "   i. Item 1.b.i\n"
                      "   i. Item 1.b.ii\n"
                      " 1. Item 2\n"
                        ),
      ('<ul>\n'
       '<li>Item 1\n'
       '<ul>\n'
       '<li>Item 1.1\n'
       '</li></ul>\n'
       '</li><li>Item 2\n'
       '</li></ul>\n'
       '\n'
       '<ol>\n'
       '<li>Item 1\n'
       '<ol class="loweralpha">\n'
       '<li>Item 1.a\n'
       '</li><li>Item 1.b\n'
       '<ol class="lowerroman">\n'
       '<li>Item 1.b.i\n'
       '</li><li>Item 1.b.ii\n'
       '</li></ol>\n'
       '</li></ol>\n'
       '</li><li>Item 2\n'
       '</li></ol>\n'
      ))

  def test_itemize_plus_minus(self):
    self.assertEqual(
      self.wiki.make_html(
                      " - Item 1\n"
                      " + Item 2\n"
                      " -- Item 3\n"
                      " ++ Item 4\n"
                      " --- Item 5\n"
                      " +++ Item 6\n"
                        ),
      ('<ul class="sign">\n'
       '<li class="minus">Item 1\n'
       '</li><li class="plus">Item 2\n'
       '</li><li class="doubleminus">Item 3\n'
       '</li><li class="doubleplus">Item 4\n'
       '</li><li class="tripleminus">Item 5\n'
       '</li><li class="tripleplus">Item 6\n'
       '</li></ul>\n'
      ))

  def test_bad_indent(self):
    #AssertionError: '<ul>\n<ol>\n<li>\n</li></ol>\n</ul>\n' != '<ul>\n<li><ol>\n<li>Item 1\n'
    self.assertEqual(self.wiki.make_html('  8 '),
      ('<ul>\n'
       '<ol>\n'
       '<li>\n'
       '</li></ol>\n'
       '</ul>\n'
       )
    )

  def test_bad_indent_a(self):
    self.assertEqual(self.wiki.make_html('  a. Item a'),
      ('<ul>\n'
       '<ol class="loweralpha">\n'
       '<li>Item a\n'
       '</li></ol>\n'
       '</ul>\n'
       )
    )

  def test_bad_indent_i(self):
    self.assertEqual(self.wiki.make_html('  i. Item 1'),
      ('<ul>\n'
       '<ol class="lowerroman">\n'
       '<li>Item 1\n'
       '</li></ol>\n'
       '</ul>\n'
       )
    )

  def test_bad_indent_1(self):
    self.assertEqual(self.wiki.make_html('  1. Item 1'),
      ('<ul>\n'
       '<ol>\n'
       '<li>Item 1\n'
       '</li></ol>\n'
       '</ul>\n'
       )
    )


  def test_definition(self):
    self.assertEqual(
      self.wiki.make_html("llama::\n"
                      "  some kind of mammal, with hair\n"
                      "ppython::\n"
                      "  some kind of reptile, without hair\n"
                      "  (can you spot the typo?)\n"),
      ("<dl>\n"
       "<dt>llama</dt>\n"
       "<dd>some kind of mammal, with hair\n"
       "</dd><dt>ppython</dt>\n"
       "<dd>some kind of reptile, without hair\n"
       "(can you spot the typo?)\n"
       "</dd></dl>\n"
       ))

  def test_get_formatter_0(self):
    f = self.wiki.get_formatter()
    self.assert_(isinstance(f, bglib.doc.bgwiki.LineFormatter))

  def test_get_formatter_1(self):
    e = bglib.doc.bgwiki.WrappingFormatterElement()
    self.wiki.stack.push(e)
    f = self.wiki.get_formatter()
    self.assert_(isinstance(f, bglib.doc.bgwiki.WrappingFormatterElement))

  def test_preformatted_empty(self):
    self.assertEqual(
      self.wiki.make_html('{{{\n}}}\n'),
      '<pre class="wiki"></pre>\n')

  def test_preformatted_emptyline(self):
    self.assertEqual(
      self.wiki.make_html('{{{\n\n}}}\n'),
      '<pre class="wiki">\n</pre>\n')

  def test_preformatted_emptylines(self):
    self.assertEqual(
      self.wiki.make_html('{{{\n\n\n}}}\n'),
      '<pre class="wiki">\n\n</pre>\n')

  def test_preformatted(self):
    self.assertEqual(
      self.wiki.make_html('{{{\n'
                      '  def HelloWorld():\n'
                      '     print "Hello World"\n'
                      '}}}\n'),
      ('<pre class="wiki">  def HelloWorld():\n'
       '     print "Hello World"\n'
       '</pre>\n'))

  def test_preformatted_2(self):
    self.assertEqual(
      self.wiki.make_html('{{{\n'
                      '#!preformat\n'
                      '  def HelloWorld():\n'
                      '     print "Hello World"\n'
                      '}}}\n'),
      ('<pre class="wiki">  def HelloWorld():\n'
       '     print "Hello World"\n'
       '</pre>\n'))

  def test_blockquoate(self):
    self.assertEqual(
      self.wiki.make_html('  This text is a quote from someone else.\n'),
      ('<blockquote>\n'
       '<p>\n'
       'This text is a quote from someone else.\n'
       '</p>\n'
       '</blockquote>\n'))

  def test_blockquoate_multilines(self):
    self.assertEqual(
      self.wiki.make_html(
      '  This text is a quote from someone else.\n'
      '  quote continues.\n'
      'intermission is here\n'
      '  This text is an another quote from someone else.\n'),
      ('<blockquote>\n'
       '<p>\n'
       'This text is a quote from someone else.\n'
       'quote continues.\n'
       '</p>\n'
       '</blockquote>\n'
       'intermission is here\n'
       '<blockquote>\n'
       '<p>\n'
       'This text is an another quote from someone else.\n'
       '</p>\n'
       '</blockquote>\n'
       ))

  def test_DiscussionCitations(self):
    self.assertEqual(
      self.wiki.make_html(
        ">> Someone's original text\n"
        "> Someone else's reply text\n"
        "My reply text"),
      ('''<blockquote class="citation">\n'''
       '''<blockquote class="citation">\n'''
       '''<p>\n'''
       '''Someone's original text\n'''
       '''</p>\n'''
       '''</blockquote>\n'''
       '''<p>\n'''
       '''Someone else's reply text\n'''
       '''</p>\n'''
       '''</blockquote>\n'''
       '''My reply text'''))

  def test_table(self):
    self.assertEqual(
      self.wiki.make_html('''||Cell 1||Cell 2||Cell 3||\n'''
                      '''||Cell 4||Cell 5||Cell 6||\n'''),
      ('''<table class="wiki">\n'''
       '''<tr><td>Cell 1</td><td>Cell 2</td><td>Cell 3</td></tr>\n'''
       '''<tr><td>Cell 4</td><td>Cell 5</td><td>Cell 6</td></tr>\n'''
       '''</table>\n'''))

  def test_auto_anchor(self):
    self.assertEqual(
      self.line.make_html('''http://www.tonic-water.com/'''),
      '<a class="ext-link" href="http://www.tonic-water.com/"><span class="icon">http://www.tonic-water.com/</span></a>')

  def test_auto_anchor_https(self):
    self.assertEqual(
      self.line.make_html('''https://www.tonic-water.com/'''),
      '<a class="ext-link" href="https://www.tonic-water.com/"><span class="icon">https://www.tonic-water.com/</span></a>')

  def test_external_anchor_noname(self):
    self.assertEqual(
      self.line.make_html('''[http://www.tonic-water.com/]'''),
      '''<a class="ext-link" href="http://www.tonic-water.com/"><span class="icon">http://www.tonic-water.com/</span></a>''')

  def test_external_anchor_named(self):
    self.assertEqual(
      self.line.make_html('''[http://www.tonic-water.com/ Nori's personal server]'''),
      '''<a class="ext-link" href="http://www.tonic-water.com/"><span class="icon">Nori's personal server</span></a>''')

  def test_wikiname_by_camelcase(self):
    self.assertEqual(
      self.line.make_html('''BackgammonBase'''),
      '''<a class="wiki-link" href="/wiki/BackgammonBase">'''
      '''BackgammonBase</a>''')

  def test_wikiname_by_scheme_1(self):
    self.assertEqual(
      self.line.make_html('''[wiki:BackgammonBase]'''),
      '''<a class="wiki-link" href="/wiki/BackgammonBase">'''
      '''BackgammonBase</a>''')

  def test_wikiname_by_scheme_2(self):
    self.assertEqual(
      self.line.make_html('''[wiki:blot]'''),
      '''<a class="wiki-link" href="/wiki/blot">'''
      '''blot</a>''')

  def test_entry_link(self):
    self.assertEqual(
      self.line.make_html('''Entry: #1 or entry:1'''),
      'Entry: <a class="entry" href="/entry/1" title="title">#1</a> '
      'or <a class="entry" href="/entry/1" title="title">entry:1</a>')

  def test_query_link(self):
    self.assertEqual(
      self.line.make_html('''Query: {1} or query:1'''),
      'Query: <a class="query" href="/query/1">{1}</a> or <a class="query" href="/query/1">query:1</a>')

  def test_match_link(self):
    self.assertEqual(
      self.line.make_html('''Match: m1, [1] or match:1'''),
      'Match: <a class="match" href="/match/1">m1</a>, '
      '<a class="match" href="/match/1">[1]</a> '
      'or <a class="match" href="/match/1">match:1</a>')

  def test_escaping_link(self):
    self.assertEqual(
      self.line.make_html('''!#42 is not a link'''),
      '#42 is not a link')

  def test_macros(self):
    self.assertEqual(
      self.line.make_html('''[[Timestamp]]'''),
      '<b>Sun Jul 27 08:59:07 2008</b>')

  def test_macro_analysis_move(self):
    self.assertEqual(
      self.wiki.make_html('[[Analysis(cNcxAxCY54YBBg:cAn7ADAAIAAA)]]'),
      ('''<table>\n'''
'''<tr class='headerrow'><th rowspan='2'>#</th><th rowspan='2'>move</th><th rowspan='2'>Ply</th><th colspan='6'> Eq.(diff)</th></tr>\n'''
'''<tr class='headerrow'><th>Win</th><th>WinG</th><th>WinBg</th><th>Lose</th><th>LoseG</th><th>LoseBg</th></tr>\n'''
'''<tr class='oddrow'><th rowspan='2'>1</th><td rowspan='2'>21/15(2) 13/7(2)</td><td rowspan='2'>2</td><td class='Equity' colspan='6'> +0.975 </td></tr>\n'''
'''<tr class='oddrow'><td>0.8</td><td>0.1</td><td>0.0</td><td>0.2</td><td>0.0</td><td>0.0</td></tr>\n'''
'''<tr class='evenrow'><th rowspan='2'>2</th><td rowspan='2'>21/9(2)</td><td rowspan='2'>2</td><td class='Equity' colspan='6'> +0.914 (-0.061) </td></tr>\n'''
'''<tr class='evenrow'><td>0.7</td><td>0.1</td><td>0.0</td><td>0.3</td><td>0.0</td><td>0.0</td></tr>\n'''
'''<tr class='oddrow'><th rowspan='2'>3</th><td rowspan='2'>21/15(2) 8/2*(2)</td><td rowspan='2'>0</td><td class='Equity' colspan='6'> +0.614 (-0.362) </td></tr>\n'''
'''<tr class='oddrow'><td>0.7</td><td>0.2</td><td>0.0</td><td>0.3</td><td>0.1</td><td>0.0</td></tr>\n'''
       '''</table>\n'''))
  def test_macro_analysis_cube(self):
    self.assertEqual(
      self.make_html('[[Analysis(vzsAAFhu2xFABA:QYkqASAAIAAA)]]'),
      ('''<table>\n'''
       '''<tr class='headerrow'><th rowspan='2'>Ply</th><th colspan='6'> Cubeless Eq. </th></tr>\n'''
       '''<tr class='headerrow'><th>Win</th><th>WinG</th><th>WinBg</th><th>Lose</th><th>LoseG</th><th>LoseBg</th></tr>\n'''
       '''<tr class='oddrow'><td rowspan='2'>2</td><td class='Equity' colspan='6'> +0.011 (Moeny +0.008) </td></tr>\n'''
       '''<tr class='oddrow'><td>0.5</td><td>0.1</td><td>0.0</td><td>0.5</td><td>0.1</td><td>0.0</td></tr>\n'''
       '''</table>\n'''
       '''<table>\n'''
       '''<tr class='headerrow'><th>#</th><th>action</th><th colspan='2'> Cubeful Eq. </th></tr>\n'''
       '''<tr class='actualrow'><th>1</th><td> No double </td><td> +0.236 </td><td>  </td></tr>\n'''
       '''<tr class='evenrow'><th>2</th><td> Double, pass </td><td> +0.236 </td><td> +0.764 </td></tr>\n'''
       '''<tr class='oddrow'><th>3</th><td> Double, take </td><td> -0.096 </td><td> -0.332 </td></tr>\n'''
       '''</table>\n'''))


  def test_escape_lt(self):
    self.assertEqual(
      self.line.make_html('<'),
      '&lt;')

  def test_escape_gt(self):
    self.assertEqual(
      self.line.make_html('>'),
      '&gt;')

  def test_escape_amp(self):
    self.assertEqual(
      self.line.make_html('&'),
      '&amp;')

  def test_escape_combined(self):
    self.assertEqual(
      self.line.make_html('&<>'),
      '&amp;&lt;&gt;')

  def test_escape_wiki(self):
    self.assertEqual(
      self.line.make_html('!HogeHoge'),
      'HogeHoge')

  def test_escape_combined(self):
    self.assertEqual(
      self.line.make_html('!&<>'),
      '!&amp;&lt;&gt;')

  def test_extract_references_wikiname_by_camelcase(self):
    d = self.wiki.extract_references('''BackgammonBase'''),
    self.assert_('wikiname' in d)
    self.assertEqual(d['wikiname'], ["BackgammonBase"])

  def test_wikiname_by_scheme_1(self):
    self.assertEqual('''[wiki:BackgammonBase]'''),
    self.assert_('wikiname' in d)
    self.assertEqual(d['wikiname'], ["BackgammonBase"])

  def test_wikiname_by_scheme_2(self):
    self.assertEqualself.line.make_html('''[wiki:blot]'''),
    self.assert_('wikiname' in d)
    self.assertEqual(d['wikiname'], ["blot"])

  def test_extract_references_wikinames(self):
    d = self.wiki.extract_references('''BackgammonBase, [wiki:blot]'''),
    self.assert_('wikiname' in d)
    self.assertEqual(d['wikiname'], ["BackgammonBase", "blot"])

  def test_extract_references_entry_1(self):
    d = self.wiki.extract_references('''Entry: #1 or entry:1'''),
    self.assert_('entry' in d)
    self.assertEqual(d['entry'], [1])

  def test_extract_references_entry_1(self):
    d = self.wiki.extract_references('''Entry: #1 or entry:2'''),
    self.assert_('entry' in d)
    self.assertEqual(d['entry'], [1, 2])

  def test_extract_references_query_1(self):
    d = self.wiki.extract_references('''Query: {1} or query:1''')
    self.assert_('query' in d)
    self.assertEqual(d['query'], [1])

  def test_extract_references_query_2(self):
    d = self.wiki.extract_references('''Query: {1} or query:2''')
    self.assert_('query' in d)
    self.assertEqual(d['query'], [1, 2])

  def test_extract_references_match_link_1(self):
    d = self.wiki.extract_references('''Match: m1, [1] or match:1''')
    self.assert_('query' in d)
    self.assertEqual(d['match'], [1])

  def test_extract_references_match_link_2(self):
    d = self.wiki.extract_references('''Match: m2, [1] or match:3''')
    self.assert_('query' in d)
    self.assertEqual(d['match'], [1, 2, 3])

  def test_extract_references_escaping_link(self):
    d = self.wiki.extract_references('''!#42 is not a link''')
    self.assert_('entry' in d)
    self.assert_(42 not in d['entry'])

  def test_extract_references_analysis(self):
    d = self.wiki.extract_references('Analysis(cNcxAxCY54YBBg:cAn7ADAAIAAA)')
    self.assert_('Analysis' in d)
    self.assert_('cNcxAxCY54YBBg:cAn7ADAAIAAA' in d['Analysis'])



