
import numpy as np
import matplotlib.pyplot as plt

# =============================================================================== #

def logisticRegression(X,y,plotResults=False):
    """
    X is expected to come with Xo already added ie X of dim (m,n+1)
    """
    numFeat = X.shape[1] # including bias
    # use gradient descent to find theta
    initialTheta    = np.zeros(numFeat)
    alpha           = 1
    lam             = 1
    numIters        = 100
    
    theta = gradientDescent(X, y, initialTheta, alpha, lam, numIters, plotResults)

    return theta

# =============================================================================== #

def gradientDescent(X, y, theta, alpha, lam, numIters, plotResults = False):
    """
    m is number of training examples
    n is number of features
    """
    # Initialize some useful values
    [m,n] = X.shape
    J_history = np.zeros(numIters)
    dJ = np.zeros(n)

    for itr in range(numIters):

        (J,dJ) = costFunction(theta,X,y,lam)

        theta = theta - alpha * dJ;

        J_history[itr] = J

    if plotResults:
        plt.plot(J_history)
        plt.ylabel('Cost Function')
        plt.xlabel('Number of Iterations')
        plt.show()

    return theta

# =============================================================================== #

def costFunction(theta,X,y,lam):

    m = len(y)          # number of training examples
    mf = float(m)
    n = theta.size      # number of parameters

    # output variables
    J = 0
    grad = np.zeros(n);

    # compute gradient of cost function
    z = np.dot(X,theta)
    hx = sigmoid(z)
    for j in range(n):
        grad[j] =  ((1/mf)*(hx - y)*X[:,j] ).sum()
        if j > 0:
            grad[j] += lam*theta[j]/mf
            
    # compute cost of theta
    pos = - y*np.log(hx)
    neg = - (1-y)*np.log(1-hx)
    J = ( (1/mf)*(pos + neg) ).sum() + (lam/2/mf)*(theta[1:]*theta[1:]).sum()

    return J , grad

# =============================================================================== #

def sigmoid(z):
    return 1.0/(1.0+np.exp(-z))

# =============================================================================== #

def featureNormalize(X):
    """
    X is of dimensions (m,n) with m examples and n features
    normalizes X and returns mu and sigma for each feature
    returns X, mu, sigma with n+1 rows, with first row being bias
    """
    [m,n]   = X.shape
    X_norm  = np.zeros((m,n+1)) 
    mu =    np.zeros(n+1)
    sigma = np.zeros(n+1)

    X_norm[:,1:]    = X.copy()  # X1 to Xn
    X_norm[:,0]     = 1         # Xo = 1 for all examples
    mu[0]           = 0         # mu0 = 0
    sigma[0]        = 1         # sigma0 = 0

    for feat in range(1,n+1):
        mu[feat]    = np.mean(X[:,feat-1])
        sigma[feat] = np.std(X[:,feat-1])
        for i in range(m):
            X_norm[i,feat] = (X[i,feat-1] - mu[feat]) / sigma[feat]

    return X_norm, mu, sigma

# =============================================================================== #
