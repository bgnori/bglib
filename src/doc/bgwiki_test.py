#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2006-2008 Noriyuki Hosaka nori@backgammon.gr.jp
#
import re
#import unittest

import bglib.doc.macro
import bglib.doc.bgwiki
import bglib.doc.mock
import bglib.doc.viewer_type
import bglib.doc.html


class RegexpTest(bglib.doc.html.HtmlTestCase):
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

class FormatterTest(bglib.doc.html.HtmlTestCase):
  def setUp(self):
    db = bglib.doc.mock.DataBaseMock()
    #stack = bglib.doc.bgwiki.ElementStack()
    #macroprocessor = bglib.doc.macro.Processor(db)
    bglib.doc.macro.setup(db)
    self.wiki = bglib.doc.bgwiki.Formatter(db)
    self.line = bglib.doc.bgwiki.LineFormatter(self.wiki.editor)
    #, macroprocessor)

  def test_bold(self):
    self.line.parse(r"""'''bold''', '''!''' can be bold too''', and '''! '''""")
    self.assertHtmlEqual(
      self.line.make_html(),
      r"""<strong>bold</strong>, <strong>''' can be bold too</strong>, and <strong>! </strong>""")

  def test_italic(self):
    self.line.parse(r"""''italic''""")
    self.assertHtmlEqual(
      self.line.make_html(),
      r'''<i>italic</i>''')

  def test_bolditalic(self):
    self.line.parse(r"""'''''bold italic'''''""")
    self.assertHtmlEqual(
      self.line.make_html(),
      r'''<strong><i>bold italic</i></strong>''')

  def test_underline(self):
    self.line.parse(r'''__underline__''')
    self.assertHtmlEqual(
      self.line.make_html(),
      r'''<span class="underline">underline</span>''')

  def test_monospace_1(self):
    self.line.parse(r'''`monospace`'''),
    self.assertHtmlEqual(
      self.line.make_html(),
      r'''<span class="monospace">monospace</span>''')

  def test_monospace_2(self):
    self.line.parse(r'''{{{monospace}}}''')
    self.assertHtmlEqual(
      self.line.make_html(),
      r'''<span class="monospace">monospace</span>''')

  def test_strike(self):
    self.line.parse(r'''~~strike-through~~''')
    self.assertHtmlEqual(
      self.line.make_html(),
      r'''<del>strike-through</del>''')

  def test_superscript(self):
    self.line.parse(r'''^superscript^''')
    self.assertHtmlEqual(
      self.line.make_html(),
      r'''<sup>superscript</sup> ''')

  def test_superscript(self):
    self.line.parse(r''',,subscript,,''')
    self.assertHtmlEqual(
      self.line.make_html(),
      r'''<sub>subscript</sub>''')

  def test_forced_br(self):
    self.line.parse('''Line 1[[BR]]Line 2\n''')
    self.assertHtmlEqual(
      self.line.make_html(),
      '''Line 1<br />Line 2\n''')

  def test_heading_h1(self):
    self.wiki.parse('''= heading =\n''')
    self.assertHtmlEqual(
      self.wiki.make_html(),
      '''<h1>heading</h1>\n''')

  def test_heading_h2(self):
    self.wiki.parse('''== heading ==\n''')
    self.assertHtmlEqual(
      self.wiki.make_html(),
      '''<h2>heading</h2>\n''')

  def test_heading_h3(self):
    self.wiki.parse('''=== heading ===\n''')
    self.assertHtmlEqual(
      self.wiki.make_html(),
      '''<h3>heading</h3>\n''')

  def test_itemize_style_unorder(self):
    self.wiki.parse(''' * Item 1\n'''
                    '''  * Item 1.1\n'''
                    ''' * Item 2\n''')
    self.assertHtmlEqual(
      self.wiki.make_html(),
      ('''<ul>\n'''
       '''<li>Item 1\n'''
       '''<ul>\n'''
       '''<li>Item 1.1\n'''
       '''</li></ul>\n'''
       '''</li><li>Item 2\n'''
       '''</li></ul>\n'''
       ))
  def test_itemize_style_order_numeric(self):
    self.wiki.parse(''' 1. Item 1\n'''
                      '''  1. Item 1.1\n'''
                      ''' 1. Item 2\n'''),
    self.assertHtmlEqual(
      self.wiki.make_html(),
      ('''<ol>\n'''
       '''<li>Item 1\n'''
       '''<ol>\n'''
       '''<li>Item 1.1\n'''
       '''</li></ol>\n'''
       '''</li><li>Item 2\n'''
       '''</li></ol>\n'''
       ))

  def test_itemize_style_order_alpha(self):
    self.wiki.parse(''' a. Item 1\n'''
'''  1. Item 1.1\n'''
''' a. Item 2\n'''),
    self.assertHtmlEqual(
      self.wiki.make_html(),
      ('''<ol class="loweralpha">\n'''
       '''<li>Item 1\n'''
       '''<ol>\n'''
       '''<li>Item 1.1\n'''
       '''</li></ol>\n'''
       '''</li><li>Item 2\n'''
       '''</li></ol>\n'''
       ))

  def test_itemize_style_order_alpha_maxmin(self):
    self.wiki.parse(''' a. Item a\n'''
                    ''' b. Item b\n'''
                    ''' c. Item c\n'''
                    ''' d. Item d\n'''
                    ''' e. Item e\n'''
                    ''' f. Item f\n'''
                    ''' g. Item g\n'''
                    ''' h. Item h\n'''),
    self.assertHtmlEqual(
      self.wiki.make_html(),
      ('''<ol class="loweralpha">\n'''
       '''<li>Item a\n'''
       '''</li><li>Item b\n'''
       '''</li><li>Item c\n'''
       '''</li><li>Item d\n'''
       '''</li><li>Item e\n'''
       '''</li><li>Item f\n'''
       '''</li><li>Item g\n'''
       '''</li><li>Item h\n'''
       '''</li></ol>\n'''
       ))

  def test_itemize_style_order_roman(self):
    self.wiki.parse(''' i. Item 1\n'''
                    '''  1. Item 1.1\n'''
                    ''' i. Item 2\n''')
    self.assertHtmlEqual(
      self.wiki.make_html(),
      ('''<ol class="lowerroman">\n'''
       '''<li>Item 1\n'''
       '''<ol>\n'''
       '''<li>Item 1.1\n'''
       '''</li></ol>\n'''
       '''</li><li>Item 2\n'''
       '''</li></ol>\n'''
       ))

  def test_itemize_style_order_roman_maxmin(self):
    self.wiki.parse(''' i. Item i\n'''
                    ''' ii. Item ii\n'''
                    ''' iii. Item iii\n'''
                    ''' iv. Item iv\n'''
                    ''' v. Item v\n'''
                    ''' vi. Item vi\n'''
                    ''' vii. Item vii\n'''
                    ''' viii. Item viii\n'''
                    )
    self.assertHtmlEqual(
      self.wiki.make_html(),
      ('''<ol class="lowerroman">\n'''
       '''<li>Item i\n'''
       '''</li><li>Item ii\n'''
       '''</li><li>Item iii\n'''
       '''</li><li>Item iv\n'''
       '''</li><li>Item v\n'''
       '''</li><li>Item vi\n'''
       '''</li><li>Item vii\n'''
       '''</li><li>Item viii\n'''
       '''</li></ol>\n'''
       ))


  def test_itemize_full(self):
    self.wiki.parse(
        ''' * Item 1\n'''
        '''  * Item 1.1\n'''
        ''' * Item 2\n'''
        '''\n'''
        ''' 1. Item 1\n'''
        '''  a. Item 1.a\n'''
        '''  a. Item 1.b\n'''
        '''   i. Item 1.b.i\n'''
        '''   i. Item 1.b.ii\n'''
        ''' 1. Item 2\n'''
                        ),
    self.assertHtmlEqual(
      self.wiki.make_html(),
      ('''<ul>\n'''
       '''<li>Item 1\n'''
       '''<ul>\n'''
       '''<li>Item 1.1\n'''
       '''</li></ul>\n'''
       '''</li><li>Item 2\n'''
       '''</li></ul>\n'''
       '''\n'''
       '''<ol>\n'''
       '''<li>Item 1\n'''
       '''<ol class="loweralpha">\n'''
       '''<li>Item 1.a\n'''
       '''</li><li>Item 1.b\n'''
       '''<ol class="lowerroman">\n'''
       '''<li>Item 1.b.i\n'''
       '''</li><li>Item 1.b.ii\n'''
       '''</li></ol>\n'''
       '''</li></ol>\n'''
       '''</li><li>Item 2\n'''
       '''</li></ol>\n'''
      ))

  def test_itemize_plus_minus(self):
    self.wiki.parse(
        ''' - Item 1\n'''
        ''' + Item 2\n'''
        ''' -- Item 3\n'''
        ''' ++ Item 4\n'''
        ''' --- Item 5\n'''
        ''' +++ Item 6\n'''
                        ),
    self.assertHtmlEqual(
      self.wiki.make_html(),
      ( '''<ul class="sign">\n'''
        '''<li class="minus">Item 1\n'''
        '''</li><li class="plus">Item 2\n'''
        '''</li><li class="doubleminus">Item 3\n'''
        '''</li><li class="doubleplus">Item 4\n'''
        '''</li><li class="tripleminus">Item 5\n'''
        '''</li><li class="tripleplus">Item 6\n'''
        '''</li></ul>\n'''
      ))

  def test_bad_indent(self):
    self.wiki.parse('''  8 ''')
    #AssertionError: "<ul>\n<ol>\n<li>\n</li></ol>\n</ul>\n" != "<ul>\n<li><ol>\n<li>Item 1\n'''
    self.assertHtmlEqual(self.wiki.make_html(),
      ( '''<ul>\n'''
        '''<ol>\n'''
        '''<li>\n'''
        '''</li></ol>\n'''
        '''</ul>\n'''
       )
    )

  def test_bad_indent_a(self):
    self.wiki.parse('''  a. Item a''')
    self.assertHtmlEqual(self.wiki.make_html(),
      ( '''<ul>\n'''
        '''<ol class="loweralpha">\n'''
        '''<li>Item a\n'''
        '''</li></ol>\n'''
        '''</ul>\n'''
       )
    )

  def test_bad_indent_i(self):
    self.wiki.parse('''  i. Item 1''')
    self.assertHtmlEqual(self.wiki.make_html(),
      ('''<ul>\n'''
       '''<ol class="lowerroman">\n'''
       '''<li>Item 1\n'''
       '''</li></ol>\n'''
       '''</ul>\n'''
       )
    )

  def test_bad_indent_1(self):
    self.wiki.parse('''  1. Item 1''')
    self.assertHtmlEqual(self.wiki.make_html(),
      ('''<ul>\n'''
       '''<ol>\n'''
       '''<li>Item 1\n'''
       '''</li></ol>\n'''
       '''</ul>\n'''
       )
    )


  def test_definition(self):
    self.wiki.parse(
       '''llama::\n'''
       '''  some kind of mammal, with hair\n'''
       '''ppython::\n'''
       '''  some kind of reptile, without hair\n'''
       '''  (can you spot the typo?)\n'''
       )
    self.assertHtmlEqual(
      self.wiki.make_html(),
      (
       '''<dl>\n'''
       '''<dt>llama</dt>\n'''
       '''<dd>some kind of mammal, with hair\n'''
       '''</dd><dt>ppython</dt>\n'''
       '''<dd>some kind of reptile, without hair\n'''
       '''(can you spot the typo?)\n'''
       '''</dd></dl>\n'''
       ))

  def test_complicated_definition(self):
    self.wiki.parse(
       '''[wiki:backgammon]::\n'''
       '''  some kind of board game for two players, with two dice and 15 chequers for each player\n'''
       '''BackgammonBase::\n'''
       '''  Web application to learn backgammon effectively.\n'''
       )

    print self.wiki.make_html()
    self.assertHtmlEqual(
      self.wiki.make_html(),
      (
       '''<dl>'''
       '''<dt><a href="/wiki/backgammon" class="wiki-link" title="backgammon">backgammon</a>\n</dt>'''
       '''<dd>some kind of board game for two players, with two dice and 15 chequers for each player\n</dd>'''
       '''<dt><a href="/wiki/BackgammonBase" class="wiki-link" title="BackgammonBase">BackgammonBase</a>\n</dt>'''
       '''<dd>Web application to learn backgammon effectively.\n</dd>'''
       '''</dl>'''
       ))

  def test_itemize_in_definition(self):
    self.wiki.parse(
       '''hitting::\n'''
       ''' * gains pips.\n'''
       ''' * gains tempo.\n'''
       ''' * may dance.\n'''
       ''' * put hit chequers behind of the prime.\n'''
       )
    print self.wiki.make_html()
    self.assertHtmlEqual(
      self.wiki.make_html(),
      (
       '''<dl>\n'''
       '''<dt>hitting</dt>\n'''
       '''<dd><ul>'''
       '''<li>gains pips.</li>'''
       '''<li>gains tempo.</li>'''
       '''<li>may dance.</li>'''
       '''<li>put hit chequers behind of the prime.</li>'''
       '''</ul>'''
       '''</dd></dl>\n'''
       ))

  def test_itemize_and_text_in_definition(self):
    self.wiki.parse(
       '''hitting::\n'''
       ''' merits are\n'''
       ''' * gains pips.\n'''
       ''' * gains tempo.\n'''
       ''' * may dance.\n'''
       ''' * put hit chequers behind of the prime.\n'''
       )

    print self.wiki.make_html()
    self.assertHtmlEqual(
      self.wiki.make_html(),
      (
       '''<dl>\n'''
       '''<dt>hitting</dt>\n'''
       '''<dd> merits are<ul>'''
       '''<li>gains pips.</li>'''
       '''<li>gains tempo.</li>'''
       '''<li>may dance.</li>'''
       '''<li>put hit chequers behind of the prime.</li>'''
       '''</ul>'''
       '''</dd></dl>\n'''
       ))

  def test_complex_mix_of_itemize_and_definition(self):
    self.wiki.parse(
       '''hitting::\n'''
       '''  * gains pips.\n'''
       ''' * gains tempo.\n'''
       '''  * may dance.\n'''
       ''' * put hit chequers behind of the prime.\n'''
       '''  these are merits.(this is in dd, not in li)\n'''
       '''\n'''
       '''this is not in dl'''
       )
    print self.wiki.make_html()
    self.assertHtmlEqual(
      self.wiki.make_html(),
      (
       '''<dl>\n'''
       '''<dt>hitting</dt>\n'''
       '''<dd><ul><ul>'''
       '''<li>gains pips.</li>'''
       '''</ul>'''
       '''<li>gains tempo.'''
       '''<ul>'''
       '''<li>may dance.</li>'''
       '''</ul>'''
       '''</li>'''
       '''<li>put hit chequers behind of the prime.</li>'''
       '''</ul>'''
       '''these are merits.(this is in dd, not in li)\n'''
       '''</dd></dl>\n'''
       '''this is not in dl'''
       ))

  def test_wikiname_in_definition(self):
    self.wiki.parse(
       '''Trice::\n'''
       '''  WalterTrice is author of backgammon boot camp.'''
       )

    print self.wiki.make_html()
    self.assertHtmlEqual(
      self.wiki.make_html(),
      (
       '''<dl>\n'''
       '''<dt>Trice</dt>\n'''
       '''<dd>\n'''
       '''<a href="/wiki/WalterTrice" class="wiki-link" title="WalterTrice">WalterTrice</a>'''
       '''is author of backgammon boot camp.'''
       '''</dd></dl>\n'''
       ))

  def test_get_formatter_0(self):
    f = self.wiki.get_formatter()
    self.assert_(isinstance(f, bglib.doc.bgwiki.LineFormatter))

  def test_get_formatter_1(self):
    self.wiki.editor.enter(bglib.doc.bgwiki.WrappingFormatterElement)
    f = self.wiki.get_formatter()
    self.assert_(isinstance(f, bglib.doc.bgwiki.WrappingFormatterElement))

  def test_preformatted_empty(self):
    self.wiki.parse('''{{{\n}}}\n''')
    self.assertHtmlEqual(
      self.wiki.make_html(),
      '''<pre class="wiki"></pre>\n''')

  def test_preformatted_emptyline(self):
    self.wiki.parse('''{{{\n\n}}}\n''')
    self.assertHtmlEqual(
      self.wiki.make_html(),
      '''<pre class="wiki">\n</pre>\n''')

  def test_preformatted_emptylines(self):
    self.wiki.parse('''{{{\n\n\n}}}\n''')
    self.assertHtmlEqual(
      self.wiki.make_html(),
      '''<pre class="wiki">\n\n</pre>\n''')

  def test_preformatted(self):
    self.wiki.parse('''{{{\n'''
'''  def HelloWorld():\n'''
'''     print "Hello World"\n'''
'''}}}\n''')
    self.assertHtmlEqual(
      self.wiki.make_html(),
      ('''<pre class="wiki">  def HelloWorld():\n'''
'''     print "Hello World"\n'''
'''</pre>\n'''))

  def test_preformatted_2(self):
    self.wiki.parse('''{{{\n'''
'''#!preformat\n'''
'''  def HelloWorld():\n'''
'''     print "Hello World"\n'''
'''}}}\n'''),
    self.assertHtmlEqual(
      self.wiki.make_html(),
      ('''<pre class="wiki">  def HelloWorld():\n'''
'''     print "Hello World"\n'''
'''</pre>\n'''))

  def test_blockquoate(self):
    self.wiki.parse('''  This text is a quote from someone else.\n''')
    self.assertHtmlEqual(
      self.wiki.make_html(),
      ('''<blockquote>\n'''
'''<p>\n'''
'''This text is a quote from someone else.\n'''
'''</p>\n'''
'''</blockquote>\n'''))

  def test_blockquoate_multilines(self):
    self.wiki.parse(
'''  This text is a quote from someone else.\n'''
'''  quote continues.\n'''
'''intermission is here\n'''
'''  This text is an another quote from someone else.\n''')
    self.assertHtmlEqual(
      self.wiki.make_html(),
      ('''<blockquote>\n'''
'''<p>\n'''
'''This text is a quote from someone else.\n'''
'''quote continues.\n'''
'''</p>\n'''
'''</blockquote>\n'''
'''intermission is here\n'''
'''<blockquote>\n'''
'''<p>\n'''
'''This text is an another quote from someone else.\n'''
'''</p>\n'''
'''</blockquote>\n'''
       ))

  def test_DiscussionCitations(self):
    self.wiki.parse(
'''>> Someone"s original text\n'''
'''> Someone else"s reply text\n'''
'''My reply text''')
    self.assertHtmlEqual(
      self.wiki.make_html(),
      ('''<blockquote class="citation">\n'''
       '''<blockquote class="citation">\n'''
       '''<p>\n'''
       '''Someone"s original text\n'''
       '''</p>\n'''
       '''</blockquote>\n'''
       '''<p>\n'''
       '''Someone else"s reply text\n'''
       '''</p>\n'''
       '''</blockquote>\n'''
       '''My reply text'''))

  def test_table(self):
    self.wiki.parse('''||Cell 1||Cell 2||Cell 3||\n'''
                      '''||Cell 4||Cell 5||Cell 6||\n''')
    self.assertHtmlEqual(
      self.wiki.make_html(),
      ('''<table class="wiki">\n'''
       '''<tr><td>Cell 1</td><td>Cell 2</td><td>Cell 3</td></tr>\n'''
       '''<tr><td>Cell 4</td><td>Cell 5</td><td>Cell 6</td></tr>\n'''
       '''</table>\n'''))

  def test_auto_anchor(self):
    self.line.parse('''http://www.tonic-water.com/''')
    self.assertHtmlEqual(
      self.line.make_html(),
      ('''<a href="http://www.tonic-water.com/" class="ext-link" title="title">'''
'''<span class="icon">http://www.tonic-water.com/</span></a>'''))

  def test_auto_anchor_https(self):
    self.line.parse('''https://www.tonic-water.com/''')
    self.assertHtmlEqual(
      self.line.make_html(),
      ('''<a href="https://www.tonic-water.com/" class="ext-link" title="title">'''
'''<span class="icon">https://www.tonic-water.com/</span></a>'''))

  def test_external_anchor_noname(self):
    self.line.parse('''[http://www.tonic-water.com/]''')
    self.assertHtmlEqual(
      self.line.make_html(),
      ('''<a href="http://www.tonic-water.com/" class="ext-link" title="http://www.tonic-water.com/">'''
      '''<span class="icon">http://www.tonic-water.com/</span></a>'''))

  def test_external_anchor_named(self):
    self.line.parse('''[http://www.tonic-water.com/ Nori's personal server]''')
    self.assertHtmlEqual(
      self.line.make_html(),
      ('''<a href="http://www.tonic-water.com/" class="ext-link" title="Nori's personal server">'''
       '''<span class="icon">Nori's personal server</span></a>'''))

  def test_wikiname_by_camelcase(self):
    self.line.parse('''BackgammonBase''')
    self.assertHtmlEqual(
      self.line.make_html(),
      '''<a href="/wiki/BackgammonBase" class="wiki-link" title="BackgammonBase">'''
      '''BackgammonBase</a>''')

  def test_wikiname_by_scheme_1(self):
    self.line.parse('''[wiki:BackgammonBase]''')
    self.assertHtmlEqual(
      self.line.make_html(),
      '''<a href="/wiki/BackgammonBase" class="wiki-link" title="BackgammonBase">'''
      '''BackgammonBase</a>''')

  def test_wikiname_by_scheme_2(self):
    self.line.parse('''[wiki:blot]''')
    self.assertHtmlEqual(
      self.line.make_html(),
      '''<a href="/wiki/blot" class="wiki-link" title="blot">'''
      '''blot</a>''')

  def test_entry_link(self):
    self.line.parse('''Entry: #1 or entry:1''')
    self.assertHtmlEqual(
      self.line.make_html(),
'''Entry: <a href="/entry/1" class="entry" title="#1">#1</a> '''
'''or <a href="/entry/1" class="entry" title="entry:1">entry:1</a>''')

  def test_query_link(self):
    self.line.parse('''Query: {1} or query:1''')
    self.assertHtmlEqual(
      self.line.make_html(),
'''Query: <a href="/query/1" class="query" title="{1}">{1}</a>'''
''' or <a href="/query/1" class="query" title="query:1">query:1</a>''')

  def test_match_link(self):
    self.line.parse('''Match: m1, [1] or match:1''')
    self.assertHtmlEqual(
      self.line.make_html(),
'''Match: <a class="match" title="title" href="/match/1">m1</a>, '''
'''<a class="match" title="title" href="/match/1">[1]</a> '''
'''or <a class="match" title="title" href="/match/1">match:1</a>''')

  def test_escaping_link(self):
    self.line.parse('''!#42 is not a link''')
    self.assertHtmlEqual(
      self.line.make_html(),
'''#42 is not a link''')

  def test_macro_timestamp(self):
    self.line.parse('''[[Timestamp]]''')
    self.assertHtmlEqual(
      self.line.make_html(),
'''<b>Sun Jul 27 08:59:07 2008</b>''')

  def test_macro_BR(self):
    self.line.parse('''[[BR]]''')
    self.assertHtmlEqual(
      self.line.make_html(),
'''<br />''')

  def test_macro_Position_1(self):
    self.line.parse('''[[Position(vzsAAFhu2xFABA:QYkqASAAIAAA)]]''')
    print self.line.make_html()
    self.assertHtmlEqual(
      self.line.make_html(),
      ('''<span class="position">\n'''
           '''<img src="/image?format=png'''
           '''&pid=vzsAAFhu2xFABA'''
           '''&mid=QYkqASAAIAAA'''
           '''&height=300&width=400&css=minimal" />\n'''
       '''</span>\n'''))

  def test_macro_Position_2(self):
    self.line.parse('''[[Position(jM/BATDQc+QBMA:cAkWAAAAAAAA)]]''')
    print self.line.make_html()
    self.assertHtmlEqual(
      self.line.make_html(),
      ('''<span class="position">\n'''
           '''<img src="/image?format=png'''
           '''&pid=jM%2FBATDQc%2BQBMA'''
           '''&mid=cAkWAAAAAAAA'''
           '''&height=300&width=400&css=minimal" />\n'''
       '''</span>\n'''))

  def test_macro_analysis_move(self):
    self.wiki.parse('''[[Analysis(cNcxAxCY54YBBg:cAn7ADAAIAAA)]]''')
    self.assertHtmlEqual(
      self.wiki.make_html(),
      (
       '''<table class="move">\n'''
       '''<tr class="headerrow"><th rowspan="2">#</th><th rowspan="2">move</th><th rowspan="2">Ply</th><th colspan="6"> Eq.(diff)</th></tr>\n'''
       '''<tr class="headerrow"><th>Win</th><th>WinG</th><th>WinBg</th><th>Lose</th><th>LoseG</th><th>LoseBg</th></tr>\n'''
       '''<tr class="oddrow"><th rowspan="2">1</th><td rowspan="2">21/15(2) 13/7(2)</td><td rowspan="2">2</td><td class="Equity" colspan="6"> +0.975 </td></tr>\n'''
       '''<tr class="oddrow"><td>0.8</td><td>0.1</td><td>0.0</td><td>0.2</td><td>0.0</td><td>0.0</td></tr>\n'''
       '''<tr class="evenrow"><th rowspan="2">2</th><td rowspan="2">21/9(2)</td><td rowspan="2">2</td><td class="Equity" colspan="6"> +0.914 (-0.061) </td></tr>\n'''
       '''<tr class="evenrow"><td>0.7</td><td>0.1</td><td>0.0</td><td>0.3</td><td>0.0</td><td>0.0</td></tr>\n'''
       '''<tr class="oddrow"><th rowspan="2">3</th><td rowspan="2">21/15(2) 8/2*(2)</td><td rowspan="2">0</td><td class="Equity" colspan="6"> +0.614 (-0.362) </td></tr>\n'''
       '''<tr class="oddrow"><td>0.7</td><td>0.2</td><td>0.0</td><td>0.3</td><td>0.1</td><td>0.0</td></tr>\n'''
       '''</table>\n'''
      ))

  def test_macro_analysis_cube(self):
    self.wiki.parse('''[[Analysis(vzsAAFhu2xFABA:QYkqASAAIAAA)]]''')
    self.assertHtmlEqual(
      self.wiki.make_html(),
      ('''<table class="cubeless">\n'''
       '''<tr class="headerrow"><th rowspan="2">Ply</th><th colspan="6"> Cubeless Eq. </th></tr>\n'''
       '''<tr class="headerrow"><th>Win</th><th>WinG</th><th>WinBg</th><th>Lose</th><th>LoseG</th><th>LoseBg</th></tr>\n'''
       '''<tr class="oddrow"><td rowspan="2">2</td><td class="Equity" colspan="6"> +0.011 (Money +0.008) </td></tr>\n'''
       '''<tr class="oddrow"><td>0.5</td><td>0.1</td><td>0.0</td><td>0.5</td><td>0.1</td><td>0.0</td></tr>\n'''
       '''</table>\n'''
      '''<table class="cubeaction">\n'''
       '''<tr class="headerrow"><th>#</th><th>action</th><th colspan="2"> Cubeful Eq. </th></tr>\n'''
       '''<tr class="actualrow"><th>1</th><td> No double </td><td> +0.236 </td><td>  </td></tr>\n'''
       '''<tr class="evenrow"><th>2</th><td> Double, pass </td><td> +0.236 </td><td> +0.764 </td></tr>\n'''
       '''<tr class="oddrow"><th>3</th><td> Double, take </td><td> -0.096 </td><td> -0.332 </td></tr>\n'''
       '''</table>\n'''))


  def test_escape_lt(self):
    self.line.parse('''<''')
    self.assertHtmlEqual(
      self.line.make_html(),
'''&lt;''')

  def test_escape_gt(self):
    self.line.parse('''>''')
    self.assertHtmlEqual(
      self.line.make_html(),
'''&gt;''')

  def test_escape_amp(self):
    self.line.parse('''&''')
    self.assertHtmlEqual(
      self.line.make_html(),
'''&amp;''')

  def test_escape_combined(self):
    self.line.parse('''&<>''')
    self.assertHtmlEqual(
      self.line.make_html(),
'''&amp;&lt;&gt;''')

  def test_escape_wiki(self):
    self.line.parse('''!HogeHoge''')
    self.assertHtmlEqual(
      self.line.make_html(),
'''HogeHoge''')

  def test_escape_combined(self):
    self.line.parse('''!&<>''')
    self.assertHtmlEqual(
      self.line.make_html(),
'''!&amp;&lt;&gt;''')

  def test_extract_references_wikiname_by_camelcase(self):
    self.wiki.parse('''BackgammonBase''')
    d = self.wiki.extract_references()
    self.assert_('''wikiname''' in d)
    self.assertEqual(d["wikiname"], ["BackgammonBase"])

  def test_extract_references_wikiname_by_scheme_1(self):
    self.wiki.parse('''[wiki:BackgammonBase]''')
    d = self.wiki.extract_references()
    self.assert_('''wikiname''' in d)
    self.assertEqual(d["wikiname"], ["BackgammonBase"])

  def test_extract_references_wikiname_by_scheme_2(self):
    self.wiki.parse('''[wiki:blot]''')
    d = self.wiki.extract_references()
    self.assert_('''wikiname''' in d)
    self.assertEqual(d["wikiname"], ["blot"])

  def test_extract_references_wikinames(self):
    self.wiki.parse('''BackgammonBase, [wiki:blot]'''),
    d = self.wiki.extract_references()
    self.assert_('''wikiname''' in d)
    self.assertEqual(d["wikiname"], ["BackgammonBase", "blot"])

  def test_extract_references_entry_1(self):
    self.wiki.parse('''Entry: #1 or entry:1'''),
    d = self.wiki.extract_references()
    self.assert_('''entry''' in d)
    self.assertEqual(d["entry"], [1])

  def test_extract_references_entry_1(self):
    self.wiki.parse('''Entry: #1 or entry:2'''),
    d = self.wiki.extract_references()
    self.assert_('''entry''' in d)
    self.assertEqual(d["entry"], [1, 2])

  def test_extract_references_query_1(self):
    self.wiki.parse('''Query: {1} or query:1''')
    d = self.wiki.extract_references()
    self.assert_('''query''' in d)
    self.assertEqual(d["query"], [1])

  def test_extract_references_query_2(self):
    self.wiki.parse('''Query: {1} or query:2''')
    d = self.wiki.extract_references()
    self.assert_('''query''' in d)
    self.assertEqual(d["query"], [1, 2])

  def test_extract_references_match_link_1(self):
    self.wiki.parse('''Match: m1, [1] or match:1''')
    d = self.wiki.extract_references()
    self.assert_('''query''' in d)
    self.assertEqual(d["match"], [1])

  def test_extract_references_match_link_2(self):
    self.wiki.parse('''Match: m2, [1] or match:3''')
    d = self.wiki.extract_references()
    self.assert_('''query''' in d)
    self.assertEqual(d["match"], [1, 2, 3])

  def test_extract_references_escaping_link(self):
    self.wiki.parse('''!#42 is not a link''')
    d = self.wiki.extract_references()
    self.assert_('''entry''' in d)
    self.assert_(42 not in d["entry"])

  def test_extract_references_analysis(self):
    self.wiki.parse('''Analysis(cNcxAxCY54YBBg:cAn7ADAAIAAA)''')
    d = self.wiki.extract_references()
    self.assert_('''Analysis''' in d)
    self.assert_('''cNcxAxCY54YBBg:cAn7ADAAIAAA''' in d["Analysis"])


