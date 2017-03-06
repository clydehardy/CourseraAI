import sys
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import time
import warnings

from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier

from sklearn.model_selection import cross_val_score
from sklearn.model_selection import train_test_split
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import GridSearchCV

#from sklearn.preprocessing import MinMaxScaler
#from sklearn.preprocessing import StandardScaler
#from sklearn.pipeline import Pipeline
from sklearn import metrics

if __name__ == "__main__":
#usage #$ python3 problem1_3.py input1.csv output1.csv
    try:
        warnings.filterwarnings("ignore")

        possibles = globals().copy()
        possibles.update(locals())
        inputfile = sys.argv[1]
        outputfile = sys.argv[2]

        #lr = [0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1, 5, 10]
        #n_iter = 100

        filedata = pd.read_csv(inputfile)
        l,w = filedata.shape
        y=pd.DataFrame(filedata.iloc[0:l,w-1].values)
        X= pd.DataFrame(filedata.iloc[0:l,0:w-1].values)


        #a = filedata[filedata["label"]==1]
        #b = filedata[filedata["label"]==0]
        #plt.scatter(a["A"],a["B"], color='red', marker='o')
        #plt.scatter(b["A"],b["B"], color='blue', marker='x')
        #plt.show()

        X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.6, random_state=123)

        file = open(outputfile,"w")

        seq1_50 = np.arange(1,50,1)
        seq5_60 = np.arange(5,60,5)
        seq1_10 = np.arange(1,10,1)
        seq2_10 = np.arange(2,10,1)

        models=[]
        #SVM with Linear Kernel
        clfSVCLinearKernel = SVC()
        #svcLKparameters={'kernel':['linear'],'C':[0.1, 0.5, 1, 5, 10, 50, 100]}
        svcLKparameters={'kernel':['linear'],'C':[0.1]}
        models.append(["svm_linear",clfSVCLinearKernel,svcLKparameters])

        #SVM with Polynomial Kernel
        clfSVCPolyKernel = SVC()
        #svcPKparameters={'kernel':['poly'],'C':[0.1, 1, 3],'degree':[4, 5, 6],'gamma':[0.1, 1]}
        svcPKparameters={'kernel':['poly'],'C':[3],'degree':[5],'gamma':[1]}
        models.append(["svm_polynomial",clfSVCPolyKernel,svcPKparameters])

        #SVM with RBF Kernel
        clfSVCRBFKernel = SVC()
        #svcRBFKparameters={'kernel':['rbf'],'C':[0.1, 0.5, 1, 5, 10, 50, 100],'gamma':[0.1, 0.5, 1, 3, 6, 10]}
        svcRBFKparameters={'kernel':['rbf'],'C':[50],'gamma':[6]}
        models.append(["svm_rbf",clfSVCRBFKernel,svcRBFKparameters])

        #Logistic Regression
        clfLR = LogisticRegression()
        #lrParameters={'C':[0.1, 0.5, 1, 5, 10, 50, 100]}
        lrParameters={'C':[0.1]}
        models.append(["logistic",clfLR,lrParameters])

        #K-Nearest Neighbours
        clfKNN = KNeighborsClassifier()
        #knnParameters={'n_neighbors':seq1_50,'leaf_size':seq5_60}
        knnParameters={'n_neighbors':[1],'leaf_size':[5]}
        models.append(["knn",clfKNN,knnParameters])

        #Decision Trees
        clfDT = DecisionTreeClassifier()
        #dtParameters = {'max_depth':seq1_50,'min_samples_split':seq2_10}
        dtParameters = {'max_depth':[6],'min_samples_split':[2]}
        models.append(["decision_tree",clfDT,dtParameters])

        #Random Forest
        clfRF=RandomForestClassifier()
        #rfParameters = {'max_depth':seq1_50,'min_samples_split':seq2_10}
        rfParameters = {'max_depth':[28],'min_samples_split':[4]}
        models.append(["random_forest",clfRF,rfParameters])

        for model in models:
            gs = GridSearchCV( estimator = model[1], param_grid = model[2], scoring ='accuracy', cv = 5)
            gs = gs.fit(X_train, y_train[0])
            print( "{} : Best score {}".format(model[0],gs.best_score_))
            print( gs.best_params_)
            file.write("{},{},{}\n".format(model[0],gs.cv_results_['mean_train_score'][0],gs.best_score_))

      

        file.close()

    except Exception as e:
        print("Error occured: ")
        print(str(e))