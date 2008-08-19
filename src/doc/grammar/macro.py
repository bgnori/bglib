#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2006-2008 Noriyuki Hosaka nori@backgammon.gr.jp
#
import string
import re
import bglib.model.constants

import html 

def signed_one_three(f):
  assert isinstance(f, float)
  return '%+1.3f'%f

def percent_two_one(f):
  assert isinstance(f, float)
  return '%2.1f'%f

class Processor(object):
  def __init__(self, db):
    self.db = db
  #dispatch and exec
  def dispatch(self, name, args):
    handler = getattr(self, name, None)
    if handler is not None and callable(handler):
      ret = handler(args)
      if ret == args:
        return self.bad_args_handler(name, args)
      return ret
    return self.bad_name_handler(name, args)
  
  def bad_name_handler(self, name, args):
    t = string.Template('''<div class="error">No such macro "$name" with argument "$args" </div>''')
    return t.substitute(name=html.escape(name), args=html.escape(args or 'None'))

  def bad_args_handler(self, name, args):
    return '''<div class="error">Bad args "%s" for %s</div>\n'''%(html.escape(args), name)

  def BR(self, args):
    return '<br />'

    r"(?P<_pattern_temp_map>!?temp_map\([a-zA-Z0-9/+]{14}:[a-zA-Z0-9/+]{12}\))",

  def Timestamp(self, args):
    return '<b>Sun Jul 27 08:59:07 2008</b>'

  def Position(self, args):
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

  def Analysis(self, args):
    matchobj = re.match(r"(?P<valid>(?P<pid>[a-zA-Z0-9/+]{14}):(?P<mid>[a-zA-Z0-9/+]{12}))", args)
    if not matchobj:
      return args
    d = matchobj.groupdict(dict(pid='N/A', mid='N/A'))
    cubeaction, analysis = self.db.get_analysis(d['pid'], d['mid'])
    ret = ''

    if cubeaction:
      ret += self.CubelessEquity(**(analysis[0]))
      ret += '<table>\n'
      ret += self.CubeAction_table_header()
      for i, row in enumerate(analysis[1:]):
        assert i + 1 == row['nth']
        ret += self.CubeAction_table_row(**row)
      return ret + '</table>\n'
    else:
      ret += '<table>\n'
      ret += self.Movelisting_header()
      for i, row in enumerate(analysis):
        assert i + 1 == row['nth']
        ret += self.Movelisting_row(**row)
      return ret + '</table>\n'
    

  def CubeAction_table_header(self):
    return '''<tr class='headerrow'><th>#</th><th>action</th><th colspan='2'> Cubeful Eq. </th></tr>\n'''

  def CubeAction_table_row(self, nth=0, action=0, equity=0.0, diff=None, actual=False, **kw):
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

  def Movelisting_header(self):
      return ('''<tr class='headerrow'><th rowspan='2'>#</th><th rowspan='2'>move</th><th rowspan='2'>Ply</th><th colspan='6'> Eq.(diff)</th></tr>\n'''
      '''<tr class='headerrow'>'''
      '''<th>Win</th><th>WinG</th><th>WinBg</th><th>Lose</th><th>LoseG</th><th>LoseBg</th></tr>\n'''
      )

  def Movelisting_row(self, nth, move, ply, equity, diff, Win, WinG, WinBg, Lose, LoseG, LoseBg, actual=None, **kw):
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


  def CubelessEquity(self, ply=0, cubeless=0.0, money=0.0, 
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

