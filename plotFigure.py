import matplotlib.pyplot as plt
import numpy as np

def plotFigure(img,img2=np.array([]),BGR=True):
    
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

def subPlotFigure(imgList,numPlots):
    for i in range(numPlots):
        img = imgList[i]
        img = img[:, :, ::-1].copy()
        plt.subplot(3,2,i+1)
        plt.imshow(img,interpolation='none')
    plt.show()

def plotPlayerItem(item,table,numPlayers):
    """ plots all the images of a single item for all players"""
    playerList = ['one','two','three','four','five','six']
    imgList = [img1,img2,img3,img4,img5,img6] = [0,0,0,0,0,0]
    for i in range(numPlayers):
        player = playerList[i]
        imgList[i] = table[player][item].img
    subPlotFigure(imgList,numPlayers)

def plotAllPlayerItems(table,numPlayers):
    playerList = ['one','two','three','four','five','six']
    itemList = ['name','stack','cards','bet','holeOne','holeTwo','bubble','dealer','holeCheck']
    numItems = 9
    # row, col, rowspan, colspan
    itemPlot = [(0,0,1,2),(1,0,1,2),(0,2,1,1),(2,0,2,2),(0,3,2,1),(0,4,2,1),(2,4,1,1),(1,2,1,1),(2,3,1,1)]
    for i in range(numPlayers):
        player = playerList[i]
        plt.figure()
        for j in range(numItems):
            item = itemList[j]
            img = table[player][item].img
            img = img[:, :, ::-1].copy()
        
            plt.subplot2grid((4,5), (itemPlot[j][0],itemPlot[j][1]), rowspan=itemPlot[j][2] ,colspan=itemPlot[j][3])
            plt.imshow(img,interpolation='none')

    plt.show()
