import sys

# hopefully import stuff from sikuli
#sys.path.append("C:\Users\Matthew\Documents\SikuliX\sikulixapi.jar") # add sikuli (hopefully)
import org.sikuli.basics.SikulixForJython
from sikuli import *

print '===== Sikuli Loaded ===== \n'

def main():
    #target = Image.create('options.png')
    #move(target)
    #targetExists = exists(target)
    #print 'target exists',targetExists
    #print 'match score',isMatch(targetExists)

    #while True:
    readStack()

def readStack()
    highlight"red"


def move(img):
    """
    moves mouse an image in the DEFAULT region, if the region is present
    returns True for success, False for failure
    """
    try:
        targetMatch = find(img)
        loc = targetMatch.getTarget()
        Mouse.move(loc)
    except:
        print "not found"

def isMatch(m):
    """
    returns true if match >0.5
    """
    matchScore = m.getScore()
    if matchScore > 0.5:
        return True
    else:
        return False




if __name__ == '__main__':
     main()


    
