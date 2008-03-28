#!/usr/bin/python


import FIBSCookieMonster

def _create():
  d = dict()
  r = dict()
  for name, obj in FIBSCookieMonster.__dict__.items():
    if name.startswith('FIBS') or name.startswith('CLIP'):
      try:
        i = int(obj)
      except:
        continue
      d.update({name:i})
      r.update({i:name})
  return d,r
    

pton, ntop = _create()

if __name__ == '__main__':
  for i, name in ntop.items():
    j = eval('FIBSCookieMonster.%s'%name)
    if i != j:
      print i, name, j
