#!/usr/bin/gnubg -p
from struct import pack, unpack
from base64 import standard_b64encode, standard_b64decode
from base64 import urlsafe_b64encode, urlsafe_b64decode

def _fact(n):
  if n == 0:
    return 1
  elif n == 1:
    return 1
  else:
    return fact(n-1)*n

class Fact:
  """
>>> fact = Fact()
>>> for i in range(0, 10):
...    assert(fact(i) == _fact(i))
>>> 
  """

  def __init__(self):
    self._cache = list()
    self._cache.append(1) #  0! = 1
    self._cache.append(1) #  1! = 1

  def _expand(self):
    self._cache.append(self._cache[-1] * len(self._cache))

  def __contains__(self, n):
    return len(self._cache) > n
    
  def __call__(self, n):
    assert(n >= 0)
    while n not in self:
      self._expand()
    return self._cache[n]

fact = Fact()


class Combination:
  '''
>>> C(0, 0)
1
>>> C(1, 1)
1
>>> C(4, 2)
6
>>> def _C(n, m):
...   return fact(n)/(fact(m) * fact(n-m))
>>> for i in range(0, 20):
...     for j in range(0, i):
...         assert(_C(i, j) == C(i, j))
>>> 
  '''
  def __init__(self):
    self._cache = dict()
    self._update(0, 0, 1) # C(0, 0)
    self._size = 1

  def _update(self, n, r, value):
    self._cache.update({(n, r): value})

  def _read(self, n, r):
    if n < 0 or r < 0:
      return 0
    elif n < r:
      return 0
    else:
      return self._cache[(n, r)]

  def _expand(self):
    if self._size > 100:
      import sys
      print len(self._cache)
      sys.exit('too big cache')
    n = self._size 
    for i in range(0, n+1):
      self._update(n=n, 
                   r=i, 
                   value=self._read(n=n-1, r=i-1)+self._read(n=n-1, r=i)
                  )
    self._size = n + 1

  def __contains__(self, n):
    return self._size > n

  def __call__(self, n, r):
    while n not in self:
      self._expand()
    return self._read(n, r)
C = Combination()


def D(n, m):
  '''D of Walter Trice.
  http://www.bkgm.com/rgb/rgb.cgi?view+371
  '''
  return C(n+m-1, m)

WTN = 18528584051601162496
'''
WTN : Walter Trice Number, number of Possible Backgammon Position.
  http://www.bkgm.com/rgb/rgb.cgi?view+371
'''

def BackgammonCombination(m):
  '''
>>> sum = 0
>>> for m in range(0, 16):
...     sum += BackgammonCombination(m)
>>> sum == WTN
True
  '''
  return C(24, m) * D(m+2, 15-m) * D(26-m, 15)


def BackgammonCombination_allC(m):
  '''by definition of D, it must give same result.
>>> sum = 0
>>> for m in range(0, 16):
...     sum += BackgammonCombination_allC(m)
>>> sum == WTN
True
  '''
  return C(24, m) * C(16, 15-m) * C(40-m, 15)


def C_Hash(xs, r):
  '''
>>> xs = [1, 0, 1, 0, 0]
>>> C_Hash(xs, r=2)
8
>>> xs = [0, 0, 0, 1, 1]
>>> C_Hash(xs, r=2)
0
  '''
  n = len(xs) - 1
  i = 0
  hash = 0
  while n >= r and r > 0:
    if xs[i]:
      hash += C(n, r)
      r-=1
    i+=1
    n-=1
  return hash


def C_RHash(x, n, r):
  '''
>>> C_RHash(8, 5, 2)
[1, 0, 1, 0, 0]
  '''
  result = list()
  for i in range(n, 0, -1):
    if x >= C(i - 1, r):
      result.append(1)
      x -= C(i - 1, r)
      r -= 1
    else:
      result.append(0)
  return result


def D_Hash(xs, m):
  ''' perfect hash for D)(n, m)  = C(n+m-1, m) # definition
#>>> D_Hash((6, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0,\
             0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1), 15)

#>>> D_Hash((0, 3, 2, 2, 2, 3, 0, 0, 1, 0, 0, 0, \
             0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0), 15)

  '''
  count = 0
  for x in xs:
    if x:
      count+=1
  return C_Hash(xs, count)


class ByteContext:
  def __init__(self):
    self.byte = 0 # r'\x00'
    self.count = 0
    
  def write(self, bit):
    self.byte |= bit << self.count
    self.count += 1
    return self.count < 8
    
  def pack(self):
    r = pack('<B', self.byte)
    self.reset()
    return r

  def pad(self):
    for i in range(self.count, 8): # padding
      self.write(0)
    return self.pack()

  def reset(self):
    self.byte = 0 # r'\x00'
    self.count = 0


def encode(xs):
  """
>>> for x in encode((0, 0, 0, 0, 0, 5, 2, 3, 0, 0, 0, 0,\
                     4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)):
...     x
'\\xe0'
'\\xdb'
'\\xc1'
'\\x03'
'\\x00'
  """
  byte = ByteContext()
  for x in xs:
    for i in range(0, x):
      if not byte.write(1):
        yield byte.pack()
    if not byte.write(0):
      yield byte.pack()
  if byte.count == 0:
    raise StopIteration
  else:
    yield byte.pad()


def decode(b):
  '''
>>> list(decode('\\xe0\\xdb\\xc1\\x03\\x00'))
[0, 0, 0, 0, 0, 5, 2, 3, 0, 0, 0, 0,\
 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
  '''

  n = 0
  for fragment in b:
    byte = unpack('<B', fragment)[0]
    for j in range(8):
      if byte & (1 << j):
        n += 1
      else:
        yield n
        n = 0
  yield n


def oneside_encode(xs):
  return ''.join(list(encode(xs)))


def oneside_decode(s):
  """
>>> oneside_decode(oneside_encode((6, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0,\
                                   0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1)))
(6, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1)
>>> oneside_decode(oneside_encode((0, 3, 2, 2, 2, 3, 0, 0, 1, 0, 0, 0,\
                                   0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0)))
(0, 3, 2, 2, 2, 3, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0)
  """
  return tuple(decode(s))[:25]


def twoside_encode(xs):
  s = list(encode( list(xs[0])+ list(xs[1])))
  return ''.join(s)


def twoside_decode(s):
  """
>>> twoside_decode(twoside_encode(((6, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0,\
                                    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1),\
                                   (0, 3, 2, 2, 2, 3, 0, 0, 1, 0, 0, 0,\
                                    0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0))))
((6, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0,\
 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1),\
 (0, 3, 2, 2, 2, 3, 0, 0, 1, 0, 0, 0,\
 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0))
  """
  xs = list(decode(s))
  return (tuple(xs[:25]), tuple(xs[25:50]))


def gnubg_position_encode(xs):
  """
>>> gnubg_position_encode(((6, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0,\
                   0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1),\
                  (0, 3, 2, 2, 2, 3, 0, 0, 1, 0, 0, 0,\
                   0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0)))
'vzsAAFhu2xFABA'
>>> gnubg_position_encode(((0, 0, 0, 0, 0, 5, 0, 3, 0, 0, 0, 0,\
                   5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0),\
                  (0, 0, 0, 0, 0, 5, 0, 3, 0, 0, 0, 0,\
                   5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0)))
'4HPwATDgc/ABMA'
  """
  return standard_b64encode(twoside_encode(xs)).rstrip('=')

def gnubg_position_decode(s):
  """
>>> gnubg_position_decode("vzsAAFhu2xFABA")
((6, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0,\
 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1),\
 (0, 3, 2, 2, 2, 3, 0, 0, 1, 0, 0, 0,\
 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0))

>>> gnubg_position_decode("4HPwATDgc/ABMA")
((0, 0, 0, 0, 0, 5, 0, 3, 0, 0, 0, 0,\
 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0),\
 (0, 0, 0, 0, 0, 5, 0, 3, 0, 0, 0, 0,\
 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0))
  """
  while True:
    try:
      bin = standard_b64decode(s)
    except TypeError, e:
      if str(e) != 'Incorrect padding':
        raise
      s += '='
    else:
      break
  return twoside_decode(bin)


def urlsafe_position_encode(xs):
  """
>>> urlsafe_position_encode(((6, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0,\
                     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1),\
                    (0, 3, 2, 2, 2, 3, 0, 0, 1, 0, 0, 0,\
                     0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0)))
'vzsAAFhu2xFABA'
>>> urlsafe_position_encode(((0, 0, 0, 0, 0, 5, 0, 3, 0, 0, 0, 0,\
                     5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0),\
                    (0, 0, 0, 0, 0, 5, 0, 3, 0, 0, 0, 0,\
                     5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0)))
'4HPwATDgc_ABMA'
  """
  return urlsafe_b64encode(twoside_encode(xs)).rstrip('=')


def urlsafe_position_decode(s):
  """
>>> urlsafe_position_decode("vzsAAFhu2xFABA")
((6, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0,\
 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1),\
 (0, 3, 2, 2, 2, 3, 0, 0, 1, 0, 0, 0,\
 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0))
>>> urlsafe_position_decode("4HPwATDgc_ABMA")
((0, 0, 0, 0, 0, 5, 0, 3, 0, 0, 0, 0,\
 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0),\
 (0, 0, 0, 0, 0, 5, 0, 3, 0, 0, 0, 0,\
 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0))
  """
  while True:
    try:
      bin = urlsafe_b64decode(s)
    except TypeError, e:
      if str(e) != 'Incorrect padding':
        raise
      s += '='
    else:
      break
  return twoside_decode(bin)


def convert_to_urlsafe(s):
  return s.replace('+', '-').replace('/', '_')


def convert_from_urlsafe(s):
  return s.replace('-', '+').replace('_', '/')


def urlsafe_match_encode(m):
  pass


def urlsafe_match_decode(s):
  pass


def FIBSDecode(s):
  '''
>>> b = FIBSDecode('board:You:someplayer:3:0:0:0:-2:0:0:0:0:5:0:3:0:0:0:-5:5:0:0:0:-3:0:-5:0:0:0:0:2:0:1:6:2:0:0:1:1:1:0:1:-1:0:25:0:0:0:0:2:0:0:0')
>>> b.position
((0, 0, 0, 0, 0, 5, 0, 3, 0, 0, 0, 0,\
 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0),\
 (0, 0, 0, 0, 0, 5, 0, 3, 0, 0, 0, 0,\
 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0))
>>> b.data
['board', 'You', 'someplayer', '3', '0', '0', '0', '-2',\
 '0', '0', '0', '0', '5', '0', '3', '0', '0', '0', '-5',\
 '5', '0', '0', '0', '-3', '0', '-5', '0', '0', '0', '0',\
 '2', '0', '1', '6', '2', '0', '0', '1', '1', '1', '0',\
 '1', '-1', '0', '25', '0', '0', '0', '0', '2', '0', '0', '0']
>>> b.data[b.index['you'][0]:b.index['you'][1]]
['You']
>>> b.you
['You']


  '''
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


if __name__ == "__main__":
  import doctest
  doctest.testmod()

