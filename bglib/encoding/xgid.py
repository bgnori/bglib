#!/usr/bin/env python
# -*- coding: utf8 -*-
# vim: syntax=python
#
# Copyright 2006-2011 Noriyuki Hosaka bgnori@gmail.com
#
from bglib.model.constants import *
import bglib.encoding


XGID_PLAYER2= 1
XGID_PLAYER1 = -1
XGID_CENTER= 0

#              0123456789012345
CHEQUER_HIM = "-abcdefghijklmno"
CHEQUER_YOU = "-ABCDEFGHIJKLMNO"
conv_him = dict([(v, i) for i, v in enumerate(CHEQUER_HIM)])
conv_you = dict([(v, i) for i, v in enumerate(CHEQUER_YOU)])


def decode_position(s):
  '''
    最初の部分の英文字と-からなる26文字の文字列はボードの上の駒の分布を表しています。
    小文字は相手の駒の数をあらわしていて,aが１bが2...大文字は自分の駒の数を表
    していてAが１,Bが２...となっています。-は0を表しています。１番最初の文字は
    バーにある相手の駒の数であり２番目の文字から２４ポイントから１ポイントまで
    の駒の数を表していて最後にバーにある自分の駒の数を表します。
  '''
  if len(s) != 26:
    raise bglib.encoding.DecodeError('got bad data: %s '%(s,))

  you = s[1:26]
  him = "".join(reversed(s[0:25]))

  return tuple([conv_him.get(h, 0) for h in him]), \
         tuple([conv_you.get(y, 0) for y in you])
    

def decode(model, s):

  if not s:
    raise bglib.encoding.DecodeError('got empty data. possible bad encoding')

  '''
    :がデータを区切るデリミタになっています。 
  '''
  try:
    position, cube_in_logarithm, cube_owner, \
    on_action, rolled, your_score, his_score, \
    is_crawford_jacoby, match_length, cube_max, \
    = s.split(':')
  except ValueError:
    raise bglib.encoding.DecodeError('got bad data (maybe lack of items or too many items): %s '%(s,))

  '''
    最初の部分の英文字と-からなる26文字の文字列はボードの上の駒の分布を表しています。
  '''
  him, you = decode_position(position)
  model.position = (him, you)

  '''
   2番目の部分はキューブの値を示します。 0のときはキューブの値は１,１のときは
   キューブの値は2...
  '''
  try:
    model.cube_in_logarithm = int(cube_in_logarithm)
  except ValueError:
    raise bglib.encoding.DecodeError('got bad data, non integer cube logarithm: %s '%(cube_in_logarithm,))


  '''
   3番目の部分はcubeの位置を表していて 1の場合は自分がキューブを持っていて、
   -1の場合は相手がキューブを持っていて、0の場合はセンターキューブです。
   i.e. mapping player1 == YOU player2 == HIM
  '''

  try:
    cube_owner = int(cube_owner) 
  except ValueError:
    raise bglib.encoding.DecodeError('got bad data, non integer cube owner: %s '%(cube_owner,))

  if cube_owner == XGID_PLAYER1:
    model.cube_owner = YOU
  elif cube_owner == XGID_PLAYER2:
    model.cube_owner =  HIM
  elif cube_owner == XGID_CENTER:
    model.cube_owner = CENTER
  else:
    raise bglib.encoding.InconsistentData('bad cube owner: %d '%(cube_owner,))

  '''
   4番めの部分はターンを示していて、1のときは自分の番で-1のときは相手の番
   となります。
  '''
  try:
    on_action = int(on_action)
  except ValueError:
    raise bglib.encoding.DecodeError('got bad data, non integer on action: %s '%(on_action,))
  if on_action == XGID_PLAYER1:
    model.on_action = YOU
  elif on_action == XGID_PLAYER2:
    model.on_action =  HIM
  else:
    raise bglib.encoding.InconsistentData('bad turn: %d '%(on_action,))

  if not len(rolled) == 2:
    raise bglib.encoding.InconsistentData('bad roll: %s '%(rolled, ))

  try:
    model.rolled = int(rolled[0]), int(rolled[1])
  except ValueError:
    raise bglib.encoding.DecodeError('got bad data, non integer roll: %s '%(rolled,))

  try:
    model.score = (int(his_score), int(your_score))
  except ValueError:
    raise bglib.encoding.DecodeError('got bad data, non interger score: %s '%(his_score, your_score,))

  try:
    is_crawford_jacoby = int(is_crawford_jacoby)
  except ValueError:
    raise bglib.encoding.DecodeError('got bad data, non integer Crawford/Jacoby flag: %s '%(is_crawford_jacoby,))

  if is_crawford_jacoby not in (0, 1):
    raise bglib.encoding.InconsistentData('bad Crawford/Jacoby flag: %d '%(is_crawford_jacoby, ))


  try:
    match_length = int(match_length)
  except ValueError:
    raise bglib.encoding.DecodeError('got bad data, non integer match length: %s '%(match_length,))

  if match_length == 0:
    model.crawford = False
    model.match_length = match_length
  elif match_length > 0:
    model.crawford = bool(is_crawford_jacoby)
    model.match_length = match_length
  else:
    raise bglib.encoding.InconsistentData('negative match length: %d '%(match_length, ))


  #UGH!
  model.game_state = ON_GOING  

  #UGH!
  model.on_inner_action = model.on_action

  '''
  #model.doubled = mp.doubled
  #model.resign_offer = mp.resign_offer
  '''


