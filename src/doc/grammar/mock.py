#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2006-2008 Noriyuki Hosaka nori@backgammon.gr.jp
#
import bglib.model.constants

class DataBaseMock(object):
  def get_analysis(self, pid, mid):
    test_data = {('vzsAAFhu2xFABA','QYkqASAAIAAA'):( # this is cube action ....
                   dict(name='CubelessEquity', 
                        ply=2, cubeless=0.011, money=0.008, 
                        Win=0.519, WinG=0.072, WinBg=0.002,
                        Lose=0.481, LoseG=0.101, LoseBg=0.002),
                   dict(nth=1, action=bglib.model.constants.no_double, 
                        name='No double', equity=0.236, diff=None, actual=True),
                   dict(nth=2, action=bglib.model.constants.double_pass, 
                        name='Double, pass', equity=0.236, diff=0.764),
                   dict(nth=3, action=bglib.model.constants.double_take, 
                        name='Double, take', equity=-0.096, diff=-0.332),
                 ),

                 ('cNcxAxCY54YBBg', 'cAn7ADAAIAAA'): (
                   dict(nth=1, ply=2, cubeful=True, move="21/15(2) 13/7(2)", equity=+0.975, diff=0.0, 
                      Win=0.752, WinG=0.123, WinBg=0.002, Lose=0.248, LoseG=0.028, LoseBg=0.000),
                   dict(nth=2, cubeful=True, ply=2, move="21/9(2)", equity=+0.914, diff=-0.061,
                      Win=0.733, WinG=0.093, WinBg=0.001, Lose=0.267, LoseG=0.021, LoseBg=0.000),
                   dict(nth=3, cubeful=True, ply=0, move="21/15(2) 8/2*(2)", 
                      equity=+0.614, diff=-0.362,
                      Win=0.671, WinG=0.175, WinBg=0.002, Lose=0.329, LoseG=0.060, LoseBg=0.001),
                 ),
                 ('fake','fake'):(
                   dict(nth=1, move='12/10', ply=2, equity=0.321, diff=0.0, Win=56.2, WinG=11.0, WinBg=0.3, Lose=43.8, LoseG=4.0, LoseBg=0.1, actual=False),
                   dict(nth=2, move='12/10',ply=2, equity=0.213, diff=-0.108, Win=56.2, WinG=11.0, WinBg=0.3, Lose=43.8, LoseG=4.0, LoseBg=0.1, actual=False),
                   dict(nth=3, move='12/10', ply=2, equity=0.120, diff=-0.201, Win=56.2, WinG=11.0, WinBg=0.3, Lose=43.8, LoseG=4.0, LoseBg=0.1, actual=True),
                 )
                }

    r = test_data[(pid, mid)]
    return 'CubelessEquity' == r[0].get('name', ''), r

