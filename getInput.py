"""
CONVENTIONS:

All location references are to be in (row,column) format
Location is a (row, column) pixel reference taken from the top left
"""

# vanilla imports
import time
import sys

# third party imports
from PIL import ImageGrab
import numpy as np
import cv2 as cv

# project imports
from inputElements import TableReg
from inputElements import TableInfo
from plotFigure import plotFigure
from readElements import readElements

def getInput():
    # ===== initialise ===== #
    startTime = time.time()
    numPlayers  = 6

    img		= LoadImages()
    tableReg    = TableReg(numPlayers)
    tableInfo   = TableInfo(numPlayers)
    # time ~ 0.01 s
    try:
	(img.window,found) = getWindowImage(img.siteLogo)
    except NoTableError:
	if __name__ == '__main__':
	    raise NoTableError('no poker table found')
	else:
	    runTime = int(1000*(time.time()-startTime))
	    return False,runTime
    # time ~ 0.6s - most of the search time is spent finding the table
    tableReg	= getElementImages(tableReg,img.window,numPlayers)
    tableInfo	= readElements(tableInfo,tableReg)
    runTime	= int(1000*(time.time()-startTime))
    # time ~ 0.9s
    return tableInfo,runTime    

# =============================================================================== #

def getElementImages(table,windowArr,numPlayers):
    """
    returns table with numpy array of images loaded into the class
    to do: make images player character specific
        add hole cards when necessary for PC
        don't bother looking for table cards for PC
    """
    keyList = ['one','two','three','four','five','six',
                   'pot','flopOne','flopTwo','flopThree','turn','river',
                   'foldButton','checkButton','betButton']
    keyList = (keyList[0:numPlayers])+keyList[6:]
    playerKeyList = ['name','stack','cards','holeOne','holeTwo','dealer','bet']
    for element in keyList:
        if table[element] == None:
            continue
        if table[element].__name__ == 'Region':
            region = table[element]
            loc = region.loc
            w   = region.w
            h   = region.h
            table[element].img = getRegionImg(windowArr,loc,w,h)
            #plotFigure(table[element].img)
        if table[element].__name__ == 'PlayerReg':
            for subElement in playerKeyList:
                region = table[element][subElement]
                loc = region.loc
                w   = region.w
                h   = region.h
                table[element][subElement].img = getRegionImg(windowArr,loc,w,h)
                #plotFigure(table[element][subElement].img)
            
    return table

# =============================================================================== #

def getRegionImg(imageArr,loc,width,height,rowOffset=0,colOffset=0):
    rowMin = loc[0] + rowOffset
    rowMax = loc[0] + height
    colMin = loc[1] + colOffset
    colMax = loc[1] + width
    regionImageArr = imageArr[rowMin:rowMax,colMin:colMax,:]
    return regionImageArr
        

# =============================================================================== #
        
def getWindowImage(datumImg):
    """
    returns an image array of the poker table based on a datum image (PokerStars Logo)
    returns found == False if datum image is not on screen
    """

    # find the datum image on screen
    screen = screenCap(BGR=True)
    datumLoc = findTemplate(datumImg,screen,plotResults=False)
    found = datumLoc[2]
    if found:
        # throw away the rest of the screen - assume a standard table size
        windowWidth     = 792
        windowHeight    = 570
        rowOffset       = 22
        colOffset       = 0
        window = getRegionImg(screen,datumLoc[:2],windowWidth,windowHeight,rowOffset,colOffset)
        return window,found
    else:
        raise NoTableError('poker table not found - no poker logo visible')

# =============================================================================== #

class NoTableError(Exception):
	def __init__(self,value):
	    self.value = value
	def __str__(self):
	    return repr(self.value)

# =============================================================================== #

def screenCap(BGR=False):
    """
    runs in ~10ms
    can use Image.fromarray(np.uint8(img)) to convert numpy --> PIL
    takes a screenshot with PIL, PIL must return RGB (not RGBA) or this function fails
    converts PIL Image to numpy array
    returns numpy array of dim (width,height,3)
    """
    screenPIL = ImageGrab.grab()
    screenRGB = np.array(screenPIL)
    if BGR:
        screenBGR = screenRGB[:, :, ::-1].copy()
        return screenBGR
    else:
        return screenRGB

# =============================================================================== #

def findTemplate(template,img,plotResults=False,logo=True):
    img = img.copy()
    if logo:
	# red values generally >210 in heart, <210 out
	# green generally <220 in heart, <100 outside
	# blue <200 inside, <120 outside
	# throw out all red with blue >200
	# throw out all red <220

	highBlue = img[:,:,0] > 200
	highRed = img[:,:,2] > 220
	highBlueHighRed = highBlue*highRed
	lowRed = img[:,:,2] < 220
	img[highBlueHighRed] = 0
	img[lowRed] = 0

	highBlue = template[:,:,0] > 200
	highRed = template[:,:,2] > 220
	lowRed = template[:,:,2] < 220
	highBlueHighRed = highBlue*highRed
	template[highBlueHighRed] = 0
	template[lowRed] = 0

    method = cv.TM_CCOEFF_NORMED
    result = cv.matchTemplate(img,template,method)
    (minVal,maxVal,minLoc,maxLoc) = cv.minMaxLoc(result)
    (h,w) = template.shape[:-1]
    if plotResults:
        # draw a rectangle onto img
        topLeft = maxLoc
        bottomRight = (topLeft[0]+w, topLeft[1]+h)
        cv.rectangle(img,topLeft,bottomRight,255,1)
        # plot image with rectangle
        plotFigure(img)
        
    # convert maxLoc from (col,row) format to (row,col)
    row = maxLoc[1]
    col = maxLoc[0]
    # check that the image found by matchTemplate is the image we want
    selection = img[row:(row+h),col:(col+w)]
    if plotResults:
        plotFigure(template,selection)
    found = imageMatch(template,selection,threshold=50,redOnly=True,plot=False) 
    return row,col,found

# =============================================================================== #

def imageMatch(img1,img2,threshold=0,redOnly=False,blueOnly=False,greenOnly=False,plot=False):
    """
    compares img1 to img2 (both numpy arrays)
    returns match = True if images sufficiently similar
    match method = compare pixel by pixel
    TO DO: Add support for blueOnly and greenOnly
    """
    # this is an ugly hack to make it recognize the pokerstars logo
    # logo is 14wx17h but only want to check inner 8x8
    img1 = img1[4:12,3:11]
    img2 = img2[4:12,3:11]
    
    if redOnly:
        # image in BGR format, keep only red
        img1=img1[:,:,2]
        img2=img2[:,:,2]
    elif blueOnly:
        # image in BGR format, keep only blue
        img1=img1[:,:,0]
        img2=img2[:,:,0]
    elif greenOnly:
        # image in BGR format, keep only green
        img1=img1[:,:,1]
        img2=img2[:,:,1]
    if threshold > 0:
        img1[img1<threshold] = 0
        img2[img2<threshold] = 0
    
    # ===== check for similar elements ===== #
    sameDim = img1.shape == img2.shape
    if sameDim:
        tolerance = 10 # img2 values within +/- tolerance
        img1Upper = img1.copy()
        img1Lower = img1.copy()
        img1Upper[img1Upper<=255-tolerance] = img1Upper[img1Upper<=255-tolerance] + tolerance
        img1Lower[img1Lower>=tolerance] = img1Lower[img1Lower>=tolerance] - tolerance
        above = img2 > img1Upper
        below = img2 < img1Lower
        total = (above + below).sum()    
        elements = img1.size
        passRate = 100*(elements - total) / elements
        if plot:
            # for red only
            (n,m) = img1.shape
            img1plot = np.zeros((n,m,3))
            img2plot = np.zeros((n,m,3))               
            img1plot[:,:,2] = img1
            img2plot[:,:,2] = img2
            plotFigure(img1plot,img2plot)

        if passRate > 90:
            match = True
        else:
            match = False
    else:
        match = False

    #plotFigure(img1,img2,BGR=False)

    return match

# =============================================================================== #

class LoadImages:
    def __init__(self):
        self.siteLogo   = cv.imread('tableElements\siteLogo.png',1)
        self.window     = None
        #self.holeCards  = cv.imread('tableElements\holeCards.png',1)

# =============================================================================== #

# ===== run main ===== #
if __name__ == '__main__':
    startTime = time.time()
    getInput()
    endTime = time.time()
    print 'script took ',int(endTime-startTime),'s'






    
