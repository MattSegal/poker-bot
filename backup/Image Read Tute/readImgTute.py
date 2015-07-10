import numpy as np
from matplotlib import pylab
from matplotlib import image
import mahotas as mh

#http://pythonvision.org/basic-tutorial/

dna = mh.imread('dna.jpeg')
print dna.shape
print dna.dtype
print dna.max()
print dna.min()
dnaFilt = mh.gaussian_filter(dna,8)
dnaFilt = dnaFilt.astype('uint8') # convert float32 to int8
T = mh.thresholding.otsu(dnaFilt) # threshold vector

pylab.figure()
pylab.gray()
pylab.imshow(dnaFilt.squeeze()>T)
pylab.show()

