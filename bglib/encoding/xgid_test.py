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

  def xgid2gnubg_itikawa_SecondWorstRoll_test(self):
    from_xgid = BoardEditor()
    from_gnubgid = BoardEditor()
    xgid.decode(from_xgid, '---CBbB-B----E-a--bcbcb-A-:1:1:1:21:0:1:0:5:10')
    gnubgid.decode(from_gnubgid, '7HYjAAPczOADIA','UQmlABAAAAAA')
    self.assertEqual(from_gnubgid, from_xgid)

  def xgid2gnubg_itikawa_DenmarkVWorldAtNordic2010_test(self):
    from_xgid = BoardEditor()
    from_gnubgid = BoardEditor()
    xgid.decode(from_xgid, '-Ba-CBBCB----------Abc-ed-:1:1:1:00:7:1:0:15:16')
    gnubgid.decode(from_gnubgid, '73MDABDjthsAAQ','UQngARAAOAAA')
    self.assertEqual(from_gnubgid, from_xgid)

  def xgid2gnubg_itikawa_OhsakaOpenQuiz2010_test(self):
    from_xgid = BoardEditor()
    from_gnubgid = BoardEditor()
    xgid.decode(from_xgid, '--BBCbB---BBd------c-Bbca-:0:0:1:33:0:0:3:0:10')
    gnubgid.decode(from_gnubgid, '3TjgAQO2M2wABg','cIkNAAAAAAAA')
    self.assertEqual(from_gnubgid, from_xgid)

  def xgid2gnubg_Festival2009QuizQ01_test(self):
    from_xgid = BoardEditor()
    from_gnubgid = BoardEditor()
    xgid.decode(from_xgid, '-aBa--DaB---cE---d-e---AA-:0:0:1:56:3:1:0:5:8')
    gnubgid.decode(from_gnubgid, '4PPgICSGZ/ABKA','cIm6ABAAGAAA')
    self.assertEqual(from_gnubgid, from_xgid)

  def xgid2gnubg_Festival2009QuizQ02_test(self):
    from_xgid = BoardEditor()
    from_gnubgid = BoardEditor()
    xgid.decode(from_xgid, '-bB-BBC-B---bBA--bbdc---A-:0:0:1:35:0:0:3:0:8')
    gnubgid.decode(from_gnubgid, 'cG+DATBmO4MFIA','cIkVAAAAAAAA')

    self.assertEqual(from_gnubgid, from_xgid)

  def xgid2gnubg_Festival2009QuizQ03_test(self):
    from_xgid = BoardEditor()
    from_gnubgid = BoardEditor()
    xgid.decode(from_xgid, '---a--EBBBB-b----ccd--b-B-:0:0:1:12:1:0:0:3:8')
    gnubgid.decode(from_gnubgid, 'jHcHAwjg2zYAMA','cIloAAAACAAA')
    self.assertEqual(from_gnubgid, from_xgid)

  def xgid2gnubg_Festival2009QuizQ04_test(self):
    from_xgid = BoardEditor()
    from_gnubgid = BoardEditor()
    xgid.decode(from_xgid, '-a---BDaCb---A--b-bcbbCB--:1:1:1:55:0:2:0:5:8')
    gnubgid.decode(from_gnubgid, '2G4GTCCw5yCAGw','UYm2ACAAAAAA')
    self.assertEqual(from_gnubgid, from_xgid)

  def xgid2gnubg_Festival2009QuizQ05_test(self):
    from_xgid = BoardEditor()
    from_gnubgid = BoardEditor()
    xgid.decode(from_xgid, '--BBCBC-a-----A----cBce-c-:0:0:1:32:0:0:3:0:8')
    gnubgid.decode(from_gnubgid, '5zsHQAC22wECAw','cIkJAAAAAAAA')
    self.assertEqual(from_gnubgid, from_xgid)

  def xgid2gnubg_Festival2009QuizQ06_test(self):
    from_xgid = BoardEditor()
    from_gnubgid = BoardEditor()
    xgid.decode(from_xgid, '-B-BCaC-BB--b-ab-a-c-bb-aA:0:0:1:21:4:2:1:5:10')
    gnubgid.decode(from_gnubgid, '2ZwsAwKzczYAQA','8AmlACAAIAAA')
    self.assertEqual(from_gnubgid, from_xgid)

  def xgid2gnubg_Festival2009QuizQ07_test(self):
    from_xgid = BoardEditor()
    from_gnubgid = BoardEditor()
    xgid.decode(from_xgid, '-A--b-D-D--BeB---c-e-AA---:0:0:1:66:0:0:3:0:8')
    gnubgid.decode(from_gnubgid, '4HPwAQbB85gBCg','cAkbAAAAAAAA')
    self.assertEqual(from_gnubgid, from_xgid)

  def xgid2gnubg_Festival2009QuizQ08_test(self):
    from_xgid = BoardEditor()
    from_gnubgid = BoardEditor()
    xgid.decode(from_xgid, '--D-CaBbB---BBa---bbbc-b--:0:0:1:23:1:0:0:3:8')
    gnubgid.decode(from_gnubgid, '5rYhYAKeM8MGAA','cAltAAAACAAA')
    self.assertEqual(from_gnubgid, from_xgid)


  def xgid2gnubg_Festival2009QuizQ09_test(self):
    from_xgid = BoardEditor()
    from_gnubgid = BoardEditor()
    xgid.decode(from_xgid, '-aa-B-DBB--AdB--ab-d-b--B-:0:0:1:51:0:0:3:0:10')
    gnubgid.decode(from_gnubgid, 'mGfhASiYt5EBMA', 'cIkGAAAAAAAA')
    self.assertEqual(from_gnubgid, from_xgid)

  def xgid2gnubg_Festival2009QuizQ10_test(self):
    from_xgid = BoardEditor()
    from_gnubgid = BoardEditor()
    xgid.decode(from_xgid, '-B-bABEAA--Ba---accc--b-A-:1:-1:1:43:0:0:3:0:8')
    gnubgid.decode(from_gnubgid, 'jLsLAQyjfcUAIA','QQkOAAAAAAAA')
    self.assertEqual(from_gnubgid, from_xgid)

