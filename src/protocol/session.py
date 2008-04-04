#!/usr/bin/python
import socket
import os
import time
import thread
import threading
import logging
import telnetlib
from string import Template

from bglib.protocol.fibshelper import pton, ntop
import FIBSCookieMonster


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
  
  subscribers = list()

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
    for subscriber in self.subscribers:
      logging.debug('subscriber %s is not unregistered.', str(subscriber))
    telnetlib.Telnet.close(self)
    self._active = False
    self._termination_requested = True
    

  def _listener(self):
    logging.debug('started listener')
    FIBSCookieMonster.ResetFIBSCookieMonster()
    try:
      while True:
        nth, matchobj, s = self.expect([CRLF, 'login: '])
        if not nth:
          s = s[:-2] # remove CRLF
        self._dispatch(FIBSCookieMonster.FIBSCookie(s), s)
    except socket.error, e:
      self._dispatch('socket_error', e)
    except EOFError, e:
      self._dispatch('EOFError', e)
    except:
      logging.exception('exception in listener thread:')
    thread.exit()

  @synchronized_with(lock)
  def _dispatch(self, id, got):
    if self._termination_requested:
      thread.exit()
    try:
      int(id)
      name = ntop[id]
    except ValueError:
      name = id
    for subscriber in self.subscribers:
      try:
        f = getattr(subscriber, name)
      except AttributeError:
        f = None
      if f:
        f(got)
        logging.debug('dispatched %s', str(f))

  @synchronized_with(lock)
  def send_line(self, line):
    logging.debug('sending %s', line)
    self.write(line+CRLF)

  @classmethod
  def register(cls, *args):
    cls._lock.acquire() #ugh!
    try:
      for subscriber in args:
        cls.subscribers.append(subscriber)
        logging.debug('subscriber %s is registered.', str(subscriber))
    finally:
      cls._lock.release()

  @classmethod
  def unregister(self, *args):
    cls._lock.acquire() #ugh!
    try:
      for subscriber in args:
        cls.subscribers.remove(subscriber)
        logging.debug('subscriber %s is unregistered.', str(subscriber))
    finally:
      cls._lock.release()


class Subscriber:
  lock = lambda self, *args, **kw : self._lock
  def __init__(self, **kw):
    self._lock = threading.Condition()
    self.kw = kw
    Session.register(self)
  def __del__(self):
    Session.unregister(self)
    
  @synchronized_with(lock)
  def nop(self):
    pass


class Session(Transport):
  def __init__(self, timeout=None, debug=0):
    Transport.__init__(self, timeout=timeout, debug=debug)
    if self.debuglevel:
      from fibs.debugging import Debug
      Debug()

if __name__ == '__main__':
  logging.basicConfig(level=logging.DEBUG,
                     format='%(asctime)s %(levelname)s %(message)s',
                     filename='./session.log',
                     filemode='w')
