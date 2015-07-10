from PIL import Image
import os.path
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
"""http://pythonprogramming.net/image-recognition-python/"""

def createExamples():
    numberArrayExamples = open('numArEx.txt','a')
    numbersWeHave = range(0,10)
    versionsWeHave = range(1,10)

    for eachNum in numbersWeHave:
        for eachVersion in versionsWeHave:
            # define image path
            path = 'C:/PartyTime/imageRecognition/images/numbers/'
            imgFilePath = path+str(eachNum)+'.'+str(eachVersion)+'.png'
            imgFilePath = os.path.normpath(imgFilePath)
            # open image
            exImg = Image.open(imgFilePath)
            exImgArr = np.array(exImg)
            exImgArrList = str(exImgArr.tolist())
            lineToWrite = str(eachNum)+'::'+exImgArrList+'\n'
            numberArrayExamples.write(lineToWrite)
            

def threshold(imgArray):
    """ coverts every pixel to black or white"""
    balanceArray = []
    newArray = imgArray
    
    for eachRow in imgArray: # iterates over rows
        for eachPix in eachRow:
            pix = eachPix[:3].astype('int64')
            avgNum = reduce(lambda x,y:x+y,pix)/3
            balanceArray.append(avgNum)
    balance =  reduce(lambda x,y:(x+y),balanceArray)/len(balanceArray)

    for eachRow in newArray:
        for eachPix in eachRow:
            pix = eachPix[:3].astype('int64')
            if reduce(lambda x,y:(x+y),pix)/3 > balance:
                eachPix[0] = 255
                eachPix[1] = 255
                eachPix[2] = 255
                eachPix[3] = 255
            else:
                eachPix[0] = 0
                eachPix[1] = 0
                eachPix[2] = 0
                eachPix[3] = 255
    return newArray

def whatNumIsThis(filePath):
    matchedArray = []
    # pixel by pixel search, check if
    loadExamples =open('numArEx.txt','r').read()
    loadExamples = loadExamples.split('\n') # split into list on every newline

    img = Image.open(filePath)
    imgArr = np.array(img)
    imgList = imgArr.tolist()

    inQuestion = str(imgList)

    for eachExample in loadExamples:
        if len(eachExample) > 3: # for blank line at the end of loadExamples string
            splitExample = eachExample.split('::')
            currentNum = splitExample[0]
            currentArr = splitExample[1]
            # if target image dimensions were variable then you would
            # have to normalise the image to a standard size

            eachPixEx = currentArr.split('],')
            eachPixInQuestion = inQuestion.split('],')

            count = 0
            while count < len(eachPixEx):
                if eachPixEx[count] == eachPixInQuestion[x]:
                    matchedArray.append(int(currentNum))
                count += 1
    print matchedArr
    x = Counter(matchedArr) # creates a dict that counts the occurrence of each element
    
    # for off centre images you could do one of two things
    # (1) write a centring function to centre the image to a standardized position
    # (2) introduce a set of offset images into your training set
    # (3) blur the training set so that a match offset by 1 pixel is matched 50% 
            






    

        

