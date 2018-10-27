
#!/usr/bin/env python
# encoding: utf-8

from table import TABLE,row,col, black, white,space
from evaluate import evaluate_line
from copy import deepcopy
import random, pygame
import numpy as np
from vv import values
vv={'l2a': 90, 'l2c': 60, 'l2b': 75, 'l3b': 7500, 'd': 0, 'l3a': 8600, 'l4': 200000, 'w': 1000000, 'l1': 3, 'd4': 5000, 'd2': 5, 'd3': 100, 'd1': 1}
vv2={'l2a': 450, 'l2c': 300, 'l2b': 375, 'l3b': 20000, 'd': 0, 'l3a': 40000, 'l4': 400000, 'w': 1000000, 'l1': 11, 'd4': 400000, 'd2': 25, 'd3': 500, 'd1': 1}

values[(1, 0, 0, 0, 1, 1, 0, 0, 1)]='l2a'
values[()]='d'
values[(1, 0, 0, 1, 1, 0, 0, 0, 1)]='l2a'
from newmethod import returnrowvalue
class NODE():
    def __init__(self, table, deep, status):
        self.table = table
        self.status = status
        self.deep = deep
        self.pos_i = -1
        self.pos_j = -1
        self.value = 0

    def evaluate(self):

        vecs = []
        # 1.1 '---' *15
        for i in xrange(0, row):
            vecs.append(self.table.table[i])
        # 1.2 '|' * 15
        for j in xrange(0, col):
            vecs.append([self.table.table[i][j] for i in range(0, row)])

        # 1.3 '\' *21
        vecs.append([self.table.table[x][x] for x in range(0, row)])
        for i in xrange(1, row - 4):
            vec = [self.table.table[x][x - i] for x in range(i, row)]
            vecs.append(vec)
            vec = [self.table.table[y - i][y] for y in range(i, col)]
            vecs.append(vec)
            # print [(y-i,y) for y in range(i, col)]

        # 1.4 '/'*21
        # vecs.append([self.table.table[x][row-x-1] for x in range(0, row)])
        # print [(x, row-x-1) for x in xrange(0, row)]
        for i in xrange(4, row - 1):
            vec = [self.table.table[x][i - x] for x in xrange(i, -1, -1)]
            vecs.append(vec)
            vec = [self.table.table[x][col - x + row - i - 2] for x in xrange(row - i - 1, row)]
            vecs.append(vec)
            # print [(x,i-x) for x in xrange(i,-1,-1)]
            # print [(x,col-x+row-i-2) for x in xrange(row-i-1, row)]

        table_score = 0
        for vec in vecs:
            score = evaluate_line(vec)
            if self.status == black:

                table_score += score[white][0] - score[black][0] - score[black][1]
            else:

                table_score += score[black][0] - score[white][0] - score[white][1]

        return table_score


def valueFunc1(node, game, changePos = True):
    maxsc = -10000000
    for i, j in node.table.temp:
        newTable = deepcopy(node.table.table)
        newTable[i][j] = node.status
        sc = score_in_table(newTable, node.status, vv) -\
                           score_in_table(newTable, -node.status, vv2)
        if sc > maxsc:
            maxsc = sc
            mi = i
            mj = j
        if changePos is True:
            x = game.chessboard.start_x + j * game.chessboard.grid_size
            y = game.chessboard.start_y + i * game.chessboard.grid_size
            if sc > 100000:
                color = (255, 0, 0)
            else:
                c = max(127 + int((np.log(abs(sc)+1.1))*(-0.5+(sc>0)))*25, 0)
                color = (c, 255-c, 255-c)
            pygame.draw.circle(game.screen, color, [x, y], game.chessboard.grid_size // 6)
            pygame.display.update()
    if changePos is True:
        node.pos_i = mi
        node.pos_j = mj
    return maxsc



def score_in_table(table, color, vv):
    score = 0
    Dict = returnrowvalue(table, color)
    for key in Dict:
        score += vv[key]*Dict[key]
    return score

