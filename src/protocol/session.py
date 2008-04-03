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
    self.subscribers = list()

  def open(self, hostname, port):
    telnetlib.Telnet.open(self, hostname, port)
    thread.start_new_thread(self._listener, ())

  @synchronized_with(lock)
  def close(self):
    for subscriber in self.subscribers:
      logging.debug('subscriber %s is not unregistered.', str(subscriber))
    telnetlib.Telnet.close(self)

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

  @synchronized_with(lock)
  def _dispatch(self, id, got):
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

  @synchronized_with(lock)
  def register(self, *args):
    for subscriber in args:
      self.subscribers.append(subscriber)
      subscriber.post_register()
      logging.debug('subscriber %s is registered.', str(subscriber))

  @synchronized_with(lock)
  def unregister(self, *args):
    for subscriber in args:
      self.subscribers.remove(subscriber)
      logging.debug('subscriber %s is unregistered.', str(subscriber))


class Subscriber:
  lock = lambda self, *args, **kw : self._lock
  def __init__(self, **kw):
    self._lock = threading.Condition()
    self.kw = kw
    self._done = False
    self.results = list()
    
  @synchronized_with(lock)
  def post_register(self):
    pass

  @synchronized_with(lock)
  def append(self, result):
    if self._done:
      raise ValueError("already done!")
    self.results.append(result)
    
  @synchronized_with(lock)
  def done(self):
    if self._done:
      raise ValueError("already done!")
    self._done = True
    self._lock.notifyAll()

  @synchronized_with(lock)
  def is_done(self):
    return self._done

  @synchronized_with(lock)
  def wait_for_result(self): # this must be in Main thread
    self._lock.wait()
    if not self._done:
      raise Timeout
    return self.results


class BannerGrabber(Subscriber):
  def FIBS_PreLogin(self, got):
    self.append(got)
  def FIBS_LoginPrompt(self, got):
    pass #self.done() # it is not okay on login fail
  def CLIP_MOTD_END(self, got):
    self.done()


class Session(Transport):
  def __init__(self, timeout=None, debug=0):
    Transport.__init__(self, timeout=timeout, debug=debug)
    if self.debuglevel:
      from debugging import Debug
      self.debug_subscribers = [Debug(self)]
      self.register(*self.debug_subscribers)
    else:
      self.debug_subscribers = []

  def blocking(self, subscriber):
    self.register(subscriber)
    ret = subscriber.wait_for_result()
    self.unregister(subscriber)
    return ret
    
if __name__ == '__main__':
  logging.basicConfig(level=logging.DEBUG,
                     format='%(asctime)s %(levelname)s %(message)s',
                     filename='./session.log',
                     filemode='w')
  session = Session(debug=1)
  session.open('fibs.com', 4321)
  print session.login(client_name='test', 
                      clip_version=FIBSCookieMonster.CLIP_VERSION, 
                      username='bgnori', password='hogehoge')
  time.sleep(10)
  print session.exit()

