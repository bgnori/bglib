#!/usr/bin/env python
# -*- coding: utf8 -*-
# vim: syntax=python
#
# Copyright 2006-2008 Noriyuki Hosaka nori@backgammon.gr.jp
#

import tempfile
import unittest

from bglib.model import BoardEditor
from bglib.encoding import gnubgid 
from bglib.encoding import xgid


class EncodingTest(unittest.TestCase):
  def preparation_test(self):
    from_gnubgid1 = BoardEditor()
    from_gnubgid2 = BoardEditor()
    gnubgid.decode(from_gnubgid1, 'sM/BATCwZ/ABMA','cAmgAEAAGAAA')
    gnubgid.decode(from_gnubgid2, 'sM/BATCwZ/ABMA','cAmgAEAAGAAA')
    print from_gnubgid1 == from_gnubgid2
    self.assertEqual(from_gnubgid1, from_gnubgid2)

  def xgid2gnubg_1_test(self):
    from_xgid = BoardEditor()
    from_gnubgid = BoardEditor()
    xgid.decode(from_xgid, '-b---BD-B---cE---c-eb---B-:0:0:1:00:3:4:0:5:10')
    gnubgid.decode(from_gnubgid, 'sM/BATCwZ/ABMA','cAmgAEAAGAAA')
    self.assertEqual(from_gnubgid, from_xgid)

  def xgid2gnubg_0_test(self):
    from_xgid = BoardEditor()
    from_gnubgid = BoardEditor()
    xgid.decode(from_xgid, '-B-BAaCBC-----a-----cdBcc-:1:-1:1:66:1:4:0:5:10')
    gnubgid.decode(from_gnubgid, 'd96BAAKz3A4ADA','QQm7AEAACAAA')
    self.assertEqual(from_gnubgid, from_xgid)

  def xgid2gnubg_bgonline_HowToTrapAnAnchor_test(self):
    '''
      from
      How to trap an anchor
        gnuid http://www.bgonline.org/forums/webbbs_config.pl?read=65226
        xgid  http://www.bgonline.org/forums/webbbs_config.pl?read=65334
    '''
    from_xgid = BoardEditor()
    from_gnubgid = BoardEditor()
    xgid.decode(from_xgid, '-----bBBBCBB----A--A---cc-:1:1:1:12:0:0:0:0:10')
    gnubgid.decode(from_gnubgid, 'dwAABsC22yACAA','UYkIAAAAAAAA')
    self.assertEqual(from_gnubgid, from_xgid)

  def xgid2gnubg_jbl_LateHitOriginal_test(self):
    '''
      from
      http://www.backgammon.gr.jp/forum/viewtopic.php?f=2&t=1072
      怪しいキューブ
    '''
    from_xgid = BoardEditor()
    from_gnubgid = BoardEditor()
    xgid.decode(from_xgid, '-bCCa-B-a------a---bbbbb-A:1:-1:-1:00:0:0:3:0:10')
    gnubgid.decode(from_gnubgid, '7hgAANm2ISDEAA','AQEAAAAAAAAA')
    self.assertEqual(from_gnubgid, from_xgid)
    
  def xgid2gnubg_jbl_LateHitRef1_test(self):
    '''
      from
      http://www.backgammon.gr.jp/forum/viewtopic.php?f=2&t=1072
      怪しいキューブ
    '''
    from_xgid = BoardEditor()
    from_gnubgid = BoardEditor()
    xgid.decode(from_xgid, '-DC---------------bcccbbB-:1:-1:-1:00:0:0:3:0:10')
    gnubgid.decode(from_gnubgid, '7wAAwNjubgAAAA','AQEAAAAAAAAA')
    self.assertEqual(from_gnubgid, from_xgid)
    
  def xgid2gnubg_jbl_LateHitRef2_test(self):
    '''
      from
      http://www.backgammon.gr.jp/forum/viewtopic.php?f=2&t=1072
      怪しいキューブ
    '''
    from_xgid = BoardEditor()
    from_gnubgid = BoardEditor()
    xgid.decode(from_xgid, '-DCa---------------ccccbB-:1:-1:-1:00:0:0:3:0:10')
    gnubgid.decode(from_gnubgid, '7wAAwNjdHQAgAA','AQEAAAAAAAAA')
    self.assertEqual(from_gnubgid, from_xgid)

  def xgid2gnubg_jbl_LateHitRef3_test(self):
    '''
      from
      http://www.backgammon.gr.jp/forum/viewtopic.php?f=2&t=1072
      怪しいキューブ
    '''
    from_xgid = BoardEditor()
    from_gnubgid = BoardEditor()
    xgid.decode(from_xgid, '-DCaa--------------cccbbB-:1:-1:-1:00:0:0:3:0:10')
    gnubgid.decode(from_gnubgid, '7wAAwNjuDgAoAA','AQEAAAAAAAAA')
    self.assertEqual(from_gnubgid, from_xgid)

  def xgid2gnubg_bgonline_25ptMatchVMoney_test(self):
    '''
      from
      http://www.bgonline.org/forums/webbbs_config.pl?read=64989
      Surprising difference between 25-away/25-away and money
    '''
    from_xgid = BoardEditor()
    from_gnubgid = BoardEditor()
    xgid.decode(from_xgid, '-BAC-----------------abab-:1:1:1:00:0:0:0:0:10')
    gnubgid.decode(from_gnubgid, 'awEAgHUAAAAAAA','UQkAAAAAAAAA')
    self.assertEqual(from_gnubgid, from_xgid)





