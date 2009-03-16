#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2006-2008 Noriyuki Hosaka nori@backgammon.gr.jp
#
import sys
import time
import os
import socket
import select

def serve_forever(addr, f):
  sock = socket.socket(socket.SO_REUSEADDR)
  sock.bind(addr)
  sock.listen(1)
  conn, address = sock.accept()
  try:
    for line in f.readlines():
      conn.send(line)
      time.sleep(.01)
  finally:
    sock.close()

#addr = ('127.0.0.1', 4321)
addr = ('localhost', 4321)
f = file(sys.argv[1])
try:
  serve_forever(addr, f)
finally:
  f.close()

