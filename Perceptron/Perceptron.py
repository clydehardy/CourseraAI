import numpy as np
import pandas as pd
import sys

class Perceptron(object):
    """Python Machine Learning, Sebastian Raschka
    Perceptron classifier.

    Parameters
    ------------
    eta : float
        Learning rate (between 0.0 and 1.0)
    n_iter : int
        Passes over the training dataset

    Attributes
    ------------
    w_ : 1d-array
        Weights after fitting.
    errors_ : list
        Number of misclassifications in every epoch.

    """
    def __init__(self, eta=0.3, n_iter=10):
        self.eta =eta
        self.n_iter = n_iter

    def fit(self, X, y):
        """Fit training data.

        Parameters
        --------------
        X : {array-like}, shape = [n_samples, n_features]
            Training vectors, where n_samples
            is the number of samples and 
            n_features is the number of features.
        y : array-like, shape = [n_samples]
            Target values.

        Returns
        ---------------
        self : object
        """

        #self.w_ = np.zeros(1 + X.shape[1])
        self.w_ = np.array([0.5,0.5,0.5])
        self.errors_ = []

        for _ in range(self.n_iter):
            errors = 0
            for xi, target in zip(X,y):
                update = self.eta * (target - self.predict(xi))
                self.w_[1:] += update * xi
                self.w_[0] += update
                errors += int(update != 0.0)
            self.errors_.append(errors)
        return self

    def net_input(self, X):
        """Calculate net input"""
        return np.dot(X, self.w_[1:]) + self.w_[0]

    def predict(self, X):
        """Return class label after unit step"""
        return np.where(self.net_input(X) >= 0.0, 1, -1)

if __name__ == "__main__":
#usage #$ python3 problem1_3.py input1.csv output1.csv
    try:
        possibles = globals().copy()
        possibles.update(locals())
        inputfile = sys.argv[1]
        outputfile = sys.argv[2]
        #sys.argv[2].split(",")
        
        #inputfile = "input1.csv"
        #outputfile = "output1.csv"

        filedata = pd.read_csv(inputfile,header=None)
        l,w = filedata.shape
        y=filedata.iloc[0:l,w-1].values
        X=filedata.iloc[0:l,0:w-1].values

        perceptron = Perceptron()
        rtn = perceptron.fit(X,y)

        print(rtn.w_)
        file = open(outputfile,"w")
        file.write("{}\n".format(rtn.w_))
        file.close()
    except Exception as e:
        print("Error occured: ")
        print(str(e))
