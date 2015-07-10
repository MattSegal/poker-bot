"""
store all info in csv files, and get classes to rip from there - this module looks gross

add general info (pot, community cards) to TableInfo
"""
import numpy as np

class TableInfo:
    def __init__(self,numPlayers):
        self.__name__   = 'TableInfo'
        self.pot        = None
        self.flopOne    = None
        self.flopTwo    = None
        self.flopThree  = None
        self.turn       = None
        self.river      = None
        # works for 2-6 players
        self.numPlayers = numPlayers
        self.heroSeat   = None

        self.one    = PlayerInfo() if numPlayers>0 else  None
        self.two    = PlayerInfo() if numPlayers>1 else  None
        self.three  = PlayerInfo() if numPlayers>2 else  None
        self.four   = PlayerInfo() if numPlayers>3 else  None
        self.five   = PlayerInfo() if numPlayers>4 else  None
        self.six    = PlayerInfo() if numPlayers>5 else  None

        # ===== for __getitem__ ===== #
        self.tableList = [self.one,self.two,self.three,self.four,self.five,self.six]
        self.keyList = ['one','two','three','four','five','six']
	self.keyListDigit = [0,1,2,3,4,5,6]
    def __getitem__(self,key):
        
        for i in range(self.numPlayers):
	    if key == self.keyList[i] or key == self.keyListDigit[i]:
                return self.tableList[i]

# =============================================================================== #
        
class PlayerInfo:
    def __init__(self):
        self.isHero         = None  # player is hero or villain
        self.hasButton      = None  # boolean
        self.hasHoleCards   = None  # bool
        self.isAllIn        = None  # bool
        self.isSittingOut   = None  # bool
        self.isPlaying      = None  # bool
        self.stack          = None  # integer value of stack
        self.bet            = None  # integer value of bet
        self.hasCards       = None  # boolean, villain only
        self.holeOne        = None  # tuple of 1st hole card (value,suit) value is 2 (2) to 14 (A), suit is of [H,D,C,S]
        self.holeTwo        = None  # 2nd hole card

# =============================================================================== #

class Region():
    def __init__(self,location,width,height):
        self.__name__ = 'Region'
        self.loc = location
        self.w = width
        self.h = height
        self.img = None        

# =============================================================================== #

class PlayerReg():
    def __init__(self,playerNum):
        """table image regions for each player"""
        self.__name__ = 'PlayerReg'
        
        playerLoc = np.genfromtxt('playerLocations.csv', delimiter=',')
        playerLoc = playerLoc[playerNum-1,1:].astype('int32')
        
        self.name       = Region((playerLoc[0], playerLoc[1]),  playerLoc[2],  playerLoc[3])
        self.stack      = Region((playerLoc[4], playerLoc[5]),  playerLoc[6],  playerLoc[7])
        self.cards      = Region((playerLoc[8], playerLoc[9]),  playerLoc[10], playerLoc[11]) 
        self.holeOne    = Region((playerLoc[12],playerLoc[13]), playerLoc[14], playerLoc[15])
        self.holeTwo    = Region((playerLoc[16],playerLoc[17]), playerLoc[18], playerLoc[19])
        self.dealer     = Region((playerLoc[20],playerLoc[21]), playerLoc[22], playerLoc[23])
        self.bet        = Region((playerLoc[24],playerLoc[25]), playerLoc[26], playerLoc[27])
        # ===== for __getitem__ ===== #
        self.tableList = [self.name,self.stack,self.cards,self.holeOne,self.holeTwo,self.dealer,self.bet]
        self.keyList = ['name','stack','cards','holeOne','holeTwo','dealer','bet']
    def __getitem__(self,key):  
        for i in range(len(self.keyList)):
            if key == self.keyList[i]:
                return self.tableList[i]
            
# =============================================================================== #

class TableReg():
    def __init__(self,numPlayers):
        self.__name__ = 'TableReg'
        self.numPlayers = numPlayers
        # ===== player specific regions ===== #
        # works for 2-6 players
        
        self.one    = PlayerReg(1) if numPlayers>0 else  None
        self.two    = PlayerReg(2) if numPlayers>1 else  None
        self.three  = PlayerReg(3) if numPlayers>2 else  None
        self.four   = PlayerReg(4) if numPlayers>3 else  None
        self.five   = PlayerReg(5) if numPlayers>4 else  None
        self.six    = PlayerReg(6) if numPlayers>5 else  None
  
        # community regions
        """
        community regions are:
        pot
        flopOne
        flopTwo
        flopThree
        turn
        river
        foldButton
        checkButton
        betButton
        """
        comCardHeight       = 33
        comCardWidth        = 13
        potWidth            = 115
        potHeight           = 17
        foldButtonHeight    = 37
        foldButtonWidth     = 92 
        checkButtonHeight   = foldButtonHeight
        checkButtonWidth    = foldButtonWidth
        betButtonHeight     = 46
        betButtonWidth      = 113
        
        potLoc              = (16,337)
        # community cards
        flopOneLoc      = (157,269)
        flopTwoLoc      = (157,323)
        flopThreeLoc    = (157,377)   
        turnLoc         = (157,431)
        riverLoc        = (157,485)
        # buttons
        foldButtonLoc   = (497,406)
        checkButtonLoc  = (497,542)
        betButtonLoc    = (492,660)

        self.pot            = Region(potLoc,        potWidth,           potHeight)
        self.flopOne        = Region(flopOneLoc,    comCardWidth,       comCardHeight)
        self.flopTwo        = Region(flopTwoLoc,    comCardWidth,       comCardHeight)
        self.flopThree      = Region(flopThreeLoc,  comCardWidth,       comCardHeight)
        self.turn           = Region(turnLoc,       comCardWidth,       comCardHeight)
        self.river          = Region(riverLoc,      comCardWidth,       comCardHeight)
        self.foldButton     = Region(foldButtonLoc, foldButtonWidth,    foldButtonHeight)
        self.checkButton    = Region(checkButtonLoc,checkButtonWidth,   checkButtonHeight)
        self.betButton      = Region(betButtonLoc,  betButtonWidth,     betButtonHeight)
        # ===== for __getitem__ ===== #
        self.tableList = [self.one,
                         self.two,
                         self.three,
                         self.four,
                         self.five,
                         self.six,
                         self.pot,
                         self.flopOne,
                         self.flopTwo,
                         self.flopThree,
                         self.turn,
                         self.river,
                         self.foldButton,
                         self.checkButton,
                         self.betButton]
        self.keyList = ['one',
                       'two',
                       'three',
                       'four',
                       'five',
                       'six',
                       'pot',
                       'flopOne',
                       'flopTwo',
                       'flopThree',
                       'turn',
                       'river',
                       'foldButton',
                       'checkButton',
                       'betButton']
        
    def __getitem__(self,key):
        for i in range(len(self.keyList)):
            if key == self.keyList[i]:
                return self.tableList[i]

# =============================================================================== #

"""
        nameWidth       = 87       # wiggle room, reference top right of box
        nameHeight      = 18        # tight
        stackWidth      = 87       # wiggle room, reference top right of box
        stackHeight     = 17        # tight
        cardsWidth      = 27        # tight
        cardsHeight     = 32        # tight
        holeWidth       = 13        # tight
        holeHeight      = 33        # tight
        dealerHeight    = 22        # tight
        dealerWidth     = 24        # tight
        if playerNum == 2 or playerNum == 5:
            betWidth    = 82        # fuzzy for now     
            betHeight   = 91
        else:
            betWidth    = 160      
            betHeight   = 26        
       
        if playerNum == 1:
            nameLoc         = (11,242)
            stackLoc        = (30,242)   
            cardsLoc        = (104,221)
            betLoc          = (121,267)         # fuzzy for now
            holeOneLoc      = (33,176)
            holeTwoLoc      = (37,194)
            dealerLoc       = (112,188)           

        elif playerNum == 2:
            nameLoc         = (249,26)
            stackLoc        = (268,26)
            cardsLoc        = (202,137)
            betLoc          = (156,181)
            holeOneLoc      = (179,52)
            holeTwoLoc      = (185,70)
            dealerLoc       = (236,129)
            holeCheckLoc    = (236,48)

        elif playerNum == 3:
            nameLoc         = (352,244)
            stackLoc        = (371,244) 
            cardsLoc        = (277,221)
            betLoc          = (279,266)
            holeOneLoc      = (334,176)
            holeTwoLoc      = (338,194)
            dealerLoc       = (307,257)
            holeCheckLoc    = (390,172)
            
        elif playerNum == 4:
            nameLoc         = (352,463)
            stackLoc        = (371,463)
            cardsLoc        = (277,540)
            betLoc          = (279,383)
            holeOneLoc      = (331,564)
            holeTwoLoc      = (338,582)
            dealerLoc       = (284,585)
            
        elif playerNum == 5:
            nameLoc         = (249,680)
            stackLoc        = (268,680)
            cardsLoc        = (202,614)
            betLoc          = (156,533)
            holeOneLoc      = (179,688)
            holeTwoLoc      = (183,706)
            dealerLoc       = (169,630)
            
        elif playerNum == 6:
            nameLoc         = (11,463)  
            stackLoc        = (30,463)
            cardsLoc        = (104,540)
            betLoc          = (121,393)
            holeOneLoc      = (30,564)
            holeTwoLoc      = (35,582) 
            dealerLoc       = (83,494)
"""
