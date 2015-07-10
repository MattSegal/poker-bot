import numpy as np

# project imports
from inputElements import TableReg
from inputElements import TableInfo
from classImg import classifyImage
from classImg import classifyMultiImage
from processImage import processImage
from plotFigure import plotFigure

def readElements(tableInfo,tableReg):
    """
    reads information from table element images and returns it 
    raw information is info straight from the images
    meta information is derived from raw info
    this module currently passes all info to brain - may be possible to hide info later
    """
    numPlayers  = tableInfo.numPlayers
    InfoKeyList = tableInfo.keyList

    # ===== raw table information ===== #
    
    pot = readPot(tableReg)
    commCards   = readCommCards(tableReg)
    heroAction  = detectHeroAction(tableReg)

    tableInfo.pot           = pot
    tableInfo.flopOne       = commCards[0]
    tableInfo.flopTwo       = commCards[1]
    tableInfo.flopThree     = commCards[2]
    tableInfo.turn          = commCards[3]
    tableInfo.river         = commCards[4]
    tableInfo.heroAction    = heroAction

    # =====  raw player information ===== #
    for p in range(numPlayers):
        playerName  = InfoKeyList[p]
        playerReg   = tableReg[playerName]

        hasCards = checkCards(playerReg)
        hasButton = checkButton(playerReg)
        (stack,isSittingOut,isAllIn,isNoPlayer) = readStack(playerReg)
        (hasHoleCards,valOne,valTwo,suitOne,suitTwo) = readHoleCards(playerReg)
       	betSize = readBet(playerReg,p)
	if not isNoPlayer:
	    isHero	= checkHero(playerReg)
	else:
	    isHero	= False
		

	tableInfo[playerName].isHero  	    = isHero
        tableInfo[playerName].hasHoleCards  = hasHoleCards 
        tableInfo[playerName].isAllIn       = isAllIn
        tableInfo[playerName].isSittingOut  = isSittingOut
	tableInfo[playerName].isNoPlayer    = isNoPlayer
        tableInfo[playerName].hasCards      = hasCards
        tableInfo[playerName].hasButton     = hasButton
        tableInfo[playerName].stack         = stack
        tableInfo[playerName].holeOne       = (valOne,suitOne)
        tableInfo[playerName].holeTwo       = (valTwo,suitTwo)
	tableInfo[playerName].bet	    = betSize

	

    # ===== meta information ===== #
    
    # implemented
    # street	    - int value for street of play [0,1,2,3] is [pre,flop,turn,river]
    # inHandArr	    - seat numbers of players in hand, ordered from BU to UTG
    # isPlaying	    - is a given player in the hand
    # heroSeat	    - seat number of hero (starts at 0)
    # buttonSeat    - seat number of button (starts at 0)

    # to do
    # handRank	    - how good is your hand (consider elsewhere)
    # bigBlind	    - value of big blind
    # action	    - array of action so far
    # callReq	    - 0 for check, 1+ for how much you need to call
    # minBet	    - minimum bet allowed

    # ===== meta player info ===== #
    maxBet = 0 
    for p in range(numPlayers):
	isPlaying = (tableInfo[p].hasCards + tableInfo[p].hasHoleCards)*(not tableInfo[p].isSittingOut)*(not tableInfo[p].isNoPlayer)
	tableInfo[p].isPlaying     = isPlaying

	# number of hero (starts at 0)
	if tableInfo[p].isHero:
	    tableInfo.heroSeat = p
	    tableInfo.heroBet = tableInfo[p].bet
	# number of button (starts at 0)
	if tableInfo[p].hasButton:
	    tableInfo.buttonSeat = p
	if tableInfo[p].bet > maxBet:
	    maxBet = tableInfo[p].bet
    tableInfo.maxBet = maxBet

    # ===== meta table info ===== #
	
    # street of play
    commCardList = [tableInfo.flopOne,tableInfo.flopTwo,tableInfo.flopThree,tableInfo.turn,tableInfo.river]
    isFlop = tableInfo.flopOne[0] != None
    isTurn = tableInfo.turn[0] != None
    isRiver = tableInfo.river[0] != None

    if isFlop and isTurn == False:
	street = 1 # flop
    elif isFlop and isTurn and isRiver == False:
	street = 2 # turn
    elif isFlop and isTurn and isRiver:
	street = 3 # river
    else:
	street = 0 # preflop

    # players in current hand
    numPlayers = tableInfo.numPlayers
    isPlayingArr = np.zeros((numPlayers),dtype='int8')
    hasButtonArr = np.zeros((numPlayers),dtype='int8') 
    for p in range(numPlayers):
	if tableInfo[p].isPlaying == True:
	    isPlayingArr[p] = 1
	if tableInfo[p].hasButton == True:
	    hasButtonArr[p] = 1
    position = np.where(hasButtonArr == 1)[0][0] # start at the button position
    numInHand = isPlayingArr.sum()
    inHandArr = np.zeros(numInHand,dtype='int8') # array of players in hand, sorted by position
    i = 0
    for dummy in range(numPlayers):
	if isPlayingArr[position] == 1:
	    inHandArr[i] = position
	    i += 1
	position +=1
	if position == numPlayers:
	    position = 0

    tableInfo.inHand = inHandArr
    tableInfo.street = street

    return tableInfo
        
# =============================================================================== #

def checkOrCall(tableReg):
    """not yet complete"""
    canCheck,callValue = False,0
    return canCheck,callValue

# =============================================================================== #

def readBet(playerReg,p):
	chipSideList = ['left','left','left','right','right','right']
	chipSide = chipSideList[p]
	betImg = playerReg.bet.img
	(digitBin,numDigits) = processImage(betImg,'bet'+chipSide)
	if numDigits == 0:
	    return 0
	else:
	    bet = 0
        for i in range(numDigits):
	    if numDigits == 1:
		thisDigit   = classifyMultiImage(digitBin[:,:],'betDigit','betDigitTheta.csv')
	    else:
		thisDigit   = classifyMultiImage(digitBin[:,:,i],'betDigit','betDigitTheta.csv')
            bet = bet + int(thisDigit)*10**(numDigits-i-1)
	return bet
  

# =============================================================================== #

def checkHero(playerReg):
    	heroArr = np.array([[0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0],
		       	[0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0],
		    	[0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,1],
		    	[0,1,1,1,1,0,0,1,1,0,0,1,1,0,0,0,1,1,1,1],
		    	[1,1,1,0,0,0,0,1,1,0,0,1,1,0,0,0,1,1,0,1],
		    	[1,1,0,0,0,0,0,1,1,0,0,1,1,0,0,0,1,1,0,1],
		    	[1,1,0,0,0,0,0,1,1,0,0,1,1,0,0,0,1,1,0,1],
		    	[1,1,0,0,0,0,0,1,1,0,0,1,1,0,0,1,1,1,0,1],
		    	[1,1,1,0,0,0,0,1,1,0,0,1,1,1,1,1,1,1,0,1],
		    	[0,1,1,1,1,0,0,1,1,0,0,0,1,1,1,0,1,1,0,1]])
	nameImg = playerReg.name.img.copy()
        playerArr = processImage(nameImg,'heroName')
	if playerArr.shape == heroArr.shape:
		matchVal =  100*(playerArr==heroArr).sum()/playerArr.size
		negMatchVal = 100*((-1*playerArr+2)==heroArr).sum()/playerArr.size
	else:
		matchVal,negMatchVal = 0,0
	if matchVal >= 90 or negMatchVal >= 90:
		return True
	else:
		return False
# =============================================================================== #

def detectHeroAction(tableReg):
    # detects presence of red fold button - action is on hero
    foldArr = tableReg.foldButton.img.copy()
    foldArr = foldArr[:,:,1]
    foldThresh = foldArr[(foldArr<50)*(foldArr>0)]
    if foldThresh.size > 2000:
        return True
    else:
        return False

# =============================================================================== #

def readPot(tableReg):
    imgArr = tableReg.pot.img.copy()
    # check for pot
    threshold = 150
    totalCount  = imgArr.size
    threshCount = imgArr[imgArr>threshold].size
    proportion  = 100*threshCount/totalCount
    potExists = proportion > 1
    if potExists:
        # classify each digit, add digits sequentially to get stack value
        (digitBin,numDigits) = processImage(imgArr,'pot',returnBin=True)
        pot = 0
        for i in range(numDigits):
	    if numDigits == 1:
		thisDigit   = classifyMultiImage(digitBin[:,:],'digit','digitTheta.csv')
	    else:
		thisDigit   = classifyMultiImage(digitBin[:,:,i],'digit','digitTheta.csv')
            if thisDigit == 'A' or thisDigit == 'S':
                raise ValueError('digit misread as A or S when reading pot')
            pot = pot + int(thisDigit)*10**(numDigits-i-1)
    else:
        pot = 0
    return pot

# =============================================================================== #

def readCommCards(tableReg):
    oneImg      = tableReg.flopOne.img    
    twoImg      = tableReg.flopTwo.img   
    threeImg    = tableReg.flopThree.img  
    fourImg     = tableReg.turn.img       
    fiveImg     = tableReg.river.img

    one     = (None,None)
    two     = (None,None)
    three   = (None,None)
    four    = (None,None)
    five    = (None,None)

    commImgList     = [oneImg,twoImg,threeImg,fourImg,fiveImg]
    commCardList    = [one,two,three,four,five]

    for i in range(5):
        img = commImgList[i]
    
        # check for comm card
        imgType     = 'faceCardExists'
        paramName   = 'commCardTheta.csv'
        hasCommCards = classifyImage(img,imgType,paramName)

        if hasCommCards:
            val,suit = readFaceCard(img)
            commCardList[i] = (val,suit)
    
    return commCardList

# =============================================================================== #

def readFaceCard(imgArr):
    imgType = 'faceCard'
    (valBin,suitBin) = processImage(imgArr,imgType,returnBin=True)

    # ===== classify value ===== #
    imgType = 'cardVal'
    parameterName = 'cardValTheta.csv'
    val = classifyMultiImage(valBin,imgType,parameterName)

    # ===== classify suit ===== #
    imgType = 'suit'
    parameterName = 'suitTheta.csv'
    #print suitBin,suitBin.shape
    suit = classifyMultiImage(suitBin,imgType,parameterName)
    
    return val,suit

# =============================================================================== #

def readHoleCards(playerReg):
    imgArrOne = playerReg.holeOne.img.copy()
    imgArrTwo = playerReg.holeTwo.img.copy()

    # check for hole card
    imgType     = 'faceCardExists'
    paramName   = 'holeCardTheta.csv'
    hasHoleCards = classifyImage(imgArrOne,imgType,paramName)

    if hasHoleCards:
        valOne,suitOne = readFaceCard(imgArrOne)
        valTwo,suitTwo = readFaceCard(imgArrTwo)
    else:
        (valOne,valTwo,suitOne,suitTwo) = (None,None,None,None)
            
    return hasHoleCards,valOne,valTwo,suitOne,suitTwo

# =============================================================================== #

def readStack(playerReg):
            # ===== read stack ===== #
            imgArr = playerReg.stack.img.copy()
            isSittingOut = False
            isAllIn = False
            isNoPlayer = False
            # check for no stack present - sum up colors greater than threshold
            threshold = 150
            totalCount  = imgArr.size
            threshCount = imgArr[imgArr>200].size
            proportion  = 100*threshCount/totalCount
            # number 1 has 27 pixels, stack image size is 87*17, which makes digit 1 ~1.8% of the image
            stackExists = proportion > 1
            if stackExists:
                # grab 1st digit and classify (numbers 1-9, A or S - 0 not an option for 1st digit)
                digitOne = processImage(imgArr,'stackCheck',returnBin=True)
                imageCat = classifyMultiImage(digitOne,'digit','digitTheta.csv')
                if imageCat == 'S':
                    isSittingOut = True
                    stack = 0
                elif imageCat == 'A':
                    isAllIn = True
                    stack = 0
                elif int(imageCat) > 0 and int(imageCat) <=9:
                    # classify each digit, add digits sequentially to get stack value
                    (digitBin,numDigits) = processImage(imgArr,'stack',returnBin=True)
                    digitArr = np.zeros(numDigits)
                    stack = 0
                    for i in range(numDigits):
			if numDigits == 1:
			    thisDigit   = classifyMultiImage(digitBin[:,:],'digit','digitTheta.csv')
			else:
			    thisDigit   = classifyMultiImage(digitBin[:,:,i],'digit','digitTheta.csv')
                        if thisDigit == 'A' or thisDigit == 'S':
                            raise ValueError('digit misread as A or S when reading stack')
                        stack = stack + int(thisDigit)*10**(numDigits-i-1)
                else:
                    raise ValueError('no valid integer read as first digit of stack')
            else:
                stack = 0
                isNoPlayer = True

            return stack,isSittingOut,isAllIn,isNoPlayer

# =============================================================================== #

def checkButton(playerReg):
            # ===== check for dealer button ===== #
            imgArr = playerReg.dealer.img.copy()
            # sum up all the red
            redArr      = imgArr[3:18,3:18,2]
            totalCount  = redArr.size
            redCount    = redArr[redArr>200].size
            proportion  = 100*redCount/totalCount
            if proportion > 30:
                hasButton = True
            else:
                hasButton = False
            return hasButton

# =============================================================================== #

def checkCards(playerReg):
            # ===== check for table cards ===== #
            imgArr = playerReg.cards.img.copy()
            # sum up all the red
            redArr      = imgArr[:,:,2]
            totalCount  = redArr.size
            redCount    = redArr[redArr>100].size
            proportion  = 100*redCount/totalCount
            if proportion > 50:
                hasCards = True
            else:
                hasCards = False
            return hasCards

# =============================================================================== #

# ===== run main ===== #
if __name__ == '__main__':
    readElements()


