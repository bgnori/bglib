#!/usr/bin/env python
# -*- coding: utf8 -*-
# vim: syntax=python
#
# Copyright 2006-2008 Noriyuki Hosaka nori@backgammon.gr.jp
#
from bglib.model.constants import *


XGID_YOU= -1
XGID_HIM = 1
XGID_CENTER= 0

#              0123456789012345
CHEQUER_HIM = "-abcdefghijklmno"
CHEQUER_YOU = "-ABCDEFGHIJKLMNO"


def decode_position(s):
  # 最初の部分の英文字と-からなる26文字の文字列はボードの上の駒の分布を表しています。
  # 小文字は相手の駒の数をあらわしていて,aが１bが2...大文字は自分の駒の数を表
  # していてAが１,Bが２...となっています。-は0を表しています。１番最初の文字は
  # バーにある相手の駒の数であり２番目の文字から２４ポイントから１ポイントまで
  # の駒の数を表していて最後にバーにある自分の駒の数を表します。
  assert len(s) == 26

  conv_him = dict([(v, i) for i, v in enumerate(CHEQUER_HIM)])
  conv_you = dict([(v, i) for i, v in enumerate(CHEQUER_YOU)])

  you = s[1:26]
  him = "".join(reversed(s[0:25]))

  return tuple([conv_you.get(y, 0) for y in you]), \
         tuple([conv_him.get(h, 0) for h in him])
    

def decode(model, s):
  # :がデータを区切るデリミタになっています。
  position, cube_in_logarithm, cube_owner, \
  on_action, rolled, your_score, his_score, \
  is_crawford_jacoby, match_length, cube_max, \
  = s.split(':')

  # 最初の部分の英文字と-からなる26文字の文字列はボードの上の駒の分布を表しています。
  you, him = decode_position(position)
  model.position = (you, him)

  # 2番目の部分はキューブの値を示します。 0のときはキューブの値は１,１のときは
  # キューブの値は2...
  model.cube_in_logarithm = int(cube_in_logarithm)


  # 3番目の部分はcubeの位置を表していて 1の場合は自分がキューブを持っていて、
  # -1の場合は相手がキューブを持っていて、0の場合はセンターキューブです。
  cube_owner = int(cube_owner) 
  if cube_owner == XGID_YOU:
    model.cube_owner = YOU
  elif cube_owner == XGID_HIM:
    model.cube_owner =  HIM
  elif cube_owner == XGID_CENTER:
    model.cube_owner = CENTER
  else:
    print cube_owner
    assert False

  # 4番めの部分はターンを示していて、1のときは自分の番で-1のときは相手の番
  # となります。
  on_action = int(on_action)
  if on_action == XGID_YOU:
    model.on_action = YOU
  elif cube_owner == XGID_HIM:
    model.cube_owner =  HIM
  elif cube_owner == XGID_CENTER:
    model.cube_owner = CENTER
  else:
    assert False

  assert len(rolled) == 2
  model.rolled = int(rolled[0]), int(rolled[1])

  model.score = (int(your_score), int(his_score))

  is_crawford_jacoby = int(is_crawford_jacoby)
  match_length = int(match_length)
  if match_length == 0:
    model.crawford = False
    model.match_length = match_length
  else:
    model.crawford = bool(is_crawford_jacoby)
    model.match_length = match_length

  #model.game_state = mp.game_state
  #model.on_inner_action = mp.on_inner_action
  #model.doubled = mp.doubled
  #model.resign_offer = mp.resign_offer




