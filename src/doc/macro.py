#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2006-2008 Noriyuki Hosaka nori@backgammon.gr.jp
#
import types
import string
import re
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
    t = string.Template('''<div class="error">No such macro "$name" with argument "$args" </div>''')
    return t.substitute(name=bglib.doc.html.escape(name), args=bglib.doc.html.escape(args or 'None'))

def _bad_args_handler(editor, name, args):
    return '''<div class="error">Bad args "%s" for %s</div>\n'''%(bglib.doc.html.escape(args), name)

class Processor(object):
  pass


def BR(editor, args):
  editor.enter(bglib.doc.doctree.BRElement)
  editor.leave(bglib.doc.doctree.BRElement)
  return True
  

register(BR)

  #r"(?P<_pattern_temp_map>!?temp_map\([a-zA-Z0-9/+]{14}:[a-zA-Z0-9/+]{12}\))",

def Timestamp(editor, args):
    return '<b>Sun Jul 27 08:59:07 2008</b>'
register(Timestamp)

def Position(editor, args):
    def replace(matchobj):
      d = matchobj.groupdict(dict(pid='N/A', mid='N/A'))
      t = string.Template(
        '''<div class="position">\n'''
        '''<img src="/image?format=png'''
        '''&pid=$pid'''
        '''&mid=$mid'''
        '''&height=300&width=400&css=minimal" />'''
        '''\n</div>\n''')
      return t.substitute(d)
    r = r"(?P<valid>(?P<pid>[a-zA-Z0-9/+]{14}):(?P<mid>[a-zA-Z0-9/+]{12}))"
    return re.sub(r, replace, args)
register(Position)

def Analysis(editor, args):
    matchobj = re.match(r"(?P<valid>(?P<pid>[a-zA-Z0-9/+]{14}):(?P<mid>[a-zA-Z0-9/+]{12}))", args)
    if not matchobj:
      return args
    d = matchobj.groupdict(dict(pid='N/A', mid='N/A'))
    cubeaction, analysis = _db.get_analysis(d['pid'], d['mid'])
    ret = ''

    if cubeaction:
      ret += CubelessEquity(editor, **(analysis[0]))
      ret += '<table>\n'
      ret += CubeAction_table_header(editor)
      for i, row in enumerate(analysis[1:]):
        assert i + 1 == row['nth']
        ret += CubeAction_table_row(editor, **row)
      return ret + '</table>\n'
    else:
      ret += '<table>\n'
      ret += Movelisting_header(editor)
      for i, row in enumerate(analysis):
        assert i + 1 == row['nth']
        ret += Movelisting_row(editor, **row)
      return ret + '</table>\n'
register(Analysis) 

def CubeAction_table_header(editor):
    return '''<tr class='headerrow'><th>#</th><th>action</th><th colspan='2'> Cubeful Eq. </th></tr>\n'''

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
    t = string.Template('''<tr class='$klass'><th>$nth</th><td> $action </td><td> $equity </td><td> $diff </td></tr>\n''')
    return t.substitute(klass=klass, nth=nth, 
                        action=bglib.model.constants.cubeaction_strings[action],
                        equity=equity, diff=diff)

def Movelisting_header(editor):
      return ('''<tr class='headerrow'><th rowspan='2'>#</th><th rowspan='2'>move</th><th rowspan='2'>Ply</th><th colspan='6'> Eq.(diff)</th></tr>\n'''
      '''<tr class='headerrow'>'''
      '''<th>Win</th><th>WinG</th><th>WinBg</th><th>Lose</th><th>LoseG</th><th>LoseBg</th></tr>\n'''
      )

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

    t = string.Template(
        '''<tr class='$klass'><th rowspan='2'>$nth</th><td rowspan='2'>$move</td>'''
        '''<td rowspan='2'>$ply</td><td class='Equity' colspan='6'> $equity $diff</td></tr>\n'''
        '''<tr class='$klass'><td>$Win</td><td>$WinG</td><td>$WinBg</td>'''
        '''<td>$Lose</td><td>$LoseG</td><td>$LoseBg</td></tr>\n'''
        )
    return t.substitute(nth=nth, klass=klass, move=move, ply=ply,
                        equity=equity, diff=diff,
                        Win=Win, WinG=WinG, WinBg=WinBg,
                        Lose=Lose, LoseG=LoseG, LoseBg=LoseBg)


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

    t = string.Template(
        '''<table>\n'''
        '''<tr class='headerrow'><th rowspan='2'>Ply</th><th colspan='6'> Cubeless Eq. </th></tr>\n'''
        '''<tr class='headerrow'><th>Win</th><th>WinG</th><th>WinBg</th><th>Lose</th><th>LoseG</th><th>LoseBg</th></tr>\n'''
        '''<tr class='oddrow'><td rowspan='2'>$ply</td><td class='Equity' colspan='6'> $cubeless (Moeny $money) </td></tr>\n'''
        '''<tr class='oddrow'><td>$Win</td><td>$WinG</td><td>$WinBg</td><td>$Lose</td><td>$LoseG</td><td>$LoseBg</td></tr>\n'''
    '''</table>\n''')
    return t.substitute(cubeless=cubeless, money=money, ply=ply,
                        Win=Win, WinG=WinG, WinBg=WinBg,
                         Lose=Lose, LoseG=LoseG, LoseBg=LoseBg)

