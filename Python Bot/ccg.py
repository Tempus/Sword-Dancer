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


class Character:
    """Character card class"""
    
    def __init__(self, cardID):
        """Looks up a character by ID from the SQL database, and loads the info"""
        
        
        # ToDo: Load card from database


        self.type = 0
        
        self.name = ''
        self.description = ''
        
        self.rarity = 1
        self.equip = bf() # A sliceable integer class, where int[0] is the lower bit
        self.artes = bf() # A sliceable integer class, where int[0] is the lower bit

        self.TP = None * (Level/100 + 1)
        self.HP = None * (Level/100 + 1)
        self.Att = None * (Level/100 + 1)
        self.Mag = None * (Level/100 + 1)
        self.Dfn = None * (Level/100 + 1)
        
        self.currentHP = self.HP
        self.currentTP = self.TP
        

        # Effect list. Format: EffectID, Effect Amount, ExpiryDate, EquipAttach (0 is none, 2 is weapon, 3 armour, 4 accessory)
        self.effectList = []
        
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
        
        self.currentHP += modifier
        if self.currentHP < 0:
            self.currentHP = 0
            self.ko = true
        
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

        # ToDo: apply effects
        
        stats = [self.TP + self.weapon[0] + self.armor[0] + self.accessory[0],
                 self.HP + self.weapon[1] + self.armor[1] + self.accessory[1],
                 self.Att + self.weapon[2] + self.armor[2] + self.accessory[2],
                 self.Dfn + self.weapon[3] + self.armor[3] + self.accessory[3],
                 self.Mag + self.weapon[4] + self.armor[4] + self.accessory[4]]
                 
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
            if effectList[x][3] == card.type:
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
            effectList.append([card.EffA, card.AQuan, -1, card.type])
        
        
    def arteCheck(self, card):
        """Checks to see if an arte can be used"""
        
        if card.type != 1:
            return False
            
        if self.artes[len(card.family) - 1] == True:
            return True
    
        return False


    def applyEffect(self, card):
        """Applies effects from a card"""

#        if card.type != 1 or 5 or 6:
#            return
#        
#        if card.EffA > 0:
#            if card.EffA == 10 or 12 or 15 or 17 or 20 or 22:
#                duration = 1
#            if card.EffA == 11 or 13 or 16 or 18 or 21 or 23:
#                duration = 3
#                
#            effectList.append([card.EffA, card.AQuan, duration, 0])
#
#        try:
#            if card.EffB > 0:
#                if card.EffB == 10 or 12 or 15 or 17 or 20 or 22:
#                    duration = 1
#                if card.EffB == 11 or 13 or 16 or 18 or 21 or 23:
#                    duration = 3
#
#                effectList.append([card.EffB, card.BQuan, duration, 0])

    # ToDo: apply effects to characters
    # ToDo: turnly effect resolutions




class Card:
    """Abstract class implementation of a card"""
    
    def __init__(self, cardID):
        """Looks up a card by ID from the SQL database, and loads the info"""
        
        
        # ToDo: Load card from database
        
        self.type = 1
        
        self.name = ''
        self.description = ''
        
        self.rarity = 1
        self.family = bf() # A sliceable integer class, where int[0] is the lower bit
        
        if type != 6:
            self.TP = None
        
        if type == 2 or 3 or 4:
            self.HP = None

        if type != 5 or 6:
            self.Att = None
            self.Mag = None

        if type == 2 or 3 or 4:
            self.Dfn = None

        self.EffA = None
        self.AQuan = None
        
        if type == 5 or 6:
            self.EffB = None
            self.BQuan = None
        
        it type == 1 or 5 or 6:
            self.target = None

        it type == 1:
            self.category = None
        
        
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
        
        # ToDo: Pull a cardlist from SQL here
        # only the card IDs are necessary - pass it to the Card class
        # don't put in the type 0  character cards
        cards = []
        
        
        # Now shuffle the cards randomly, and put them into the deck
        for x in xrange(len(cards)):
            card = random.choice(cards)
            self.cardList.append(card)
            cards.pop(cards.index(card))
            
            
        # ToDo: Grab the characters from SQL, and put them into their boxes
        
        self.cOneHP = 0
        self.cTwoHP = 0
        
        self.characters[0] = Character(cardID)
        self.characters[1] = Character(cardIDb)
        

    
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
        

    def useItem(self, cardName, targetChar, userChar):
        """Uses an item card"""
    
        cardID = self.cardLookup(cardName)
        card = Card(cardID)
    
        if card.type != 5:
            return "{0} isn't an item".format(card.name())
    
        for char in self.characters:
            if char.name() == targetChar:
                target = char
            if char.name() == userChar:
                user = char
    
        if user.currentTP() < card.TP:
            return "{0} doesn't have enough to TP to use that item".format(user.name())
        
        if (card.target != 5) and (targetChar == None):
            return "You need to say who to use it on."
        
        if card.target == 6:
            for handCard in self.hand:
                if targetChar == handCard.name():
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
                self.parent.decks = 
            
                returnString.append(self.parent.)

            #
            if effect[0] == 44:
                               
        return "".join(["%s\n" % (k) for k in returnString])
    
    def useRecipe(self, cardName, targetChar):
        """Uses a recipe card"""
    
        cardID = self.cardLookup(cardName)
        card = Card(cardID)
    

    def useEquip(self, cardName, targetChar):
        """Uses an equip card"""
    
        cardID = self.cardLookup(cardName)
        card = Card(cardID)

    
    def useArte(self, cardName, targetChar, userChar):
        """Uses an arte or combo immediately"""
    
        cardID = self.cardLookup(cardName)
        card = Card(cardID)




    def cardLookup(self, cardName):
    
        pass
        
        #ToDo: the function ^_^
        # return cardID

    def processEffect(self ):
        
        # ToDo: make a function that processes new effects if passed
        #       and processes all the old effects if not?
        
        
        
        
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
        
