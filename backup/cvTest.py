from PIL import ImageGrab
import numpy as np
import matplotlib.pyplot as plt
import cv2 as cv

# take a screenshot
# img = ImageGrab.grab()

# use tenplate matching from OpenCV
# gotta install OpenCV tomorrow
# http://opencv-python-tutroals.readthedocs.org/en/latest/py_tutorials/py_imgproc/py_template_matching/py_template_matching.html

#OpenCV reads BGR not RGB
# 0 returns greyscale, 1 BGR, -1 BGRA
img = cv.imread('desktop.png',0)
print img.shape
template = cv.imread('league.png',0)
method = cv.TM_CCOEFF

result = cv.matchTemplate(img,template,method)
(minVal,maxVal,minLoc,maxLoc) = cv.minMaxLoc(result)

# make a rectangle
(w,h) = template.shape
topLeft = maxLoc
bottomRight = (topLeft[0]+w, topLeft[1]+h)
cv.rectangle(img,topLeft,bottomRight,255,2)



plt.figure()
plt.imshow(result,cmap = 'gray')
plt.show()
