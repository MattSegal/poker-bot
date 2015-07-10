# ===== imports ===== #
# vanilla imports
import time
import sys
import os

# third party imports
import numpy as np
import cv2 as cv

# project imports
from inputElements import * 
from getInput import *
from processImage import *
from classImg import classifyImage


def main():

    numPlayers  = 6
    numTables   = 68
    batchSaveImages(numPlayers,numTables)
    #batchSortImages()
    batchProcessImages()

# =============================================================================== #
    
def batchSaveImages(numPlayers,numTables):
    datumImgA   = cv.imread('tableElements\siteLogoGrey.png',1)
    datumImgB   = cv.imread('tableElements\siteLogoBlack.png',1)
    datumImgC   = cv.imread('tableElements\siteLogoWhite.png',1)

    for tableNum in range(1,numTables+1):
        # ===== open up table screenshot ===== #
        #print 'TABLE NUMBER ',tableNum
        path = 'tableExamples/table'+str(tableNum)+'.png'
        #path = 'pokerWindowCheck.png'
        path = os.path.normpath(path)
        screen    = cv.imread(path,1)
        # ===== open up tableImg from screenshot ===== #
        try:
            datumImg    = datumImgA
            datumLoc = findTemplate(datumImg,screen,plotResults=False)
        except ValueError:
            try:
                print 'grey didnt work, try black'
                datumImg    = datumImgB
                datumLoc = findTemplate(datumImg,screen,plotResults=False)
            except ValueError:
                try:
                    print 'black didnt work, try white'
                    datumImg    = datumImgB
                    datumLoc = findTemplate(datumImg,screen,plotResults=False)
                except ValueError:
                    raise ValueError('saveImages: poker table not found')
        found = datumLoc[2]

        if found:
            # throw away the rest of the screen - assume a standard table size
            windowWidth     = 792
            windowHeight    = 570
            rowOffset       = 22
            colOffset       = 0
            tableImg = getRegionImg(screen,datumLoc[:2],windowWidth,windowHeight,rowOffset,colOffset)
        else:
            raise ValueError('poker table not found - no poker logo visible')

        # ===== get region images from table ===== #
        tableReg = TableReg(numPlayers)
        tableReg = getElementImages(tableReg,tableImg,numPlayers)

        # ===== save each image from table ===== #
        
        # player images
        playerList  = ['one','two','three','four','five','six']
        elementList = ['name','stack','cards','bet','holeOne','holeTwo','dealer']
        playerList  = playerList[0:numPlayers]
        holeCard = np.array(['holeOne','holeTwo'])
        for p in range(numPlayers):
            player = playerList[p]
            identity = str(tableNum)+'_'+str(p+1)
            for element in elementList:
                img = tableReg[player][element].img

                if np.any(element == holeCard):
                        elementName = 'holeCard'
                        path = 'elementLibrary/raw/'+elementName+'/'+element+'_'+identity+'.png'
		elif element == 'bet':
		    if p < 3:
			elementName = 'betLeft'
		    else:
			elementName = 'betRight'
		    path = 'elementLibrary/raw/'+elementName+'/'+element+'_'+identity+'.png'
                    
                else:
                    elementName = element            
                    path = 'elementLibrary/raw/'+elementName+'/'+element+'_'+identity+'.png'            
                path = os.path.normpath(path)
                cv.imwrite(path,img)
                
        # community images
        elementList = ['pot',
                       'flopOne',
                       'flopTwo',
                       'flopThree',
                       'turn',
                       'river',
                       'foldButton',
                       'checkButton',
                       'betButton']
        communityCard = np.array(['flopOne','flopTwo','flopThree','turn','river'])
        identity = str(tableNum)
        for element in elementList:
            img = tableReg[element].img
            if np.any(element == communityCard):
                elementName = 'communityCard'
                identity = str(tableNum)+'_'+element
            else:
                elementName = element
                identity = str(tableNum)
            path = 'elementLibrary/raw/'+elementName+'/'+elementName+'_'+identity+'.png'
            path = os.path.normpath(path)
            cv.imwrite(path,img)

# =============================================================================== #

def batchSortImages():
    
    # sort community cards into card and not-card categories
    
    DIR = os.path.normpath('elementLibrary/raw/communityCard')
    imageList = [name for name in os.listdir(DIR)if os.path.isfile(os.path.join(DIR, name))]
    i = 0
    j = 0
    for imageName in imageList:
        readPath = os.path.normpath('elementLibrary/raw/communityCard/'+imageName)
        imgArr = cv.imread(readPath,1)
        imgType = 'faceCardExists'
        paramName = 'commCardTheta.csv'
        isCommCard = classifyImage(imgArr,imgType,paramName)
        # save
        if isCommCard:
            idenity = 'commCard/commCard_'+str(i)
            i += 1
        else:
            idenity = 'commCardNot/notCommCard_'+str(j)
            j += 1   
        writePath = os.path.normpath('elementLibrary/sorted/'+idenity+'.png')
        cv.imwrite(writePath,imgArr)

    # sort hole cards into card and not-card categories
   
    DIR = os.path.normpath('elementLibrary/raw/holeCard')
    imageList = [name for name in os.listdir(DIR)if os.path.isfile(os.path.join(DIR, name))]
    i = 0
    j = 0
    for imageName in imageList:
        readPath = os.path.normpath('elementLibrary/raw/holeCard/'+imageName)
        imgArr = cv.imread(readPath,1)
        imgType = 'faceCardExists'
        paramName = 'holeCardTheta.csv'
        isHoleCard = classifyImage(imgArr,imgType,paramName)
        # save
        if isHoleCard:
            idenity = 'holeCard/holeCard_'+str(i)
            i += 1
        else:
            idenity = 'holeCardNot/notholeCard_'+str(j)
            j += 1   
        writePath = os.path.normpath('elementLibrary/sorted/'+idenity+'.png')
        cv.imwrite(writePath,imgArr)
    
    # stack sort
    
    DIR = os.path.normpath('elementLibrary/raw/stack')
    imageList = [name for name in os.listdir(DIR)if os.path.isfile(os.path.join(DIR, name))]
    i = 0
    j = 0
    for imageName in imageList:
        readPath = os.path.normpath('elementLibrary/raw/stack/'+imageName)
        imgArr = cv.imread(readPath,1)
        imgType = 'stack'
        # sum up colors greater than threshold
        threshold = 150
        totalCount  = imgArr.size
        threshCount    = imgArr[imgArr>200].size
        proportion  = 100*threshCount/totalCount
        # number 1 has 27 pixels, stack size is 87*17, which makes 1 ~1.8% of the image
        if proportion > 1:
            stackExists = True
        else:
            stackExists = False
        # save
        if stackExists:
            idenity = 'stack/stack_'+str(i)
            i += 1
        else:
            idenity = 'stackNot/notStack_'+str(j)
            j += 1   
        writePath = os.path.normpath('elementLibrary/sorted/'+idenity+'.png')
        cv.imwrite(writePath,imgArr)


    # sort bet images into bet and non-bet categories
    
    
# =============================================================================== #

def batchProcessImages():
    """
    #  ===== community cards ===== #
    path = 'elementLibrary/sorted/commCard'
    DIR = os.path.normpath(path)
    imageList = [name for name in os.listdir(DIR)if os.path.isfile(os.path.join(DIR, name))]
    i = 0
    for imageName in imageList:
        readPath = os.path.normpath(path+'/'+imageName)
        imgArr = cv.imread(readPath,1)
        imgType = 'faceCard'
        (valImgArr,suitImgArr) = processImage(imgArr,imgType)
    
        # save suit
        identity = 'faceCardSuit/suit_'+str(i)
       
        writePath = os.path.normpath('elementLibrary/processed/'+identity+'.png')
        cv.imwrite(writePath,suitImgArr)
        # save value
        identity = 'faceCardVal/val_'+str(i)
    
        writePath = os.path.normpath('elementLibrary/processed/'+identity+'.png')
        cv.imwrite(writePath,valImgArr)        
        i += 1

    #  ===== hole cards ===== #
    path = 'elementLibrary/sorted/holeCard'
    DIR = os.path.normpath(path)
    imageList = [name for name in os.listdir(DIR)if os.path.isfile(os.path.join(DIR, name))]
    for imageName in imageList:
        readPath = os.path.normpath(path+'/'+imageName)
        imgArr = cv.imread(readPath,1)
        imgType = 'faceCard'
        (valImgArr,suitImgArr) = processImage(imgArr,imgType)
    
        # save suit
        identity = 'faceCardSuit/suit_'+str(i)
   
        writePath = os.path.normpath('elementLibrary/processed/'+identity+'.png')
        cv.imwrite(writePath,suitImgArr)
        # save value
        identity = 'faceCardVal/val_'+str(i)

        writePath = os.path.normpath('elementLibrary/processed/'+identity+'.png')
        cv.imwrite(writePath,valImgArr)        
        i += 1
        
    #  ===== stack ===== #
    path = 'elementLibrary/sorted/stack'
    DIR = os.path.normpath(path)
    i = 0
    imageList = [name for name in os.listdir(DIR)if os.path.isfile(os.path.join(DIR, name))]
    for imageName in imageList:
        readPath = os.path.normpath(path+'/'+imageName)
        imgArr = cv.imread(readPath,1)
        imgType = 'stack'

        # grab 1st digit and classify (numbers 1-9, A or S - 0 not an option for 1st digit)
        digitOne = processImage(imgArr,'stackCheck',returnBin=True)
        imageCat = classifyMultiImage(digitOne,'digit','digitTheta.csv')
        if imageCat == 'S' or imageCat == 'A':
            digitArr = processImage(imgArr,'stackCheck',returnBin=False)
            numDigits = 1
        else:
            (digitArr,numDigits) = processImage(imgArr,imgType)

        # save digits
        for j in range(numDigits):
            if numDigits>1:
                digitImgArr = digitArr[:,:,:,j]
            else:
                digitImgArr = digitArr[:,:,j]
            identity = 'stack/digit_'+str(i)
            writePath = os.path.normpath('elementLibrary/processed/'+identity+'.png')
            cv.imwrite(writePath,digitImgArr)
            i += 1

    # ===== not stack ===== #

    path = 'elementLibrary/sorted/stackNot'
    DIR = os.path.normpath(path)
    i = 0
    imageList = [name for name in os.listdir(DIR)if os.path.isfile(os.path.join(DIR, name))]
    for imageName in imageList:
        readPath = os.path.normpath(path+'/'+imageName)
        imgArr = cv.imread(readPath,1)
        imgType = 'stackNot'
        digitArr = processImage(imgArr,imgType)
        # save first digit only
        identity = 'stackNot/digit_'+str(i)
        writePath = os.path.normpath('elementLibrary/processed/'+identity+'.png')
        cv.imwrite(writePath,digitArr)
        i += 1
    """

    #  ===== bet left  ===== #
    path = 'elementLibrary/raw/betLeft'
    DIR = os.path.normpath(path)
    i = 0
    imageList = [name for name in os.listdir(DIR)if os.path.isfile(os.path.join(DIR, name))]
    for imageName in imageList:
        readPath = os.path.normpath(path+'/'+imageName)
        imgArr = cv.imread(readPath,1)
        imgType = 'betleft'
	print imageName
        (digitBinArr,numDigits) = processImage(imgArr,imgType)
	if numDigits == 0:
	    continue

        # save digits
        for j in range(numDigits):
            digitBin = digitBinArr[:,:,j]
	    digitImgArr = np.zeros((digitBin.shape[0],digitBin.shape[1],3),dtype='int32')
	    digitImgArr[:,:,0] = digitBin*255
	    digitImgArr[:,:,1] = digitBin*255
	    digitImgArr[:,:,2] = digitBin*255
	    identity = 'bet/digit_'+str(i)
            writePath = os.path.normpath('elementLibrary/processed/'+identity+'.png')
            cv.imwrite(writePath,digitImgArr)
            i += 1
    
    #  ===== bet right  ===== #
    path = 'elementLibrary/raw/betRight'
    DIR = os.path.normpath(path)
    #keep i from bet left
    imageList = [name for name in os.listdir(DIR)if os.path.isfile(os.path.join(DIR, name))]
    for imageName in imageList:
        readPath = os.path.normpath(path+'/'+imageName)
        imgArr = cv.imread(readPath,1)
        imgType = 'betright'
	print imageName
        (digitBinArr,numDigits) = processImage(imgArr,imgType)
	if numDigits == 0:
	    continue

        # save digits
        for j in range(numDigits):
            digitBin = digitBinArr[:,:,j]
	    digitImgArr = np.zeros((digitBin.shape[0],digitBin.shape[1],3),dtype='int32')
	    digitImgArr[:,:,0] = digitBin*255
	    digitImgArr[:,:,1] = digitBin*255
	    digitImgArr[:,:,2] = digitBin*255
	    identity = 'bet/digit_'+str(i)
            writePath = os.path.normpath('elementLibrary/processed/'+identity+'.png')
            cv.imwrite(writePath,digitImgArr)
            i += 1
        
# ===== run main ===== #
if __name__ == '__main__':
    main()










