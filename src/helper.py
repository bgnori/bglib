#!/usrbin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2006-2008 Noriyuki Hosaka nori@backgammon.gr.jp
#

import encoding.base
import encoding.gnubg
import encoding.urlsafe
import model

def decode_gnubg(positionid, matchid):
  p = encoding.gnubg.decode_position(positionid)
  m = encoding.gnubg.decode_match(matchid)
  b = model.board(position=p,
            cube_value=pow(2, m.cube_in_logarithm),
            cube_owner=m.cube_owner,
            crawford=m.crawford,
            on_action=m.on_action,
            on_inner_action=m.on_inner_action,
            game_state=m.game_state,
            )
  return b

if __name__ == '__main__':
  import doctest
  doctest.testfile('helper.test')
