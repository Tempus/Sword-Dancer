#!/usr/bin/env python

#
# Tales CCG Python IRCBot, originally 'TickTock'
#    - Tempus, Aaron/AerialX <www.talesofgraces.com>
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
from irclib import nm_to_n, nm_to_h, nm_to_uh, nm_to_u, irc_lower
import botcommon
from ccg import Deck

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
# parsed by the default_Response function, but since a loop in that function
# will freeze all commands until it finishes (at which point it'll
# playback the buffer), it's better to have multiple functions called
# from the private and public message functions when you want a loop.


GameRoom = '#CCGtest'
ViewRoom = '#ObservationDeck'


class TickTock(SingleServerIRCBot):

    def __init__(self):
        # Bot Nickname
        self.nickname = 'SwordDancer'
        
        # The args for the class are the server, port, Nick, and TrueName
        SingleServerIRCBot.__init__(self, [('irc.freenode.net', 6667)], self.nickname, 'TalesCCGReferee')
        
        # Channels to join on connect. I've modified the base class to print joins
        self.channel = [GameRoom, ViewRoom]
        
        # Dunno what this is, but it breaks without it. Stolen from example bot.
        self.queue = botcommon.OutputManager(self.connection)
        
        
        # Card Game variables
        self.players = []
        self.decks = []
        self.turn = None

        # This runs the main loop.
        self.queue.start()
        

    # Case for nickname in use
    def on_nicknameinuse(self, c, e):
        self.nickname = c.get_nickname() + "Ref"
        c.nick(self.nickname)

    # Called after the welcome message from the server. For now, it just joins everything in the
    # channel list, but in the future, identify and ns stuff can be put here.
    def on_welcome(self, c, e):
        for i in self.channel:
             c.join(i)


    # The all important 'message received!'. All private and public messages are parsed into something usable.
    #
    # e.source                        - raw nickmask
    # nm_to_n(nickmask)     - Full Nickname
    # nm_to_uh(nickmask)    - Userhost
    # nm_to_h(nickmask)     - Host
    # nm_to_u(nickmask)     - User
    #
    
    def on_privmsg(self, c, e):
        sender = nm_to_n(e.source())
        msg = e.arguments()[0].strip()

        if self.players.count(sender) > 0:
            self.sekrit_Commands(c, e, msg, sender)
                
        else:
            self.default_Response(c, e, msg, sender)


    def on_pubmsg(self, c, e):
        sender = nm_to_n(e.source())
        msg = e.arguments()[0].strip()
        room = e.target()
        
        if room == GameRoom:        
            if msg[:27] == "I challenge you to a duel, ":
                self.begin_Duel(c, e, msg, sender)
            
            elif (msg == 'Cancel Duel'):
                pass
                        
            elif sender == self.turn:
                self.game_Controls(c, e, msg, sender)
                

        else (msg[0] == '!'):
            self.default_Response(c, e, msg[1:], sender)
            
        return


    # Used internally for targetting purposes.
    def say_public(self, text):
        "Print TEXT into public channel message originated from, for all to see."
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

    def call_Response(self, e, sender):
    
        # sets up the replies to the proper target
        if e.target() != self.nickname:
            # self.reply() sees 'sender = None' and sends to public channel.
            target = e.target()
        else:
            # assume that sender comes from a 'privmsg' event.
            target = sender.strip()
        
        return target




    # Response handlers
    #
    # c is the base connection class 
    # e is the base message
    # msg is the received string to be handled
    # sender is the nick of the sender

    def begin_Duel(self, c, e, msg, sender):

        challenger = msg[27:]

        # Check to see if a duel is going on
        if self.players != []:
            self.reply("One duel at a time, please.", GameRoom)

        # Check to see if challenged player exists
        if self.channels[GameRoom].has_user(challenger):
            self.reply("{0} has been challenged by {1}. You may now choose your decks.".format(challenger, sender), GameRoom)
            self.reply("Players may type 'Cancel Duel' to cancel.", GameRoom)
            
            # Players recieve choose deck messages
            # ToDo: base this off the decks in the database
            self.reply("Choose between 'Deck 1', 'Deck 2', etc", sender)
            self.reply("Choose between 'Deck 1', 'Deck 2', etc", challenger)
            self.players = [sender, challenger]
            self.decks = [None, None]
        else:
            self.reply("There's no point in challenging someone that isn't here. Duel cancelled.", GameRoom)


    def cancel_Duel(self, c, e, msg, sender):
        
        if self.players == []:
            self.reply("No duel active.", GameRoom)
            return
        
        if (self.players.count(sender) > 0) or (self.channels[GameRoom].is_oper(sender) == sender):
            self.reply("Duel Cancelled.", GameRoom)
        
            self.players = []
            self.turn = None
            self.decks = []
        
        # ToDo: penalty for users cancelling ongoing duels        

        else:
            self.reply("You don't have the authority to stop this duel.", GameRoom)


    def game_Controls(self, c, e, msg, sender):

        # Get the card list
        try:
            deckIndex = self.players.index(sender)
        except:
            print sender
            self.reply("Something bad has happened.", GameRoom)
            return
        
        hand = self.decks[deckIndex].displayHand()
        
        
        # Get the list of possible characters
        ownChars = self.decks[deckIndex].charNames()
        otherChars = []
        
        for x in xrange(len(self.decks)):
            if x == deckIndex:
                pass
            else:
                otherChars.extend(self.decks[x].charNames())
        
        

        # Use an item
        if 'recipe' in msg.lower():
            char = None
        
            # Look for the Card name
            for recipe in hand:
                if recipe.lower() in msg.lower():

                    for charac in ownChars:
                        if charac.lower() in msg.lower():
                            char = charac
                            
                    reply = self.decks[deckIndex].useRecipe(recipe, char)
                    self.reply(reply, GameRoom)
                    return

        
        # Use an item
        if 'item' in msg.lower():
            char = None
            user = None
        
            # Look for the Card name
            for item in hand:
                if item.lower() in msg.lower():

                    for charac in ownChars:
                        if charac.lower() in msg.lower():
                            user = charac

                    if user == None:
                        self.reply("You didn't specify who to use the item with")
                        
                    for charac in ownChars:
                        if 'on ' + charac.lower() in msg.lower():
                            char = charac
                    
                    for carda in hand:
                        if 'on ' + cards.lower() in msg.lower():
                            char = carda                    
                            
                    reply = self.decks[deckIndex].useItem(item, char, user)
                    self.reply(reply, GameRoom)
                    return
            
        
        # Equip a card
        elif 'equip' in msg.lower():
            char = None
        
            # Look for the Card name
            for equip in hand:
                if equip.lower() in msg.lower():

                    for charac in ownChars:
                        if charac.lower() in msg.lower():
                            char = charac
                            
                    reply = self.decks[deckIndex].useEquip(equip, char)
                    self.reply(reply, GameRoom)
                    return

                
        # Execute an arte
        elif 'arte' in msg.lower():
            char = None
            user = None
            
            # Look for the Card name
            for arte in hand:
                if arte.lower() in msg.lower():

                    for charac in ownChars:
                        if charac.lower() in msg.lower():
                            user = charac

                    for 'on ' + charac in otherChars:
                        if charac.lower() in msg.lower():
                            char = charac
                            
                    reply = self.decks[deckIndex].useArte(arte, char, user)
                    self.reply(reply, GameRoom)
                    return

        
        # End your turn
        elif 'end' and 'turn' in msg.lower():
            self.end_turn()

        
    def end_turn(self):
        self.reply("{0}'s turn is over.".format(self.turn), GameRoom)
        
        
        
        
        # ToDo: End turn crap


    def sekrit_Commands(self, c, e, msg, sender):
        
        # Deck setting command
        if msg[:5] == 'Deck ':
            try:
                deckNum = int(msg[5:])
                self.decks[self.players.index(sender)] = Deck(self, sender, deckNum)
                
                # return if the other players haven't set their deck yet.
                try:
                    self.decks.index(None) 
                except:
                    return
                
                # Beginning the match
                self.turn = random.choice(self.players)
                
                self.reply("Some Reply", sender)
                
            except:
                self.reply("Not a valid choice, check your spelling.", sender)


    def admin_Response(self, c, e, msg, sender):

        target = self.call_Response(e, sender)



    def default_Response(self, c, e, msg, sender):
    
        target = self.call_Response(e, sender)


        # Parses '<Botnick>: string' into 'string'
        if msg[:len(self.nickname)] == self.nickname:
            msg = msg[len(self.nickname) + 1:].strip()
        
        
        # TickTock Commands follow here. Each one has a check for admin, but this can be improved by
        # not assininely check each time and just using some proper nested commands and checks and junk.
        #
        # This is just a very basic sample.

        # A basic help print from TickTock
        if msg[:4] == 'help':            
            self.reply("Prefix: '!' or 'TickTock:' .Supported Commands: join, part, quit, help", target)

        # A basic join, part and quit from TickTock                
        elif msg[:4] == 'join':
            if self.adminList.count(sender) > 0:
                self.reply(random.choice(adminConfirm), target)
                if len(msg) >= 4:
                    c.join(msg[5:])
                else:
                    self.reply("You need to tell me which channel to join")
            else:
                self.reply(random.choice(notAdmin), target)

        elif msg[:4] == 'part':
            if self.adminList.count(sender) > 0:
                self.reply(random.choice(adminConfirm), target)
                if len(msg) >= 4:
                    c.part(msg[5:])
            else:
                self.reply(random.choice(notAdmin), target)

        elif msg[:4] == 'quit':
            if self.adminList.count(sender) > 0:
                self.reply(random.choice(adminConfirm), target)
                if len(msg) >= 5:
                    c.quit(msg[5:])
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
        
            if whitelist.count(sender) > 0:
                self.reply("{0} is {1}!".format(sender, random.choice(compliments)), target)
                
            else:
                self.reply("Sorry, {0} I didn't quite catch that.".format(sender), target)
                

# Main
if __name__ == "__main__":
    try:
        # Runs bot
        botcommon.trivial_bot_main(TickTock)
        
    except KeyboardInterrupt:
        # Gives and exit message to your console on manual stop.
        print "Shutting down."

