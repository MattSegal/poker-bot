"""
consider making a new class to hold all the .img files ... or not
store all info in csv files, and get classes to rip from there - this module looks gross

add general info (pot, community cards) to TableInfo
"""

class TableInfo:
    def __init__(self,numPlayers,heroNum):
        self.__name__ = 'TableInfo'
        # works for 2-6 players
        self.numPlayers = numPlayers
        self.heroNum    = heroNum
        if heroNum == 1:
            self.one    = PlayerInfo('hero')
        else:
            self.one    = PlayerInfo('villain')
        if numPlayers > 1 and heroNum == 2:
            self.two    = PlayerInfo('hero')
        elif numPlayers > 1:
            self.two    = PlayerInfo('villain')
        else:
            self.two    = None
        if numPlayers > 2 and heroNum == 3:
            self.three  = PlayerInfo('hero')
        elif numPlayers > 2:
            self.three  = PlayerInfo('villain')
        else:
            self.three  = None
        if numPlayers > 3 and heroNum == 4:
            self.four   = PlayerInfo('hero')
        elif numPlayers > 3:
            self.four   = PlayerInfo('villain')    
        else:
            self.four   = None
        if numPlayers > 4 and heroNum == 5:
            self.five   = PlayerInfo('hero')
        elif numPlayers > 4:
            self.five   = PlayerInfo('villain')
        else:
            self.five   = None
        if numPlayers > 5 and heroNum == 6:
            self.six    = PlayerInfo('hero')
        elif numPlayers > 5:
            self.six    = PlayerInfo('villain')
        else:
            self.six    = None
        # ===== for __getitem__ ===== #
        self.tableList = [self.one,self.two,self.three,self.four,self.five,self.six]
        self.keyList = ['one','two','three','four','five','six']
    def __getitem__(self,key):
        
        for i in range(self.numPlayers):
            if key == self.keyList[i]:
                return self.tableList[i]
        
class PlayerInfo:
    def __init__(self,playerType):
        self.playerType = playerType    # player is hero or villain
        self.hasButton      = None  # boolean
        self.hasHoleCards   = None  # bool
        self.isAllIn        = None  # bool
        self.isSittingOut   = None  # bool
        self.isPlaying      = None  # bool
        self.stack          = None  # integer value of stack
        self.bet            = None  # integer value of bet
        #if playerType == 'villain':
        self.handAction = None      # string - bet, fold, check, raise
        self.hasCards   = None      # boolean
        #if playerType == 'hero':
        self.holeOne    = None      # tuple of 1st hole card (value,suit) value is 2 (2) to 14 (A), suit is of [H,D,C,S]
        self.holeTwo    = None      # 2nd hole card
        self.seatNum    = None      # number of seat (1 to 6)

        # ===== for __getitem__ ===== #
        self.tableList = [self.playerType,
                         self.hasButton,
                         self.stack,
                         self.bet]
        self.keyList = ['playerType',
                       'hasButton',
                       'stack',
                       'bet']
        if self.playerType == 'hero':
            self.tableList += [self.holeOne,self.holeTwo,self.seatNum]
            self.keyList += ['holeOne','holeTwo','seatNum']
        else:
            self.tableList += [self.handAction,self.hasCards]
            self.keyList += ['handAction','hasCards']
    def __getitem__(self,key):
        for i in range(len(self.keyList)):
            if key == self.keyList[i]:
                return self.tableList[i]


class Region():
    def __init__(self,location,width,height):
        self.__name__ = 'Region'
        self.loc = location
        self.w = width
        self.h = height
        self.img = None        

class PlayerReg():
    def __init__(self,playerNum):
        """
        each player has a:
            stack
            name
            cards
            bet
            dealerChip
            holeOne
            holeTwo
            holdCheck
        """
        self.__name__ = 'PlayerReg'
        # dimensions of regions in pixels
        nameWidth       = 87       # wiggle room, reference top right of box
        nameHeight      = 18        # tight
        stackWidth      = 87       # wiggle room, reference top right of box
        stackHeight     = 17        # tight
        cardsWidth      = 27        # tight
        cardsHeight     = 32        # tight
        holeWidth       = 13        # tight
        holeHeight      = 33        # tight
        bubbleHeight    = 34        # fuzzy for now
        bubbleWidth     = 48        # fuzzy for now
        dealerHeight    = 22        # tight
        dealerWidth     = 24        # tight
        holeCheckWidth  = 13
        holeCheckHeight = 13
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
            bubbleLoc       = (42,174)          # fuzzy for now
            dealerLoc       = (112,188)         # fuzzy for now     
            holeCheckLoc    = (89,172)

        elif playerNum == 2:
            nameLoc         = (249,26)
            stackLoc        = (268,26)
            cardsLoc        = (202,137)
            betLoc          = (156,181)
            holeOneLoc      = (179,52)
            holeTwoLoc      = (185,70)
            bubbleLoc       = (42,174)          # player 1
            dealerLoc       = (236,129)
            holeCheckLoc    = (236,48)

        elif playerNum == 3:
            nameLoc         = (352,244)
            stackLoc        = (371,244) 
            cardsLoc        = (277,221)
            betLoc          = (279,266)
            holeOneLoc      = (334,176)
            holeTwoLoc      = (338,194)
            bubbleLoc       = (42,174)          # player 1 
            dealerLoc       = (307,257)
            holeCheckLoc    = (390,172)
            
        elif playerNum == 4:
            nameLoc         = (352,463)
            stackLoc        = (371,463)
            cardsLoc        = (277,540)
            betLoc          = (279,383)
            holeOneLoc      = (331,564)
            holeTwoLoc      = (338,582)
            bubbleLoc       = (42,174)          # player 1 
            dealerLoc       = (284,585)
            holeCheckLoc    = (390,559)
            
        elif playerNum == 5:
            nameLoc         = (249,680)
            stackLoc        = (268,680)
            cardsLoc        = (202,614)
            betLoc          = (156,533)
            holeOneLoc      = (179,688)
            holeTwoLoc      = (183,706)
            bubbleLoc       = (42,174)          # player 1 
            dealerLoc       = (169,630)
            holeCheckLoc    = (177,744) 
            
        elif playerNum == 6:
            nameLoc         = (11,463)  
            stackLoc        = (30,463)
            cardsLoc        = (104,540)
            betLoc          = (121,393)
            holeOneLoc      = (30,564)
            holeTwoLoc      = (35,582) 
            bubbleLoc       = (42,174)          # player 1 
            dealerLoc       = (83,494)
            holeCheckLoc    = (31,618)
        

        self.name       = Region(nameLoc,       nameWidth,      nameHeight)
        self.stack      = Region(stackLoc,      stackWidth,     stackHeight)
        self.cards      = Region(cardsLoc,      cardsWidth,     cardsHeight)
        self.bet        = Region(betLoc,        betWidth,       betHeight)
        self.holeOne    = Region(holeOneLoc,    holeWidth,      holeHeight)
        self.holeTwo    = Region(holeTwoLoc,    holeWidth,      holeHeight)
        self.bubble     = Region(bubbleLoc,     bubbleWidth,    bubbleHeight)
        self.dealer     = Region(dealerLoc,     dealerWidth,    dealerHeight)
        self.holeCheck  = Region(holeCheckLoc,  holeCheckWidth, holeCheckHeight)

        # ===== for __getitem__ ===== #
        self.tableList = [self.name,self.stack,self.cards,self.bet,self.holeOne,self.holeTwo,self.bubble,self.dealer,self.holeCheck]
        self.keyList = ['name','stack','cards','bet','holeOne','holeTwo','bubble','dealer','holeCheck']
    def __getitem__(self,key):  
        for i in range(len(self.keyList)):
            if key == self.keyList[i]:
                return self.tableList[i]


class TableReg():
    def __init__(self,numPlayers):
        self.__name__ = 'TableReg'
        # ===== player specific regions ===== #
        # works for 2-6 players
        self.one    = PlayerReg(1)
        self.two    = PlayerReg(2)
        if numPlayers > 2:
            self.three  = PlayerReg(3)
        else:
            self.three = None
        if numPlayers > 3:
            self.four   = PlayerReg(4)
        else:
            self.four = None
        if numPlayers > 4:
            self.five   = PlayerReg(5)
        else:
            self.five = None
        if numPlayers > 5:
            self.six   = PlayerReg(6)
        else:
            self.six = None
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
