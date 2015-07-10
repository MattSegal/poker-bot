import numpy as np
import mahotas as mh

def main():
    whichNumberFile('10_0.png')


def whichNumber(img):
    profile = np.loadtxt('digitProfile.txt',dtype='int8',delimiter=',')
    digitList = profile[:,0]
    profile = profile[:,1:]
    imgSum = img.sum(axis=0)
    #print imgSum
    matchVector = (profile == imgSum).sum(axis=1)
    digitIndex = np.where(matchVector==matchVector.max())[0][0]
    digit = digitList[digitIndex]
    print 'digit is ',digit

def whichNumberFile(fileName):
    profile = np.loadtxt('digitProfile.txt',dtype='int8',delimiter=',')
    digitList = profile[:,0]
    profile = profile[:,1:]
    #print profile
    img = mh.imread(fileName)
    img = img[:,:,0:3] # remove alpha from RGB
    img = RGBToBinary(img,invert=False)
    imgSum = img.sum(axis=0)
    #print imgSum
    matchVector = (profile == imgSum).sum(axis=1)
    digitIndex = np.where(matchVector==matchVector.max())[0][0]
    digit = digitList[digitIndex]
    print 'digit is ',digit
    

def createProfile():
    # ===== import image ===== #
    numImagesList = [5,2,3,6,3,1,3,3,7,9,2] # 10 is 'A'
    profile = np.zeros((len(numImagesList),7),dtype='int8')
    for n in range(len(numImagesList)):
        profile[n,0] = n
        imgName = str(n)
        numImages = numImagesList[n]
        digits = np.zeros((10,6,numImages),dtype='int8')

        imgSum = 0
        for i in range(numImages):
            fileName = imgName+'_'+str(i)+'.png'
            img = mh.imread(fileName)
            img = img[:,:,0:3] # remove alpha from RGB
            img = RGBToBinary(img,invert=False)
            #binaryToRGB(img,imgName+'_'+str(i)+'_COPY.png')
            digits[:,:,i] = img
            imgSum += img.sum(axis=0)
        imgSum = imgSum/numImages
        profile[n,1:] = imgSum
        #print 'digit ',n,' has sum',imgSum
    np.savetxt('digitProfile.txt',profile,fmt='%d',delimiter=',')

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

def RGBToBinary(img,invert=True):
    """
    output is binary matrix of 1 - white 0 - black
    filters RGB .png image (does not accept RGBA)
    """
    alreadyFiltered = (img==255).sum() + (img==0).sum() == img.size
    if not alreadyFiltered:
        # filter using otsu method if not already filtered
        T = mh.thresholding.otsu(img)
        img[img<T] = 0
        img[img>=T] = 1
    else:
        img[img==255] = 1

    # convert nxmx3 RGB matrix to nxm binary matrix
    imgSum = img.sum(axis=2)
    inverseColors = img[imgSum==3].size >  img[imgSum<3].size
    if inverseColors and invert:
        img[imgSum<3] = 1
        img[imgSum==3] = 0
    else:    
        img[imgSum<3] = 0
        img[imgSum==3] = 1
    
    img = img[:,:,0]
    return img

import sys
if __name__ == '__main__':
    #if len(sys.argv) > 1:
    main()
