#
# Tales CCG Python IRCBot, originally 'TickTock'
#    - Tempus, Aaron/AerialX <www.talesofgraces.com>
#
# python-irclib by Joel Rosdahl <joel@rosdahl.net>
#

"""

Tales CCG IRC Library.

This Library is intended to handle the actual game logic of the ccg,
as well as outlining the class to keep the current game state.

"""

from math import log
from time import sleep
from collections import deque
from random import choice
import sqlite3

GameRoom = '#CCGtest'
ViewRoom = '#ObservationDeck'

con = sqlite3.connect('/Users/Tempus/Projects/Tales Online CCG/Docs/Raw Tables/CardDatabase.csv')
cur = con.cursor()


class Character:
    """Character card class"""
    
    def __init__(self, cardID, reply):
        """Looks up a character by ID from the SQL database, and loads the info"""
        
        
        cur.execute('SELECT * from CardList where ID=?', (cardID,))
        cardData = cur.fetchall()[0]


        # ToDo - calculate the level of the Hero from the SQL database
        # Level = 
        
        self.reply = reply
        self.type = 0
        
        self.name = cardData[2]
        self.description = cardData[3]
        
        self.rarity = cardData[5]
        self.equip = bf(cardData[11]) # A sliceable integer class, where int[0] is the lower bit
        self.artes = bf(cardData[12]) # A sliceable integer class, where int[0] is the lower bit

        self.TP = cardData[6] * (Level/100 + 1)
        self.HP = cardData[7] * (Level/100 + 1)
        self.Att = cardData[8] * (Level/100 + 1)
        self.Mag = cardData[10] * (Level/100 + 1)
        self.Dfn = cardData[9] * (Level/100 + 1)
        
        self.currentHP = self.HP
        self.currentTP = self.TP
        

        # Effect list. Format: EffectID, Effect Amount, EquipAttach (0 is none, 2 is weapon, 3 armour, 4 accessory)
        self.effectList = []
        
        # Temporary Effects: A deque of three lists that pops left each turn and appends an empty list right. Att, Dfn, Mag
        self.tempEffects = deque([[0,0,0], [0,0,0], [0,0,0]])
        
        # Equipment list. Format: TP, HP, Att, Def, Mag
        self.weapon = [0,0,0,0,0]
        self.armour = [0,0,0,0,0]
        self.accessory = [0,0,0,0,0]
        
        self.ko = False
        
    def name(self):
        """Returns the character name"""
    
        return self.name
    
    def description(self):
        """Returns the character descripton"""
    
        return string
                    
    def hurt(self, modifer):
        """Modifies the current HP by an amount"""
        
        oldHP = self.currentHP
        self.currentHP += modifier

        if self.currentHP < 0:
        
            self.currentHP = 0
            self.ko = true

            #  40	- Can not drop below 1 HP unless HP=1
            if self.hasEffect(40) != -1:
                
                if oldHP == 1:
                    pass
                else:
                    self.reply("{0}'s equipment protects them from dying!".format(self.name()), GameRoom) 
                    self.currentHP = 1
                    self.ko = False        

            #  45	- Revive on Death			    % chance to revive on dying, removing the accessory from the battle
            a = self.hasEffect(45)
            if a != -1:
            
                if random.randint(0, 100) < a:
                    self.reply("{0}'s equipment revives them, and recovers 30% health.".format(self.name()), GameRoom) 
                    self.ko = False
                    self.heal(30)
            
            self.reply("{0} was knocked unconcious!".format(self.name()), GameRoom)
        
        return self.currentHP
    
    def heal(self, modifier):
        """Modifies the current HP by a multipler/100"""
        
        if self.ko = True:
            return self.currentHP
        
        self.currentHP = self.currentHP * (1 + (modifier/100))
        if self.currentHP > (self.HP + self.weapon[2] + self.armor[2] + self.accessory[2]):
            self.currentHP = (self.HP + self.weapon[2] + self.armor[2] + self.accessory[2])
            
        return self.currentHP

    def revive(self):
        """Revives the character"""
        
        self.ko = False
                
            
    def currentHP(self):
        """Returns the currentHP"""

        return self.currentHP


    def currentTP(self):
        """Returns the currentTP"""

        return self.currentTP


    def modifyTP(self, amount=0):
        """Modifies the current HP by an amount"""

        self.currentTP += amount
        
        if self.currentTP > (self.TP + self.weapon[0] + self.armor[0] + self.accessory[0]):
            self.currentTP = (self.TP + self.weapon[0] + self.armor[0] + self.accessory[0])
            
        if self.currentTP < 0:
            self.currentTP = 0
            
        return self.currentTP
        
        
    def stats(self)
        """Returns a list of the current statistics for the player: TP, HPmax, Att, Def, Mag"""

        bonus = self.rotateEffects()
        
        stats = [self.TP + self.weapon[0] + self.armor[0] + self.accessory[0],
                 self.HP + self.weapon[1] + self.armor[1] + self.accessory[1],
                 (self.Att + self.weapon[2] + self.armor[2] + self.accessory[2]) * (1+(bonus[0]/100)),
                 (self.Dfn + self.weapon[3] + self.armor[3] + self.accessory[3]) * (1+(bonus[1]/100)),
                 (self.Mag + self.weapon[4] + self.armor[4] + self.accessory[4]) * (1+(bonus[2]/100))]
                 
        return stats
        
        
    def equipCheck(self, card):
        """Checks to see if a card can be equipped"""
        
        if card.type != 2 or 3 or 4:
            return False
            
        if self.equip[len(card.family) - 1] == True:
            return True
    
        return False
    
    
    def equip(self, card):
        """Equips a card to the appropriate slot. Clears the previous slot."""
        
        # Remove equipment effects
        for x in xrange(len(effectList)):
            if effectList[x][2] == card.type:
                effectList.pop(x)
        
        # Add in the stats
        if card.type == 2
            self.weapon = [card.TP, card.HP, card.Att, card.Dfn, card.Mag]
            
        if card.type == 3
            self.armour = [card.TP, card.HP, card.Att, card.Dfn, card.Mag]

        if card.type == 4
            self.accessory = [card.TP, card.HP, card.Att, card.Dfn, card.Mag]
            
        # Add the effect if it exists    
        if card.EffA > 0:
            effectList.append([card.EffA, card.AQuan, card.type])
        
        
    def arteCheck(self, card):
        """Checks to see if an arte can be used"""
        
        if card.type != 1:
            return False
            
        if self.artes[len(card.family) - 1] == True:
            return True
    
        return False


    def hasEffect(self, effType):
        """Checks for an effect type, and returns the amount"""

        for effect in self.effectList:
            if effect[0] == effType:
                return effect[1]

        return -1

        #  4	- HP restored on hit			% HP restored
        #  8	- TP restored on hit			# TP restored
        #  25	- Gold Reward Increased			% Increased
        #  26	- EXP Reward Increased			% Increased
        #  27	- Dodge					        % Chance of enemy attacks missing
        #  28	- Death					        % Chance of instant death to target
        #  30	- Block Magic Combo			    # of artes to block from next magic combo targeted at player
        #  31	- Block Physical Combo			# of rates to block from next physical combo targeted at player
        #  32	- Block Artes Combo			    # of rates to block from next combo targeted at player
        #  34	- Damage				        # of Damage to deal to target
        #  36	- Cancels Dodge Chance			
        #  41	- Grants a free card after battle
        #  42	- Reveals the cards the enemy draws


    def cardDraws(self):
        """Returns the bonus card draws from equipped effects"""
        
        #  35	- Draw Cards				    # of Cards to draw
        c = 0
        
        for effect in self.effectList:
            if effect[0] == 35:
                c += effect[1]

        return c
        

    def rotateEffects(self):
        """Rotates the temporary effects and returns a sum"""
        
        a = [0,0,0]
        
        for b in self.tempEffects:
            a[0] += b[0]
            a[1] += b[1]
            a[2] += b[2]
                
        return a
        
        
    def expireEffects(self):
        """Processes effects that expire. Run at end of turn."""
        
        self.tempEffects.popleft()
        self.tempEffects.append([0,0,0])
        
    
    def addTempEffect(self, index, temptype, amount):
        """Adds temporary percentage based boosts."""

        if index == 1:
            alist = self.tempEffects.popleft()
            alist[temptype] += amount
            self.tempEffects.appendleft(alist)

        if index == 3:
            alist = self.tempEffects.pop()
            alist[temptype] += amount
            self.tempEffects.append(alist)



class Card:
    """Abstract class implementation of a card"""
    
    def __init__(self, cardID):
        """Looks up a card by ID from the SQL database, and loads the info"""
        
        
        cur.execute('SELECT * from CardList where ID=?', (cardID,))
        cardData = cur.fetchall()[0]

        self.ID = cardID
        self.type = cardData[1]
        
        self.name = cardData[2]
        self.description = cardData[3]
        
        self.rarity = cardData[5]
        self.family = bf(cardData[4]) # A sliceable integer class, where int[0] is the lower bit
        
        if type != 6:
            self.TP = cardData[6]
        
        if type == 2 or 3 or 4:
            self.HP = cardData[7]

        if type != 5 or 6:
            self.Att = cardData[8]
            self.Mag = cardData[10]

        if type == 2 or 3 or 4:
            self.Dfn = cardData[9]

        self.EffA = cardData[16]
        self.AQuan = cardData[17]
        
        if type == 5 or 6:
            self.EffB = cardData[18]
            self.BQuan = cardData[19]
        
        it type == 1 or 5 or 6:
            self.target = cardData[14]

        it type == 1:
            self.category = cardData[15]
        
        self.TPcost = cardData[13]
        
        
        # For the plaintext outputting
        
        self.typeString = ['Arte', 'Weapon', 'Armour', 'Accessory', 'Item', 'Recipe']
        self.arteCategories = ['Base', 'Master', 'Arcane', 'Novice', 'Intermediate', 'Advanced', 'Mystic']
        
        
        

    def description(self):
        """Returns a plaintext string containing a description of the card"""
        
        # Strings for artes
        if self.type == 1:
        
            '{5} {2}: {0}\n'
            '{1}\n'
            'Rarity: {8}\n'
            'TP Cost: {6}\n'
            'Physical Power: {3}\n'
            'Magical Power: {4}\n'
            'Families: {9}\n'
            'Effect: {7}'
            
            
            '.format(self.name,
                     self.description,
                     self.typeString[self.type-1],
                     self.Att,
                     self.Mag,
                     self.arteCategories[self.category],
                     self.TP,
                     self.effectString(self.EffA, self.AQuan),
                     self.rarityString(self.rarity),
                     self.familyString(self.family)
                     )
          
        # ToDo: all the other card types
                     
                     
    def effectString(self, effect, amount):
        """Returns a nice string for complicated effects"""

        # ToDo: add effect descriptions

        return 'ToDo'
        

    def rarityString(self, effect, amount):
        """Returns a nice string for rarity levels"""

        rarityStrings = ['Very Common', 'Common', 'Uncommon', 'Rare', 'Legendary']
        
        return rarityStrings[amount/20]


    def familyString(self, effect, amount):
        """Returns a nice string for mapped families"""

        familyStrings = ['Demon Fang', 'Sword Rain', 'Sonic Thrust', 'Swallow Kick',
        'Tiger Blade', 'Rising Falcon', 'Tempest', 'Beast', 'Light Spear', 'Raging Blast',
        'Crescent Strike', 'Azure Edge', 'Fang Blade', 'Physical Buffs', 'Guardian Moves',
        'Chi Healing', 'Shadow Rush', 'Talon Storm', 'Triple Kick', 'Eagle Dive', 
        '', '', '', '', '', '', '', '', '', '', '', '',
        'Basic Spells', 'Water Spells', 'Fire Spells', 'Lightning Spells', 'Earth Spells',
        'Wind Spells', 'Ice Spells', 'Gravity Spells', 'Light Spells', 'Dark Spells',
        'Pow Hammer', 'Healing Spells', 'Revival Spells', 'Debuffs', 'Status Buffs',
        'High Level Spells', 'Mid Level Spells']
        
        string = ''
        
        for bit in xrange(len(self.family)):
            if self.family[bit] == true:
                string += familyStrings[bit] + ', '
                
        return string[:-2]


    def effects(self):
        """Returns the effects in a nice list of lists"""
        
        returnList = []

        if self.EffA != None:
            returnList.append[self.EffA, self.AQuan]
        if self.EffB != None:
            returnList.append[self.EffB, self.BQuan]
            
        return returnList
    


class Deck:
    """Class representing a player deck, and it's current state."""
    
    def __init__(self, parent, player, deckNum):
        """Initializes the player, deck and characters, and draws
        the standard amount of cards for a hand"""
        
        # Persistant variables necessary for the game
        self.player = player
        self.cardList = deque([])
        self.hand = []
        
        self.characters = []
                
        self.stack = [[], []]
        self.parent = parent
        
        # Actions taken to fulfill the init
        self.loadDeck(deckNum)
        self.drawCards(7)
        

        
    def loadDeck(self, deckNum=1):
        """Loads a deck into the class"""
        
        # Get the player ID
        # ToDo: identification by registration info or hostmask?
        cur.execute('SELECT ID from PlayerList where Name=?', (self.player))
        
        PlayerID = cur.fetchall()[0]
        if PlayerID == None:
            parent.reply("Sorry, we couldn't find your name in the database.", GameRoom)
            
            # ToDo: figure out how to handle this scenario.
        
        
        # only the card IDs are necessary - pass it to the Card class
        # don't put in the type 0  character cards
        cur.execute('SELECT CardID from CardList where PID=? and Deck=?', (PlayerID,deckNum))
        cards = []
        characterTemp = []

        for x in cur.fetchall():
            card = Card(x[0])
            if card.type != 0:
                cards.append(card)
            else:
                characterTemp(card)
        
        cardID = characterTemp[0].ID
        cardIDb = characterTemp[1].ID
        
        # Now shuffle the cards randomly, and put them into the deck
        self.cardList = random.shuffle(cards)
                    
            
        # ToDo: Grab the characters from SQL, and put them into their boxes
                
        self.characters[0] = Character(cardID, self.parent.reply)
        self.characters[1] = Character(cardIDb, self.parent.reply)
        

    
    def drawCards(self, amount=1):
        """ Removes cards from the deck, and places them in the hand"""
        string = []
    
        for x in xrange(amount):
            card = self.cardList.popleft()
            self.hand.append(card)
            string.append(card.name())
            
            
        if len(string) == 1:
            return "Drew {0}.".format(string[0])
            
        elif len(string) == 2:
            return "Drew {0} and {1}.".format(string[0], string[1])
        
        else:
            return "Drew {0}and {1}.".format("".join(["%s, " % (k) for k in string[:-1]]), string[-1])
    
        
    def discard(self, card):
        """Removes cards from the hand, and places them at the 
        end of the deck"""
    
        self.hand.pop(self.hand.index(card))
        self.cardList.append(card)    
    
        
    def charNames(self):
        """Returns the character names in order as a list of strings."""
        
        return [self.characters[0].name(), self.characters[1].name()]


    def charDescriptions(self):
        """Returns the character descriptions in order as a list of strings."""
        
        return [self.characters[0].description(), self.characters[1].description()]

    
    def hurt(self, targetChar, modifier=0):
        """Returns the HP of the character, applying damage if necessary"""
    
        self.characters[targetChar].hurt(modifier)
        return self.characters[targetChar].currentHP()
        

    def heal(self, targetChar, modifier=0):
        """Returns the HP of the character, applying healing if necessary"""
    
        self.characters[targetChar].heal(modifier)
        return self.characters[targetChar].currentHP()
    
        
    def displayHand(self):
        """Returns a list of all cards in hand as strings"""
        
        handyList = []
        
        for card in self.hand:
            handyList.append(card.name())
         
        return handyList
        
        
    def cardInfo(self, cardName):
        """Returns a readable representation of the card info based on it's name"""
        
        cardID = self.cardLookup(cardName)
        
        card = Card(cardID)
        return card.description()        
        

    def addToStack(self, cardName, targetChar):
        """Adds an arte to execute to the stack"""
        
        cardID = self.cardLookup(cardName)

        card = Card(cardID)
        if self.characters[targetChar].arteCheck():
            self.stack[targetChar].append(card)
            

    def removeFromStack(self, cardName, targetChar):
        """Removes an arte to execute from the stack"""
        
        cardID = self.cardLookup(cardName)

        card = Card(cardID)
        try:
            self.stack[targetChar].remove(card)
            self.hand.append(card)
                        
        except:
            pass
        

    def useItem(self, cardName, target, user):
        """Uses an item card"""
    
        cardID = self.cardLookup(cardName)
        card = Card(cardID)
    
        if card.type != 5:
            return "{0} isn't an item".format(card.name())
        
        if user.currentTP() < card.TP:
            return "{0} doesn't have enough to TP to use that item".format(user.name())
        
        if (card.target != 5) and (target == None):
            return "You need to say who to use it on."
        
        if card.target == 6:
            for handCard in self.hand:
                if target == handCard.name():
                    target = handCard

        if (card.target == 6) and (target == None):
            return "You need to say which card to use it on."
        
        user.modifyTP(-(card.TP))
        self.hand.discard(card)
        
        returnString = []
        # Processes effects
        for effect in card.effects():            
            
            # Heal One
            if effect[0] == 1:
                result = target.heal(effect[1])
                returnString.append("{0} was healed to {1}.".format(target.name(), result))

            # Heal All
            if effect[0] == 2:
                resultA = self.character[0].heal(effect[1])
                resultB = self.character[1].heal(effect[1])
                returnString.append("{0} was healed to {1} and {1} was healed to {2}.".format(self.character[0].name(), resultA, self.character[1].name(), resultB))

            # TP add One
            if effect[0] == 5:
                result = target.modifyTP(effect[1])
                returnString.append("{0} gained {1} extra TP.".format(target.name(), effect[1]))

            # TP add All
            if effect[0] == 6:
                self.character[0].modifyTP(effect[1])
                self.character[1].modifyTP(effect[1])
                returnString.append("{0} and {1} both gained {2} extra TP.".format(self.character[0].name(), self.character[1].name(), effect[1]))
                
            # Revive
            if effect[0] == 24:
                target.revive()
                returnString.append("{0} was revived.".format(target.name()))

            # AllDivide
            if effect[0] == 29:
                pass
                # ToDo: All divide

            # SkipTurn
            if effect[0] == 33:
                # ToDo: Skip Turn

            # Draw Cards
            if effect[0] == 35:
                returnString.append(self.drawCards(effect[1]))

            # Ends own turn
            if effect[0] == 39:
                self.parent.end_turn()

            # Reveals Enemy hand
            if effect[0] == 43:
                currentDeck = self.parent.players.index(self.parent.turn)
                if currentDeck == 1:
                    deckIndex = 0
                else:
                    deckIndex = 1
                hand = self.parent.decks[deckIndex].displayHand()
            
                if len(hand) == 1:
                    temp = "{1} has just {0} in his hand.".format(hand[0], self.parent.players[deckIndex])
                    
                elif len(hand) == 2:
                    temp = "{2} has {0} and {1}.".format(hand[0], hand[1], self.parent.players[deckIndex])
                
                else:
                    temp = "{2} has {0}and {1}.".format("".join(["%s, " % (k) for k in hand[:-1]]), hand[-1], self.parent.players[deckIndex])
            
                returnString.append(temp)

            # Rune Bottle
            if effect[0] == 44:
                # ToDo: Rune bottle effect
                
                                      
        return "".join(["%s\n" % (k) for k in returnString])
    
    
    def useRecipe(self, cardName, target):
        """Uses a recipe card"""
    
        cardID = self.cardLookup(cardName)
        card = Card(cardID)
    
        if card.type != 6:
            return "{0} isn't a recipe".format(card.name())
                
        if (card.target != 5) and (targetChar == None):
            return "You need to say who to use it on."
                
        self.hand.discard(card)
        
        returnString = []
        # Processes effects
        for effect in card.effects():            
            
            # Heal One
            if effect[0] == 1:
                result = target.heal(effect[1])
                returnString.append("{0} was healed to {1}.".format(target.name(), result))

            # Heal All
            if effect[0] == 2:
                resultA = self.character[0].heal(effect[1])
                resultB = self.character[1].heal(effect[1])
                returnString.append("{0} was healed to {1} and {1} was healed to {2}.".format(self.character[0].name(), resultA, self.character[1].name(), resultB))

            # TP add One
            if effect[0] == 5:
                result = target.modifyTP(effect[1])
                returnString.append("{0} gained {1} extra TP.".format(target.name(), effect[1]))

            # TP add All
            if effect[0] == 6:
                self.character[0].modifyTP(effect[1])
                self.character[1].modifyTP(effect[1])
                returnString.append("{0} and {1} both gained {2} extra TP.".format(self.character[0].name(), self.character[1].name(), effect[1]))
                
            # Att+ 1 turn to allies
            if effect[0] == 12:
                target.addAttackEffect(1, 0, effect[1])

            # Def+ 1 turn to allies
            if effect[0] == 17:
                target.addDefenseEffect(1, 1, effect[1])

            # Mag+ 1 turn to allies
            if effect[0] == 22:
                target.addMagicEffect(1, 2, effect[1])

            # Revive
            if effect[0] == 24:
                target.revive()
                returnString.append("{0} was revived.".format(target.name()))

            # Draw Cards
            if effect[0] == 35:
                returnString.append(self.drawCards(effect[1]))
                
                                      
        return "".join(["%s\n" % (k) for k in returnString])
    

    def useEquip(self, cardName, target):
        """Uses an equip card"""
    
        cardID = self.cardLookup(cardName)
        card = Card(cardID)

        if card.type != 2 or 3 or 4:
            return "{0} isn't equipment".format(card.name())
                
        if not target.equipCheck(card):
            return "{0} can't equip that!".format(target.name())
 
        if target.currentTP() < card.TP:
            return "{0} doesn't have enough to TP to use that item".format(user.name())


        target.modifyTP(-4)
        self.hand.discard(card)
        target.equip(card)
        
        return "{0} equipped.".format(card.name())

    
    def useArte(self, cardName, targetChar, userChar):
        """Uses an arte or combo immediately"""
    
        cardID = self.cardLookup(cardName)
        card = Card(cardID)



    def getCharacter(self, charName):
        """Returns a character class from a name."""
        
        for char in self.characters:
            if char.name() == charName:
                return char


    def getCardDraws(self):
        """Returns the amount of cards to draw at the beginning of a turn"""
        
        c = 1
        for char in self.characters:
            c += char.cardDraws()
            
        return c
        

    def cardLookup(self, cardName):
    
        pass
        
        cur.execute('SELECT ID from CardList where Name=?', (cardName,))
        cardData = cur.fetchall()
        
        if cardData = []:
            print "Card lookup for {0} failed.".format(cardName)
            # ToDo: handle failure case better
            return 0
        else:
            return cardData[0][0]

        
        
        
        
class bf(object):
    def __init__(self,value=0):
        self._d = value

    def __getitem__(self, index):
        return (self._d >> index) & 1 

    def __setitem__(self,index,value):
        value    = (value&1L)<<index
        mask     = (1L)<<index
        self._d  = (self._d & ~mask) | value

    def __getslice__(self, start, end):
        mask = 2L**(end - start) -1
        return (self._d >> start) & mask

    def __setslice__(self, start, end, value):
        mask = 2L**(end - start) -1
        value = (value & mask) << start
        mask = mask << start
        self._d = (self._d & ~mask) | value
        return (self._d >> start) & mask

    def __int__(self):
        return self._d

    def __len__(self):
        if self._d == 0:
            return 0
            
        return int(log(self._d, 2)) + 1
    
    def __iter__(self):
        return self
    
    def next(self):
        if self._d == 0:
            raise StopIteration
        
        returning = self._d AND 1
        self._d = self._d >> 1

        return returning
        
