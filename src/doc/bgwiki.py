#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2006-2008 Noriyuki Hosaka nori@backgammon.gr.jp
#
import re
import string

import bglib.doc
import bglib.doc.doctree
import bglib.doc.html
import bglib.doc.macro
import bglib.doc.rst


class BaseFormatter(bglib.doc.Formatter):
  _compiled = None
  def __init__(self):
    self.reset()
  
  def reset(self):
    self.doctree = bglib.doc.doctree.BgWikiElementRoot()
    self.editor = bglib.doc.doctree.HtmlEditor()
    self.editor.start(self.doctree)
    
  def make_pdf(self):
    #FIXME not implemented
    return ''

  def make_html(self):
    self.editor.leave(bglib.doc.doctree.BgWikiElementRoot)
    self.editor.done()
    writer = bglib.doc.doctree.HtmlWriter() # Visit
    self.editor.accept(writer)
    return writer.html()


  @classmethod
  def patterns(cls):
    for p in cls._patterns:
      yield p

  def get_regexp(self):
    if self._compiled is None:
      self._compiled = re.compile( '(%s)'%'|'.join([re_str for re_str in self.patterns()]), re.UNICODE|re.LOCALE)
    return self._compiled

  def start_handler(self, element_class, **d):
    editor = self.editor
    editor.enter(element_class, **d)

  def end_handler(self, element_class):
    editor = self.editor
    assert editor 
    assert isinstance(editor, bglib.doc.doctree.Editor)
    editor.leave(element_class)

  def start_on_not_exist_handler(self, element_class, **d):
    editor = self.editor
    found = editor.ancestor(element_class)
    if not found:
      editor.enter(element_class, **d)

  def start_or_end_handler(self, element_class, **d):
    editor = self.editor
    found = editor.ancestor(element_class)
    if found:
      self.end_handler(element_class)
    else:
      self.start_handler(element_class, **d)


class WrappingFormatterElement(bglib.doc.doctree.BgWikiElementNode, BaseFormatter):
  PREFORMAT_END_TOKEN = r"}}}"
  _patterns = [ #order matters!, first come first match.
    r"(?P<_pattern_preformat_end>^%s$)"%PREFORMAT_END_TOKEN,
    r"(?P<_pattern_processor_specifier>^#!(?P<processor_name>\w+)$)",
    r"(?P<_pattern_rest_of_the_world>^.*$)",
  ]
  _known_formatters = None

  def __init__(self, parent, **d):
    bglib.doc.doctree.BgWikiElementNode.__init__(self, parent)
    self.editor = None
    self.buf = ''
    self.wrapped = None
    self.ret = ''
    self._known_formatters = dict(
         rst=bglib.doc.rst.Formatter,
         preformat=PreformatFormatter,
    )
  def open(self):
    return ''

  def close(self):
    if self.wrapped is None:
      self.prepare_formatter()
    self.wrapped.parse(self.buf)
    return self.wrapped.make_html()

  def set_editor(self, editor):
    self.editor = editor

  def prepare_formatter(self, name=None):
    klass = self._known_formatters.get(name, PreformatFormatter)
    self.wrapped = klass()

  def parse(self, input_line):
    if input_line:
      for matchobj in self.get_regexp().finditer(input_line):
        for name, match in matchobj.groupdict().items():
          if match:
            handler_name = '_handle' + name
            handler = getattr(self, handler_name, None)
            if handler:
              handler(match, matchobj)
    else:
      self.buf += '\n' # adding EmptyLine

  def make_html(self):
    assert False

  def _handle_pattern_preformat_end(self, match, matchobj):
    self.end_handler(WrappingFormatterElement) #self terminating

  def _handle_pattern_rest_of_the_world(self, match, matchobj):
    self.buf += match + '\n'

  def _handle_pattern_processor_specifier(self, match, matchobj):
    d = matchobj.groupdict()
    self.prepare_formatter(d['processor_name'])



class PreformatFormatter(bglib.doc.Formatter):
  def __init__(self):
    bglib.doc.Formatter.__init__(self)
    self.text = ''
  def parse(self, text):
    self.text += text
  def make_html(self):
    return '<pre class="wiki">' + bglib.doc.html.escape(self.text) + '</pre>\n'


class LineFormatter(BaseFormatter):

  BOLD_TOKEN = "'''"
  ITALIC_TOKEN = "''"
  BOLDITALIC_TOKEN = "'''''"
  UNDERLINE_TOKEN = "__"
  STRIKE_TOKEN = "~~"
  SUBSCRIPT_TOKEN = ",,"
  SUPERSCRIPT_TOKEN = r"\^"
  MONOSPACE_TOKEN = r"`"
  PREFORMAT_START_TOKEN = r"{{{"
  PREFORMAT_END_TOKEN = r"}}}"
  URL = r"(?P<url%s>https?://[a-zA-Z0-9./\-]+)"

  _patterns = [ #order matters!, first come first match.
    r"(?P<_pattern_bolditalic>!?%s)"%BOLDITALIC_TOKEN, # must come earlier than BOLD and italic
    r"(?P<_pattern_bold>!?%s)"%BOLD_TOKEN,
    r"(?P<_pattern_italic>!?%s)"%ITALIC_TOKEN,
    r"(?P<_pattern_underline>!?%s)"%UNDERLINE_TOKEN,
    r"(?P<_pattern_strike>!?%s)"%STRIKE_TOKEN,
    r"(?P<_pattern_subscript>!?%s)"%SUBSCRIPT_TOKEN,
    r"(?P<_pattern_superscript>!?%s)"%SUPERSCRIPT_TOKEN,
    r"(?P<_pattern_monospace>!?%s)"%MONOSPACE_TOKEN,
    r"(?P<_pattern_preformat_start>!?^%s$)"%PREFORMAT_START_TOKEN,
    r"(?P<_pattern_preformat_end>!?^%s$)"%PREFORMAT_END_TOKEN,
    r"(?P<_pattern_monospace_start>!?%s)"%PREFORMAT_START_TOKEN,
    r"(?P<_pattern_monospace_end>!?%s)"%PREFORMAT_END_TOKEN,
    r"(?P<_pattern_heading_h3>!?===)",
    r"(?P<_pattern_heading_h2>!?==)",
    r"(?P<_pattern_heading_h1>!?=)",
    r"(?P<_pattern_macro>\[\[(?P<macro_name>\w+)(\((?P<macro_args>[a-zA-Z0-9,.=/#:]+)\))?\]\])",
    r"(?P<_pattern_entry_link>!?(#|entry:)\d+)",
    r"(?P<_pattern_query_link>!?((query:\d+)|(\{\d+\})))",
    r"(?P<_pattern_match_link>!?((m\d+)|(match:\d+)|(\[\d+\])))",
    r"(?P<_pattern_table_end>!?\|\|\s*$)", # line ends with ||, must come earlier than table cell
    r"(?P<_pattern_table_cell>!?\|\|)",
    r"(?P<_pattern_scheme_url>!?\[%s(?P<disp>[ ][^]]+)?\])"%(URL%('_1')),
    r"(?P<_pattern_scheme_wikiname>!?\[wiki:[A-Za-z]+\])",
    r"(?P<_pattern_auto_anchor>!?%s)"%(URL%('_2')),
    r"(?P<_pattern_camelcase>!?[A-Z][a-z0-9]+([A-Z][a-z0-9]+)+)",
    r"(?P<_pattern_itemize>^[ ]+"
      r"((?P<star>[*])"
       r"|(?P<sign>(?P<plus>[+]{1,3})|(?P<minus>-{1,3}))"
       r"|(?P<ordered_numeric>[1-8]\.?)"
       r"|(?P<ordered_alpha>[a-h]\.?)"
       r"|(?P<ordered_roman>[iv]+\.?)"
      r")[ ])",
    r"(?P<_pattern_citation>^[>]+[ ])",
    #r"(?P<_pattern_definition_header>^([.+])+::$)",
    r"(?P<_pattern_comsume_definition_header>::$)",
    r"(?P<_pattern_quote_or_definition_body>^[ ]{2,})", # Line starts with WhiteSpaces but NOT ITEMIZE.
    r"(?P<_pattern_escape_html>(%s))"%bglib.doc.html.UNSAFE_LETTERS,
    r"(?P<_pattern_rest_of_the_world>.)",
  ]

  def __init__(self, editor):
  #, macroprocessor):
    self.editor = editor
    #self.macroprocessor = macroprocessor

  def parse(self, input_line):
    editor = self.editor
    if input_line:
      if input_line[0] not in ' >':
        editor.leave((bglib.doc.doctree.BlockQuoteElement, 
                      bglib.doc.doctree.CitationElement, 
                      bglib.doc.doctree.DefinitionBodyElement))
      if input_line.endswith('::'):
        self.start_definition_header()
        pass
      for matchobj in self.get_regexp().finditer(input_line):
        for name, match in matchobj.groupdict().items():
          if match:
            if match[0] == '!' and name != "_pattern_rest_of_the_world":
              editor.append_text(bglib.doc.html.escape(match[1:]))
              continue
            handler_name = '_handle' + name
            handler = getattr(self, handler_name, None)
            if handler:
              handler(match, matchobj)
      if input_line.endswith('::'):
        self.end_definition_header()
    else:
      t = editor.done()

  def _handle_pattern_rest_of_the_world(self, match, matchobj):
    self.editor.append_text(match)

  def _handle_pattern_escape_html(self, match, matchobj):
    self.editor.append_text(bglib.doc.html.escape(match))

  def _handle_pattern_bold(self, match, matchobj):
    self.start_or_end_handler(bglib.doc.doctree.BoldElement)

  def _handle_pattern_italic(self, match, matchobj):
    self.start_or_end_handler(bglib.doc.doctree.ItalicElement)

  def _handle_pattern_bolditalic(self, match, matchobj):
    #FIXME ?! see start_or_end_handler. for similarity.
    editor = self.editor
    found = editor.ancestor(
        (bglib.doc.doctree.BoldElement,
        bglib.doc.doctree.ItalicElement))
    if found:
      self.end_handler(bglib.doc.doctree.BoldElement)
      self.end_handler(bglib.doc.doctree.ItalicElement)
    else:
      self.start_handler(bglib.doc.doctree.BoldElement)
      self.start_handler(bglib.doc.doctree.ItalicElement)

  def _handle_pattern_underline(self, match, matchobj):
    self.start_or_end_handler(
        bglib.doc.doctree.UnderlineElement)

  def _handle_pattern_strike(self, match, matchobj):
    self.start_or_end_handler(
        bglib.doc.doctree.StrikeElement)

  def _handle_pattern_subscript(self, match, matchobj):
    self.start_or_end_handler(
        bglib.doc.doctree.SubscriptElement)

  def _handle_pattern_superscript(self, match, matchobj):
    self.start_or_end_handler(
        bglib.doc.doctree.SuperscriptElement)

  def _handle_pattern_heading_h3(self, match, matchobj):
    #r"(?P<_pattern_heading_h3>!?===)",
    self.start_or_end_handler(
        bglib.doc.doctree.H3Element)

  def _handle_pattern_heading_h2(self, match, matchobj):
    #r"(?P<_pattern_heading_h2>!?==)",
    self.start_or_end_handler(
        bglib.doc.doctree.H2Element)

  def _handle_pattern_heading_h1(self, match, matchobj):
    #r"(?P<_pattern_heading_h1>!?=)",
    self.start_or_end_handler(
        bglib.doc.doctree.H1Element)

  def _handle_pattern_monospace(self, match, matchobj):
    self.start_or_end_handler(
        bglib.doc.doctree.MonospaceElement)

  def _handle_pattern_monospace_start(self, match, matchobj):
    self.start_handler(
          bglib.doc.doctree.MonospaceElement)

  def _handle_pattern_monospace_end(self, match, matchobj):
    self.end_handler(
        bglib.doc.doctree.MonospaceElement)

  def _handle_pattern_table_cell(self, match, matchobj):
    self.start_on_not_exist_handler(
        bglib.doc.doctree.TableElement, **{'class':'wiki'})
    self.start_on_not_exist_handler(
        bglib.doc.doctree.TableRowElement)
    self.end_handler(
        bglib.doc.doctree.TableCellElement)
    self.start_handler(
        bglib.doc.doctree.TableCellElement)

  def _handle_pattern_table_end(self, match, matchobj):
    self.end_handler(
        bglib.doc.doctree.TableRowElement)

  def _handle_pattern_preformat_start(self, match, matchobj):
    self.start_handler(WrappingFormatterElement)
    self.editor.current.set_editor(self.editor)

  def _calc_indent(self, match, letter):
    indent = 0
    for c in match:
      if c in letter:
        indent += 1
      else:
        return indent

  def _unnest(self, indent, nest, klass_or_klasses):
    editor = self.editor
    while indent < nest:
      editor.leave(klass_or_klasses)
      nest -= 1
    return nest

  def _nest(self, indent, nest, klass):
    editor = self.editor
    while indent > nest:
      editor.enter(klass)
      nest += 1
    return nest

  def _handle_pattern_citation(self, match, matchobj):
    #r"(?P<_pattern_citation>^[>]+)",
    editor = self.editor
    indent = self._calc_indent(match, '>')
    nest = editor.count_nesting(
        bglib.doc.doctree.CitationElement)

    nest = self._unnest(indent, nest, 
        bglib.doc.doctree.CitationElement)
    nest = self._nest(indent, nest, 
        bglib.doc.doctree.CitationElement)

    assert indent == nest
    self.start_on_not_exist_handler(bglib.doc.doctree.CitationContentElement)

  def _handle_pattern_itemize(self, match, matchobj):
    editor = self.editor
    indent = self._calc_indent(match, ' ')
    nest = editor.count_nesting(bglib.doc.doctree.ListElement) \
          -  editor.count_nesting(bglib.doc.doctree.DefinitionListElement)
    

    nest = self._unnest(indent, nest, bglib.doc.doctree.ListElement)

    if indent == nest:
      editor.leave(bglib.doc.doctree.ItemizeElement)
    elif indent > nest:
      while indent > nest + 1:
        #bad indentation, push ListElement to balance.
        editor.enter(bglib.doc.doctree.ListElement,
                        star=None,
                        ordered_numeric=None,
                        ordered_roman=None,
                        ordered_alpha=None,
                        sign=None)
        nest += 1
      assert indent == nest + 1
      # need to nest just one more List Element
      d = matchobj.groupdict()
      editor.enter(bglib.doc.doctree.ListElement, **d)
    else:
      assert indent < nest
      assert False
    d = matchobj.groupdict()
    d.update({'style':editor.current.get_style()})
    editor.enter(bglib.doc.doctree.ItemizeElement, **d)


  def start_definition_header(self):
    editor = self.editor
    self.start_on_not_exist_handler(bglib.doc.doctree.DefinitionListElement)
    self.start_handler(bglib.doc.doctree.DefinitionHeaderElement)

  def end_definition_header(self):
    editor = self.editor
    self.end_handler(bglib.doc.doctree.DefinitionHeaderElement)

  def _handle_pattern_quote_or_definition_body(self, match, matchobj):
    editor = self.editor
    found = self.editor.ancestor(bglib.doc.doctree.DefinitionListElement)
    if found:
      self.start_on_not_exist_handler(bglib.doc.doctree.DefinitionBodyElement)
    else:
      self.start_on_not_exist_handler(bglib.doc.doctree.BlockQuoteElement)

  def _handle_pattern_entry_link(self, match, matchobj):
    editor = self.editor
    if match[0] == '#':
      a = editor.enter(bglib.doc.doctree.AnchorElement,
                      **{'class':"entry", 'title':match, 'href':"/entry/%s"%match[1:]})
    elif match.startswith('entry:'):
      a = editor.enter(bglib.doc.doctree.AnchorElement,
                      **{'class':"entry", 'title':match, 'href':"/entry/%s"%match[6:]})
    else:
      assert False
    editor.append_text(match)
    editor.leave(bglib.doc.doctree.AnchorElement)

  def _handle_pattern_query_link(self, match, matchobj):
    editor = self.editor
    if match[0] == '{':
      a = editor.enter(bglib.doc.doctree.AnchorElement, 
                      **{'class':"query", 'title':match, "href":"/query/%s"%match[1:-1]})
    elif match.startswith('query:'):
      a = editor.enter(bglib.doc.doctree.AnchorElement, 
                      **{'class':"query", 'title':match, "href":"/query/%s"%match[6:]})
    else:
      assert False
    editor.append_text(match)
    editor.leave(bglib.doc.doctree.AnchorElement)

  def _handle_pattern_match_link(self, match, matchobj):
    editor = self.editor
    a = editor.enter(bglib.doc.doctree.AnchorElement, 
                      **{'class':"match", 'title':"title"})
    if match[0] == '[':
      a.set_url("/match/%s"%match[1:-1])
    elif match.startswith('match:'):
      a.set_url("/match/%s"%match[6:])
    elif match.startswith('m'):
      a.set_url("/match/%s"%match[1:])
    else:
      assert False
    editor.append_text(match)
    editor.leave(bglib.doc.doctree.AnchorElement)


  def _handle_pattern_camelcase(self, match, matchobj):
    editor = self.editor
    a = editor.enter(bglib.doc.doctree.AnchorElement, **{'class':"wiki-link", 'title':match})
    a.set_url("/wiki/%s"%match)
    editor.append_text(match)
    editor.leave(bglib.doc.doctree.AnchorElement)

  def _handle_pattern_auto_anchor(self, match, matchobj):
    #t = string.Template('<a class="ext-link" href="$url"><span class="icon">$url</span></a>')
    url=bglib.doc.html.escape(match)
    editor = self.editor
    a = editor.enter(bglib.doc.doctree.AnchorElement, 
                      **{'class':"ext-link", 'title':"title"})
    a.set_url(url)
    editor.enter(bglib.doc.doctree.SpanElement, **{'class':'icon'})
    editor.append_text(match)
    editor.leave(bglib.doc.doctree.SpanElement)
    editor.leave(bglib.doc.doctree.AnchorElement)

  def _handle_pattern_scheme_wikiname(self, match, matchobj):
    #>!?\[wiki:\w+\])",
    #t = string.Template('<a class="wiki-link" href="/wiki/$wikiname">$wikiname</a>')
    assert match[0:6] == '[wiki:'
    assert match[-1] == ']'
    #return t.substitute(wikiname=bglib.doc.html.escape(match[6:-1]))
    editor = self.editor
    a = editor.enter(bglib.doc.doctree.AnchorElement, 
                      **{'class':"wiki-link", 'title':match[6:-1]})
    a.set_url("/wiki/%s"%match[6:-1])
    editor.append_text(match[6:-1])
    editor.leave(bglib.doc.doctree.AnchorElement)

  def _handle_pattern_scheme_url(self, match, matchobj):
    editor = self.editor
    d = matchobj.groupdict()
    if d['disp']:
      disp = bglib.doc.html.escape(d['disp'][1:])
    else:
      disp = bglib.doc.html.escape(d['url_1'])
    #t = string.Template('''<a class="ext-link" href="$url"><span class="icon">$disp</span></a>''')
    #return t.substitute(url=bglib.doc.html.escape(d['url_1']), disp=disp)
    a = editor.enter(bglib.doc.doctree.AnchorElement, 
                      **{'class':"ext-link", 'title':disp})
    a.set_url("%s"%bglib.doc.html.escape(d['url_1']))
    editor.enter(bglib.doc.doctree.SpanElement, **{'class':'icon'})
    editor.append_text(disp)
    editor.leave(bglib.doc.doctree.SpanElement)
    editor.leave(bglib.doc.doctree.AnchorElement)


  def _handle_pattern_macro(self, match, matchobj):
    editor = self.editor
    d = matchobj.groupdict()
    bglib.doc.macro.dispatch(editor, d['macro_name'], d['macro_args'])
    
class Formatter(BaseFormatter):
  def __init__(self, db):
    self.db = db
    self.doctree = bglib.doc.doctree.BgWikiElementRoot()
    self.editor = bglib.doc.doctree.Editor()
    self.editor.start(self.doctree)
    #self.macroprocessor = bglib.doc.macro.Processor(db)
    self.line_formatter = LineFormatter(self.editor)
   # , self.macroprocessor)
    self.preformat_formatter = None

  def get_formatter(self):
    if isinstance(self.editor.current, WrappingFormatterElement):
      return self.editor.current
    else:
      return self.line_formatter

  def parse(self, wiki):
    for line in wiki.splitlines():
      formatter = self.get_formatter()
      formatter.parse(line)

  def extract_references(self):
    d = dict()
    writer = bglib.doc.doctree.HtmlWriter() # Visit
    self.doctree.accept(writer)
    #writer.references()
    return d


from bglib.doc.fuzzing import Gene
class wGene(Gene):
  seps = '\n '
  symbols = """[]'"_~^`{}.:*=-+#|!<>/&Xx"""
  numeric = '1234567890'
  alpha_n = 'abcdefgh'
  romaon_n ='iv'
  words = ["""http:""", """https:""", 
           """query:""", """entry:""", 
           """match:""", """wiki:""",
           """||""", """CamelWord""",]
  single = list(seps + symbols + numeric + alpha_n + romaon_n)
  multi = words


if __name__ == "__main__":
  from bglib.doc.fuzzing import fuzz_it
  from bglib.doc.mock import DataBaseMock
  
  db = DataBaseMock()
  fuzz_it(wGene, Formatter(db))


