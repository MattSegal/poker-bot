"""
https://docs.python.org/2/library/unittest.html
tests methods from the classImage module in the following order:
    testSingle

"""


import unittest
import numpy as np

from classImage import testSingle
class TestSingleTest(unittest.TestCase):
    def test_1(self):
	exampleArr=np.array([[1,1],[1,1]])  # m x n
	outcomeArr=np.array([1,1])	    # m x 1
	theta=np.array([0.5,0.5])	    # n x 1
	muArr=np.array([0])		    # m x 1
	sigmaArr=np.array([1])		    # m x 1
	calculated = testSingle(exampleArr,outcomeArr,theta,muArr,sigmaArr)
	expected = 100
	message = 'did not work'
	self.assertEqual(calculated,expected,message)
    def test_2(self):
	exampleArr=np.array([[2,2],[-1,-1]])  # m x n
	outcomeArr=np.array([1,0])	    # m x 1
	theta=np.array([0.5,0.5])	    # n x 1
	muArr=np.array([0,0])		    # m x 1
	sigmaArr=np.array([1,1])		    # m x 1
	calculated = testSingle(exampleArr,outcomeArr,theta,muArr,sigmaArr)
	expected = 100
	message = 'did not work'
	self.assertEqual(calculated,expected,message)
	

suite = unittest.TestLoader().loadTestsFromTestCase(TestSingleTest)
unittest.TextTestRunner(verbosity=2).run(suite)
