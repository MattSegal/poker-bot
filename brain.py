"""
GUI for simple display and commands for poker bot
--> trivial alteration for Git tutorial
--> a second trivial alteration
--> MORE CHANGES!!
--> BAHAHA
"""
from Tkinter import *
from getInput import getInput
import autopy
import random
import time

def brain():
    root = Tk()
    app = App(root)
    root.mainloop()

class App:
    def __init__(self, master):
	self.master = master
	self.brainAfterID = None
	self.actionAfterID = None
	self.runBrainBool = True
	self.action = None
	self.tableInfo = None
	self.caughtAction = None
	self.numPlayers = 6
	self.tableFound = StringVar()
	self.isRunning = StringVar()
	self.runTime	= StringVar()
	self.heroHoleCards = StringVar()
	self.heroHand = StringVar()
	# table variables
	self.pot	= StringVar()
	self.bigBlind	= StringVar()
	self.buttonSeat = StringVar()
	self.heroSeat	= StringVar()
	self.board	= StringVar()
	# player variables
	self.stackOne	= StringVar()
	self.stackTwo	= StringVar()
	self.stackThree = StringVar()
	self.stackFour	= StringVar()
	self.stackFive	= StringVar()
	self.stackSix	= StringVar()

	self.betOne	= StringVar()
	self.betTwo	= StringVar()
	self.betThree	= StringVar()
	self.betFour	= StringVar()
	self.betFive	= StringVar()
	self.betSix	= StringVar()

	self.inPlayOne	= StringVar()
	self.inPlayTwo	= StringVar()
	self.inPlayThree= StringVar()
	self.inPlayFour	= StringVar()
	self.inPlayFive	= StringVar()
	self.inPlaySix	= StringVar()

	# FRAME HEIRACHY:
	# frame
	#   metaFrame
	#	getInfoButton
	#	tableFound
	#   pokerFrame
	#	tableFrame
	#	playerFrame
	#	heroFrame
	#   actionFrame (not implemented)
	#	time for action
	#	check
	#	call
	#	bet
	#	fold

	frame = Frame(master)
	frame.grid(row=0)

        metaFrame = Frame(frame)
	pokerFrame = Frame(frame)
	actionFrame = Frame(frame)
	metaFrame.grid(row=0)
	pokerFrame.grid(row=1)
	actionFrame.grid(row=2)

	# ===== meta-info frame ===== #
        getInfoButton = Button(metaFrame, text="Get Info", command=self.getInfo,width=10).grid(row=0,column=0)
	getInfoButton = Button(metaFrame, text="Run", command=self.runBrain,width=10).grid(row=0,column=1)
	getInfoButton = Button(metaFrame, text="Stop", command=self.killBrain,width=10).grid(row=0,column=2)
	Label(metaFrame, textvariable=self.isRunning,padx=2,pady=2,width=10).grid(row=0,column=3)
	Label(metaFrame, text='Found:',padx=2,pady=2,width=10).grid(row=1,column=0)
	Label(metaFrame, textvariable=self.tableFound,padx=2,pady=2,relief = SUNKEN,width=10).grid(row=1,column=1)
	Label(metaFrame, text='Time:',padx=2,pady=2,width=10).grid(row=1,column=2)
	Label(metaFrame, textvariable=self.runTime,padx=2,pady=2,relief = SUNKEN,width=10).grid(row=1,column=3)
	
	
	# ===== poker info frame ===== #
	tableFrame = Frame(pokerFrame)
	playerFrame = Frame(pokerFrame)
	tableFrame.grid(row=0)
	playerFrame.grid(row=2)

	
	# ===== table frame ===== #
	Label(tableFrame, text='Pot:',padx=2,pady=2,width=10).grid(row=0,column=0)
	Label(tableFrame, textvariable=self.pot,relief = SUNKEN,padx=2,pady=2,width =10).grid(row=0,column=1)
	Label(tableFrame, text='BB:',padx=2,pady=2,width=10).grid(row=0,column=2)
	Label(tableFrame, textvariable=self.bigBlind,relief = SUNKEN,padx=2,pady=2,width =10).grid(row=0,column=3)
	Label(tableFrame, text='Hero:',padx=2,pady=2,width=10).grid(row=1,column=0)
	Label(tableFrame, textvariable=self.heroSeat,relief = SUNKEN,padx=2,pady=2,width =10).grid(row=1,column=1)
	Label(tableFrame, text='Button:',padx=2,pady=2,width=10).grid(row=1,column=2)
	Label(tableFrame, textvariable=self.buttonSeat,relief = SUNKEN,padx=2,pady=2,width =10).grid(row=1,column=3)
	Label(tableFrame, text='Board:',padx=2,pady=2,width=10).grid(row=2,column=0)
	Label(tableFrame, textvariable=self.board,relief = SUNKEN,padx=2,pady=2,width =32).grid(row=2,column=1,columnspan=3)
	Label(tableFrame, text='Hand:',padx=2,pady=2,width=10).grid(row=3,column=0)
	Label(tableFrame, textvariable=self.heroHoleCards,relief = SUNKEN,padx=2,pady=2,width =10).grid(row=3,column=1)
	Label(tableFrame, textvariable=self.heroHand,relief = SUNKEN,padx=2,pady=2,width =20).grid(row=3,column=2,columnspan=2)

	# ===== player frame ===== #
	
	# column headers
	headerList =['Player','Stack','Bet','In Hand']
	for i in range(len(headerList)):
	    Label(playerFrame, text=headerList[i],padx=2,pady=2).grid(row=0,column=i)	
	
	# grid info
	playerList = ['1','2','3','4','5','6']
	self.stackList = [self.stackOne,self.stackTwo,self.stackThree,self.stackFour,self.stackFive,self.stackSix]
	self.betList = [self.betOne,self.betTwo,self.betThree,self.betFour,self.betFive,self.betSix]
	self.inPlayList = [self.inPlayOne,self.inPlayTwo,self.inPlayThree,self.inPlayFour,self.inPlayFive,self.inPlaySix]
	
	for i in range(self.numPlayers):
	    Label(playerFrame, text=playerList[i],padx=2,pady=2,width=8).grid(row=1+i,column=0)
	    Label(playerFrame, textvariable=self.stackList[i],relief = SUNKEN,padx=2,pady=2,width=8).grid(row=1+i,column=1)
	    Label(playerFrame, textvariable=self.betList[i],relief = SUNKEN,padx=2,pady=2,width=8).grid(row=1+i,column=2)
	    Label(playerFrame, textvariable=self.inPlayList[i],relief = SUNKEN,padx=2,pady=2,width=8).grid(row=1+i,column=3)


	# ===== action frame ===== #
	getInfoButton = Button(actionFrame, text="Fold", command=lambda: self.commandAction('fold'),width=10).grid(row=0,column=0)
	getInfoButton = Button(actionFrame, text="Check", command=lambda:self.commandAction('check'),width=10).grid(row=0,column=1)
	getInfoButton = Button(actionFrame, text="Call", command=lambda:self.commandAction('call'),width=10).grid(row=0,column=2)
	getInfoButton = Button(actionFrame, text="Bet", command=lambda:self.commandAction('bet'),width=10).grid(row=0,column=3)

	
	self.cleanTable()
    
    def runBrain(self):
	print 'still alive'
	if self.runBrainBool:
	    if self.actionAfterID != None:
		self.master.after_cancel(self.actionAfterID)
	    self.isRunning.set("Running")
	    self.getInfo()
	    if self.tableInfo != False:
		if self.tableInfo.heroAction:
		    self.runBrainBool = False
		    self.action = None
		    print "to take action!"
		    self.takeAction()
	self.brainAfterID = self.master.after(200,self.runBrain)

    def killBrain(self):
	self.master.after_cancel(self.brainAfterID)
	if self.actionAfterID != None:
	    self.master.after_cancel(self.actionAfterID)
	self.runBrainBool = True
	print 'this works'
	self.isRunning.set("Stopped")

    def commandAction(self,action):
	self.action = action

    def takeAction(self):
	"""
	action is string 'bet','fold','call','check'
	"""
	#self.isRunning.set("Need Input")
	#userInput = self.action
	self.isRunning.set("Thinking")
	print self.tableInfo.heroBet,self.tableInfo.maxBet
	if self.tableInfo.heroBet < self.tableInfo.maxBet:
	    userInput = 'call'
	else:
	    userInput = 'check'
	print userInput


	if userInput in ['bet','fold','call','check']:
	    print userInput
	    x = random.randint(0,100)
	    y = random.randint(0,100)
	    autopy.mouse.smooth_move(1000+x,500+y)
	    autopy.mouse.click()
	    randPause = int(random.randint(0,10))/100
	    time.sleep(0.5+randPause)
	    if userInput == 'fold':
		autopy.key.tap('q')
	    elif userInput == 'check':
		autopy.key.tap('w')
	    elif userInput == 'call': 
		autopy.key.tap('e')
	    elif userInput == 'bet':
		autopy.key.tap('9')
		time.sleep(0.5)
		autopy.key.tap('r')
	    else:
		raise ValueError('wrong action command')
	    self.runBrainBool = True
	else:
	    self.actionAfterID = self.master.after(100,self.takeAction)

    def getInfo(self):
	(self.tableInfo,runTime) = getInput()
	if self.tableInfo == False:
	    self.tableFound.set('No')
	    self.cleanTable()
	    self.runTime.set(str(runTime)+'ms')
	else:
	    self.tableFound.set('Yes')
	    self.runTime.set(str(runTime)+'ms')

	    #table info
	    self.pot.set(self.tableInfo.pot)
	    self.buttonSeat.set(self.tableInfo.buttonSeat+1)
	    self.heroSeat.set(self.tableInfo.heroSeat+1)
	    # board info
	    if self.tableInfo.street == 0: # preflop
		commOne	    = '  '
		commTwo	    = '  '
		commThree   = '-'
		commFour    = '  '
		commFive    = '  '
	    elif self.tableInfo.street == 1: # flop
		commOne	    = self.tableInfo.flopOne[0]+self.tableInfo.flopOne[1][0]
		commTwo	    = self.tableInfo.flopTwo[0]+self.tableInfo.flopTwo[1][0]
		commThree   = self.tableInfo.flopThree[0]+self.tableInfo.flopThree[1][0]
		commFour    = '  '
		commFive    = '  '
	    elif self.tableInfo.street == 2: # turn
		commOne	    = self.tableInfo.flopOne[0]+self.tableInfo.flopOne[1][0]
		commTwo	    = self.tableInfo.flopTwo[0]+self.tableInfo.flopTwo[1][0]
		commThree   = self.tableInfo.flopThree[0]+self.tableInfo.flopThree[1][0]
		commFour    = self.tableInfo.turn[0]+self.tableInfo.turn[1][0]
		commFive    = '  '
	    elif self.tableInfo.street == 3: # river 
		commOne	    = self.tableInfo.flopOne[0]+self.tableInfo.flopOne[1][0]
		commTwo	    = self.tableInfo.flopTwo[0]+self.tableInfo.flopTwo[1][0]
		commThree   = self.tableInfo.flopThree[0]+self.tableInfo.flopThree[1][0]
		commFour    = self.tableInfo.turn[0]+self.tableInfo.turn[1][0]
		commFive    = self.tableInfo.river[0]+self.tableInfo.river[1][0]
	    self.board.set(commOne+' '+commTwo+' '+ commThree+' '+commFour+' '+commFive)
	    # player info
	    for i in range(self.numPlayers):
		self.stackList[i].set(self.tableInfo[i].stack)
		self.betList[i].set(self.tableInfo[i].bet)
	    
		if self.tableInfo[i].isPlaying > 0:
		    if i == self.tableInfo.heroSeat:
			inPlay = 'hero'
		    else:
			inPlay = 'villain'
		else:
		    inPlay = '-'
		self.inPlayList[i].set(inPlay)
	    # hero info
	    if self.tableInfo[self.tableInfo.heroSeat].hasHoleCards:
		holeOne = self.tableInfo[self.tableInfo.heroSeat].holeOne[0]+self.tableInfo[self.tableInfo.heroSeat].holeOne[1][0]
		holeTwo = self.tableInfo[self.tableInfo.heroSeat].holeTwo[0]+self.tableInfo[self.tableInfo.heroSeat].holeTwo[1][0]
		heroHoleCards = holeOne+' '+holeTwo
	    else:
		heroHoleCards = '-'
	    self.heroHoleCards.set(heroHoleCards)
        
    def cleanTable(self):
	#table info
	self.pot.set('-')
	self.heroSeat.set('-')
	self.buttonSeat.set('-')
	self.bigBlind.set('-')
	self.board.set('-')
	self.heroHoleCards.set('-')
	self.heroHand.set('-')
	#player info
	for i in range(self.numPlayers):
	    self.stackList[i].set('-')
	    self.betList[i].set('-')
	    self.inPlayList[i].set('-')
	



# ===== run main ===== #
if __name__ == '__main__':
    brain()

# PokerStars Hotkeys
# fold          q
# check         w
# call          e
# bet/raise     r

# bet 1 bb      1 
# bet 2 bb      2
# bet 3 bb      3
# bet 1/4 pot   4
# bet 1/3 pot   5
# bet 1/2 pot   6
# bet 2/3 pot   7
# bet 3/4 pot   8
# bet 1/1 pot   9
# all in        -


