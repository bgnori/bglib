#!/usr/bin/python
import socket
import os
import time
import thread
import threading
import logging
import telnetlib
from string import Template

#from bglib.protocol.fibshelper import pton, ntop
#import FIBSCookieMonster

import bglib.protocol.fibs

class Timeout(Exception):
  pass

CRLF = '\r\n'

def synchronized_with(accessor):
  def bind(critical_section):
    def synchronized(self, *args, **kw):
      lock = accessor(self, *args, **kw)
      lock.acquire()
      try:
        ret = critical_section(self, *args, **kw)
      finally:
        lock.release()
      return ret
    return synchronized
  return bind


class Transport(telnetlib.Telnet):
  _lock = threading.RLock()
  lock = lambda self, *args, **kw : self._lock
  
  def __init__(self, timeout=None, debug=None):
    telnetlib.Telnet.__init__(self)
    if timeout:
      self.timeout = timeout
    else:
      self.timeout = 5.0
    if debug is None:
      self.set_debuglevel(0)
    else:
      self.set_debuglevel(debug)
    self.r, self.w = os.pipe()
    self._active = False
    self._termination_requested = False

  def open(self, hostname, port):
    telnetlib.Telnet.open(self, hostname, port)
    self._active = True
    thread.start_new_thread(self._listener, ())

  @synchronized_with(lock)
  def is_active(self):
    return self._active

  @synchronized_with(lock)
  def close(self):
    telnetlib.Telnet.close(self)
    self._active = False
    self._termination_requested = True
    
  @synchronized_with(lock)
  def send_line(self, line):
    logging.debug('sending %s', line)
    self.write(line+CRLF)


class Subscriber:
  lock = lambda self, *args, **kw : self._lock
  def __init__(self, **kw):
    self._lock = threading.Condition()
    self.kw = kw
    
  @synchronized_with(lock)
  def nop(self):
    pass


class Session(Transport):
  def __init__(self, timeout=None, debug=0):
    Transport.__init__(self, timeout=timeout, debug=debug)
    self.monster = bglib.protocol.fibs.CookieMonster()
    self.subscribers = list()
    if self.debuglevel:
      from fibs.debugging import Debug
      Debug()

  def _listener(self):
    logging.debug('started listener')
    try:
      while True:
        nth, matchobj, s = self.expect([CRLF, 'login: '])
        if not nth:
          s = s[:-2] # remove CRLF
        self._dispatch(self.monster.make_cookie(s), s)
    except socket.error, e:
      self._dispatch('socket_error', e)
    except EOFError, e:
      self._dispatch('EOFError', e)
    except:
      logging.exception('exception in listener thread:')
    thread.exit()

  @synchronized_with(Transport.lock)
  def _dispatch(self, name, got):
    if self._termination_requested:
      thread.exit()
    for subscriber in self.subscribers:
      try:
        f = getattr(subscriber, name)
      except AttributeError:
        f = None
      if f:
        f(got)
        logging.debug('dispatched %s', str(f))

  @synchronized_with(Transport.lock)
  def register(self, *args):
    for subscriber in args:
      self.subscribers.append(subscriber)
      logging.debug('subscriber %s is registered.', str(subscriber))

  @synchronized_with(Transport.lock)
  def unregister(self, *args):
    for subscriber in args:
      self.subscribers.remove(subscriber)
      logging.debug('subscriber %s is unregistered.', str(subscriber))


if __name__ == '__main__':
  logging.basicConfig(level=logging.DEBUG,
                     format='%(asctime)s %(levelname)s %(message)s',
                     filename='./session.log',
                     filemode='w')
