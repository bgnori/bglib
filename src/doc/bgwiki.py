#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2006-2008 Noriyuki Hosaka nori@backgammon.gr.jp
#
import re
import string

import bglib.doc
import bglib.doc.html
import bglib.doc.macro
import bglib.doc.rst

class Element(object):
  html_element = None

  def __init__(self, **kw):
    self.attrs = kw
    
  def __repr__(self):
    return '<%s %s>'%(id(self), self.__class__)

  def acceptables(self):
    return ()

  def is_acceptable(self, e):
    return isinstance(e, self.acceptables())

  def open(self):
    # on push
    return '<%s>'%self.html_element

  def close(self):
    # on pop
    return '</%s>'%self.html_element

class LineElement(Element):
  def acceptables(self):
    return (SpanElement,)

class SpanElement(LineElement):
  pass

class BoldElement(SpanElement):
  html_element = 'strong'

class ItalicElement(SpanElement):
  html_element = 'i'

class UnderlineElement(SpanElement):
  html_element = 'span'
  def open(self):
    return '<span class="underline">'

class StrikeElement(SpanElement):
  html_element = 'del'
  
class SubscriptElement(SpanElement):
  html_element = 'sub'

class SuperscriptElement(SpanElement):
  html_element = 'sup'

class MonospaceElement(SpanElement):
  html_element = 'span'
  def open(self):
    return '<span class="monospace">'

class TableCellElement(LineElement):
  html_element = 'td'

class TableRowElement(LineElement):
  def acceptables(self):
    return super(TableRowElement, self).acceptables() + \
          (TableCellElement,)
  html_element = 'tr'

class ItemizeElement(LineElement):
  html_element = 'li'
  def acceptables(self):
    return super(ItemizeElement, self).acceptables() + \
          (ListElement, ItemizeElement)
    
  def open(self):
    style = self.attrs['style']
    if style is None:
      return '<%s>'%(self.html_element)
    else:
      m = self.attrs.get('minus', None) or self.attrs.get('plus', None)
      return '<%s %s>'%(self.html_element, style[m])

class DefinitionHeaderElement(LineElement):
  html_element = 'dt'

class DefinitionBodyElement(LineElement):
  html_element = 'dd'

class BoxElement(Element):
  def acceptables(self):
    return (SpanElement,)
  def open(self):
    return '<%s>\n'%self.html_element
  def close(self):
    return '</%s>\n'%self.html_element
  
class DefinitionListElement(BoxElement):
  html_element = 'dl'
  def acceptables(self):
    return super(DefinitionListElement, self).acceptables() + \
           (DefinitionHeaderElement, DefinitionBodyElement)

class TableElement(BoxElement):
  html_element = 'table'
  def acceptables(self):
    return super(TableElement, self).acceptables() + \
          (TableRowElement, TableCellElement)
  def open(self):
    return '<table class="wiki">\n' # \n for readability

class BlockQuoteElement(BoxElement):
  def open(self):
    return '<blockquote>\n<p>\n'
  def close(self):
    return '</p>\n</blockquote>\n'

class CitationContentElement(LineElement):
  html_element = 'p'
  def acceptables(self):
    return super(CitationContentElement, self).acceptables() + \
           (CitationElement, CitationContentElement)
  def open(self):
    return '<p>\n'
  def close(self):
    return '</p>\n'

class CitationElement(BoxElement):
  def acceptables(self):
    return super(CitationElement, self).acceptables() + \
         (CitationElement, CitationContentElement)
  def open(self):
    return '<blockquote class="citation">\n'
  def close(self):
    return '</blockquote>\n'

class ListElement(BoxElement):
  _design = dict(star=('ul', None, None),
              sign = ('ul', 'class="sign"', 
               {'+':'class="plus"', # class names for li elements
                '++':'class="doubleplus"', 
                '+++':'class="tripleplus"',
                '-':'class="minus"', 
                '--':'class="doubleminus"', 
                '---':'class="tripleminus"'}),
             ordered_numeric=('ol', None, None),
             ordered_alpha=('ol', 'class="loweralpha"', None),
             ordered_roman=('ol', 'class="lowerroman"', None),
             )
  def acceptables(self):
    return super(ListElement, self).acceptables() + \
           (ListElement, ItemizeElement)

  def get_design_name(self):
    for key in self._design:
      if self.attrs[key] is not None:
        return key
    assert False

  def get_tag_info(self):
    return self._design[self.get_design_name()][:2]

  def get_style(self):
    return self._design[self.get_design_name()][2]

  def open(self):
    self.count = 0
    tag, attrs = self.get_tag_info()
    if attrs:
      return '<%s %s>\n'%(tag, attrs)
    else:
      return '<%s>\n'%(tag)

  def close(self):
    tag, attrs = self.get_tag_info()
    return '</%s>\n'%(tag)

    

class ElementStack(object):
  def __init__(self):
    self._stack = list()

  def __nonzero__(self):
    return len(self._stack)

  def __len__(self):
    return len(self._stack)

  def peek(self):
    assert self
    return self._stack[-1]
    
  def push(self, e):
    s = ''
    L = None
    for i, a in enumerate(self._stack):
      if not a.is_acceptable(e):
        L = list(reversed(self._stack[i:]))
        break
    if L:
      s += ''.join(list(self.pop_L(L)))
    self._stack.append(e)
    s += e.open()
    return s
    
  def pop(self, e):
    popped = self._stack.pop()
    assert popped == e
    return e.close()

  def iter_from_top(self):
    for e in reversed(self._stack):
      yield e
    
  def find(self, klass_or_klasses):
    L = list()
    for e in self.iter_from_top():
      L.append(e)
      if isinstance(e, klass_or_klasses):
        return True, L
    return False, L

  def pop_L(self, L):
    for e in L:
      yield self.pop(e)

  def empty(self):
    return ''.join(list(self.pop_L(self.iter_from_top())))

class BaseFormatter(bglib.doc.Formatter):
  _compiled = None
  def make_pdf(self, text):
    #FIXME not implemented
    return ''

  @classmethod
  def patterns(cls):
    for p in cls._patterns:
      yield p

  def get_regexp(self):
    if self._compiled is None:
      self._compiled = re.compile( '(%s)'%'|'.join([re_str for re_str in self.patterns()]))
    return self._compiled

  def start_handler(self, *element_classes):
    s = ''
    for element_class in element_classes:
      e = element_class()
      s += self.stack.push(e)
    return s

  def end_handler(self, element_class):
    found, L = self.stack.find(element_class)
    assert isinstance(L, list)
    if found:
      return ''.join(list(self.stack.pop_L(L)))
    return ''

  def start_on_not_exist_handler(self, element_class):
    found, L = self.stack.find(element_class)
    if found:
      return ''
    e = element_class()
    return self.stack.push(e)

  def start_or_end_handler(self, *element_classes):
    element_class = element_classes[0]
    found, L = self.stack.find(element_class)
    if found:
      return ''.join(list(self.stack.pop_L(L)))
    else:
      return self.start_handler(*element_classes)


class WrappingFormatterElement(Element, BaseFormatter):
  PREFORMAT_END_TOKEN = r"}}}"
  _patterns = [ #order matters!, first come first match.
    r"(?P<_pattern_preformat_end>^%s$)"%PREFORMAT_END_TOKEN,
    r"(?P<_pattern_processor_specifier>^#!(?P<processor_name>\w+)$)",
    r"(?P<_pattern_rest_of_the_world>^.*$)",
  ]
  _known_formatters = None

  def __init__(self):
    Element.__init__(self)
    self.stack = None #BaseFormatter needs this.
    self.buf = ''
    self.wrapped = None
    self._known_formatters = dict(
         rst=bglib.doc.rst.Formatter,
         preformat=PreformatFormatter,
    )
  def open(self):
    return ''

  def close(self):
    if self.wrapped is None:
      self.prepare_formatter()
    return self.wrapped.make_html(self.buf)

  def set_stack(self, stack):
    self.stack = stack

  def prepare_formatter(self, name=None):
    klass = self._known_formatters.get(name, PreformatFormatter)
    self.wrapped = klass()

  def make_html(self, input_line):
    print 'WrappingFormatterElement::make_html', repr(input_line)
    if input_line:
      return re.sub(self.get_regexp(), self._format, input_line)
    else:
      self.buf += '\n' # adding EmptyLine
      return

  def _format(self, matchobj):
    assert self.stack
    for name, match in matchobj.groupdict().items():
      if match:
        handler_name = '_handle' + name
        handler = getattr(self, handler_name, None)
        if handler:
          return handler(match, matchobj)

  def _handle_pattern_preformat_end(self, match, matchobj):
    assert self.stack
    return self.end_handler(WrappingFormatterElement) #self terminating

  def _handle_pattern_rest_of_the_world(self, match, matchobj):
    assert self.stack
    print '_handle_pattern_rest_of_the_world', repr(match)
    self.buf += match + '\n'
    return ''

  def _handle_pattern_processor_specifier(self, match, matchobj):
    assert self.stack
    d = matchobj.groupdict()
    self.prepare_formatter(d['processor_name'])
    return ''


class PreformatFormatter(bglib.doc.Formatter):
  def make_html(self, text):
    print 'PreformatFormatter got:', repr(text)
    return '<pre class="wiki">' + bglib.doc.html.escape(text) + '</pre>\n'

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
    r"(?P<_pattern_definition_header>^\w+::$)",
    r"(?P<_pattern_quote_or_definition_body>^[ ]{2})", # Line starts with WhiteSpaces but NOT ITEMIZE.
    r"(?P<_pattern_macro>\[\[(?P<macro_name>\w+)(\((?P<macro_args>[a-zA-Z0-9,.=/#]+)\))?\]\])",
    r"(?P<_pattern_escape_html>(%s))"%bglib.doc.html.UNSAFE_LETTERS,
  ]

  def __init__(self, stack, macroprocessor):
    self.stack = stack
    self.macroprocessor = macroprocessor
    
  def make_html(self, input_line):
    r = ''
    if input_line:
      if input_line[0] not in ' >':
        found, L = self.stack.find((BlockQuoteElement, CitationElement, DefinitionBodyElement))
        if found:
          r += ''.join(list(self.stack.pop_L(L)))
      r += re.sub(self.get_regexp(), self._format, input_line)
    else:
      r += self.stack.empty()
    return r

  def _format(self, matchobj):
    for name, match in matchobj.groupdict().items():
      if match:
        if match[0] == '!':
          return bglib.doc.html.escape(match[1:])
        handler_name = '_handle' + name
        handler = getattr(self, handler_name, None)
        if handler:
          return handler(match, matchobj)

  def _handle_pattern_escape_html(self, match, matchobj):
    return bglib.doc.html.escape(match)

  def _handle_pattern_bold(self, match, matchobj):
    return self.start_or_end_handler(BoldElement)

  def _handle_pattern_italic(self, match, matchobj):
    return self.start_or_end_handler(ItalicElement)

  def _handle_pattern_bolditalic(self, match, matchobj):
    return self.start_or_end_handler(BoldElement, ItalicElement)

  def _handle_pattern_underline(self, match, matchobj):
    return self.start_or_end_handler(UnderlineElement)

  def _handle_pattern_strike(self, match, matchobj):
    return self.start_or_end_handler(StrikeElement)

  def _handle_pattern_subscript(self, match, matchobj):
    return self.start_or_end_handler(SubscriptElement)

  def _handle_pattern_superscript(self, match, matchobj):
    return self.start_or_end_handler(SuperscriptElement)

  def _handle_pattern_monospace(self, match, matchobj):
    return self.start_or_end_handler(MonospaceElement)

  def _handle_pattern_monospace_start(self, match, matchobj):
    print '_handle_pattern_monospace_start'
    return self.start_handler(MonospaceElement)

  def _handle_pattern_monospace_end(self, match, matchobj):
    return self.end_handler(MonospaceElement)

  def _handle_pattern_table_cell(self, match, matchobj):
    return self.start_on_not_exist_handler(TableElement) + \
           self.start_on_not_exist_handler(TableRowElement) + \
           self.end_handler(TableCellElement) + \
           self.start_handler(TableCellElement)

  def _handle_pattern_table_end(self, match, matchobj):
    return self.end_handler(TableRowElement)

  def _handle_pattern_preformat_start(self, match, matchobj):
    return self.start_handler(WrappingFormatterElement)

  def _calc_indent(self, match, letter):
    indent = 0
    for c in match:
      if c in letter:
        indent += 1
      else:
        return indent

  def _calc_nesting(self, klass_or_klasses):
    nest = 0
    for e in self.stack.iter_from_top():
      if isinstance(e, klass_or_klasses):
        nest += 1
    return nest

  def _unnest(self, indent, nest, klass_or_klasses):
    r = ''
    while indent < nest:
      found, L = self.stack.find(klass_or_klasses)
      assert found
      r += ''.join(list(self.stack.pop_L(L)))
      nest -= 1
    return r, nest

  def _nest(self, indent, nest, klass):
    r = ''
    while indent > nest:
      r += self.stack.push(klass())
      nest += 1
    return r, nest

  def _handle_pattern_citation(self, match, matchobj):
    #r"(?P<_pattern_citation>^[>]+)",
    r = ''
    indent = self._calc_indent(match, '>')
    nest = self._calc_nesting(CitationElement)

    s, nest = self._unnest(indent, nest, CitationElement)
    r += s
    s, nest = self._nest(indent, nest, CitationElement)
    r += s

    assert indent == nest
    found, L = self.stack.find(CitationContentElement)
    if not found:
      e = CitationContentElement()
      r += self.stack.push(e)
    return r


  def _handle_pattern_itemize(self, match, matchobj):
    r = ''
    indent = self._calc_indent(match, ' ')
    nest = self._calc_nesting(ListElement)

    s, nest = self._unnest(indent, nest, ListElement)
    r += s

    if indent == nest:
      r += self.end_handler(ItemizeElement)
      found, L = self.stack.find(ListElement)
      parent = L[-1]
    elif indent > nest:
      assert indent == nest + 1 #indentation error
      # need to nest one more List Element
      d = matchobj.groupdict()
      parent = ListElement(**d)
      r += self.stack.push(parent)
    else:
      assert indent < nest
      assert False
    d = matchobj.groupdict()
    d.update({'style':parent.get_style()})
    e = ItemizeElement(**d)
    r += self.stack.push(e)
    return r

  def _handle_pattern_definition_header(self, match, matchobj):
    r"(?P<_pattern_definition_header>^\w+::$)",
    return self.end_handler(DefinitionHeaderElement) + \
           self.start_on_not_exist_handler(DefinitionListElement) + \
           '<dt>%s</dt>'%bglib.doc.html.escape(match[:-2])

  def _handle_pattern_quote_or_definition_body(self, match, matchobj):
    found, L = self.stack.find(DefinitionListElement)
    if found:
      return self.start_on_not_exist_handler(DefinitionBodyElement)
    else:
      return self.start_on_not_exist_handler(BlockQuoteElement)

  def _handle_pattern_entry_link(self, match, matchobj):
    if match[0] == '#':
      t = string.Template('''<a class="entry" href="/entry/$n" title="title">#$n</a>''')
      n = match[1:]
    elif match.startswith('entry:'):
      n = match[6:]
      t = string.Template('''<a class="entry" href="/entry/$n" title="title">entry:$n</a>''')
    return t.substitute(n=n)

  def _handle_pattern_query_link(self, match, matchobj):
    if match[0] == '{':
      t = string.Template('''<a class="query" href="/query/$n">{$n}</a>''')
      n = match[1:-1]
    elif match.startswith('query:'):
      n = match[6:]
      t = string.Template('''<a class="query" href="/query/$n">query:$n</a>''')
    return t.substitute(n=n)

  def _handle_pattern_match_link(self, match, matchobj):
    if match[0] == '[':
      t = string.Template('''<a class="match" href="/match/$n">[$n]</a>''')
      n = match[1:-1]
    elif match.startswith('match:'):
      n = match[6:]
      t = string.Template('''<a class="match" href="/match/$n">match:$n</a>''')
    elif match.startswith('m'):
      n = match[1:]
      t = string.Template('''<a class="match" href="/match/$n">m$n</a>''')
    return t.substitute(n=n)

  def _handle_pattern_camelcase(self, match, matchobj):
    t = string.Template(
      '''<a class="wiki-link" href="/wiki/$camelcased">'''
      '''$camelcased</a>''')
    return t.substitute(camelcased=bglib.doc.html.escape(match))

  def _handle_pattern_auto_anchor(self, match, matchobj):
    t = string.Template('<a class="ext-link" href="$url"><span class="icon">$url</span></a>')
    return t.substitute(url=bglib.doc.html.escape(match))

  def _handle_pattern_scheme_wikiname(self, match, matchobj):
    #>!?\[wiki:\w+\])",
    t = string.Template('<a class="wiki-link" href="/wiki/$wikiname">$wikiname</a>')
    assert match[0:6] == '[wiki:'
    assert match[-1] == ']'
    return t.substitute(wikiname=bglib.doc.html.escape(match[6:-1]))

  def _handle_pattern_scheme_url(self, match, matchobj):
    t = string.Template('''<a class="ext-link" href="$url"><span class="icon">$disp</span></a>''')
    d = matchobj.groupdict()
    if d['disp']:
      disp = bglib.doc.html.escape(d['disp'][1:])
    else:
      disp = bglib.doc.html.escape(d['url_1'])
    return t.substitute(url=bglib.doc.html.escape(d['url_1']), disp=disp)

  def _handle_pattern_macro(self, match, matchobj):
    d = matchobj.groupdict()
    return self.macroprocessor.dispatch(d['macro_name'],d['macro_args'])

class Formatter(BaseFormatter):
  def __init__(self, db):
    self.db = db
    self.stack = ElementStack()
    self.macroprocessor = bglib.doc.macro.Processor(db)
    self.line_formatter = LineFormatter(self.stack, self.macroprocessor)
    self.preformat_formatter = None

  def get_formatter(self):
    if self.stack and isinstance(self.stack.peek(), WrappingFormatterElement):
      wrapper = self.stack.peek()
      wrapper.set_stack(self.stack)
      return wrapper
    else:
      return self.line_formatter

  def make_html(self, wiki):
    html = ''
    for line in wiki.splitlines():
      formatter = self.get_formatter()
      html_fragment = formatter.make_html(line)
      if html:
        if html_fragment:
          html = html + '\n' + html_fragment 
      else:
        html = html_fragment
    return html + self.flush()

  def flush(self):
    if not self.stack:
      return ''
    return '\n' + self.stack.empty()

