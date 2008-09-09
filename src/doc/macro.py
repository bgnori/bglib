#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2006-2008 Noriyuki Hosaka nori@backgammon.gr.jp
#
import types
import string
import re
import time
import datetime

import bglib.model.constants
import bglib.doc.html 
import bglib.doc.doctree

def signed_one_three(f):
  assert isinstance(f, float)
  return '%+1.3f'%f

def percent_two_one(f):
  assert isinstance(f, float)
  return '%2.1f'%f

_handlers = dict()

def _get_name(handler):
  if isinstance(handler, Processor):
    return handler.__class__.__name__
  elif isinstance(handler, types.FunctionType):
    return handler.func_name
  else:
    assert False

def register(handler):
  assert callable(handler)
  _handlers.update({_get_name(handler):handler})

def unregister(name, handler):
  _handlers.remove(_get_name(handler))

_db = None
def setup(db):
  global _db
  _db = db

def dispatch(editor, name, arg_string):
  assert isinstance(editor, bglib.doc.doctree.Editor)
  handler = _handlers.get(name, None)
  if handler is not None and callable(handler):
    ret = handler(editor, arg_string)
    if not ret:
      _bad_args_handler(editor, name, arg_string)
    return
  _bad_name_handler(editor, name, arg_string)

  
def _bad_name_handler(editor, name, args):
  t = string.Template('''No such macro "$name" with argument "$args"''')
  editor.enter(bglib.doc.doctree.DivElement, **{"class":"error"})
  editor.append_text(
      t.substitute(name=bglib.doc.html.escape(name), 
                   args=bglib.doc.html.escape(args or 'None'))
                    )
  editor.leave(bglib.doc.doctree.DivElement)

def _bad_args_handler(editor, name, args):
  editor.enter(bglib.doc.doctree.DivElement, **{"class":"error"})
  editor.append_text('''Bad args "%s" for %s\n'''%(bglib.doc.html.escape(args or 'None'), name))
  editor.leave(bglib.doc.doctree.DivElement)

class Processor(object):
  pass


def BR(editor, args):
  editor.enter(bglib.doc.doctree.BRElement)
  editor.leave(bglib.doc.doctree.BRElement)
  return True
register(BR)


  #r"(?P<_pattern_temp_map>!?temp_map\([a-zA-Z0-9/+]{14}:[a-zA-Z0-9/+]{12}\))",
def Timestamp(editor, args):
  editor.enter(bglib.doc.doctree.BoldElement)
  now = datetime.datetime.now()
  editor.append_text(now.isoformat())
  editor.leave(bglib.doc.doctree.BoldElement)
  return True
register(Timestamp)

class TocEditor(bglib.doc.doctree.Editor):
  pass

class TocVisitor(bglib.doc.doctree.Visitor):
  
  nestingmap = {
   bglib.doc.doctree.H1Element:0,
   bglib.doc.doctree.H2Element:1,
   bglib.doc.doctree.H3Element:2,
  }
  def __init__(self, editor):
    super(TocVisitor, self).__init__()
    self.editor = editor
    self.nesting = 0
    self.fragment_count = 0

  def match_nesting(self, node):
    editor = self.editor
    n = self.nestingmap[node.__class__]
    while self.nesting < n:
      editor.enter(bglib.doc.doctree.ListElement,
                          star=None,
                          ordered_numeric=1,
                          ordered_roman=None,
                          ordered_alpha=None,
                          sign=None)
      self.nesting +=1
    while self.nesting > n:
      editor.leave(bglib.doc.doctree.ListElement)#, style='ordered_numeric')
      self.nesting -=1

  def enter(self, node):
    editor = self.editor
    if isinstance(node, bglib.doc.doctree.HeadingElement):
      self.match_nesting(node)
      d = dict()
      d.update({'style':editor.current.get_style()})
      editor.enter(bglib.doc.doctree.ItemizeElement, **d)
      editor.enter(bglib.doc.doctree.AnchorElement, **{'href':'#fragment%i'%self.fragment_count})
      if node.children:
        editor.current.children = list(node.children)#FIXME!
      editor.leave(bglib.doc.doctree.AnchorElement)
      editor.leave(bglib.doc.doctree.ItemizeElement)
      node.attrs['id'] = 'fragment%i'%self.fragment_count
      self.fragment_count += 1

class TableOfContentNode(bglib.doc.doctree.BgWikiElementMacroNode):
  def open(self):
    editor = TocEditor()
    toc = bglib.doc.doctree.BgWikiElementRoot()
    editor.start(toc)
    editor.enter(bglib.doc.doctree.ListElement, 
                        star=None,
                        ordered_numeric=1,
                        ordered_roman=None,
                        ordered_alpha=None,
                        sign=None)

    root = self.attrs['editor'].root
    visitor = TocVisitor(editor)
    root.accept(visitor)

    editor.leave(bglib.doc.doctree.ListElement)
    editor.done()

    writer = bglib.doc.doctree.HtmlWriter()
    toc.accept(writer)
    return writer.html()


def TableOfContent(editor, args):
  editor.append(TableOfContentNode, editor=editor)
  return True
register(TableOfContent)


def Position(editor, args):
  editor.enter(bglib.doc.doctree.DivElement, **{"class":"position"})
  matchobj = re.match(r"(?P<valid>(?P<pid>[a-zA-Z0-9/+]{14}):(?P<mid>[a-zA-Z0-9/+]{12}))", args)
  if not matchobj:
    return False
  d = matchobj.groupdict(dict(pid='N/A', mid='N/A'))
  if d['pid'] == 'N/A' or d['mid'] == 'N/A':
    return False
  t = string.Template(
        '''/image?format=png'''
        '''&pid=$pid'''
        '''&mid=$mid'''
        '''&height=300&width=400&css=minimal''')
  editor.enter(bglib.doc.doctree.ImgElement,
      src=t.substitute(d))
  editor.leave(bglib.doc.doctree.DivElement)
  return True
register(Position)


def Analysis(editor, args):
  matchobj = re.match(r"(?P<valid>(?P<pid>[a-zA-Z0-9/+]{14}):(?P<mid>[a-zA-Z0-9/+]{12}))", args)
  if not matchobj:
    return False
  d = matchobj.groupdict(dict(pid='N/A', mid='N/A'))
  if d['pid'] == 'N/A' or d['mid'] == 'N/A':
    return False
  cubeaction, analysis = _db.get_analysis(d['pid'], d['mid'])

  if cubeaction:
    CubelessEquity(editor, **(analysis[0]))
    editor.enter(bglib.doc.doctree.TableElement, **{'class':'cubeaction'})
    CubeAction_table_header(editor)
    for i, row in enumerate(analysis[1:]):
      assert i + 1 == row['nth']
      CubeAction_table_row(editor, **row)
    editor.leave(bglib.doc.doctree.TableElement)
  else:
    editor.enter(bglib.doc.doctree.TableElement, **{'class':'move'})
    Movelisting_header(editor)
    for i, row in enumerate(analysis):
      assert i + 1 == row['nth']
      Movelisting_row(editor, **row)
    editor.leave(bglib.doc.doctree.TableElement)
  return True
register(Analysis) 


def CubeAction_table_header(editor):
    editor.enter(bglib.doc.doctree.TableRowElement,
                **{'class':'headerrow'})
    editor.enter(bglib.doc.doctree.TableHeaderElement)
    editor.append_text('#')
    editor.leave(bglib.doc.doctree.TableHeaderElement)

    editor.enter(bglib.doc.doctree.TableHeaderElement)
    editor.append_text('action')
    editor.leave(bglib.doc.doctree.TableHeaderElement)

    editor.enter(bglib.doc.doctree.TableHeaderElement, colspan="2")
    editor.append_text(' Cubeful Eq. ')
    editor.leave(bglib.doc.doctree.TableHeaderElement)

    editor.leave(bglib.doc.doctree.TableRowElement)

def CubeAction_table_row(editor, nth=0, action=0, equity=0.0, diff=None, actual=False, **kw):
    assert isinstance(nth, int)
    assert actual in bglib.model.constants.cubeaction_types
    assert isinstance(equity, float)
    assert diff is None or isinstance(diff, float)

    if diff is None or diff == 0.0:
      diff = ''
    else:
      diff = signed_one_three(diff)
    equity = signed_one_three(equity)

    if actual:
      klass = 'actualrow'
    else:
      klass = ('evenrow', 'oddrow')[nth%2]
    #t = string.Template('''<tr class='$klass'><th>$nth</th><td> $action </td><td> $equity </td><td> $diff </td></tr>\n''')
    #t.substitute(klass=klass, nth=nth, 
    #                    action=bglib.model.constants.cubeaction_strings[action],
    #                    equity=equity, diff=diff)
    editor.enter(bglib.doc.doctree.TableRowElement, **{'class':klass})
    editor.enter(bglib.doc.doctree.TableHeaderElement)
    editor.append_text('%i'%nth)
    editor.leave(bglib.doc.doctree.TableHeaderElement)
    editor.enter(bglib.doc.doctree.TableCellElement)
    editor.append_text(bglib.model.constants.cubeaction_strings[action])
    editor.leave(bglib.doc.doctree.TableCellElement)
    editor.enter(bglib.doc.doctree.TableCellElement)
    editor.append_text(equity)
    editor.leave(bglib.doc.doctree.TableCellElement)
    editor.enter(bglib.doc.doctree.TableCellElement)
    editor.append_text(diff)
    editor.leave(bglib.doc.doctree.TableCellElement)
    editor.leave(bglib.doc.doctree.TableRowElement)




def Movelisting_header(editor):
  #return ('''<tr class='headerrow'><th rowspan='2'>#</th><th rowspan='2'>move</th><th rowspan='2'>Ply</th><th colspan='6'> Eq.(diff)</th></tr>\n'''
  #    '''<tr class='headerrow'>'''
  #    '''<th>Win</th><th>WinG</th><th>WinBg</th><th>Lose</th><th>LoseG</th><th>LoseBg</th></tr>\n'''
  #    )
  editor.enter(bglib.doc.doctree.TableRowElement, **{'class':'headerrow'})
  editor.enter(bglib.doc.doctree.TableHeaderElement, rowspan="2")
  editor.append_text('#')
  editor.leave(bglib.doc.doctree.TableHeaderElement)
  editor.enter(bglib.doc.doctree.TableHeaderElement, rowspan="2")
  editor.append_text('move')
  editor.leave(bglib.doc.doctree.TableHeaderElement)
  editor.enter(bglib.doc.doctree.TableHeaderElement, rowspan="2")
  editor.append_text('Ply')
  editor.leave(bglib.doc.doctree.TableHeaderElement)
  editor.enter(bglib.doc.doctree.TableHeaderElement, colspan="6")
  editor.append_text('Eq.(diff)')
  editor.leave(bglib.doc.doctree.TableHeaderElement)
  editor.leave(bglib.doc.doctree.TableRowElement)

  editor.enter(bglib.doc.doctree.TableRowElement, **{'class':'headerrow'})
  editor.enter(bglib.doc.doctree.TableHeaderElement)
  editor.append_text('Win')
  editor.leave(bglib.doc.doctree.TableHeaderElement)
  editor.enter(bglib.doc.doctree.TableHeaderElement)
  editor.append_text('WinG')
  editor.leave(bglib.doc.doctree.TableHeaderElement)
  editor.enter(bglib.doc.doctree.TableHeaderElement)
  editor.append_text('WinBg')
  editor.leave(bglib.doc.doctree.TableHeaderElement)
  editor.enter(bglib.doc.doctree.TableHeaderElement)
  editor.append_text('Lose')
  editor.leave(bglib.doc.doctree.TableHeaderElement)
  editor.enter(bglib.doc.doctree.TableHeaderElement)
  editor.append_text('LoseG')
  editor.leave(bglib.doc.doctree.TableHeaderElement)
  editor.enter(bglib.doc.doctree.TableHeaderElement)
  editor.append_text('LoseBg')
  editor.leave(bglib.doc.doctree.TableHeaderElement)
  editor.leave(bglib.doc.doctree.TableRowElement)


def Movelisting_row(editor, nth, move, ply, equity, diff, Win, WinG, WinBg, Lose, LoseG, LoseBg, actual=None, **kw):
  assert isinstance(nth, int)
  assert isinstance(move, str)
  assert isinstance(ply, int)
  assert isinstance(equity, float)
  assert diff is None or isinstance(diff, float)
  assert isinstance(Win, float)
  assert isinstance(WinG, float)
  assert isinstance(WinBg, float)
  assert isinstance(Lose, float)
  assert isinstance(LoseG, float)
  assert isinstance(LoseBg, float)
  if actual:
    klass = 'actualrow'
  else:
    klass = ('evenrow', 'oddrow')[nth%2]

  equity = signed_one_three(equity)
  if diff:
    diff = '(%+1.3f) '%diff
  else:
    diff = ''
  ply = '%i'%ply
  Win = percent_two_one(Win)
  WinG = percent_two_one(WinG)
  WinBg = percent_two_one(WinBg)
  Lose = percent_two_one(Lose)
  LoseG = percent_two_one(LoseG)
  LoseBg = percent_two_one(LoseBg)

  #t = string.Template(
  #    '''<tr class='$klass'><th rowspan='2'>$nth</th><td rowspan='2'>$move</td>'''
  #    '''<td rowspan='2'>$ply</td><td class='Equity' colspan='6'> $equity $diff</td></tr>\n'''
  #    '''<tr class='$klass'><td>$Win</td><td>$WinG</td><td>$WinBg</td>'''
  #    '''<td>$Lose</td><td>$LoseG</td><td>$LoseBg</td></tr>\n'''
  #    )
  #return t.substitute(nth=nth, klass=klass, move=move, ply=ply,
  #                    equity=equity, diff=diff,
  #                    Win=Win, WinG=WinG, WinBg=WinBg,
  #                    Lose=Lose, LoseG=LoseG, LoseBg=LoseBg)
  editor.enter(bglib.doc.doctree.TableRowElement, **{'class':klass})
  editor.enter(bglib.doc.doctree.TableHeaderElement, rowspan="2")
  editor.append_text('%i'%nth)
  editor.leave(bglib.doc.doctree.TableHeaderElement)

  editor.enter(bglib.doc.doctree.TableCellElement, rowspan="2")
  editor.append_text(move)
  editor.leave(bglib.doc.doctree.TableCellElement)

  editor.enter(bglib.doc.doctree.TableCellElement, rowspan="2")
  editor.append_text(ply)
  editor.leave(bglib.doc.doctree.TableCellElement)

  editor.enter(bglib.doc.doctree.TableCellElement, **{'class':'Equity', 'colspan':"6"})
  editor.append_text('%s %s'%(equity, diff))
  editor.leave(bglib.doc.doctree.TableCellElement)
  editor.leave(bglib.doc.doctree.TableRowElement)


  editor.enter(bglib.doc.doctree.TableRowElement, **{'class':klass})
  editor.enter(bglib.doc.doctree.TableCellElement)
  editor.append_text(Win)
  editor.leave(bglib.doc.doctree.TableCellElement)

  editor.enter(bglib.doc.doctree.TableCellElement)
  editor.append_text(WinG)
  editor.leave(bglib.doc.doctree.TableCellElement)

  editor.enter(bglib.doc.doctree.TableCellElement)
  editor.append_text(WinBg)
  editor.leave(bglib.doc.doctree.TableCellElement)

  editor.enter(bglib.doc.doctree.TableCellElement)
  editor.append_text(Lose)
  editor.leave(bglib.doc.doctree.TableCellElement)

  editor.enter(bglib.doc.doctree.TableCellElement)
  editor.append_text(LoseG)
  editor.leave(bglib.doc.doctree.TableCellElement)

  editor.enter(bglib.doc.doctree.TableCellElement)
  editor.append_text(LoseBg)
  editor.leave(bglib.doc.doctree.TableCellElement)
  editor.leave(bglib.doc.doctree.TableRowElement)




def CubelessEquity(editor, ply=0, cubeless=0.0, money=0.0, 
                           Win=0.0, WinG=0.0, WinBg=0.0, Lose=0.0, LoseG=0.0, LoseBg=0.0, **kw):
    assert isinstance(ply, int)
    assert isinstance(money, float)
    assert isinstance(cubeless, float)
    assert isinstance(Win, float)
    assert isinstance(WinG, float)
    assert isinstance(WinBg, float)
    assert isinstance(Lose, float)
    assert isinstance(LoseG, float)
    assert isinstance(LoseBg, float)

    ply = str(ply)
    cubeless = signed_one_three(cubeless)
    money = signed_one_three(money)
    Win = percent_two_one(Win)
    WinG = percent_two_one(WinG)
    WinBg = percent_two_one(WinBg)
    Lose = percent_two_one(Lose)
    LoseG = percent_two_one(LoseG)
    LoseBg = percent_two_one(LoseBg)

    #t = string.Template(
    #    '''<table>\n'''
    #    '''<tr class='headerrow'><th rowspan='2'>Ply</th><th colspan='6'> Cubeless Eq. </th></tr>\n'''
    #    '''<tr class='headerrow'><th>Win</th><th>WinG</th><th>WinBg</th><th>Lose</th><th>LoseG</th><th>LoseBg</th></tr>\n'''
    #    '''<tr class='oddrow'><td rowspan='2'>$ply</td><td class='Equity' colspan='6'> $cubeless (Money $money) </td></tr>\n'''
    #    '''<tr class='oddrow'><td>$Win</td><td>$WinG</td><td>$WinBg</td><td>$Lose</td><td>$LoseG</td><td>$LoseBg</td></tr>\n'''
    #'''</table>\n''')
    #return t.substitute(cubeless=cubeless, money=money, ply=ply,
    #                    Win=Win, WinG=WinG, WinBg=WinBg,
    #                     Lose=Lose, LoseG=LoseG, LoseBg=LoseBg)

    editor.enter(bglib.doc.doctree.TableElement, **{'class':'cubeless'})
    editor.enter(bglib.doc.doctree.TableRowElement, **{'class':'headerrow'})
    editor.enter(bglib.doc.doctree.TableHeaderElement, rowspan='2')
    editor.append_text('Ply')
    editor.leave(bglib.doc.doctree.TableHeaderElement)
    editor.enter(bglib.doc.doctree.TableHeaderElement, colspan='6')
    editor.append_text('Cubeless Eq. ')
    editor.leave(bglib.doc.doctree.TableHeaderElement)
    editor.leave(bglib.doc.doctree.TableRowElement)

    editor.enter(bglib.doc.doctree.TableRowElement, **{'class':'headerrow'})
    editor.enter(bglib.doc.doctree.TableHeaderElement)
    editor.append_text('Win')
    editor.leave(bglib.doc.doctree.TableHeaderElement)
    editor.enter(bglib.doc.doctree.TableHeaderElement)
    editor.append_text('WinG')
    editor.leave(bglib.doc.doctree.TableHeaderElement)
    editor.enter(bglib.doc.doctree.TableHeaderElement)
    editor.append_text('WinBg')
    editor.leave(bglib.doc.doctree.TableHeaderElement)
    editor.enter(bglib.doc.doctree.TableHeaderElement)
    editor.append_text('Lose')
    editor.leave(bglib.doc.doctree.TableHeaderElement)
    editor.enter(bglib.doc.doctree.TableHeaderElement)
    editor.append_text('LoseG')
    editor.leave(bglib.doc.doctree.TableHeaderElement)
    editor.enter(bglib.doc.doctree.TableHeaderElement)
    editor.append_text('LoseBg')
    editor.leave(bglib.doc.doctree.TableHeaderElement)
    editor.leave(bglib.doc.doctree.TableRowElement)

    editor.enter(bglib.doc.doctree.TableRowElement, **{'class':'oddrow'})
    editor.enter(bglib.doc.doctree.TableCellElement, rowspan='2')
    editor.append_text(ply)
    editor.leave(bglib.doc.doctree.TableCellElement)
    editor.enter(bglib.doc.doctree.TableCellElement, **{'class':'Equity', 'colspan':"6"})
    editor.append_text('%s (Money %s)'%(cubeless, money))
    editor.leave(bglib.doc.doctree.TableCellElement)
    editor.leave(bglib.doc.doctree.TableRowElement)

    editor.enter(bglib.doc.doctree.TableRowElement, **{'class':'oddrow'})
    editor.enter(bglib.doc.doctree.TableCellElement)
    editor.append_text(Win)
    editor.leave(bglib.doc.doctree.TableCellElement)

    editor.enter(bglib.doc.doctree.TableCellElement)
    editor.append_text(WinG)
    editor.leave(bglib.doc.doctree.TableCellElement)

    editor.enter(bglib.doc.doctree.TableCellElement)
    editor.append_text(WinBg)
    editor.leave(bglib.doc.doctree.TableCellElement)

    editor.enter(bglib.doc.doctree.TableCellElement)
    editor.append_text(Lose)
    editor.leave(bglib.doc.doctree.TableCellElement)

    editor.enter(bglib.doc.doctree.TableCellElement)
    editor.append_text(LoseG)
    editor.leave(bglib.doc.doctree.TableCellElement)

    editor.enter(bglib.doc.doctree.TableCellElement)
    editor.append_text(LoseBg)
    editor.leave(bglib.doc.doctree.TableCellElement)
    editor.leave(bglib.doc.doctree.TableRowElement)

    editor.leave(bglib.doc.doctree.TableElement)

