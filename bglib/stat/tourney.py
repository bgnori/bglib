#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2006-2009 Noriyuki Hosaka bgnori@gmain.com
#
import random

from bglib.stat.rating import upset_chance, winning_chance

def tourney_chance(player, average, rounds, length):
  if player >= average:
    uc = upset_chance(player, average, length)
    tourney_winner_chance = (1.0 - uc) ** rounds
    tourney_runnerup_chance = (1.0 - uc) ** (rounds -1) * uc 
  else:
    wc = upset_chance(average, player, length)
    tourney_winner_chance = (wc) ** rounds
    tourney_runnerup_chance = (wc) ** (rounds -1) * (1.0 - wc)
  return tourney_winner_chance, tourney_runnerup_chance


def prize_handicap(player, average, rounds, length, winner, runnerup):
  '''
    find value for the winner to average expectancy of series of tourney,
    with respecting his rating.
    
    100.0pt for average guy(rating=1000.0).
    i.e.

    >>> prize_handicap(1000.0, 1000.0, 4, 7, 100.0, 30.0)
    (100.0, 30.0)
  '''
  av_w, av_r = tourney_chance(average, average, rounds, length)
  expected_w = av_w * winner
  expected_r = av_r * runnerup
  w, r = tourney_chance(player, average, rounds, length)
  return expected_w/w, expected_r/r


def entryfee_handicap(player, average, rounds, length, fee):
  '''
    from given average, rounds ,length and fee,
    find handicapped entry fee for player
    
    example is 100.0pt for average guy(rating=1000.0).
    with $100.00.
    i.e.

    >>> entryfee_handicap(1000.0, 1000.0, 4, 7, 100.0)
    100.0
  '''
  av_w, av_r = tourney_chance(average, average, rounds, length)
  expected_w = fee / av_w 
  #expected_r = fee / av_r 
  w, r = tourney_chance(player, average, rounds, length)
  return expected_w*w #+ expected_r*r



class Player(object):
  def __init__(self, lives, r):
    self.lives = lives
    self.rating = r

  def lost(self):
    self.lives -= 1

  def isdead(self):
    return self.lives <= 0
    

class Tourney(object):
  def __init__(self, n, entries=None):
    if entries is None:
      self.alive = dict([(i, Player(3, 1000)) for i in range(n)])
    else:
      assert isinstance(entries, dict)
      self.alive = dict(entries)
    self.dead = {}
    self.matchlength = 7

  def round(self):
    xs = self.alive.keys()
    random.shuffle(xs)
   
    for i in range(len(xs)/2):
      a = xs[2*i]
      b = xs[2*i+1]
      r_a = self.alive[a].rating
      r_b = self.alive[b].rating

      if r_a >= r_b:
        high = r_a
        low = r_b
        w_a = winning_chance(high, low, self.matchlength)
      else:
        high = r_b
        low = r_a
        w_a = 1.0 - winning_chance(high, low, self.matchlength)

      if random.random() <= w_a:
        self.alive[b].lost()
        if self.alive[b].isdead():
          self.dead.update({b: self.alive[b]})
          self.alive.pop(b)
      else:
        self.alive[a].lost()
        if self.alive[a].isdead():
          self.dead.update({a: self.alive[a]})
          self.alive.pop(a)


