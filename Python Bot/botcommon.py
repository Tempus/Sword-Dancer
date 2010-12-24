"""\
Common bits and pieces used by the various bots.
"""

import sys
import os
import time
from threading import Thread, Event


class OutputManager(Thread):
  def __init__(self, connection, delay=.5):
    Thread.__init__(self)
    self.setDaemon(1)
    self.connection = connection
    self.delay = delay
    self.event = Event()
    self.queue = []

  def run(self):
    while 1:
      self.event.wait()
      while self.queue:
        msg,target = self.queue.pop(0)
        self.connection.privmsg(target, msg)
        time.sleep(self.delay)
      self.event.clear()

  def send(self, msg, target):
    self.queue.append((msg.strip(),target))
    self.event.set()


# This looks like where to add arguments!
def trivial_bot_main(botClass):
  if len(sys.argv) != 8:
    botname = os.path.basename(sys.argv[0])
    print "Incorrect Usage Message and Instructions go here"
#    sys.exit(1)

  # Actual arguments are...?
  # botClass(sys.argv[1], sys.argv[2], etc...).start()
  # The counterparts go into TickTock.py's 'def __init__' arg list

  botClass().start()
