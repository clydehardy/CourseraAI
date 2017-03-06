from random import randint
from BaseAI_3 import BaseAI
from Grid_3 import Grid
import math
from copy import deepcopy

actionDic = {
    0: "UP",
    1: "DOWN",
    2: "LEFT",
    3: "RIGHT"
}
 
class PlayerAI(BaseAI):
    def CalcScore(self,grid):
        gmap = deepcopy(grid.map)
        #numzeros = 0
        rownzeros = [len(list(filter((0).__ne__,l))) for l in gmap]
        numzeros = 16-sum(rownzeros)

        f=0.9
        tot = 0 
        if rownzeros[0] == 4:
            tot += 600

        slist = gmap[0]+gmap[1]+gmap[2]+gmap[3]
        if slist[0] == max(slist):
            tot += 4000
        if slist[0]>=slist[1] and slist[1]>=slist[2] and slist[2]>=slist[3] and slist[0]>=slist[4] and slist[1] > slist[4] and slist[4] >= slist[5] and slist[5] >= slist[6] and slist[6]>=slist[7] and slist[1] >= slist[5] and slist[2] >= slist[6] and slist[4] != 0:
            tot += 4000

        tot += sum([slist[i]*f**i for i in range(len(slist))])*10

        if gmap[0][0] != 0 and gmap[1][0] != 0 and gmap[2][0] != 0 and gmap[3][0] != 0:
            tot += 10

        if numzeros < 8 and slist[0] >= 512:
            numzeros = numzeros*100
        else:
            numzeros = numzeros*10 

        if rownzeros[0] == 4 and rownzeros[3] == 0:
            if rownzeros[1] == 3 and rownzeros[2] == 0:
                zidx = gmap[1].index(0)
                chklst = [[0,zidx]]
                if zidx != 0:
                    chklst.append([1,zidx-1])
                if zidx != 3:
                    chklst.append([1,zidx+1])
                chk = [gmap[l[0]][l[1]] for l in chklst]
                if not all(x in chk for x in [2,4]):
                    tot -= 6000
            if rownzeros[1] == 4 and rownzeros[2] == 3:
                zidx = gmap[2].index(0)
                chklst = [[1,zidx]]
                if zidx != 0:
                    chklst.append([2,zidx-1])
                if zidx != 3:
                    chklst.append([2,zidx+1])
                chk = [gmap[l[0]][l[1]] for l in chklst]
                if not all(x in chk for x in [2,4]):
                    tot -= 6000

        return numzeros+tot

    def minplay(self,grid,alpha,beta,level):
        level -= 1
        score = beta
        if level == 0:
            score = self.CalcScore(grid)
            #print('score min0',score,0,alpha, 0,beta, 'level'+str(level))
            #print('             min0score',score)
        else:
            cgrid = grid.clone()
            cells = cgrid.getAvailableCells()
            if cells:
                if (0,0) in cells:
                    cgrid.setCellValue((0,0),2)
                elif (0,1) in cells:
                    cgrid.setCellValue((0,1),2)
                elif (0,2) in cells:
                    cgrid.setCellValue((0,2),2)
                else:
                    cgrid.setCellValue(cells[randint(0, len(cells) - 1)], self.getNewTileValue())
                score,a,b = self.maxplay(cgrid,alpha,beta,level)
                #print('maxscore',score,a,alpha,b, beta, 'level'+str(level))
                #print('     minscore',score)
                if score < beta:
                    beta = score
            else:
                score = self.CalcScore(grid)
        return score,alpha,beta

    def maxplay(self,grid,alpha,beta,level):
        level -= 1
        bestscore = 0
        if level == 0:
            bestscore = self.CalcScore(grid)
            #print('score max0',score,0,alpha, 0,beta, 'level'+str(level))
            #print('max0score',bestscore)
        else:
            moves = grid.getAvailableMoves()
            for move in moves:
                #print('move b ',actionDic[move])
                cgrid = grid.clone()
                cgrid.move(move)
                minscore,a,b = self.minplay(cgrid,alpha,beta,level)
                #print('minscore',minscore,a,alpha, b, beta,'level'+str(level),'move'+str(actionDic[move]))
                #print('         maxplayscore',minscore,'move'+str(actionDic[move]))
                if minscore > bestscore:
                    bestscore = minscore
                    alpha = bestscore
                if alpha >= beta:
                    #print('prune on max',alpha,beta)
                    return bestscore,alpha,beta
        return bestscore,alpha,beta

    def minimax(self,grid,level):
        alpha = -math.inf #largest value for Max
        beta = math.inf #lowest value for Min
        moves = grid.getAvailableMoves()
        bestmove = moves[0]
        bestscore = 0
        for move in moves:
            #print('move a ',actionDic[move])
            cgrid = grid.clone()
            cgrid.move(move)
            score,a,b = self.minplay(cgrid,alpha,beta,level)
            #print('score',score,a,alpha, b,beta, 'level'+str(level),'move'+str(actionDic[move]))
            #print('mmplayscore',score,'move'+str(actionDic[move]))
            if score > bestscore:
                bestmove = move
                bestscore = score
                alpha = score
        return bestmove

    def getMove(self, grid):
        level = 3 #set depth limit
        #print('')
        move = self.minimax(grid,level)
        return move

    def getNewTileValue(self):
        if randint(0,99) < 100 * 0.9: 
            return 2 
        else: 
            return 4






