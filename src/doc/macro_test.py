#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2006-2008 Noriyuki Hosaka nori@backgammon.gr.jp
#
import bglib.model.constants
import bglib.doc.html
import bglib.doc.macro
import bglib.doc.mock
import bglib.doc.doctree

class MacroTest(bglib.doc.html.HtmlTestCase):
  def setUp(self):
    bglib.doc.macro.setup(bglib.doc.mock.DataBaseMock())
    self.root = bglib.doc.doctree.BgWikiElementRoot()
    self.editor = bglib.doc.doctree.Editor()
    self.editor.start(self.root)
    self.writer = bglib.doc.doctree.HtmlWriter()
    self.debugvisitor = bglib.doc.doctree.DebugVisitor()

  def test_bad_handler(self):
    bglib.doc.macro.dispatch(self.editor, "badname", None)
    self.editor.done()
    self.editor.accept(self.writer)
    self.assertHtmlEqual(
      self.writer.html(),
      """<span class="error">No such macro "badname" with argument "None"</span>"""
      )
    
  def test_BR(self):
    bglib.doc.macro.dispatch(self.editor, "BR", None)
    self.editor.done()
    self.editor.accept(self.writer)
    self.assertHtmlEqual(
      self.writer.html(),
      "<br />"
      )

  def test_position_box_1(self):
    bglib.doc.macro.dispatch(self.editor, "Position", "vzsAAFhu2xFABA:QYkqASAAIAAA")
    self.editor.done()
    self.editor.accept(self.writer)
    self.assertHtmlEqual(
      self.writer.html(),
      ("""<span class="position">\n"""
           """<img src="/image?"""
           """format=png"""
           """&pid=vzsAAFhu2xFABA"""
           """&mid=QYkqASAAIAAA"""
           """&height=300&width=400"""
           """&css=minimal"""
           """" />\n"""
       """</span>\n"""))

  def test_position_box_2(self):
    bglib.doc.macro.dispatch(self.editor, "Position", "4HPwATDgc/ABMA:MAAAAAAAAAAA")
    self.editor.done()
    self.editor.accept(self.writer)
    self.assertHtmlEqual(
      self.writer.html(),
      ("""<span class="position">\n"""
           """<img src="/image?format=png"""
           """&pid=4HPwATDgc%2FABMA"""
           """&mid=MAAAAAAAAAAA"""
           """&height=300&width=400&css=minimal" />\n"""
       """</span>\n"""))

  def test_position_box_3(self):
    bglib.doc.macro.dispatch(self.editor, "Position", "haha:hahaha")
    self.editor.done()
    self.editor.accept(self.writer)
    self.assertHtmlEqual(
      self.writer.html(),
      """<span class="position"><span class="error">Bad args "haha:hahaha" for Position</span></span>""")

  def test_position_box_4(self):
    bglib.doc.macro.dispatch(self.editor, "Position", "vzsAAFhu2xFABA:QYkqASAAIAAA, css=safari")
    self.editor.done()
    self.editor.accept(self.writer)
    print self.writer.html()
    self.assertEqual(
      self.writer.html(),
      ("""<span class="position">\n"""
           """<img src="/image?format=png"""
           """&pid=vzsAAFhu2xFABA"""
           """&mid=QYkqASAAIAAA"""
           """&height=300&width=400&css=safari" />\n"""
       """</span>\n"""))

  def test_position_box_5(self):
    bglib.doc.macro.dispatch(self.editor, "Position", "vzsAAFhu2xFABA:QYkqASAAIAAA,css=safari")
    self.editor.done()
    self.editor.accept(self.writer)
    print self.writer.html()
    self.assertEqual(
      self.writer.html(),
      ("""<span class="position">\n"""
           """<img src="/image?format=png"""
           """&pid=vzsAAFhu2xFABA"""
           """&mid=QYkqASAAIAAA"""
           """&height=300&width=400&css=safari" />\n"""
       """</span>\n"""))

  def test_position_box_6(self):
    bglib.doc.macro.dispatch(self.editor, "Position", "jM/BATDQc+QBMA:cAkWAAAAAAAA")
    self.editor.done()
    self.editor.accept(self.writer)
    print self.writer.html()
    self.assertHtmlEqual(
      self.writer.html(),
      ("""<span class="position">\n"""
           """<img src="/image?format=png"""
           """&pid=jM%2FBATDQc%2BQBMA"""
           """&mid=cAkWAAAAAAAA"""
           """&height=300&width=400&css=minimal" />\n"""
       """</span>\n"""))

  def test_analysis_box_cubeaction_1(self):
    bglib.doc.macro.dispatch(self.editor, "Analysis", "vzsAAFhu2xFABA:QYkqASAAIAAA")
    self.editor.done()
    self.editor.accept(self.writer)
    self.assertHtmlEqual(
      self.writer.html(),
      ("""<table class="cubeless">\n"""
       """<tr class="headerrow"><th rowspan="2">Ply</th><th colspan="6"> Cubeless Eq. </th></tr>\n"""
       """<tr class="headerrow"><th>Win</th><th>WinG</th><th>WinBg</th><th>Lose</th><th>LoseG</th><th>LoseBg</th></tr>\n"""
       """<tr class="oddrow"><td rowspan="2">2</td><td class="Equity" colspan="6"> +0.011 (Money +0.008) </td></tr>\n"""
       """<tr class="oddrow"><td>0.5</td><td>0.1</td><td>0.0</td><td>0.5</td><td>0.1</td><td>0.0</td></tr>\n"""
       """</table>\n"""
       """<table class="cubeaction">\n"""
       """<tr class="headerrow"><th>#</th><th>action</th><th colspan="2"> Cubeful Eq. </th></tr>\n"""
       """<tr class="actualrow"><th>1</th><td> No double </td><td> +0.236 </td><td>  </td></tr>\n"""
       """<tr class="evenrow"><th>2</th><td> Double, pass </td><td> +0.236 </td><td> +0.764 </td></tr>\n"""
       """<tr class="oddrow"><th>3</th><td> Double, take </td><td> -0.096 </td><td> -0.332 </td></tr>\n"""
       """</table>\n"""))

  def test_analysis_box_move_2(self):
    bglib.doc.macro.dispatch(self.editor, "Analysis", "cNcxAxCY54YBBg:cAn7ADAAIAAA")
    self.editor.done()
    self.editor.accept(self.writer)
    self.assertHtmlEqual(
      self.writer.html(),
      ("""<table class="move">\n"""
"""<tr class="headerrow"><th rowspan="2">#</th><th rowspan="2">move</th><th rowspan="2">Ply</th><th colspan="6"> Eq.(diff)</th></tr>\n"""
"""<tr class="headerrow"><th>Win</th><th>WinG</th><th>WinBg</th><th>Lose</th><th>LoseG</th><th>LoseBg</th></tr>\n"""
"""<tr class="oddrow"><th rowspan="2">1</th><td rowspan="2">21/15(2) 13/7(2)</td><td rowspan="2">2</td><td class="Equity" colspan="6"> +0.975 </td></tr>\n"""
"""<tr class="oddrow"><td>0.8</td><td>0.1</td><td>0.0</td><td>0.2</td><td>0.0</td><td>0.0</td></tr>\n"""
"""<tr class="evenrow"><th rowspan="2">2</th><td rowspan="2">21/9(2)</td><td rowspan="2">2</td><td class="Equity" colspan="6"> +0.914 (-0.061) </td></tr>\n"""
"""<tr class="evenrow"><td>0.7</td><td>0.1</td><td>0.0</td><td>0.3</td><td>0.0</td><td>0.0</td></tr>\n"""
"""<tr class="oddrow"><th rowspan="2">3</th><td rowspan="2">21/15(2) 8/2*(2)</td><td rowspan="2">0</td><td class="Equity" colspan="6"> +0.614 (-0.362) </td></tr>\n"""
"""<tr class="oddrow"><td>0.7</td><td>0.2</td><td>0.0</td><td>0.3</td><td>0.1</td><td>0.0</td></tr>\n"""
       """</table>\n"""))

  def test_analysis_box_2(self):
    bglib.doc.macro.dispatch(self.editor, "Analysis", "haha:hahaha")
    self.editor.done()
    self.editor.accept(self.writer)
    self.assertHtmlEqual(
      self.writer.html(),
      """<span class="error">Bad args "haha:hahaha" for Analysis</span>\n""")
  def test_analysis_box_3(self):
    bglib.doc.macro.dispatch(self.editor, "Analysis", "cNcxAxCY54YBBg:cAn7ADAAIAAA"),
    self.editor.done()
    self.editor.accept(self.writer)
    self.assertHtmlEqual(
      self.writer.html(),
      (
       """<table class="move">\n"""
       """<tr class="headerrow"><th rowspan="2">#</th><th rowspan="2">move</th><th rowspan="2">Ply</th><th colspan="6"> Eq.(diff)</th></tr>\n"""
       """<tr class="headerrow"><th>Win</th><th>WinG</th><th>WinBg</th><th>Lose</th><th>LoseG</th><th>LoseBg</th></tr>\n"""
       """<tr class="oddrow"><th rowspan="2">1</th><td rowspan="2">21/15(2) 13/7(2)</td><td rowspan="2">2</td><td class="Equity" colspan="6"> +0.975 </td></tr>\n"""
       """<tr class="oddrow"><td>0.8</td><td>0.1</td><td>0.0</td><td>0.2</td><td>0.0</td><td>0.0</td></tr>\n"""
       """<tr class="evenrow"><th rowspan="2">2</th><td rowspan="2">21/9(2)</td><td rowspan="2">2</td><td class="Equity" colspan="6"> +0.914 (-0.061) </td></tr>\n"""
       """<tr class="evenrow"><td>0.7</td><td>0.1</td><td>0.0</td><td>0.3</td><td>0.0</td><td>0.0</td></tr>\n"""
       """<tr class="oddrow"><th rowspan="2">3</th><td rowspan="2">21/15(2) 8/2*(2)</td><td rowspan="2">0</td><td class="Equity" colspan="6"> +0.614 (-0.362) </td></tr>\n"""
       """<tr class="oddrow"><td>0.7</td><td>0.2</td><td>0.0</td><td>0.3</td><td>0.1</td><td>0.0</td></tr>\n"""
       """</table>\n"""
      ))
  def test_cube_action_table_row_nd(self):
    bglib.doc.macro.CubeAction_table_row(self.editor, 
        nth=3, action=bglib.model.constants.no_double, 
        equity=0.926, diff=-0.075, actual=False)
    self.editor.done()
    self.editor.accept(self.writer)
    self.assertHtmlEqual(
      self.writer.html(),
      """<tr class="oddrow"><th>3</th><td> No double </td><td> +0.926 </td><td> -0.075 </td></tr>\n"""
      )

  def test_cube_action_table_row_dt(self):
    bglib.doc.macro.CubeAction_table_row(self.editor,
        nth=2, action=bglib.model.constants.double_take,
        equity=1.296, diff=0.296, actual=False)
    self.editor.done()
    self.editor.accept(self.writer)
    self.assertHtmlEqual(
      self.writer.html(),
      """<tr class="evenrow"><th>2</th><td> Double, take </td><td> +1.296 </td><td> +0.296 </td></tr>\n"""
      )

  def test_movelisting_header(self):
    bglib.doc.macro.Movelisting_header(self.editor)
    self.editor.done()
    self.editor.accept(self.writer)
    self.assertHtmlEqual(
      self.writer.html(),
      ("""<tr class="headerrow"><th rowspan="2">#</th><th rowspan="2">move</th><th rowspan="2">Ply</th><th colspan="6"> Eq.(diff)</th></tr>\n"""
      """<tr class="headerrow">"""
      """<th>Win</th><th>WinG</th><th>WinBg</th><th>Lose</th><th>LoseG</th><th>LoseBg</th></tr>\n"""
      ))

  def test_movelisting_row_odd(self):
    bglib.doc.macro.Movelisting_row(self.editor,
        nth=1, move="12/10", ply=2, equity=0.321, diff=0.0, 
        Win=56.2, WinG=11.0, WinBg=0.3, Lose=43.8, LoseG=4.0, LoseBg=0.1, actual=False)
    self.editor.done()
    self.editor.accept(self.writer)
    self.assertHtmlEqual(
      self.writer.html(),
      ("""<tr class="oddrow"><th rowspan="2">1</th><td rowspan="2">12/10</td><td rowspan="2">2</td><td class="Equity" colspan="6"> +0.321 </td></tr>\n"""
      """<tr class="oddrow"><td>56.2</td><td>11.0</td><td>0.3</td><td>43.8</td><td>4.0</td><td>0.1</td></tr>\n"""
      ))

  def test_movelisting_row_even(self):
    bglib.doc.macro.Movelisting_row(self.editor,
        nth=2, move="12/10",ply=2, equity=0.213, diff=-0.108, 
        Win=56.2, WinG=11.0, WinBg=0.3, Lose=43.8, LoseG=4.0, LoseBg=0.1, actual=False)
    self.editor.done()
    self.editor.accept(self.writer)
    self.assertHtmlEqual(
      self.writer.html(),
      ("""<tr class="evenrow"><th rowspan="2">2</th><td rowspan="2">12/10</td><td rowspan="2">2</td><td class="Equity" colspan="6"> +0.213 (-0.108) </td></tr>\n"""
      """<tr class="evenrow"><td>56.2</td><td>11.0</td><td>0.3</td><td>43.8</td><td>4.0</td><td>0.1</td></tr>\n"""
      ))

  def test_movelisting_row_actual(self):
    bglib.doc.macro.Movelisting_row(self.editor,
        nth=3, move="12/10", ply=2, equity=0.120, diff=-0.201,
        Win=56.2, WinG=11.0, WinBg=0.3, Lose=43.8, LoseG=4.0, LoseBg=0.1, actual=True)
    self.editor.done()
    self.editor.accept(self.writer)
    self.assertHtmlEqual(
      self.writer.html(),
      ("""<tr class="actualrow"><th rowspan="2">3</th><td rowspan="2">12/10</td><td rowspan="2">2</td><td class="Equity" colspan="6"> +0.120 (-0.201) </td></tr>\n"""
      """<tr class="actualrow"><td>56.2</td><td>11.0</td><td>0.3</td><td>43.8</td><td>4.0</td><td>0.1</td></tr>\n"""
      ))

  def test_cubeless_equity(self):
    bglib.doc.macro.CubelessEquity(self.editor,
        cubeless=0.706, money=0.696, ply=2,
        Win=76.6, WinG=23.6, WinBg=1.0, Lose=23.4, LoseG=7.8, LoseBg=0.3)
    self.editor.done()
    self.editor.accept(self.writer)
    self.assertHtmlEqual(
      self.writer.html(),
      ("""<table class="cubeless">\n"""
       """<tr class="headerrow"><th rowspan="2">Ply</th><th colspan="6"> Cubeless Eq. </th></tr>\n"""
       """<tr class="headerrow"><th>Win</th><th>WinG</th><th>WinBg</th><th>Lose</th><th>LoseG</th><th>LoseBg</th></tr>\n"""
       """<tr class="oddrow"><td rowspan="2">2</td><td class="Equity" colspan="6"> +0.706 (Money +0.696) </td></tr>\n"""
       """<tr class="oddrow"><td>76.6</td><td>23.6</td><td>1.0</td><td>23.4</td><td>7.8</td><td>0.3</td></tr>\n"""
       """</table>\n"""))

  def test_cube_action_table_header(self):
    bglib.doc.macro.CubeAction_table_header(self.editor)
    self.editor.done()
    self.editor.accept(self.writer)
    self.assertHtmlEqual(
      self.writer.html(),
      """<tr class="headerrow"><th>#</th><th>action</th><th colspan="2"> Cubeful Eq. </th></tr>\n"""
      )

  def test_cube_action_table_row_dp(self):
    bglib.doc.macro.CubeAction_table_row(self.editor,
        nth=1, action=bglib.model.constants.double_pass,
        equity=1.000, actual=False)
    self.editor.done()
    self.editor.accept(self.writer)
    self.assertHtmlEqual(
      self.writer.html(),
      """<tr class="oddrow"><th>1</th><td> Double, pass </td><td> +1.000 </td><td>  </td></tr>\n"""
      )


  def test_empty_TOC(self):
    bglib.doc.macro.TableOfContent(self.editor, None)
    self.editor.done()
    self.editor.accept(self.debugvisitor)
    self.assertEqual(
      self.debugvisitor.buf,
      'Root\nTableOfContentNode\n'
    )
    # The html tags in TOC are generated on visit
    self.editor.accept(self.writer)
    print self.writer.html()
    self.assertHtmlEqual(
      self.writer.html(),
      """<ol>"""
      """</ol>"""
      )

  def test_TOC_1(self):
    editor = self.editor
    bglib.doc.macro.TableOfContent(editor, None)
    editor.enter(bglib.doc.doctree.H1Element)
    editor.append_text('This is First H1')
    editor.leave(bglib.doc.doctree.H1Element)
    editor.enter(bglib.doc.doctree.H2Element)
    editor.append_text('This is H2 under First H1')
    editor.leave(bglib.doc.doctree.H2Element)
    editor.enter(bglib.doc.doctree.H1Element)
    editor.append_text('This is second H1')
    editor.leave(bglib.doc.doctree.H1Element)

    editor.done()
    editor.accept(self.debugvisitor)
    self.assertEqual(
      self.debugvisitor.buf,
      'Root\n'
      'TableOfContentNode\n'
      'H1Element\n'
      'Text:This is First H1\n'
      'H2Element\n'
      'Text:This is H2 under First H1\n'
      'H1Element\n'
      'Text:This is second H1\n'
    )
    # The html tags in TOC are generated on visit
    self.editor.accept(self.writer)
    print self.writer.html()
    self.assertHtmlEqual(
      self.writer.html(),
      """<ol>"""
      """<li><a href="#fragment0">This is First H1</a></li>"""
        """<ol>"""
        """<li><a href="#fragment1">This is H2 under First H1</a></li>"""
        """</ol>"""
      """<li><a href="#fragment2">This is second H1</a></li>"""
      """</ol>"""
      """<h1 id="fragment0">This is First H1</h1>"""
      """<h2 id="fragment1">This is H2 under First H1</h2>"""
      """<h1 id="fragment2">This is second H1</h1>"""
      )

