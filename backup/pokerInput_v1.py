import sys
from collections import namedtuple
import subprocess # for running python scripts

# import sikuli
import org.sikuli.basics.SikulixForJython
from sikuli import *
org.sikuli.basics.Settings.OcrTextRead = True
org.sikuli.basics.Settings.OcrTextSearch = True



print '===== Imports Loaded ===== '

# ===== to do list ===== #
# stack size reader


def main():

    # load images
    #playerName          = Image.create('.\playCash\playerName.png')         # bots name
    #playerNameFlash     = Image.create('.\playCash\playerNameFlash.png')    # bots name when flashing
    #playerBoxTop        = Image.create('.\playCash\playerBox\playerBoxTop.png')
    #playerBoxBot        = Image.create('.\playCash\playerBox\playerBoxBot.png')
    #playerBoxLeft       = Image.create('.\playCash\playerBox\playerBoxLeft.png')
    #playerBoxRight      = Image.create('.\playCash\playerBox\playerBoxRight.png')
    #dealerChip          = Image.create('.\playCash\dealerChip.png')
    siteLogoImg         = Image.create('.\playCash\siteLogo.png')
    holeCardsImg        = Image.create('.\playCash\holeCards.png')
    # integrate elsewhere
    stackWidth      =   50
    stackHeight     =   12
    cardsWidth      =   27
    cardsHeight     =   33

    #print 'mouse',Mouse.at()


    player = assignSixPlayers(siteLogoImg)
    print 'read stack for players'
    numPlayers = 6
    stack = []
    for i in range(numPlayers):
        playerStackLoc =player[i][0]
        playerStack = readStackFromLoc(playerStackLoc)
        stack.append(playerStack)
    print 'stack is ',stack
    
def readStackFromLoc(stackLoc):
    stackWidth      =   50
    stackHeight     =   12
    stackReg = stackLoc.grow(stackWidth,stackHeight)
    #highlightLoc(stackLoc,stackWidth,stackHeight,1) # debug
    # convert region into a png file 
    stackImg = capture(stackReg)
    stack = 0
    #stack = os.system('python readStack.py '+stackImg)
    stack = pythonScript('readStack','readStack',stackImg)
    stack = int(stack)
    return stack

def pythonScript(script,func,arg):
    arg = """'"""+arg+"""'"""
    command = 'from '+script+' import '+func+'; '+func+'('+arg+')'
    output = subprocess.Popen(['python','-c', command], stdout=subprocess.PIPE).communicate()[0]
    return output

def hasCards(cardLoc,cardImg):
    cardsWidth      =   27
    cardsHeight     =   33
    cardReg = cardLoc.grow(cardsWidth,cardsHeight)
    cardMatch = cardReg.exists(cardImg,0)
    if cardMatch == None:
        return False
    else:
        if cardMatch.getScore() >= 0.7:
            return True
        else:
            return False
 

def assignSixPlayers(image):
    """"
    returns the locations occupied by each players stack and cards
    the locations are referenced off of the pokerstars logo in the top left of the screen
    first player is top left six seated, then anticlockwise
    TO DO:
    add bet region to playerRegionTuple tuple later
    consider making a class to hold all player locations
    """
    referenceLoc = findItem(image)
    playerTuple = namedtuple('player','one two three four five six')
    LocTuple = namedtuple('playerLoc','stack cards')

    # integrate elsewhere
    stackWidth      =   50
    stackHeight     =   12
    cardsWidth      =   27
    cardsHeight     =   33

    
    playerOneStack      = referenceLoc.offset(278,52)
    playerOneCards      = referenceLoc.offset(227,133)
    #playerOneBet        = ?
    
    playerTwoStack      = referenceLoc.offset(60,290)
    playerTwoCards      = referenceLoc.offset(144,231)
    #playerTwoBet        = ?

    playerThreeStack    = referenceLoc.offset(275,392)
    playerThreeCards    = referenceLoc.offset(228,308)
    #playerThreeBet      = ?

    playerFourStack     = referenceLoc.offset(496,393)
    playerFourCards     = referenceLoc.offset(546,308) 
    #playerFourBet       = ?

    playerFiveStack     = referenceLoc.offset(712,290)
    playerFiveCards     = referenceLoc.offset(620,232)
    #playerFiveBet       = ?

    playerSixStack      = referenceLoc.offset(496,52)
    playerSixCards      = referenceLoc.offset(546,133)
    #playerSixBet        = ?

    one = LocTuple(playerOneStack,playerOneCards)
    two = LocTuple(playerTwoStack,playerTwoCards)
    three = LocTuple(playerThreeStack,playerThreeCards)
    four = LocTuple(playerFourStack,playerFourCards)
    five = LocTuple(playerFiveStack,playerFiveCards)
    six = LocTuple(playerSixStack,playerSixCards)
    player = playerTuple(one,two,three,four,five,six)
    return player


def highlightLoc(location,width,height,time):
        imgReg = location.grow(width,height)
        imgReg.highlight(time)

def findItem(img):
    (match, found) = tryFind(img)
    if found == False:
        print 'findTable: no poker table found'
    imgLoc = match.getTarget()
    return imgLoc

    # highlight location of img
    highlight = True
    if highlight:
        width = 20
        height = 20
        imgReg = imgLoc.grow(width,height)
        imgReg.highlight(1)

    


def findAllPlayers(playerFeature):
    # find all seated players
    try:
        playerMatch = findAll(playerFeature)
        counter = 0
        while playerMatch.hasNext():
            counter += 1
            currentMatch = playerMatch.next()
            playerLoc = currentMatch.getTarget()
            # highlight a player
            width       = 20
            height      = 20
            playerReg    = playerLoc.grow(width,height)
            playerReg.highlight(3)
            if counter > 10:
                break
    except:
        print 'no players found'

def readStack(playerLoc):
    xOff        = 0
    yOff        = 17 # guess
    stackLoc    = playerLoc.offset(xOff,yOff)
    width       = 50
    height      = 12
    stackReg    = stackLoc.grow(width,height)
    stackReg.highlight(3)

    readText = stackReg.text() #returns text or null
    #stackSize = float(readText)
    
    return readText
    


def findPlayer(name,nameFlash):
    
    (match, found) = tryFind(name)
    if found == False:
        (match, found) =tryFind(nameFlash)    
        if found == False:
            print 'player name not found'
    print 'match ',match
    playerLocation = match.getTarget()

    # highlight location of player
    #width = 80
    #height = 15
    #playerReg = playerLocation.grow(width,height)
    #playerReg.highlight(1)
    return playerLocation


    #return playerLocation
        
def tryFind(img):
    try:
        targetMatch = find(img)
        return targetMatch,True
    except:
        targetMatch = 0
        return targetMatch, False

def tryFindInRegion(img,targetReg):
    try:
        targetMatch = targetReg.find(cardImg)
        return targetMatch,True
    except:
        targetMatch = 0
        return targetMatch, False
    
def move(img):
    """
    moves mouse an image in the DEFAULT region, if the region is present
    returns True for success, False for failure
    """
    try:
        targetMatch = find(img)
        loc = targetMatch.getTarget()
        Mouse.move(loc)
        return True
    except:
        print "not found"
        return False

def isMatch(match):
    """
    returns true if match >0.5
    """
    matchScore = match.getScore()
    if matchScore > 0.5:
        return True
    else:
        return False

# ===== run main ===== #
if __name__ == '__main__':
     main()


    
