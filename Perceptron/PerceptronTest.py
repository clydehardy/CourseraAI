import numpy as np
import pandas as pd
import sys

if __name__ == "__main__":
#usage #$ python3 problem1_3.py input1.csv output1.csv
    try:
        possibles = globals().copy()
        possibles.update(locals())
        inputfile = sys.argv[1]
        outputfile = sys.argv[2]

        eta =0.3
        #n_iter = 50
        w_ = np.array([0.5,0.5,0.5])
        errors_ = []

        #inputfile = "input1.csv"
        #outputfile = "output1.csv"
        file = open(outputfile,"w")

        filedata = pd.read_csv(inputfile,header=None)
        l,w = filedata.shape
        y=filedata.iloc[0:l,w-1].values
        X=filedata.iloc[0:l,0:w-1].values

        runcount = 0
        errchk = False
        while(errchk == False):
            runcount += 1
            errors = 0
            for xi, target in zip(X,y):
                dp = np.dot(xi, w_[1:]) + w_[0]
                predict = np.where(dp >= 0.0, 1, -1)
                update = eta * (target - predict)
                w_[1:] += update * xi
                w_[0] += update
                errors += int(update != 0.0)
    
            file.write("{},{},{}\n".format(w_[1],w_[2],w_[0]))
            #errors_.append(errors)
            #print("errors {}".format(errors))
            if (errors == 0 or runcount == 10000):
                errchk = True
                #print(w_[1],w_[2],w_[0])

        file.close()
        
    except Exception as e:
        print("Error occured: ")
        print(str(e))