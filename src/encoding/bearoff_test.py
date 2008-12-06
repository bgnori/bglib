#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2006-2008 Noriyuki Hosaka nori@backgammon.gr.jp
#
import unittest
import unittest

from bglib.encoding.bearoff import oneside_index
from bglib.encoding.bearoff import key_to_index 
from bglib.encoding.bearoff import human_readable_eq
from bglib.encoding.bearoff import DBReader

class gnubgTest(unittest.TestCase):
  def setUp(self):
    self.reader = DBReader()
    self.reader.open('/home/nori/Desktop/work/BearoffDatabase/BEAR4.DTA')

  def tearDown(self):
    self.reader.close()

  def oneside_index_1_test(self):
    self.assertEqual(1, oneside_index((1,0,0,0,0,0, 0,0,0,0,0,0, 0,0,0,0,0,0, 0,0,0,0,0,0, 0), 1, 1))

  def oneside_index_2_test(self):
    self.assertEqual(4927, oneside_index((0, 0, 1, 2, 5, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0), 6, 9))

  def oneside_index_3_test(self):
    self.assertEqual(505, oneside_index((2, 3, 0, 1, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0), 6, 8))

  def key_to_index_1_test(self):
    pid = 'AQAABAAAAAAAAA:cAkAAAAAAAAA'
    self.assertEqual(key_to_index(pid), 3-1)

  def readable_4_test(self):
    self.assertEqual(self.reader.human_readable(4), (1.0, 2.0, 2.0, 1.0))

  def readable_9_test(self):
    self.assertEqual(self.reader.human_readable(9), (1.0, 2.0, 2.0, 1.0))

  def readable_171_test(self):
    self.assertEqual(self.reader.human_readable(171), 
        (0.4444444477558136, 0.8888888955116272, 0.8888888955116272, 0.72222220897674561))
        #(0.444444, 0.888889, 0.888889, 0.722222))

  def key_171_test(self):
    pid = 'AQAAGAAAAAAAAA:cAkAAAAAAAAA'
    self.assertEqual(key_to_index(pid), 171- 1)
    self.assertEqual(human_readable_eq(self.reader[pid]),
        (0.4444444477558136, 0.8888888955116272, 0.8888888955116272, 0.72222220897674561))

  def readable_10314995_test(self):
    self.assertEqual(self.reader.human_readable(10314995), 
        (0.67126756906509399, 0.7498512864112854, 1.4217830896377563, 0.71829420328140259))
    #(0.671267569065, 0.749851286411, 1.42178308964, 0.718294203281))

  def key_10314995_test(self):
    pid = 'zyYAABxPAAAAAA:cAkAAAAAAAAA'
    self.assertEqual(key_to_index(pid), 10314995 - 1)
    self.assertEqual(human_readable_eq(self.reader[pid]),
        (0.67126756906509399, 0.7498512864112854, 1.4217830896377563, 0.71829420328140259))

  def readable_15235967_test(self):
    self.assertEqual(self.reader.human_readable(15235967), 
        (0.012089979834854603, -0.26332512497901917, 0.33395415544509888, 0.51265531778335571))

  def key_15235967_test(self):
    pid = 'XhUAADo3AAAAAA:cAkAAAAAAAAA'
    self.assertEqual(key_to_index(pid), 15235967 - 1)
    self.assertEqual(human_readable_eq(self.reader[pid]),
        (0.012089979834854603, -0.26332512497901917, 0.33395415544509888, 0.51265531778335571))

  def readable_3188889_test(self):
    self.assertEqual(self.reader.human_readable(3188889),
        (0.44046294689178467, 0.42413434386253357, 1.0182017087936401, 0.64632552862167358))
        #(0.440462946892, 0.424134343863, 1.01820170879, 0.646325528622))

  def key_3188889_test(self):
    pid = 'bxQAALALAAAAAA:cAkAAAAAAAAA'
    self.assertEqual(key_to_index(pid), 3188889 - 1)
    self.assertEqual(human_readable_eq(self.reader[pid]),
        (0.44046294689178467, 0.42413434386253357, 1.0182017087936401, 0.64632552862167358))
        #(0.440462946892, 0.424134343863, 1.01820170879, 0.646325528622))

  def readable_24281655_test(self):
    self.assertEqual(self.reader.human_readable(24281655),
        (0.91166210174560547, 1.3082666397094727, 1.8547927141189575, 0.84428143501281738))
        #(0.911662, 1.308267, 1.854793, 0.844281))

  def key_24281655_test(self):
    pid = 'tC8AAOzkAAAAAA:cAkAAAAAAAAA'
    self.assertEqual(key_to_index(pid), 24281655 - 1)
    self.assertEqual(human_readable_eq(self.reader[pid]),
        (0.91166210174560547, 1.3082666397094727, 1.8547927141189575, 0.84428143501281738))
        #(0.911662, 1.308267, 1.854793, 0.844281))
        


