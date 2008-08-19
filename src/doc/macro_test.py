#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2006-2008 Noriyuki Hosaka nori@backgammon.gr.jp
#
import unittest
import bglib.model.constants
import bglib.doc.macro
import bglib.doc.mock

class MacroTest(unittest.TestCase):
  def setUp(self):
    self.macroprocessor = bglib.doc.macro.Processor(bglib.doc.mock.DataBaseMock())

  def test_bad_handler(self):
    self.assertEqual(
      self.macroprocessor.bad_name_handler('badname', None),
      '''<div class="error">No such macro "badname" with argument "None" </div>'''
      )
    
  def test_RB(self):
    self.assertEqual(
      self.macroprocessor.BR(None),
      '<br />'
      )

  def test_position_box_1(self):
    self.assertEqual(
      self.macroprocessor.dispatch('Position', 'vzsAAFhu2xFABA:QYkqASAAIAAA'),
      ('''<div class="position">\n'''
           '''<img src="/image?format=png'''
           '''&pid=vzsAAFhu2xFABA'''
           '''&mid=QYkqASAAIAAA'''
           '''&height=300&width=400&css=minimal" />\n'''
       '''</div>\n'''))

  def test_position_box_2(self):
    self.assertEqual(
      self.macroprocessor.dispatch('Position', '4HPwATDgc/ABMA:MAAAAAAAAAAA'),
      ('''<div class="position">\n'''
           '''<img src="/image?format=png'''
           '''&pid=4HPwATDgc/ABMA'''
           '''&mid=MAAAAAAAAAAA'''
           '''&height=300&width=400&css=minimal" />\n'''
       '''</div>\n'''))

  def test_position_box_3(self):
    self.assertEqual(
      self.macroprocessor.dispatch('Position', 'haha:hahaha'),
      '''<div class="error">Bad args "haha:hahaha" for Position</div>\n''')

  def test_analysis_box_cubeaction_1(self):
    self.assertEqual(
      self.macroprocessor.dispatch('Analysis', 'vzsAAFhu2xFABA:QYkqASAAIAAA'),
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

  def test_analysis_box_move_2(self):
    self.assertEqual(
      self.macroprocessor.dispatch('Analysis', 'cNcxAxCY54YBBg:cAn7ADAAIAAA'),
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

  def test_analysis_box_2(self):
    self.assertEqual(
      self.macroprocessor.dispatch('Analysis', 'haha:hahaha'),
      '''<div class="error">Bad args "haha:hahaha" for Analysis</div>\n''')
  def test_analysis_box_3(self):
    self.assertEqual(
      self.macroprocessor.dispatch('Analysis', 'cNcxAxCY54YBBg:cAn7ADAAIAAA'),
      (
       '''<table>\n'''
       '''<tr class='headerrow'><th rowspan='2'>#</th><th rowspan='2'>move</th><th rowspan='2'>Ply</th><th colspan='6'> Eq.(diff)</th></tr>\n'''
       '''<tr class='headerrow'><th>Win</th><th>WinG</th><th>WinBg</th><th>Lose</th><th>LoseG</th><th>LoseBg</th></tr>\n'''
       '''<tr class='oddrow'><th rowspan='2'>1</th><td rowspan='2'>21/15(2) 13/7(2)</td><td rowspan='2'>2</td><td class='Equity' colspan='6'> +0.975 </td></tr>\n'''
       '''<tr class='oddrow'><td>0.8</td><td>0.1</td><td>0.0</td><td>0.2</td><td>0.0</td><td>0.0</td></tr>\n'''
       '''<tr class='evenrow'><th rowspan='2'>2</th><td rowspan='2'>21/9(2)</td><td rowspan='2'>2</td><td class='Equity' colspan='6'> +0.914 (-0.061) </td></tr>\n'''
       '''<tr class='evenrow'><td>0.7</td><td>0.1</td><td>0.0</td><td>0.3</td><td>0.0</td><td>0.0</td></tr>\n'''
       '''<tr class='oddrow'><th rowspan='2'>3</th><td rowspan='2'>21/15(2) 8/2*(2)</td><td rowspan='2'>0</td><td class='Equity' colspan='6'> +0.614 (-0.362) </td></tr>\n'''
       '''<tr class='oddrow'><td>0.7</td><td>0.2</td><td>0.0</td><td>0.3</td><td>0.1</td><td>0.0</td></tr>\n'''
       '''</table>\n'''
      ))
  def test_cube_action_table_row_nd(self):
    self.assertEqual(
      self.macroprocessor.CubeAction_table_row(nth=3, action=bglib.model.constants.no_double,
                                     equity=0.926, diff=-0.075, actual=False),
      '''<tr class='oddrow'><th>3</th><td> No double </td><td> +0.926 </td><td> -0.075 </td></tr>\n'''
      )

  def test_cube_action_table_row_dt(self):
    self.assertEqual(
      self.macroprocessor.CubeAction_table_row(nth=2, action=bglib.model.constants.double_take,
                                     equity=1.296, diff=0.296, actual=False),
      '''<tr class='evenrow'><th>2</th><td> Double, take </td><td> +1.296 </td><td> +0.296 </td></tr>\n'''
      )

  def test_movelisting_header(self):
    self.assertEqual(
      self.macroprocessor.Movelisting_header(),
      ('''<tr class='headerrow'><th rowspan='2'>#</th><th rowspan='2'>move</th><th rowspan='2'>Ply</th><th colspan='6'> Eq.(diff)</th></tr>\n'''
      '''<tr class='headerrow'>'''
      '''<th>Win</th><th>WinG</th><th>WinBg</th><th>Lose</th><th>LoseG</th><th>LoseBg</th></tr>\n'''
      ))

  def test_movelisting_row_odd(self):
    self.assertEqual(
      self.macroprocessor.Movelisting_row(nth=1, move='12/10', ply=2, equity=0.321, diff=0.0, Win=56.2, WinG=11.0, WinBg=0.3, Lose=43.8, LoseG=4.0, LoseBg=0.1, actual=False),
      ('''<tr class='oddrow'><th rowspan='2'>1</th><td rowspan='2'>12/10</td><td rowspan='2'>2</td><td class='Equity' colspan='6'> +0.321 </td></tr>\n'''
      '''<tr class='oddrow'><td>56.2</td><td>11.0</td><td>0.3</td><td>43.8</td><td>4.0</td><td>0.1</td></tr>\n'''
      ))

  def test_movelisting_row_even(self):
    self.assertEqual(
      self.macroprocessor.Movelisting_row(nth=2, move='12/10',ply=2, equity=0.213, diff=-0.108, Win=56.2, WinG=11.0, WinBg=0.3, Lose=43.8, LoseG=4.0, LoseBg=0.1, actual=False),
      ('''<tr class='evenrow'><th rowspan='2'>2</th><td rowspan='2'>12/10</td><td rowspan='2'>2</td><td class='Equity' colspan='6'> +0.213 (-0.108) </td></tr>\n'''
      '''<tr class='evenrow'><td>56.2</td><td>11.0</td><td>0.3</td><td>43.8</td><td>4.0</td><td>0.1</td></tr>\n'''
      ))

  def test_movelisting_row_actual(self):
    self.assertEqual(
      self.macroprocessor.Movelisting_row(nth=3, move='12/10', ply=2, equity=0.120, diff=-0.201, Win=56.2, WinG=11.0, WinBg=0.3, Lose=43.8, LoseG=4.0, LoseBg=0.1, actual=True),
      ('''<tr class='actualrow'><th rowspan='2'>3</th><td rowspan='2'>12/10</td><td rowspan='2'>2</td><td class='Equity' colspan='6'> +0.120 (-0.201) </td></tr>\n'''
      '''<tr class='actualrow'><td>56.2</td><td>11.0</td><td>0.3</td><td>43.8</td><td>4.0</td><td>0.1</td></tr>\n'''
      ))

  def test_cubeless_equity(self):
    self.assertEqual(
      self.macroprocessor.CubelessEquity(cubeless=0.706, money=0.696, ply=2,
                              Win=76.6, WinG=23.6, WinBg=1.0, Lose=23.4, LoseG=7.8, LoseBg=0.3),
      ('''<table>\n'''
       '''<tr class='headerrow'><th rowspan='2'>Ply</th><th colspan='6'> Cubeless Eq. </th></tr>\n'''
       '''<tr class='headerrow'><th>Win</th><th>WinG</th><th>WinBg</th><th>Lose</th><th>LoseG</th><th>LoseBg</th></tr>\n'''
       '''<tr class='oddrow'><td rowspan='2'>2</td><td class='Equity' colspan='6'> +0.706 (Moeny +0.696) </td></tr>\n'''
       '''<tr class='oddrow'><td>76.6</td><td>23.6</td><td>1.0</td><td>23.4</td><td>7.8</td><td>0.3</td></tr>\n'''
       '''</table>\n'''))

  def test_cube_action_table_header(self):
    self.assertEqual(
      self.macroprocessor.CubeAction_table_header(),
      '''<tr class='headerrow'><th>#</th><th>action</th><th colspan='2'> Cubeful Eq. </th></tr>\n'''
      )

  def test_cube_action_table_row_dp(self):
    self.assertEqual(
      self.macroprocessor.CubeAction_table_row(nth=1, action=bglib.model.constants.double_pass,
                                     equity=1.000, actual=False),
      '''<tr class='oddrow'><th>1</th><td> Double, pass </td><td> +1.000 </td><td>  </td></tr>\n'''
      )


