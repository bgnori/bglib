import math

def upset_chance(high, low, length):
  '''
    based on http://www.backgammon.gr.jp/rating/about_rating.html

    >>> upset_chance(1100, 1000, 9)
    0.41450132132819051
  '''
  assert high >= low
  return 1/(pow(10, ( high - low ) * math.sqrt(length)/2000) +1)


def winning_chance(high, low, length):
  return 1.0 - upset_chance(high, low, length)
  

def gain_won_win(player, opp, length):
  '''
    >>> gain_won_win(1000, 1100, 9)
    5.2694881080462856
    >>> gain_won_win(1100, 1000, 9)
    3.7305118919537144
  '''
  if player >= opp:
    return length * upset_chance(player, opp, length)
  if player < opp:
    return length * (1.0 - upset_chance(opp, player, length))


def tourney_chance(player, average, rounds, length):
  '''
    >>> tourney_chance(1000.0, 1000.0, 3, 7)
    (0.125, 0.125)

    >>> tourney_chance(1000.0, 1000.0, 3, 5)
    (0.125, 0.125)

    >>> tourney_chance(1000.0, 1000.0, 2, 5)
    (0.25, 0.25)
  '''
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



if __name__ == '__main__':
  import doctest
  doctest.testmod()

