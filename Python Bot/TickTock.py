#!/usr/bin/env python

#
# Tales CCG Python IRCBot, originally 'TickTock'
#  - Tempus, Aaron/AerialX <www.talesofgraces.com>
#
# python-irclib by Joel Rosdahl <joel@rosdahl.net>
#

"""

Tales CCG IRC Bot.

Currently accepts any commands beginning with a bang (!), or
any phrase that contains its name. That doesn't means it parses
them intelligently, of course!

"""

import sys, string, random, time, re
from ircbot import SingleServerIRCBot, IRCDict
from irclib import nm_to_n, nm_to_h, irc_lower
import botcommon

#--------------------------------------------------------------------
# Confirmation strings for admins.

adminConfirm = [
 "Of course, Master",
 "Certanly, O Great One.",
 "As you say, so it shall be.",
 "With alacricity, Master",
 "At your command.",
 "It would be my deepest honour.",
 "It is a pleasure to serve.",
 "By thine will.",
 "So it is written, so it is done."
 ]


#--------------------------------------------------------------------
# Denial string for a request with insufficient permissions.

notAdmin = [
 "I'm not that easy, jerkwad.",
 "Why don't you pass me a sweet 100$?",
 "Sure, you and what army?",
 "Did your girlfriend put you up to this? Whipped!",
 "I can't let you do that Dave.",
 "I don't take orders from Hoomans.",
 "Hmm, who are you, Mr. Big Man?",
 "Ha! Good luck.",
 "In life, you don't always get what you want."
]



#---------------------------------------------------------------------
# The bot class. The main loops and buffer are handled by the library,
# thankfully, so we can get right to business. Commands are called from
# the on_privmsg and on_pubmsg functions. Currently all commands are
# parsed by the do_command function, but since a loop in that function
# will freeze all commands until it finishes (at which point it'll
# playback the buffer), it's better to have multiple functions called
# from the private and public message functions when you want a loop.


class TickTock(SingleServerIRCBot):

  def __init__(self):
    # The args for the class are the server, port, Nick, and TrueName
    SingleServerIRCBot.__init__(self, [('irc.freenode.net', 6667)], 'TickTock', 'TickTockBot')
    
    # Channels to join on connect. I've modified the base class to print joins
    self.channel = ['#Graces']
    
    # Bot Nickname
    self.nickname = 'TickTock'
    
    # Dunno what this is, but it breaks without it. Stolen from example bot.
    self.queue = botcommon.OutputManager(self.connection)
    
    # An Admin List, populated with Admins. Whitelists by nicks, currently, we should set these to hostmasks
    self.adminList = ['Tempus', 'ruta', 'Aaron`']
    
    # This runs the main loop.
    self.queue.start()
    

  # Case for nickname in use
  def on_nicknameinuse(self, c, e):
    self.nickname = c.get_nickname() + "Clock"
    c.nick(self.nickname)

  # Called after the welcome message from the server. For now, it just joins everything in the
  # channel list, but in the future, identify and ns stuff can be put here.
  def on_welcome(self, c, e):
    for i in self.channel:
       c.join(i)


  # The all important 'message received!'. All private and public messages are parsed into something usable.
  #
  # e.source            - raw nickmask
  # nm_to_n(nickmask)   - Full Nickname
  # nm_to_uh(nickmask)  - Userhost
  # nm_to_h(nickmask)   - Host
  # nm_to_u(nickmask)   - User
  #
  
  def on_privmsg(self, c, e):
    from_nick = nm_to_n(e.source())
    self.do_command(c, e, e.arguments()[0], from_nick)

  def on_pubmsg(self, c, e):
    from_nick = nm_to_n(e.source())
    if (e.arguments()[0][0] == '!') or (e.arguments()[0].find(self.nickname) != -1):
      self.do_command(c, e, string.strip(e.arguments()[0][1:]), from_nick)
    return


  # Used internally for targetting purposes.
  def say_public(self, text):
    "Print TEXT into public channel, for all to see."
    self.queue.send(text, self.channel)

  def say_private(self, nick, text):
    "Send private message of TEXT to NICK."
    self.queue.send(text,nick)

  def reply(self, text, to_private=None):
    "Send TEXT to either public channel or TO_PRIVATE nick (if defined)."

    if to_private is not None:
      self.say_private(to_private, text)
    else:
      self.say_public(text)


  # The current response handler for all responses.
  #
  # c is the base connection class 
  # e is the base message
  # cmd is the received string to be handled
  # from_private is the nick of the sender

  def do_command(self, c, e, cmd, from_private):
  
    # sets up the replies to the proper target
    if e.target() != self.nickname:
      # self.reply() sees 'from_private = None' and sends to public channel.
      target = e.target()
    else:
      # assume that from_private comes from a 'privmsg' event.
      target = from_private.strip()


    # Parses '<Botnick>: string' into 'string'
    if cmd[:len(self.nickname)] == self.nickname:
      cmd = cmd[len(self.nickname) + 1:].strip()
    
    
    # TickTock Commands follow here. Each one has a check for admin, but this can be improved by
    # not assininely check each time and just using some proper nested commands and checks and junk.
    #
    # This is just a very basic sample.

    # A basic help print from TickTock
    if cmd[:4] == 'help':
      self.reply("Prefix: '!' or 'TickTock:' .Supported Commands: join, part, quit, help", target)


    # A basic join, part and quit from TickTock        
    elif cmd[:4] == 'join':
      if self.adminList.count(from_private) > 0:
        self.reply(random.choice(adminConfirm), target)
        if len(cmd) >= 4:
          c.join(cmd[5:])
        else:
          self.reply("You need to tell me which channel to join")
      else:
        self.reply(random.choice(notAdmin), target)

    elif cmd[:4] == 'part':
      if self.adminList.count(from_private) > 0:
        self.reply(random.choice(adminConfirm), target)
        if len(cmd) >= 4:
          c.part(cmd[5:])
      else:
        self.reply(random.choice(notAdmin), target)

    elif cmd[:4] == 'quit':
      if self.adminList.count(from_private) > 0:
        self.reply(random.choice(adminConfirm), target)
        if len(cmd) >= 5:
          c.quit(cmd[5:])
          quit()
        else:
          c.quit("Looks like I'm out of time")
          quit()
      else:
        self.reply(random.choice(notAdmin), target)


    # Default reply from TickTock. Praises the whitelist and ignores anyone else.            
    else:
      whitelist = ['ruta', 'ruta-work', 'Tempus', 'Aaron`', 'Carnivol', 'DragonSamurai55', 'gbcft', 'Jazzysan', 'Kajitani-Eizan', 'LunaHoshino', 'Kennoko', 'throughhim413']
    
      compliments = ['fantastic', 'magnificient', 'superb', 'marvelous', 'wonderful', 'sensational', 'outstanding', 'stupendous', 'super', 'excellent', 'first-rate', 'first-class', 'dazzling', 'out of this world', 'breathtaking', 'great', 'terrific', 'fabulous', 'ace', 'magic', 'cool', 'wicked', 'awesome', 'brilliant']
    
      if whitelist.count(from_private) > 0:
        self.reply("{0} is {1}!".format(from_private, random.choice(compliments)), target)
        
      else:
        self.reply("Sorry, {0} I didn't quite catch that.".format(from_private), target)
        

# Main
if __name__ == "__main__":
  try:
    # Runs bot
    botcommon.trivial_bot_main(TickTock)
    
  except KeyboardInterrupt:
    # Gives and exit message to your console on manual stop.
    print "Shutting down."

