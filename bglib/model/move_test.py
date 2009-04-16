#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2006-2008 Noriyuki Hosaka nori@backgammon.gr.jp
#

import tempfile
import unittest
import nose

from bglib.model.constants import *
from bglib.model import *

class MoveTest(unittest.TestCase):
  def setUp(self):
    self.board = Board()
    self.temp = tempfile.NamedTemporaryFile()

  def tearDown(self):
    pass

  def av_non_doubles_test(self):
    av = AvailableToPlay((3, 2))
    self.assertEqual(av[1], 0)
    self.assertEqual(av[2], 1)
    self.assertEqual(av[3], 1)
    self.assertEqual(av[4], 0)
    self.assertEqual(av[5], 0)
    self.assertEqual(av[6], 0)

    self.assertFalse(1 in av)
    self.assert_(2 in av)
    self.assert_(3 in av)
    self.assertFalse(4 in av)
    self.assertFalse(5 in av)
    self.assertFalse(6 in av)

    self.assertEqual(len(av), 2)
    self.assertEqual(av.items(), [(1, 0), (2, 1), (3, 1), (4, 0), (5, 0), (6, 0)])
    self.assertFalse(av.is_doubles())
    self.assertEqual(repr(av), '<AvailableToPlay: [(1, 0), (2, 1), (3, 1), (4, 0), (5, 0), (6, 0)]>')
    self.assertEqual(3, av.get_max())

    av.consume(2)
    
    self.assertEqual(av[1], 0)
    self.assertEqual(av[2], 0)
    self.assertEqual(av[3], 1)
    self.assertEqual(av[4], 0)
    self.assertEqual(av[5], 0)
    self.assertEqual(av[6], 0)

    self.assertFalse(1 in av)
    self.assertFalse(2 in av)
    self.assert_(3 in av)
    self.assertFalse(4 in av)
    self.assertFalse(5 in av)
    self.assertFalse(6 in av)

    self.assertEqual(len(av), 1)
    self.assertEqual(av.items(), [(1, 0), (2, 0), (3, 1), (4, 0), (5, 0), (6, 0)])
    self.assertFalse(av.is_doubles())
    self.assertEqual(repr(av), '<AvailableToPlay: [(1, 0), (2, 0), (3, 1), (4, 0), (5, 0), (6, 0)]>')
    self.assertEqual(3, av.get_max())

    try:
      av.consume(4)
      self.assertFalse(True, 'exception must be raised')
    except:
      pass

    av.add(4)

    self.assertEqual(av[1], 0)
    self.assertEqual(av[2], 0)
    self.assertEqual(av[3], 1)
    self.assertEqual(av[4], 1)
    self.assertEqual(av[5], 0)
    self.assertEqual(av[6], 0)

    self.assertFalse(1 in av)
    self.assertFalse(2 in av)
    self.assert_(3 in av)
    self.assert_(4 in av)
    self.assertFalse(5 in av)
    self.assertFalse(6 in av)

    self.assertEqual(len(av), 2)
    self.assertEqual(av.items(), [(1, 0), (2, 0), (3, 1), (4, 1), (5, 0), (6, 0)])
    self.assertFalse(av.is_doubles())
    self.assertEqual(repr(av), '<AvailableToPlay: [(1, 0), (2, 0), (3, 1), (4, 1), (5, 0), (6, 0)]>')

    self.assertEqual(4, av.get_max())


  def av_doubles_test(self):
    av = AvailableToPlay((4, 4))
    self.assertEqual(av[1], 0)
    self.assertEqual(av[2], 0)
    self.assertEqual(av[3], 0)
    self.assertEqual(av[4], 4)
    self.assertEqual(av[5], 0)
    self.assertEqual(av[6], 0)

    self.assertFalse(1 in av)
    self.assertFalse(2 in av)
    self.assertFalse(3 in av)
    self.assert_(4 in av)
    self.assertFalse(5 in av)
    self.assertFalse(6 in av)

    self.assertEqual(len(av), 4)
    self.assertEqual(av.items(), [(1, 0), (2, 0), (3, 0), (4, 4), (5, 0), (6, 0)])
    self.assert_(av.is_doubles())
    self.assertEqual(repr(av), '<AvailableToPlay: [(1, 0), (2, 0), (3, 0), (4, 4), (5, 0), (6, 0)]>')

  def av_creation_by_copy_test(self):
    src = AvailableToPlay((3, 2))
    av = AvailableToPlay(copy_src=src)
    self.assertNotEqual(id(src), id(av))

    self.assertEqual(av[1], 0)
    self.assertEqual(av[2], 1)
    self.assertEqual(av[3], 1)
    self.assertEqual(av[4], 0)
    self.assertEqual(av[5], 0)
    self.assertEqual(av[6], 0)

    self.assertFalse(1 in av)
    self.assert_(2 in av)
    self.assert_(3 in av)
    self.assertFalse(4 in av)
    self.assertFalse(5 in av)
    self.assertFalse(6 in av)

    self.assertEqual(len(av), 2)
    self.assertEqual(av.items(), [(1, 0), (2, 1), (3, 1), (4, 0), (5, 0), (6, 0)])
    self.assertFalse(av.is_doubles())
    self.assertEqual(repr(av), '<AvailableToPlay: [(1, 0), (2, 1), (3, 1), (4, 0), (5, 0), (6, 0)]>')

  def pm_1_test(self):
    pm = PartialMove(6, 12, 6, True)
    self.assertEqual(repr(pm), "<PartialMove: 13/7*>")
    self.assert_(pm.is_hitting)
    self.assertFalse(pm.is_undo())

  def pm_2_test(self):
    pm = PartialMove(1, 24, 23, False)
    self.assertEqual(repr(pm), "<PartialMove: bar/24>")
    self.assertFalse(pm.is_hitting)
    self.assertFalse(pm.is_undo())

  def pm_3_test(self):
    pm = PartialMove(4, 3, -1, False)
    self.assertEqual(repr(pm), "<PartialMove: 4/off>")
    self.assertFalse(pm.is_hitting)
    self.assertFalse(pm.is_undo())

  def pm_4_test(self):
    pm = PartialMove(4, 3, 3, False)
    self.assertFalse(pm.is_undo())
    self.assert_(pm.is_dance())

  def pm_5_test(self):
    pm = PartialMove(4, -1, 3, False)
    self.assertEqual(repr(pm), "<PartialMove: off/4>")
    self.assert_(pm.is_undo())

    pm2 = PartialMove(4, 3, -1, False)
    self.assert_(pm2.are_invertible_element(pm))

  def move_test(self):
    m = Move()
    self.assertEqual(repr(m), "<Move: []>")
    pm2 = PartialMove(4, 3, -1, False)
    m.append(pm2)
    self.assertEqual(repr(m), "<Move: [<PartialMove: 4/off>]>")
    pm3 = PartialMove(2, 1, -1, False)
    m.append(pm3)
    self.assertEqual(repr(m), "<Move: [<PartialMove: 4/off>, <PartialMove: 2/off>]>")

    pm = PartialMove(4, -1, 3, False)
    m.append(pm)
    self.assertEqual(repr(m), "<Move: [<PartialMove: 2/off>]>")

  def mf_1_test(self):
    b = Board()
    b.rolled = (3, 1)
    mf = MoveFactory(b)
    found = mf.guess_your_single_pm_from_source(util.move_pton('bar'))
    self.assertEqual(repr(found), "<MoveFactory.Error: No chequer to move>")

    found = mf.guess_your_single_pm_from_source(util.move_pton('6'))
    self.assertEqual(repr(found), "<PartialMove: 6/3>")

    mf.append(found)
    self.assertEqual(mf.board.position[YOU], 
     (0, 0, 1, 0, 0, 4, 0, 3, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0))
    self.assertEqual(repr(mf.move), "<Move: [<PartialMove: 6/3>]>")
    self.assertEqual(repr(mf.available), 
    "<AvailableToPlay: [(1, 1), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0)]>")
    found = mf.guess_your_single_pm_from_source(
                    util.move_pton('6'))
    self.assertEqual(repr(found), "<PartialMove: 6/5>")
    mf.append(found)
    self.assertEqual(mf.board.position[constants], 
      (0, 0, 1, 0, 1, 3, 0, 3, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0)
      )
    self.assertEqual(repr(mf.move), "<Move: [<PartialMove: 6/3>, <PartialMove: 6/5>]>")
    self.assertEqual(repr(mf.available), 
      "<AvailableToPlay: [(1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0)]>")
    found = mf.guess_your_single_pm_from_source(util.move_pton('6')) 
    self.assertEqual(repr(found), "<MoveFactory.Error: No die is available>")

  def mf_2_test(self):
    b = Board(position=((0, 5, 4, 3, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),(0, 0, 0, 0, 2, 4, 0, 2, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0)), rolled = (6, 1))
    mf = MoveFactory(b)
    found = mf.guess_your_single_pm_from_source(util.move_pton('6')) 
    self.assertEqual(repr(found), "<PartialMove: 6/off>")

  def mf_3_test(self):
    b = Board(
        position=((0, 5, 4, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),(0, 0, 0, 0, 2, 4, 0, 2, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0)), 
        rolled=(6, 1)
        )
    mf = MoveFactory(b)
    found = mf.guess_your_single_pm_from_source(util.move_pton('5')) 

    self.assertEqual(repr(found), "<PartialMove: 5/off>")

  def mf_4_test(self):
    b = Board(
        position=((0, 5, 4, 0, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),(0, 0, 0, 0, 2, 4, 0, 2, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0)),
        rolled = (4, 1)
        )
    mf = MoveFactory(b)
    found = mf.guess_your_single_pm_from_dest(util.move_pton('off')) 
    self.assertEqual(repr(found), "<MoveFactory.Error: No die is available>")

  def mf_5_test(self):
    b = Board(
        position=((0, 0, 0, 0, 0, 5, 0, 3, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0),(0, 0, 0, 0, 2, 4, 0, 2, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0)),
        rolled = (4, 1))

    mf = MoveFactory(b)
    found = mf.guess_your_single_pm_from_source(util.move_pton('24'))
    self.assertEqual(repr(found), "<PartialMove: 24/23>")

    mf.append(found)
    self.assertEqual(mf.board.position[YOU],
      (0, 0, 0, 0, 0, 5, 0, 3, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0))
    self.assertEqual(repr(mf.move),  "<Move: [<PartialMove: 24/23>]>")
    self.assertEqual(repr(mf.available), "<AvailableToPlay: [(1, 0), (2, 0), (3, 0), (4, 1), (5, 0), (6, 0)]>")

    found = mf.guess_your_single_pm_from_source(util.move_pton('24'))
    self.assertEqual(repr(found), "<MoveFactory.Error: No die is available>")

  def mf_6_test(self):
    b = Board(
        position=((0, 0, 0, 0, 0, 5, 0, 3, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0),(0, 0, 0, 0, 2, 4, 0, 2, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0)),
        rolled = (4, 1))

    mf = MoveFactory(b)
    found = mf.guess_your_single_pm_from_source(util.move_pton('24'))
    self.assertEqual(repr(found), "<PartialMove: 24/23>")
    mf.append(found)
    self.assertEqual(mf.board.position[YOU],
      (0, 0, 0, 0, 0, 5, 0, 3, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0))
    self.assertEqual(repr(mf.move), "<Move: [<PartialMove: 24/23>]>")
    self.assertEqual(repr(mf.available), "<AvailableToPlay: [(1, 0), (2, 0), (3, 0), (4, 1), (5, 0), (6, 0)]>")
    found = mf.guess_your_single_pm_from_source(util.move_pton('24'))
    self.assertEqual(repr(found), "<MoveFactory.Error: No die is available>")

  def mf_7_test(self):
    b = Board(rolled=(3, 1))
    mf = MoveFactory(b)
    found = mf.guess_your_single_pm_from_dest(util.move_pton('6'))
    self.assertEqual(repr(found), "<MoveFactory.Error: No die is available>")

    found = mf.guess_your_single_pm_from_dest(util.move_pton('5'))
    self.assertEqual(repr(found), "<PartialMove: 8/5>")
    mf.append(found)
    self.assertEqual(mf.board.position[YOU], (0, 0, 0, 0, 1, 5, 0, 2, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0))
    self.assertEqual(repr(mf.move), "<Move: [<PartialMove: 8/5>]>")
    self.assertEqual(repr(mf.available), "<AvailableToPlay: [(1, 1), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0)]>")

    found = mf.guess_your_single_pm_from_dest(util.move_pton('5'))
    self.assertEqual(repr(found), "<PartialMove: 6/5>")

    mf.append(found)
    self.assertEqual(mf.board.position[YOU], 
(0, 0, 0, 0, 2, 4, 0, 2, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0))
    self.assertEqual(repr(mf.move), "<Move: [<PartialMove: 8/5>, <PartialMove: 6/5>]>")
    self.assertEqual(repr(mf.available), "<AvailableToPlay: [(1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0)]>")
    found = mf.guess_your_single_pm_from_dest(util.move_pton('5'))
    self.assertEqual(repr(found), "<MoveFactory.Error: No die is available>")

  def mf_8_test(self):
    b = Board(
          position=((0, 0, 0, 0, 0, 5, 0, 3, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0),(0, 0, 0, 0, 2, 4, 0, 2, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0)),
          rolled = (4, 1))
    self.assertEqual(b.position, 
        ((0, 0, 0, 0, 0, 5, 0, 3, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0),
         (0, 0, 0, 0, 2, 4, 0, 2, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0)))

    mf = MoveFactory(b)
    found = mf.guess_your_single_pm_from_dest(util.move_pton('20'))
    self.assertEqual(repr(found), "<MoveFactory.Error: Can't land there>")

  def mf_9_test(self):
    b = Board(
        position=((0, 0, 0, 0, 0, 5, 0, 3, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0),(0, 0, 0, 0, 2, 4, 0, 2, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0)),
        rolled = (6, 4))

    mf = MoveFactory(b)
    found = mf.guess_your_multiple_pms(util.move_pton('24'), 
                                       util.move_pton('15'))
    self.assertEqual(repr(found), "<MoveFactory.Error: No die is available>")

    found = mf.guess_your_multiple_pms(util.move_pton('24'), 
                                       util.move_pton('14'))
    self.assertEqual(repr(found), "<Move: [<PartialMove: 24/18>, <PartialMove: 18/14>]>")

  def mf_10_test(self):
    b = Board(
        position=((0, 0, 0, 0, 0, 5, 0, 3, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0),(0, 0, 0, 0, 0, 5, 2, 2, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0)),
        rolled = (6, 4))

    mf = MoveFactory(b)
    found = mf.guess_your_single_pm_from_source(util.move_pton('24'))
    self.assertEqual(repr(found), "<PartialMove: 24/20>")
    self.assertEqual(repr(util.move_ntop(found.dest)), "'20'")
    mf.append(found)

    found = mf.guess_your_single_pm_from_source(util.move_pton('20'))
    self.assertEqual(repr(found), "<PartialMove: 20/14>")
    self.assertEqual(repr(util.move_ntop(found.dest)), "'14'")

  def mf_11_test(self):
    b = Board(
        position=((0, 0, 0, 0, 0, 5, 0, 3, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0),(0, 0, 0, 0, 0, 5, 2, 2, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0)),
        rolled = (6, 4))

    mf = MoveFactory(b)
    found = mf.guess_your_multiple_pms(util.move_pton('24'), util.move_pton('14'))
    self.assertEqual(repr(found), "<Move: [<PartialMove: 24/20>, <PartialMove: 20/14>]>")

  def mf_12_test(self):
    b = Board(
        position=((0, 0, 0, 0, 1, 4, 0, 3, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0),(0, 0, 0, 0, 0, 5, 2, 2, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0)),
        rolled = (4, 4))

    mf = MoveFactory(b)
    found = mf.guess_your_multiple_pms(util.move_pton('13'), util.move_pton('1'))
    self.assertEqual(repr(found), "<Move: [<PartialMove: 13/9>, <PartialMove: 9/5>, <PartialMove: 5/1*>]>")

  def mf_13_test(self):
    b = Board(
        position=((1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),(8, 3, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)), rolled=(4, 2))
    mf = MoveFactory(b)
    found = mf.guess_your_multiple_pms(util.move_pton('5'), util.move_pton('3'))
    self.assertEqual(repr(found), "<Move: [<PartialMove: 5/3>]>")
    mf.add(found)
    self.assertEqual(b.position, 
((1, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0), (8, 3, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0))
    )
    self.assertEqual(b.has_chequer_to_move(util.move_pton('3')), 2)

    found = mf.guess_your_multiple_pms(util.move_pton('3'), util.move_pton('off'))
    self.assertEqual(repr(found), "<Move: [<PartialMove: 3/off>]>")


  def mf_14_test(self):
    b = Board(
        position=((0, 0, 0, 0, 1, 4, 0, 3, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0),(0, 0, 0, 0, 0, 5, 2, 2, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0)),
        rolled=(4, 4))

    mf = MoveFactory(b)
    found = mf.guess_your_single_pm_from_source(util.move_pton('13'))
    self.assertEqual(repr(found), "<PartialMove: 13/9>")

    mf.append(found)
    found = mf.guess_your_multiple_pms(util.move_pton('13'), util.move_pton('1'))
    self.assertEqual(repr(found), "<Move: [<PartialMove: 13/9>, <PartialMove: 9/5>, <PartialMove: 5/1*>]>")

    self.assertEqual(repr(mf.move), "<Move: [<PartialMove: 13/9>]>")

    mf.add(found)
    self.assertEqual(repr(mf.move), "<Move: [<PartialMove: 13/9>, <PartialMove: 13/9>, <PartialMove: 9/5>, <PartialMove: 5/1*>]>")

  def mf_15_test(self):
    b = Board(
        position=((0, 0, 0, 0, 1, 4, 0, 3, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1),(0, 0, 0, 0, 0, 5, 2, 2, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0)),
        rolled = (5, 5))

    mf = MoveFactory(b)
    found = mf.guess_your_multiple_pms(util.move_pton('bar'), util.move_pton('5'))

    self.assertEqual(repr(found), "<Move: [<PartialMove: bar/20>, <PartialMove: 20/15>, <PartialMove: 15/10>, <PartialMove: 10/5>]>")
    mf.add(found)

    found = None
    found = mf.guess_your_multiple_partial_undoes(util.move_pton('5'), util.move_pton('15'))
    self.assertEqual(repr(found), "<Move: [<PartialMove: 5/10>, <PartialMove: 10/15>]>")

    mf.add(found)
    self.assertEqual(repr(mf.move), "<Move: [<PartialMove: bar/20>, <PartialMove: 20/15>]>")

  def mf_16_test(self):
    b = Board(
        position=((2, 0, 3, 3, 3, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0),(1, 0, 0, 2, 2, 2, 2, 0, 0, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0, 0)),
        rolled = (6, 5))

    mf = MoveFactory(b)
    found = mf.guess_your_single_pm_from_source(util.move_pton('13'))
    self.assertEqual(repr(found), "<PartialMove: 13/7>")

    mf.append(found)

    self.assert_(mf.is_leagal_to_pickup_dice())

  def mf_17_test(self):
    b = Board(
      position=((2, 0, 3, 3, 3, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0),(1, 0, 0, 2, 2, 2, 2, 0, 0, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0, 0)),
      rolled=(6, 5)
      )

    mf = MoveFactory(b)
    found = mf.guess_your_single_pm_from_source(util.move_pton('23'))
    self.assertEqual(repr(found), "<PartialMove: 23/17>")
    mf.append(found)

    found = None
    self.assert_(mf.is_leagal_to_pickup_dice())

  def mf_18_test(self):
    b = Board(
          position=((0, 2, 3, 3, 3, 0, 
                     0, 0, 0, 0, 0, 0, 
                     2, 0, 0, 0, 0, 0, 
                     0, 0, 0, 0, 2, 0, 0),
                    (1, 0, 0, 2, 2, 2,
                     2, 0, 0, 0, 0, 0,
                     2, 0, 0, 0, 2, 0,
                     0, 0, 0, 0, 0, 2, 0)),
           rolled=(6, 5)
           )

    mf = MoveFactory(b)
    found = mf.guess_your_single_pm_from_source(util.move_pton('23'))
    self.assertEqual(repr(found), "<PartialMove: 23/17>")
    mf.append(found)
    found = None
    self.assertFalse(mf.is_leagal_to_pickup_dice())

  def mf_19_test(self):
    b = Board(
          position=((0, 3, 3, 3, 3, 2,
                     0, 0, 0, 0, 0, 0,
                     0, 0, 0, 0, 0, 0,
                     0, 0, 0, 0, 1, 0, 0),
                    (1, 0, 0, 2, 2, 4,
                     0, 0, 0, 0, 0, 0,
                     2, 0, 0, 0, 2, 0,
                     0, 0, 0, 0, 0, 2, 0)),
          rolled = (6, 5))

    mf = MoveFactory(b)
    found = mf.guess_your_single_pm_from_source(util.move_pton('23'))
    self.assertEqual(repr(found), "<PartialMove: 23/17>")
    mf.append(found)
    self.assert_(mf.is_leagal_to_pickup_dice())

  def mf_20_test(self):
    b = Board(
          position=((0, 3, 3, 3, 3, 2,
                     0, 0, 0, 0, 0, 0,
                     0, 0, 0, 0, 0, 0,
                     0, 0, 0, 0, 1, 0, 0),
                    (1, 0, 0, 2, 2, 4,
                     0, 0, 0, 0, 0, 0,
                     2, 0, 0, 0, 2, 0,
                     0, 0, 0, 0, 0, 2, 0)),
          rolled = (6, 5))

    mf = MoveFactory(b)
    found = mf.guess_your_multiple_pms(util.move_pton('23'), util.move_pton('18'))
    self.assertEqual(repr(found), "<Move: [<PartialMove: 23/18>]>")
    mf.add(found)
    self.assertFalse(mf.is_leagal_to_pickup_dice())

