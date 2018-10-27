#!/usr/bin/env python
# encoding: utf-8
import math
import numpy as np
from copy import deepcopy
from newmethod import returnrowvalue
#import Chessboard
col = 15
row = 15

black = 1
white = -1
space = 0
dead = -2

class MoveERROR(Exception):
    def __init__(self, arg):
        self.args = arg


def left_diagonal(current, table):
    left_diagonal_list = list()
    posList = []
    min_board = -min(current[0], current[1])
    max_board = col - max(current[0], current[1])
    for i in range(min_board, max_board):
        left_diagonal_list.append(table[current[0] + i][current[1] + i])
        posList.append((current[0] + i, current[1] + i))
    return left_diagonal_list, -min_board, posList


def right_diagonal(current, table):
    right_diagonal_list = list()
    posList = []
    sum_coor = sum(current)
    for i in range(0, sum_coor+1):
        if i <= 14 and sum_coor - i <= 14:
            right_diagonal_list.append(table[i][sum_coor - i])
            posList.append((i, sum_coor - i))
    return right_diagonal_list, current[0]-max(0,sum_coor-14), posList


class TABLE():
    def __init__(self, plane=None):
        self.Five = {black: [], white: []}
        self.DFour = {black: [], white: []}
        self.LThree = {black: [], white: []}
        if plane == None:
            self.table = [ [0]*col for i in xrange(row)]
        else:
            self.table = plane
        self.temp = [(7, 7)]
        self.dist = 1
        self.value = 0
        self.num = 0
        self.prev = (-1, -1)
        winrate = {}
        for i in range(15):
            for j in range(15):
                winrate[(i, j)] = 0
        winrate[(7, 7)] = 0.01
        self.winrate = winrate
    def get(self, i, j):
        if i < 0 or i >= row or j < 0 or j >=col:
            return space
        return self.table[i][j]


    def move(self, x, y, status):
        if status != black and status != white:
            raise MoveERROR(['No such status:' + str(status)])
        if 0 <= x< row and 0<=y<col:
            if self.table[x][y] != space:
                print self.temp
                self.display()
                raise MoveERROR(['The Place has been placed'])
            self.TFCheck(x, y, status)
            self.table[x][y] = status
        else:
            raise MoveERROR(['move beyond border:(%d,%d)'%(x, y)])
        self.returnaval(x, y)
        self.num += 1
        self.prev = (x, y)


    def judge(self, x, y, status):
        status = self.table[x][y]
        if status == space:
            return False

        # judge '-----'
        for i in xrange(x-4, x+5):
            if self.get(i, y)==status \
                    and self.get(i+1,y) == status \
                    and self.get(i+2,y) == status \
                    and self.get(i+3,y) == status \
                    and self.get(i+4,y) == status :
                return True
        # judge '|'
        for j in xrange(y-4, y+5):
            if self.get(x,j)==status \
                    and self.get(x,j+1) == status \
                    and self.get(x,j+2) == status \
                    and self.get(x,j+3) == status \
                    and self.get(x,j+4) == status :
                return True

        # judge '\'
        j = y-4
        for i in xrange(x-4, x+5):
            if self.get(i, j)==status \
                    and self.get(i+1,j+1) == status \
                    and self.get(i+2,j+2) == status \
                    and self.get(i+3,j+3) == status \
                    and self.get(i+4,j+4) == status :
                return True
            j += 1

        # judge '/'
        i = x+4
        for j in xrange(y-4, y+5):
            if self.get(i,j)==status \
                    and self.get(i-1,j+1) == status \
                    and self.get(i-2,j+2) == status \
                    and self.get(i-3,j+3) == status \
                    and self.get(i-4,j+4) == status :
                return True
            i -=1
        return False


    def returnaval(self, x, y):
        dist = self.dist
        for k in range(max(x - dist, 0), min(x + dist + 1, 15)):
            for m in range(max(y - dist, 0), min(y + dist + 1, 15)):
                if self.table[k][m]==space and (k, m) not in self.temp:
                    self.temp.append((k,m))
        if (x, y) in self.temp:
            self.temp.remove((x, y))

        return self.temp



    def is_full(self):
        for i in xrange(0, row):
            for j in xrange(0, col):
                if self.table[i][j] == space:
                    return False
        return True



    def display(self):
        head = map(lambda i: hex(i)[2:].upper(), xrange(col))
        print '  ' + ' '.join(head)
        #print '--'*(col+1)
        for i in xrange(0, row):
            chs=[]
            for j in xrange(0, col):
                if (i, j) == self.prev:
                    if self.table[i][j] == black:
                        ch = 'X'
                    if self.table[i][j] == white:
                        ch = 'O'
                elif self.table[i][j] == space:
                    ch = ' '
                elif self.table[i][j] == black:
                    ch = 'x'
                else:
                    ch = 'o'
                chs.append(ch)
            line = '%s|%s|'%(head[i], '|'.join(chs))
            print line

    def PointLine(self, i, j):
        leftDiag, pos1, posL1 = left_diagonal((i, j), self.table)
        rightDiag, pos2, posL2 = right_diagonal((i, j), self.table)
        posL3 = [(i, x) for x in range(15)]
        posL4 = [(x, j) for x in range(15)]
        return ((leftDiag, pos1, posL1), (rightDiag, pos2, posL2),\
                (self.table[i], j, posL3), (list(np.transpose(self.table)[j]), i, posL4))

    def InLine(self, line, status, positionList, method='add'):
        tDict = {}
        for i in range(0, len(line)-4):
            tlist = line[i:i+5]
            if -status not in line[i:i+5]:
                tsum = list(tlist).count(status)
                if tsum == 3:
                    for j in range(5):
                        if tlist[j] == space:
                            if method == 'remove':
                                self.DFour[status].remove(positionList[j+i])
                            else:
                                self.DFour[status].append(positionList[j+i])
                if tsum == 4:
                    for j in range(5):
                        if tlist[j] == space:
                            if method == 'remove':
                                self.Five[status].remove(positionList[j+i])
                            else:
                                self.Five[status].append(positionList[j+i])
                if tsum == 2:
                    for j in range(5):
                        if tlist[j] == space:
                            if j+i in tDict:
                                if method == 'remove':
                                    self.LThree[status].remove(positionList[j+i])
                                else:
                                    self.LThree[status].append(positionList[j+i])
                                tDict.pop(j+i)
                            else:
                                tDict[j+i] = 1
        return

    def TFCheck(self, i, j, status):
        if self.judge(i, j, status):
            self.Five[status] = (1, (i, j))
            return
        lines = self.PointLine(i, j)
        for line in lines:
            self.InLine(line[0], status, line[2], 'remove')
            self.InLine(line[0], -status, line[2], 'remove')
            line[0][line[1]] = status
            self.InLine(line[0], status, line[2], 'add')
            self.InLine(line[0], -status, line[2], 'add')
        return




#    def liveFour(line, status):
#        toReturn = 0
#        if len(line)>=6:
#            for i in range(1, len(line)-4):
#                if line[i] == status and line[i+1] == status and\
#                   line[i+2] == status and line[i+3] == status and\
#                   line[i-1] == space and line[i+4] == space:
#                       toReturn += 1
#        return toReturn
#    def dieFour(line, status):
#        toReturn = 0
#        if len(line)>=5:
#            for i in range(0, len(line)-3):
#                if sum(line[i:(i+4)])==4*status and\
#                      -status not in line[i:(i+4)]:
#                          toReturn += 1
#                          i +=
#        return toReturn

#
#values = {}
#i = 0
#
#for length1 in range(5):
#    for length2 in range(length1, 5):
#        for i in range(2**length1):
#            for j in range(2**length2):
#                t = [0] * length1 + [0] + [0] * length2
#                for k in range(1, length1+1):
#                    if i % 2**k == i % 2**(k-1):
#                        t[k-1] = 1
#                for l in range(1, length2+1):
#                    if j % 2**l == j % 2**(l-1):
#                        t[l+length1] = 1
#                if tuple(t) not in values:
#                    values[tuple(t)] = ''
#
#for value in values.values():
#    if value not in vv:
#        print value
#        vv[value] = int(raw_input())
#values=deepcopy(bak)
#bak2=values
#i = 0
#for key in values.keys():
#    if values[key] != '' and values[key] != 'q':
#        values[tuple(list(reversed(list(key))))]=values[key]
#for key in values.keys():
#    if values[key] == '' or values[key] == 'q':
#        i += 1
#        if tuple(list(reversed(list(key)))) in values:
#            if values[tuple(list(reversed(list(key))))] != '' and\
#                      values[tuple(list(reversed(list(key))))] != 'q':
#                values[key] = values[tuple(list(reversed(list(key))))]
#                continue
#        print key, '\t', i*1000/328
#        values[key] = raw_input()
#        if values[key] == 'q':
#            break
###bak = values
#bak = {}
#f = open('values1.txt', 'w')
##for line in f:
##    line1 = deepcopy(line)
##    line2 = deepcopy(line)
##    value = line1.split('\t')[1].split('\n')[0]
##    key = line2.split('\t')[0].split(',')
##    key.pop()
##    key = [int(x) for x in key]
##    bak[tuple(key)]=value
##    break
#for key in values:
#    for i in key:
#        f.write(str(i))
#        f.write(',')
#    f.write('\t')
#    f.write(values[key])
#    f.write('\n')
#f.close()
#a = raw_input()
#if __name__ == '__main__':
#    t = TABLE()
#    t.display()
#    j=10
#    for i in range(8,8+5):
#        t.move(i, j, black)
#        print t.judge(i, j, black)
#        j-=1
#    #t.move(0,1,white)
#    t.display()
#    import copy
#    b = copy.deepcopy(t)
#    b.display()
#    b.move(10,10,black)
#    b.display()
#    t.display()




