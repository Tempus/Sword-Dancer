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


        # Effect list. Format: EffectID, Effect Amount, ExpiryDate, EquipAttach (0 is none, 2 is weapon, 3 armour, 4 accessory)
        self.effectList = []
        
        # Equipment list. Format: TP, HP, Att, Def, Mag
        self.weapon = [0,0,0,0,0]
        self.armour = [0,0,0,0,0]
        self.accessory = [0,0,0,0,0]
        
        
        
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
    
    def heal(self, modifier):
        """Modifies the current HP by a multipler/100"""
        
        self.currentHP = self.currentHP * (1 + (modifier/100))
        if self.currentHP > (self.HP + self.weapon[2] + self.armor[2] + self.accessory[2]):
            self.currentHP = (self.HP + self.weapon[2] + self.armor[2] + self.accessory[2])
            
    def currentHP(self):
        """Returns the currentHP"""

        return self.currentHP
        
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
            
        if self.equip[len(card.family) - 1] != True:
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
        
        
        

    # ToDo: apply effects to characters
    # ToDo: turnly effect resolutions
    # ToDo: checks for characters artes



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


class Deck:
    """Class representing a player deck, and it's current state."""
    
    def __init__(self, player, deckNum):
        """Initializes the player, deck and characters, and draws
        the standard amount of cards for a hand"""
        
        # Persistant variables necessary for the game
        self.player = player
        self.cardList = deque([])
        self.hand = []
        
        self.charOne = None
        self.charTwo = None
        
        
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
        
        self.charOne = Character(cardID)
        self.charTwo = Character(cardIDb)
        

    
    def drawCards(self, amount=1):
        """ Removes cards from the deck, and places them in the hand"""
    
        for x in xrange(amount):
            self.hand.append(self.cardList.popleft())
    
    
    def discard(self, card):
        """Removes cards from the hand, and places them at the 
        end of the deck"""
    
        self.hand.pop(self.hand.index(card))
        self.cardList.append(card)    
    
        
    def charNames(self):
        """Returns the character names in order as a list of strings."""
        
        return [self.charOne.name(), self.charTwo.name()]


    def charDescriptions(self):
        """Returns the character descriptions in order as a list of strings."""
        
        return [self.charOne.description(), self.charTwo.description()]


    
    def hurtA(self, modifier=0):
        """Returns the HP of the first character, applying damage if necessary"""
    
        self.charOne.hurt(modifier)
        return self.charOne.currentHP()
    
    
    def hurtB(self, modifier=0):
        """Returns the HP of the second character, applying damage if necessary"""

        self.charTwo.hurt(modifier)
        return self.charTwo.currentHP()


    def healA(self, modifier=0):
        """Returns the HP of the first character, applying healing if necessary"""
    
        self.charOne.heal(modifier)
        return self.charOne.currentHP()
    
    
    def healB(self, modifier=0):
        """Returns the HP of the second character, applying healing if necessary"""

        self.charTwo.heal(modifier)
        return self.charTwo.currentHP()

    
    def displayHand(self):
        """Returns a list of all cards in hand as strings"""
        
        handyList = []
        
        for card in self.hand:
            handyList.append(card.name())
         
        return handyList
        
        
    def cardInfo(self, cardName):
        """Returns a readable representation of the card info based on it's name"""
        
        # SQL lookup for card name
        
        
        card = Card(cardID)
        return card.description()        
        
        
        
        
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
        
