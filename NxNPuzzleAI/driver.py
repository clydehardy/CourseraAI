import sys
import argparse
import math
import ast as alit
#import Board as bd
import os
import psutil
import time
import cProfile
from operator import itemgetter

def getMD(board):
    idx=board.index(0)
    md = [(abs(int(board.index(x)/3)-int(x/3))+abs(int(board.index(x)%3)-int(x%3))) for x in board]
    md[idx] = 0
    return sum(md)

def get_paths(board,reverse_order = False):
        idx = board.index(0)
        size = 3 #int(math.sqrt(len(board)))
        #self.no_calls_get_paths += 1
        paths = []
        #top = list(range(0,self._size,1))
        #left = list(range(0,len(self._image),self._size))
        #right = list(range(self._size-1,len(self._image),self._size))
        #bottom = list(range(len(self._image)-self._size,len(self._image),1))
        app = paths.append
        #cpy = board.copy

        if not (idx in (0,1,2)):# top: 
            timage = board[:]
            timage[idx-size], timage[idx] = timage[idx],timage[idx-size]
            app([timage,["Up"],getMD(timage),1])
        
        if not (idx in (6,7,8)): #bottom:
            timage = board[:]
            timage[idx+size], timage[idx] = timage[idx],timage[idx+size]      
            app([timage,["Down"],getMD(timage),2])
        
        if not (idx in (0,3,6)): #left:
            timage = board[:]
            timage[idx-1], timage[idx] = timage[idx],timage[idx-1] 
            app([timage,["Left"],getMD(timage),3])
        
        if not (idx in (2,5,8)):#right:
            timage = board[:]
            timage[idx+1], timage[idx] = timage[idx],timage[idx+1]            
            app([timage,["Right"],getMD(timage),4])

        #self.no_get_paths_rtn += len(paths)
        if(reverse_order):
            paths.reverse()
        return paths

def getpath(l,parent,path):
    for o in l:
        if parent==0:
            return path
        if o[2]==parent:
            path = o[1]+path
            parent=o[3]
    return path


def bfs(startBoard,goalBoard):
    start_time = time.time()
    max_depth = 0
    max_fringe = 0
    nodes_expanded = 0
    nodes_expanded2 = 0
    nodes_expanded3 = 0
    frontier = []
    #b = bd.Board(startBoard,[],0,0)
    frontier.append([startBoard,[],0,0,1])
    explored = []
    unionset = set()
    unionset.add(str(startBoard))

    while (len(frontier) > 0):
        max_fringe = max(len(frontier),max_fringe)
        state = frontier.pop(0)
        explored.append(state)

        if (state[0] == goalBoard):
            path = getpath(reversed(explored),state[3],state[1])
            p = psutil.Process(os.getpid())
            mem = p.memory_info()[0]/float(2 ** 20)
            output_msg = "path_to_goal: {}\n".format(path)
            output_msg += "cost_of_path: {}\n".format(len(path))
            output_msg += "nodes_expanded: {}\n".format(nodes_expanded)
            output_msg += "fringe_size: {}\n".format(len(frontier))
            output_msg += "max_fringe_size: {}\n".format(max_fringe)
            output_msg += "search_depth: {}\n".format(state[4]-1)
            output_msg += "max_search_depth: {}\n".format(max_depth-1)
            output_msg += "running_time: {}\n".format(time.time() - start_time)
            output_msg += "max_ram_usage: {}\n".format(mem)
            return state, output_msg

        nodes_expanded += 1

        for o in get_paths(state[0],False):
            nodes_expanded2 += 1
            timage = str(o[0])
            if not (timage in unionset):
                nodes_expanded3 += 1
                frontier.append([o[0],o[1],nodes_expanded3,state[2],state[4]+1])
                max_depth = max(state[4]+1, max_depth)
                unionset.add(timage)


    return [startBoard,[]], ""

def dfs(startBoard,goalBoard):
    start_time = time.time()
    max_depth = 0
    max_fringe = 0
    nodes_expanded = 0
    nodes_expanded2 = 0
    nodes_expanded3 = 0
    frontier = []
    #b = bd.Board(startBoard,[],0,0)
    frontier.append([startBoard,[],0,0,1])
    explored = []
    unionset = set()
    unionset.add(str(startBoard))

    while (len(frontier) > 0):
        max_fringe = max(len(frontier),max_fringe)
        state = frontier.pop()
        explored.append(state)

        if (state[0] == goalBoard):
            path = getpath(reversed(explored),state[3],state[1])
            p = psutil.Process(os.getpid())
            mem = p.memory_info()[0]/float(2 ** 20)
            output_msg = "path_to_goal: {}\n".format(path)
            output_msg += "cost_of_path: {}\n".format(len(path))
            output_msg += "nodes_expanded: {}\n".format(nodes_expanded)
            output_msg += "fringe_size: {}\n".format(len(frontier))
            output_msg += "max_fringe_size: {}\n".format(max_fringe)
            output_msg += "search_depth: {}\n".format(state[4]-1)
            output_msg += "max_search_depth: {}\n".format(max_depth-1)
            output_msg += "running_time: {}\n".format(time.time() - start_time)
            output_msg += "max_ram_usage: {}\n".format(mem)
            return state, output_msg

        nodes_expanded += 1

        for o in get_paths(state[0],True):
            nodes_expanded2 += 1
            timage = str(o[0])
            if not (timage in unionset):
                nodes_expanded3 += 1
                frontier.append([o[0],o[1],nodes_expanded3,state[2],state[4]+1])
                max_depth = max(state[4]+1, max_depth)
                unionset.add(timage)


    return [startBoard,[]], ""


def ast(startBoard,goalBoard):
    start_time = time.time()
    max_depth = 0
    max_fringe = 0
    nodes_expanded = 0
    nodes_expanded2 = 0
    nodes_expanded3 = 0
    frontier = []
    #b = bd.Board(startBoard,[],0,0)
    frontier.append([startBoard,[],0,0,1,getMD(startBoard),0])
    explored = []
    unionset = set()
    unionset.add(str(startBoard))

    while (len(frontier) > 0):
        max_fringe = max(len(frontier),max_fringe)
        frontier = sorted(frontier,key=itemgetter(5,6))
        state = frontier.pop(0)
        explored.append(state)

        if (state[0] == goalBoard):
            path = getpath(reversed(explored),state[3],state[1])
            p = psutil.Process(os.getpid())
            mem = p.memory_info()[0]/float(2 ** 20)
            output_msg = "path_to_goal: {}\n".format(path)
            output_msg += "cost_of_path: {}\n".format(len(path))
            output_msg += "nodes_expanded: {}\n".format(nodes_expanded)
            output_msg += "fringe_size: {}\n".format(len(frontier))
            output_msg += "max_fringe_size: {}\n".format(max_fringe)
            output_msg += "search_depth: {}\n".format(state[4]-1)
            output_msg += "max_search_depth: {}\n".format(max_depth-1)
            output_msg += "running_time: {}\n".format(time.time() - start_time)
            output_msg += "max_ram_usage: {}\n".format(mem)
            return state, output_msg

        nodes_expanded += 1

        for o in get_paths(state[0],True):
            nodes_expanded2 += 1
            timage = str(o[0])
            if not (timage in unionset):
                nodes_expanded3 += 1
                frontier.append([o[0],o[1],nodes_expanded3,state[2],state[4]+1,state[5]+o[2],o[3]])
                max_depth = max(state[4]+1, max_depth)
                unionset.add(timage)


    return [startBoard,[]], ""

def ida(startBoard,goalBoard):
    start_time = time.time()
    max_depth = 0
    max_fringe = 0
    nodes_expanded = 0
    nodes_expanded2 = 0
    nodes_expanded3 = 0
    frontier = []
    #b = bd.Board(startBoard,[],0,0)
    frontier.append([startBoard,[],0,0,1,getMD(startBoard),0])
    explored = []
    unionset = set()
    unionset.add(str(startBoard))

    while (len(frontier) > 0):
        max_fringe = max(len(frontier),max_fringe)
        frontier = sorted(frontier,key=itemgetter(4,5,6))
        state = frontier.pop(0)
        explored.append(state)

        if (state[0] == goalBoard):
            path = getpath(reversed(explored),state[3],state[1])
            p = psutil.Process(os.getpid())
            mem = p.memory_info()[0]/float(2 ** 20)
            output_msg = "path_to_goal: {}\n".format(path)
            output_msg += "cost_of_path: {}\n".format(len(path))
            output_msg += "nodes_expanded: {}\n".format(nodes_expanded)
            output_msg += "fringe_size: {}\n".format(len(frontier))
            output_msg += "max_fringe_size: {}\n".format(max_fringe)
            output_msg += "search_depth: {}\n".format(state[4]-1)
            output_msg += "max_search_depth: {}\n".format(max_depth-1)
            output_msg += "running_time: {}\n".format(time.time() - start_time)
            output_msg += "max_ram_usage: {}\n".format(mem)
            return state, output_msg

        nodes_expanded += 1

        for o in get_paths(state[0],True):
            nodes_expanded2 += 1
            timage = str(o[0])
            if not (timage in unionset):
                nodes_expanded3 += 1
                frontier.append([o[0],o[1],nodes_expanded3,state[2],state[4]+1,state[5]+o[2],o[3]])
                max_depth = max(state[4]+1, max_depth)
                unionset.add(timage)


    return [startBoard,[]], ""
 
if __name__ == "__main__":
#usage #$ python driver.py <method> <board>
#$ python driver.py bfs 0,8,7,6,5,4,3,2,1
    try:
        #possibles = globals().copy()
        #possibles.update(locals())
        #method = possibles.get(sys.argv[1])
        #board = sys.argv[2].split(",")
        #board = [int(x) for x in board]
        #result, outmsg = method(board,[0,1,2,3,4,5,6,7,8])
        
        #cProfile.run("dfs([1,2,5,3,4,0,6,7,8],[0,1,2,3,4,5,6,7,8])")
        #cProfile.run("get_paths([1,2,5,3,4,0,6,7,8],[], True)")

        #profile = LineProfiler(get_paths([1,2,5,3,4,0,6,7,8],[], True))
        #profile.print_stats()

        result, outmsg = bfs([1,2,5,3,4,0,6,7,8],[0,1,2,3,4,5,6,7,8])
        print(result[0],result[1])
        print(outmsg)
        file = open("output.txt","w")
        file.write(outmsg)
        file.close()
    except Exception as e:
        print("driver.py <method> <board>")
        print(str(e))