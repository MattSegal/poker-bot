"""
processes images for poker bot by cropping and manipulating colors
"""

import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt

def processImage(imgArr,imgType,returnBin=False):
    """
    MAIN LOOP:
    accepts an image of a specified type and processes it for poker bot
    return image can be a .png or binary 'Bin'
    input imgArr is BGR numpy array from openCV - all images are BGR format
    """
    
    if imgType == 'faceCard':
        return processFaceCard(imgArr,imgType,returnBin)
	
    elif imgType == 'betleft' or imgType == 'betright':
	return processBet(imgArr,imgType,returnBin)

    elif imgType == 'heroName':
	return processHeroName(imgArr,imgType,returnBin)

    elif imgType =='stack':
	return processStack(imgArr,imgType,returnBin)

    elif imgType =='stackCheck':
        return processStackCheck(imgArr,imgType,returnBin)

    elif imgType =='stackNot':
        return processStackNot(imgArr,imgType,returnBin)

    elif imgType =='pot':
        return processPot(imgArr,imgType,returnBin)
    else:
        raise ValueError('no image type found')

# =============================================================================== #
#		    the following are helper functions used
#		    in the process<name> functions		    
# =============================================================================== #

def trimImage(img,minRowPix=0,minColPix=0,trimTop=True,trimBot=True,trimRight=True):
    """
    throws away black pixels at top bottom left right
    input image must be binary image in format img[row,column]
    minRowPix find first row with <val> pixels 
    minColPix find first column with <val> pixels
    """
    
    rowSum = img.sum(axis=1)
    bot = np.max(np.where(rowSum>minRowPix))
    top = np.min(np.where(rowSum>minRowPix))
    if trimTop and trimBot:
        img = img[top:bot+1,:]
    elif trimTop:
        img = img[top:,:]
    elif trimBot:
        img = img[:bot+1,:]
    
    columnSum = img.sum(axis=0)
    left  = np.min(np.where(columnSum>minColPix))
    right = np.max (np.where(columnSum>minColPix))
    if trimRight:
	img = img[:,left:right+1]
    else:
	img = img[:,left:]
    #binaryToBGR(img,'digits.png')
    return img

# =============================================================================== #

def binaryToBGR(img,plot=False):
    """
    output final image matrix as an RGB image
    img is a nxm matrix of 1s and 0s
    name is the save name eg 'test.png'
    """    
    (m,n) = img.shape
    imgBGR = np.zeros((m,n,3),dtype='uint8')
    imgBGR[:,:,0]  = img*255
    imgBGR[:,:,1]  = img*255
    imgBGR[:,:,2]  = img*255

    if plot:
        plotFigure(imgBGR)

    return imgBGR

# =============================================================================== #

def BGRToBinary(img,imgType='faceCard'):
    """
    output is binary matrix of 1 - white 0 - black
    filters RGB .png image (does not accept RGBA)
    http://stackoverflow.com/questions/17141535/how-to-use-the-otsu-threshold-in-opencv
    TO DO: make the thresholding less arbirary
    TO DO: possible customise the thresholding for different image types
    """

    img = cv.cvtColor(img,cv.COLOR_BGR2GRAY,dstCn=1)

    if imgType == 'faceCard':
        threshVal = 200
        (ret,img) = cv.threshold(img,threshVal,255,cv.THRESH_BINARY)
        img[img<255] = 0
        img[img>=255] = 1
    elif imgType == 'stack' or imgType == 'stackNot' or imgType == 'pot' or imgType == 'name':
        (ret,img) = cv.threshold(img,0,255,cv.THRESH_BINARY | cv.THRESH_OTSU)
        img[img<255] = 0
        img[img>=255] = 1
        # check for inverted image
        numWhite = img.sum()
        numBlack = img.size - numWhite
        if numWhite > numBlack:
            imgCopy = img.copy()
            img[imgCopy==1] = 0
            img[imgCopy==0] = 1
    elif imgType == 'bet':
	threshVal = 150
        (ret,img) = cv.threshold(img,threshVal,255,cv.THRESH_BINARY)
        img[img<255] = 0
        img[img>=255] = 1
	
    else:
        raise ValueError('BGR to binary conversion not possible - no image type specified')

    #(ret,img) = cv.threshold(img,threshVal,255,cv.THRESH_BINARY)    
    #(ret,img) = cv.threshold(img,0,255,cv.THRESH_BINARY | cv.THRESH_OTSU)
    #img = cv.adaptiveThreshold(img,255,cv.ADAPTIVE_THRESH_MEAN_C,cv.THRESH_BINARY,5,3)
    
    return img

# =============================================================================== #

def plotFigure(img,img2=np.array([]),BGR=True):
    """
    plots BGR or binary image in pyplot window
    """
    
    if img2.size == 0:
        if BGR:
            img = img[:, :, ::-1].copy()
        plt.figure()
        plt.imshow(img,interpolation='none')
        plt.show()
    else:
        if BGR:
            img = img[:, :, ::-1].copy()
            img2 = img2[:, :, ::-1].copy()
        plt.subplot(1,2,1)
        plt.imshow(img,interpolation='none')
        plt.subplot(1,2,2)
        plt.imshow(img2,interpolation='none')
        plt.show()

# =============================================================================== #
#		    the following are the process functions used
#		    to process specific image types		    
# =============================================================================== #

def processHeroName(imgArr,imgType,returnBin):
    imgBin = BGRToBinary(imgArr,'name')
    imgBin = trimImage(imgBin,minRowPix=2,minColPix=2)
    nameID = imgBin[:10,:20]
    return nameID

# =============================================================================== #

def processFaceCard(imgArr,imgType,returnBin=False):
    imgBin = BGRToBinary(imgArr,imgType)
    imgBin = trimImage(imgBin)	
    valBin = imgBin[:15]
    suitBin = imgBin[-11:]
    valBin = trimImage(valBin,trimRight=False)
    valBin = valBin[:,0:7]
    suitBin = trimImage(suitBin,2,2,trimTop=False)
    if returnBin:
        return valBin,suitBin
    else:
        valImg = binaryToBGR(valBin)
        suitImg = binaryToBGR(suitBin)
        return valImg,suitImg

# =============================================================================== #

def processPot(imgArr,imgType,returnBin):
    imgBin = BGRToBinary(imgArr,'pot')
    imgBin = trimImage(imgBin,minRowPix=2,minColPix=0)
    # remove 'Pot:' symbol
    imgBin = imgBin[:,23:] 
    imgBin = trimImage(imgBin,minRowPix=0,minColPix=0)
    # process digits
    (digitBin,numDigits) = seperateStackDigits(imgBin)
    #for i in range(numDigits): #plot for debug
    #    binaryToBGR(digitBin[:,:,i],plot=True)
    if returnBin:
        return digitBin,numDigits
    else:
        digitImg = np.zeros((10,6,3,numDigits))
        for digit in range(numDigits):
            digitImg[:,:,:,digit] = binaryToBGR(digitBin[:,:,digit])
        return digitImg,numDigits   

# =============================================================================== #

def processBet(imgArr,imgType,returnBin):
    side = imgType[3:]
    # filter out grey - areas where RGB  between 30 and 60
    greyLow = 20
    greyUp = 80
    grey = (imgArr[:,:,0]>greyLow)*(imgArr[:,:,0]<greyUp)*(imgArr[:,:,1]>greyLow)*(imgArr[:,:,1]<greyUp)*(imgArr[:,:,2]>greyLow)*(imgArr[:,:,2]<greyUp)
    imgArr[grey]=0
    imgBin = imgArr[:,:,0] + imgArr[:,:,1] + imgArr[:,:,2]
    imgBin[imgBin>0] = 1
    # check that there are any pixels in first 1/4 of image
    if side == 'left':
	colStart = 0
	colEnd = imgBin.shape[1]/4
    else:
	colStart = - imgBin.shape[1]/4
	colEnd = imgBin.shape[1]
    betExists = imgBin[:,colStart:colEnd].sum()>0
    if betExists:
	imgBin = trimImage(imgBin)
	numChips = getNumChips(imgBin,side)
	if numChips == 0:
	    return 0,0
	# redefine imgBin from original imgArr to get digits
	columnsRemoved = 0
	if side == 'left':
	    colLeft = 1
	    colRight = imgArr.shape[1]
	    const = 0
	else:
	    colLeft = 0
	    colRight = -2
	    const = 1

	for column in range(imgArr.shape[1]):
	    columnIndex = column - columnsRemoved - const
	    colSum = imgArr[:,columnIndex,:].sum()
	    if colSum == 0:
		imgArr = imgArr[:,colLeft:colRight,:]
		columnsRemoved +=1
	    else:
		break
	imgBin = BGRToBinary(imgArr,'bet')
	for loop in range(numChips):
	    if side == 'left':
		imgBin = imgBin[:,23:]
	    else:
		imgBin = imgBin[:,:-23]
	try:
	    imgBin = trimImage(imgBin)
	except:
	    print 'TRIM IN PROCESS BET FAILED'
	    binaryToBGR(imgBin,plot=True)
	imgBin = imgBin[0:8,:]
	(digitBin,numDigits) = seperateBetDigits(imgBin)
	return digitBin,numDigits
    else:
	return 0,0

def seperateBetDigits(img):
    
    """
    seperate bet size digits in a line of text that are separated by a column of blackspace
    assume a 8xunknown digit size - return a 8x5 array for each digit
    returns:
        numDigits   - the number of digits
        digitArr    - a 8x5xnumDigits array of each digit's binary image 
    """

    # space and comma vectors
    comma = np.array([0,0,0,0,0,0,1,1])
    space = np.array([0,0,0,0,0,0,0,0])

    numDigits = 0
    digitColList = [] 
    numCols = len(img[0,:])
    
    # find column co-ordinates of all the digits
    # and count number of digits
    isDigit = False
    for colCount in range(numCols):
	thisCol = colCount

	isComma = (img[:,thisCol] == comma).all()
	isSpace = (img[:,thisCol] == space).all()
	
	if (isComma or isSpace) and isDigit:
	    endCol = thisCol
	    digitColList.append((startCol,endCol))
	    numDigits +=1
	    isDigit = False
	elif not (isComma or isSpace) and not isDigit:
	    startCol = thisCol
	    isDigit = True
	elif colCount == numCols-1:
	    digitColList.append((startCol,numCols))
	    numDigits +=1

    # save each digit in a standard 8x5 numpy array
    digitArr = np.zeros((8,5,numDigits),dtype='int8')
    for digit in range(numDigits):
	startCol = digitColList[digit][0]
	endCol = digitColList[digit][1]
	digitImg = img[:,startCol:endCol]
	digitCol = digitImg.shape[1]
	digitArr[:,0:digitCol,digit] = digitImg
    
    return digitArr,numDigits

def getNumChips(img,side):
    """
    throws away chips and returns bet digits of imgArr
    also returns whether chips are on left or right side
    """
    # each chip occupies a 8x24 space
    # each digit 7 pixels wide
    # bottom 3 pixels are black below digits
    maxChips=5
    numChips = 0
    if side == 'left':
	for loop in range(maxChips):
	    leftChip = img[-2:,:23]
	    if leftChip[:,0:8].sum()>0:
		img = img[:,23:]
		numChips+=1

    elif side == 'right':
	for loop in range(maxChips):
	    rightChip = img[-2:,-23:]
	    if rightChip[:,-9:].sum()>0:
		img = img[:,:-23]
		numChips+=1
    else:
	raise ValueError('incorrect bet side')

    return numChips

# =============================================================================== #

def processStack(imgArr,imgType,returnBin):
    """
    returns stack image as a list of binary images for 1 by one
    visual classification
    """
    imgBin = BGRToBinary(imgArr,imgType)
    imgBin = trimImage(imgBin,minRowPix=2,minColPix=0)
    (digitBin,numDigits) = seperateStackDigits(imgBin)
    #for i in range(numDigits): #plot for debug
    #    binaryToBGR(digitBin[:,:,i],plot=True)
    if returnBin:
        return digitBin,numDigits
    else:
        digitImg = np.zeros((10,6,3,numDigits))
        for digit in range(numDigits):
            digitImg[:,:,:,digit] = binaryToBGR(digitBin[:,:,digit])
        return digitImg,numDigits

def seperateStackDigits(img):
    """
    seperate digits in a line of text that are separated by a column of blackspace
    assume a 10x6 pixel size
    returns:
        numDigits   - the number of digits
        digitArr    - a 10x6xnumDigits array of each digit's binary image 
    """
    # grab first digit
    digitArr = img[0:10,0:6]
    img = img[:,6:]

    numDigits = 1
    digitCol = np.array([])

    # space and comma vectors
    comma = np.array([0,0,0,0,0,0,0,0,1,1])
    space = np.array([0,0,0,0,0,0,0,0,0,0])

    for i in range(len(img[0,:])):
        if i > 0:
            prevColCommaOrSpace = (img[:,i-1]==comma).all() or (img[:,i-1]==space).all()
        else:
            prevColCommaOrSpace = False
        try:
            thisColCommaOrSpace = (img[:,i]==comma).all() or (img[:,i]==space).all()
        except:
            plotFigure(binaryToBGR(img))
        if prevColCommaOrSpace and not thisColCommaOrSpace:
            numDigits += 1
            digitCol = np.append(digitCol,i)

    for i in digitCol:
            newDigit = img[0:10,i:i+6]
            digitArr = np.dstack((digitArr,newDigit))
    
    return digitArr,numDigits

def processStackCheck(imgArr,imgType,returnBin):
    """
    returns 1st digit of a stack
    """
    imgBin = BGRToBinary(imgArr,'stack')
    imgBin = trimImage(imgBin,minRowPix=2,minColPix=0)
    digitOne = imgBin[0:10,0:6]
    #binaryToBGR(digitOne,plot=True) #plot for debug
    if returnBin:
        return digitOne
    else:
        digitImg = binaryToBGR(digitOne)
        return digitImg

def processStackNot(imgArr,imgType,returnBin):
    """
    returns 1st digit of a stack - duplicate of processStackCheck?
    """
    imgBin = BGRToBinary(imgArr,imgType)
    imgBin = trimImage(imgBin,minRowPix=2,minColPix=0)
    imgPlot = binaryToBGR(imgBin)
    digitBin = imgBin[0:10,0:6]
    if returnBin:
        return digitBin
    else:
        digitImg = binaryToBGR(digitBin)
        return digitImg

# =============================================================================== #
