#!/usrbin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2006-2008 Noriyuki Hosaka nori@backgammon.gr.jp
#

def FIBSDecode(s):
  class FIBSBoardState:
    index = dict(
        you=(1, 2), 
        him=(2, 3),
        matchlength=(3, 4),
        your_score=(4, 5),
        his_score=(5, 6),
        board=(6, 32),
        turn=(32, 33),
        dice=(),
        may_double=(),
        was_doubled=(),
        colour=(),#ugh!
        direction=(),#ugh!
        OnHome=(), 
        OnBar=(),
        CanMove=(),
        ForcedMove=(),# Not USED! 
        Redoubles=(),
      )

    def __init__(self, s):
      ''' see bellow address for definition.
      http://www.fibs.com/fibs_interface.html#board_state
      '''
      self.data = s.split(':')

  class Decoded(FIBSBoardState):
    def __init__(self, s):
      FIBSBoardState.__init__(self, s)
      self.position = None

  ret = Decoded(s)
  ret.position = \
((0, 0, 0, 0, 0, 5, 0, 3, 0, 0, 0, 0,\
 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0),\
 (0, 0, 0, 0, 0, 5, 0, 3, 0, 0, 0, 0,\
 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0))
  return ret


def FIBSEncode(s):
  '''currently no use.'''
  raise NotImplemented

if __name__ == '__main__':
  import doctest
  doctest.testfile('FIBS.test')

