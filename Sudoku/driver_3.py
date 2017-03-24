import sys
import argparse
import math
import numpy as np
import itertools
import copy
import time

def getcubedim(x):
    cubes = [[0,1,2],[3,4,5],[6,7,8]]
    for c in cubes:
        if x in c:
            return c

def getdomain(x,y,board):
    domdif = [1,2,3,4,5,6,7,8,9]
    domdif = list(np.setdiff1d(domdif,[board[i,j] for (i,j) in list(itertools.product(getcubedim(x),getcubedim(y)))]))
    domdif = list(np.setdiff1d(domdif,[value for i,value in np.ndenumerate(board[x,:])]))
    domdif = list(np.setdiff1d(domdif,[value for i,value in np.ndenumerate(board[:,y])]))
    #print(x,y,domdif)
    return domdif

def getqueue(board):
    Q = []
    for (x,y), value in np.ndenumerate(board):
        if value == 0:
            domdif = getdomain(x,y,board)
            if len(domdif) == 1:
                Q.append([[x,y],domdif])
    return Q

def getfullqueue(board):
    Q = []
    for (x,y), value in np.ndenumerate(board):
        if value == 0:
            domdif = getdomain(x,y,board)
            Q.append([[x,y],domdif])
    return sorted(Q, key=lambda x: len(x[1]))

def addones(board):
    while True:
        Q = []
        Q = getqueue(board)
        if len(Q) == 0:
            break
        for x in Q:
            board[x[0][0],x[0][1]] = x[1][0]
    return board

def validboard(brd, q):
    ones = [x[1][0] for x in q if len(x[1]) == 1]
    if len(ones) != len(set(ones)):
        #print("Failed: domain restricted to duplicate ones")
        return False
    if sum([1 for x in q if len(x[1]) == 0]) > 0:
        #print("Failed: domain restricted to 0")
        return False;
    for i in range(0,8):
        rl = list(filter(lambda x: x>0,list(brd[i,:])))
        if len(rl) != len(set(rl)):
            #print("Failed: duplicated values in row {}".format(list(brd[i,:])))
            return False
        cl = list(filter(lambda x: x>0,list(brd[:,i])))
        if len(cl) != len(set(cl)):
            #print("Failed: duplicated values in col {}".format(list(brd[:,i])))
            return False
    for c1 in [[0,1,2],[3,4,5],[6,7,8]]:
        for c2 in [[0,1,2],[3,4,5],[6,7,8]]:
            cube = [brd[i,j] for (i,j) in list(itertools.product(c1,c2))]
            if len(list(filter(lambda x: x>0,cube))) != len(set(list(filter(lambda x: x>0,cube)))):
                #print("Failed: duplicated values in cube {}".format(cube))
                return False

    return True

def backtrack(asign, board):
    btboard = copy.deepcopy(board)
    btboard[asign[0][0],asign[0][1]] = asign[1][0]
    btboard = addones(btboard)
    Queue = getfullqueue(btboard)
    if not validboard(btboard,Queue):
        return False, btboard
    if 0 not in btboard:
        return True, btboard
    else:
        #print("Queue len: {}".format(len(Queue)))
        #print("Num. Queue items: {}".format(sum([len(x[1]) for x in Queue])))
        #print(Queue)
        rtnbol = True
        for x in Queue:
            for y in x[1]:
                #print("Queue item: ",x[0][0],x[0][1],[y])
                rtnbol, rtnboard = backtrack([[x[0][0],x[0][1]],[y]],btboard)
                if rtnbol:
                    return rtnbol, rtnboard
            if rtnbol == False:
                return rtnbol,rtnboard
    return False, btboard


if __name__ == "__main__":
#usage #$ python driver.py <input_string>
#e.g. $ python driver.py 203007810750190402400002000900020705075908240802070001000700008506039074027800506
    try:
        possibles = globals().copy()
        possibles.update(locals())
        inputboard = sys.argv[1]
        file = open("output.txt","w")
        
        
        #for inputboard in open("sudokus_start.txt"):
            #starttime = time.time()
        inputboard = inputboard.replace("\n","")
        npboard = np.array(list(inputboard), dtype=int)
        fullboard = np.reshape(npboard,(9,9))
        domain = [1,2,3,4,5,6,7,8,9]
        X = []
        D = []
        C = []
        #print(fullboard)
        fullboard = addones(fullboard)
        #print(fullboard)
        if 0 in fullboard:
            if validboard(fullboard,getqueue(fullboard)):
                Q=[]
                #Backtracking search
                btboard = copy.deepcopy(fullboard)
                Q = getfullqueue(btboard)
                #print("Queue len: {}".format(len(Q)))
                #print("Num. Queue items: {}".format(sum([len(x[1]) for x in Q])))
                #print(Q)
                rtnbol = False
                rtnboard = [0]
                for x in Q:
                    for y in x[1]:
                        #print("Queue item: ",x[0][0],x[0][1],[y])
                        rtnbol, rtnboard = backtrack([[x[0][0],x[0][1]],[y]],btboard)
                        if rtnbol and 0 not in rtnboard:
                            #print("Board complete: {}".format(rtnboard))
                            break
                    if rtnbol and 0 not in rtnboard:
                        #print("Board complete")
                        #print("Time taken: {}".format(time.time() - starttime))
                        #print(''.join(str(e) for e in np.array(rtnboard.flat)))
                        file.write(''.join(str(e) for e in np.array(rtnboard.flat)))
                        file.write('\n')
                        break
            else:
                Print("Invalid board")
                print(''.join(str(e) for e in np.array(fullboard.flat)))
        else:
            #print("Board complete")
            #print(''.join(str(e) for e in np.array(fullboard.flat)))
            file.write(''.join(str(e) for e in np.array(fullboard.flat)))
            file.write('\n')
            
        file.close()

    except Exception as e:
        print("usage: driver_3.py <board>, please enter a valid board")
        print(str(e))