#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2006-2008 Noriyuki Hosaka nori@backgammon.gr.jp
#

class Node(object):
  def __init__(self, parent):
    assert not parent or isinstance(parent, Node)
    self.parent = parent
    self.children = list()

  def on_enter(self, visitor):
    visitor.enter(self)

  def on_leave(self, visitor):
    visitor.leave(self)

  def append(self, node):
    assert isinstance(node, Node)
    #print self, node
    self.children.append(node)

  def remove(self, node):
    assert isinstance(node, Node)
    assert node in self.children
    self.children.remove(node)

  def accept(self, visitor):
    assert isinstance(visitor, Visitor)
    self.on_enter(visitor)
    for c in self.children:
      c.accept(visitor)
    self.on_leave(visitor)

  def __str__(self):
    return "%s"%(self.__class__.__name__)
  def __repr__(self):
    return "%s:%x"%(self.__class__.__name__, id(self))


class Root(Node):
  def __init__(self):
    Node.__init__(self, None)
  def __repr__(self):
    return "Root:%x"%(id(self))
  def __str__(self):
    return "Root"


class BgWikiElementNode(Node):
  html_element = None
  is_single = False
  def __init__(self, parent, **d):
    Node.__init__(self, parent)
    self.attrs = dict(**d)

  def acceptables(self):
    return ()

  def is_acceptable(self, e):
    return isinstance(e, self.acceptables())

  def open(self):
    if not self.html_element:
      return ''
    if self.attrs:
      attrs = ' '.join(['%s="%s"'%(key, item) for key, item in self.attrs.items()])
    else:
      attrs = ''
    if self.is_single:
      if attrs: 
        return '<%s '%self.html_element + attrs + ' />\n'
      return '<%s />\n'%self.html_element
    else:
      if attrs: 
        return '<%s '%self.html_element + attrs + '>\n'
      return '<%s>\n'%self.html_element

  def close(self):
    if not self.html_element:
      return ''
    if self.is_single:
      return ''
    else:
      return '</%s>'%self.html_element

class BgWikiElementRoot(BgWikiElementNode, Root):
  html_element = None
  def __init__(self, **d):
    BgWikiElementNode.__init__(self, None)
    self.attrs = dict(**d)
  def is_acceptable(self, e):
    return True


class LineElement(BgWikiElementNode):
  def acceptables(self):
    return (SpanElement,)

class SpanElement(LineElement):
  html_element = 'span'

class BRElement(SpanElement):
  html_element = 'br'
  is_single = True
  
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
  html_element = 'tr'
  def acceptables(self):
    return super(TableRowElement, self).acceptables() + \
          (TableCellElement, TableHeaderElement)

class TableHeaderElement(LineElement):
  html_element = 'th'

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

class AnchorElement(SpanElement):
  html_element = 'a'
  def set_url(self, url):
    self.attrs["href"] = url

class BoxElement(BgWikiElementNode):
  def acceptables(self):
    return (SpanElement,)
  
class HeadingElement(BoxElement):
  pass
class H1Element(HeadingElement):
  html_element = 'h1'
class H2Element(HeadingElement):
  html_element = 'h2'
class H3Element(HeadingElement):
  html_element = 'h3'

class DefinitionBodyElement(BoxElement):
  html_element = 'dd'
  def acceptables(self):
    return super(DefinitionBodyElement, self).acceptables() + (ListElement,)

class DivElement(BoxElement):
  html_element = 'div'
  def acceptables(self):
    return (SpanElement, BoxElement) #Any Element...

class ImgElement(BoxElement):
  html_element = 'img'
  is_single = True

class DefinitionListElement(BoxElement):
  html_element = 'dl'
  def acceptables(self):
    return super(DefinitionListElement, self).acceptables() + \
           (DefinitionHeaderElement, DefinitionBodyElement, ListElement)

class TableElement(BoxElement):
  html_element = 'table'
  def acceptables(self):
    return super(TableElement, self).acceptables() + \
          (TableRowElement, TableHeaderElement, TableCellElement)

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
              sign=('ul', 'class="sign"', 
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
      if self.attrs[key]:
        return key
    return 'star' #default design name

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



class Text(BgWikiElementNode):
  def __init__(self, parent, text=None, **d):
    BgWikiElementNode.__init__(self, parent, **d)
    if not text:
      text = ''
    self.set_text(text)

  def set_text(self, text):
    self.text = text

  def append_text(self, text):
    self.text += text

  def __repr__(self):
    return "Text:%x %s"%(id(self), self.text)

  def __str__(self):
    return "Text:%s"%(self.text)

  def open(self):
    return self.text

  def close(self):
    return ''


class Editor(object):
  def __init__(self):
    self.root = None
    self.current = None

  def start(self, root):
    assert isinstance(root, Root)
    self.root = root
    self.current = root

  def done(self):
    self.current = self.root
    return self.root

  def enter(self, klass, **d):
    self.current = self.append(klass, **d)
    return self.current

  def leave(self, *klasses):
    node = self.current
    while node:
      if isinstance(node, *klasses):
        self.current = node.parent
        return
      node = node.parent
      #implicitly leaving node.
    #assert False #ugh! No such node!

  def append(self, klass, **d):
    assert issubclass(klass, Node)
    node = klass(self.current, **d)
    c = self.current
    while c and not c.is_acceptable(node):
      c = c.parent
    c.append(node)
    self.current = c
    return node

  def remove(self, node):
    self.current.remove(node)

  def append_text(self, text):
    if self.current.children:
      n = self.current.children[-1]
      if isinstance(n, Text):
        n.append_text(text)
        return
    self.current.append(Text(self.current, text=text))

  def count_nesting(self, *klass_or_klasses):
    nest = 0
    node = self.current
    while node:
      if isinstance(node, klass_or_klasses):
        nest += 1
      node = node.parent
    return nest

  def accept(self, visitor):
    assert isinstance(visitor, Visitor)
    return self.current.accept(visitor)
    
  def ancestor(self, *klassses):
    node = self.current
    while node:
      if isinstance(node, *klassses):
        return node
      node = node.parent
    return None

class HtmlEditor(Editor):
  pass


class Visitor(object):
  def enter(self, node):
    pass
  def leave(self, node):
    pass


class DebugVisitor(Visitor):
  def __init__(self):
    self.buf = ''
  def enter(self, node):
    self.buf += str(node)+ '\n'


class PrintVisitor(Visitor):
  def enter(self, node):
    print node


class HtmlWriter(Visitor):
  def __init__(self):
    Visitor.__init__(self)
    self.buf = ''
  def enter(self, node):
    self.buf += node.open()
  def leave(self, node):
    self.buf += node.close()
  def html(self):
    return self.buf


