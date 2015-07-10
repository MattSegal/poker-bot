import numpy as np
import mahotas as mh

def readStack(imgArr):
    """
    this is a docstring
    """
    img = RGBToBinary(imgArr)
    #binaryToRGB(img,'inputFilt.png')

    # ===== throw out unwanted pixels ===== #
    # img in form img[row,column]
    # throw out pixels below row and pixels more than 10 above row
    rowSum = img.sum(axis=1)
    print rowSum
    bot = np.max(np.where(rowSum>2))+1
    top = bot-10 # hopefully this is right
    img = img[top:bot,:]
    # find first column with white text
    columnSum = img.sum(axis=0)
    left  = np.min(np.where(columnSum>0))
    right = np.max (np.where(columnSum>0))+1
    img = img[:,left:right]
    #binaryToRGB(img,'digits.png')

    # ===== seperate out digits ===== #
    # for now assume a 10x6 pixel size

    # grab first digit
    digits = img[0:10,0:6]
    img = img[:,6:]

    numDigits = 1
    digitCol = np.array([])

    # comma vector
    comma = np.array([0,0,0,0,0,0,0,0,1,1])
    space = np.array([0,0,0,0,0,0,0,0,0,0])

    for i in range(len(img[0,:])):
        prevCommaOrSpace = (img[:,i-1]==comma).all() or (img[:,i-1]==space).all()
        thisCommaOrSpace = (img[:,i]==comma).all() or (img[:,i]==space).all()
        if prevCommaOrSpace and not thisCommaOrSpace:
            numDigits += 1
            digitCol = np.append(digitCol,i)

    for i in digitCol:
            newDigit = img[0:10,i:i+6]
            digits = np.dstack((digits,newDigit))

    stack = 0
    for i in range(numDigits):
        thisDigit = whichNumber(np.array(digits[:,:,i]))
        if thisDigit == 10: # player all in
            stack = 0
            break
        stack += (10**(numDigits-i-1))*thisDigit
        #binaryToRGB(digits[:,:,i],str(i+1)+'.png')
    return stack


def whichNumber(img):
    profile = np.loadtxt('digitProfile.txt',dtype='int8',delimiter=',')
    digitList = profile[:,0]
    profile = profile[:,1:]
    imgSum = img.sum(axis=0)
    #print imgSum
    matchVector = (profile == imgSum).sum(axis=1)
    digitIndex = np.where(matchVector==matchVector.max())[0][0]
    digit = digitList[digitIndex]
    return digit

def binaryToRGB(img,name):
    """
    output final image matrix as an RGB image
    img is a nxm matrix of 1s and 0s
    name is the save name eg 'test.png'
    """
    n = img.shape[0]
    m = img.shape[1]
    imgRGB = np.zeros((n,m,3),dtype='int8')
    imgRGB[:,:,0]  = img*255
    imgRGB[:,:,1]  = img*255
    imgRGB[:,:,2]  = img*255
    mh.imsave(name, imgRGB)

def RGBToBinary(img):
    """
    output is binary matrix of 1 - white 0 - black
    filters RGB .png image (does not accept RGBA)
    """
    
    # filter using otsu method
    T = mh.thresholding.otsu(img)
    img[img<T] = 0
    img[img>=T] = 1

    # convert nxmx3 RGB matrix to nxm binary matrix
    imgSum = img.sum(axis=2)
    inverseColors = img[imgSum==3].size >  img[imgSum<3].size
    if inverseColors:
        img[imgSum<3] = 1
        img[imgSum==3] = 0
    else:    
        img[imgSum<3] = 0
        img[imgSum==3] = 1
    
    img = img[:,:,0]
    return img

import sys
if __name__ == '__main__':
    if len(sys.argv) > 1:
        fileName = sys.argv[1].strip()
        readStack(fileName)
