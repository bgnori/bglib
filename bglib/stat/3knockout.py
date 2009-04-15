
from bglib.stat.tourney import Tourney


EXP = 100000

for n in range(5, 30) + range(30, 200, 10):
  total = 0.0
  d = {}
  for exp in range(EXP):
    c = 0
    t = Tourney(n)
    while len(t.alive) > 1:
      t.round()
      c += 1
    total += c
    d.update({c:d.get(c, 0)+1})
  print n, total/EXP, d


