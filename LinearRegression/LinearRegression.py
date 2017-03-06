import numpy as np
import pandas as pd
import sys
import matplotlib.pyplot as plt

def compute_cost(X, y, b_):
    n = len(y)
    t=(np.matrix(X)*np.matrix(b_))-np.matrix(y).transpose()
    t=np.array(t)**2
    return (sum(t))/(2*n)

def gradient_descent(X,y,b_,alpha):
    n = len(y)
    t = (np.matrix(X)*np.matrix(b_))-np.matrix(y).transpose()
    s = np.matrix(X).transpose()
    grad = alpha*((s*t)/n)
    return b_ - grad


if __name__ == "__main__":
#usage #$ python3 problem1_3.py input1.csv output1.csv
    try:
        possibles = globals().copy()
        possibles.update(locals())
        inputfile = sys.argv[1]
        outputfile = sys.argv[2]

        lr = [0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1, 5, 10]
        n_iter = 100

        filedata = pd.read_csv(inputfile,header=None)
        l,w = filedata.shape
        y=filedata.iloc[0:l,w-1].values
        X=filedata.iloc[0:l,0:w-1].values

        mu1 = np.mean(X[:,0])
        sd1 = np.std(X[:,0])
        mu2 = np.mean(X[:,1])
        sd2 = np.std(X[:,1])

        X[:,0] = (X[:,0]-mu1)/sd1
        X[:,1] = (X[:,1]-mu2)/sd2
        X = pd.concat([pd.DataFrame(np.ones([len(X),1])),pd.DataFrame(X)], axis=1)

        file = open(outputfile,"w")

        for a in lr:
            #print("eta : {}".format(a))
            costhist = np.zeros(n_iter)
            b_ = np.zeros([3, 1])
            for i in range(n_iter):
                b_ = gradient_descent(X, y, b_, a)
                costhist[i] = compute_cost(X,y,b_)
            file.write("{},{},{},{},{}\n".format(a,n_iter,b_[0,0],b_[1,0],b_[2,0]))
            #plt.plot(costhist)
            #plt.show()

        my_eta = 0.6
        my_iter = 80
        #print("eta : {}".format(my_eta))
        costhist = np.zeros(my_iter)
        b_ = np.zeros([3, 1])
        for i in range(my_iter):
            b_ = gradient_descent(X, y, b_, my_eta)
            costhist[i] = compute_cost(X,y,b_)
        file.write("{},{},{},{},{}\n".format(my_eta,my_iter,b_[0,0],b_[1,0],b_[2,0]))
        #plt.plot(costhist)
        #plt.show()

        file.close()

    except Exception as e:
        print("Error occured: ")
        print(str(e))