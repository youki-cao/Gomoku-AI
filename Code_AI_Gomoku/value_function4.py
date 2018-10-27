
#!/usr/bin/env python
# encoding: utf-8

from table import TABLE,row,col, black, white,space
#from evaluate import evaluate_line
from copy import deepcopy
import random, sub_structure, pygame
import numpy as np
from value_function import NODE
from vv import values
vv={'l2a': 270, 'l2c': 180, 'l2b': 225, 'l3b': 750, 'd': 0, 'l3a': 860, 'l4': 20000, 'w': 1000000, 'l1': 3, 'd4': 700, 'd2': 5, 'd3': 300, 'd1': 1}
vv2={'l2a': 270, 'l2c': 180, 'l2b': 225, 'l3b': 750, 'd': 0, 'l3a': 860, 'l4': 20000, 'w': 1000000, 'l1': 3, 'd4': 1000, 'd2': 5, 'd3': 300, 'd1': 1}
values[(1, 0, 0, 0, 1, 1, 0, 0, 1)]='l2a'
values[()]='d'
values[(1, 0, 0, 1, 1, 0, 0, 0, 1)]='l2a'
def valueFunc4(node, game, changePos=True, printSc=False, valueType=0):
    maxsc = -10000000
    if node.table.temp == []:
        return -10000000
    for i, j in node.table.temp:
        sc = score_in_table(node.table, node.status, (i, j), printSc, valueType)
        if sc > maxsc:
            maxsc = sc
            mi = i
            mj = j
        x = game.chessboard.start_x + j * game.chessboard.grid_size
        y = game.chessboard.start_y + i * game.chessboard.grid_size
        if sc>100000:
            color = (255, 0, 0)
        else:
            c = min(int((np.log(abs(sc)+1.1))*(-0.5+(sc>0)))*50, 255)
            color = (c, 255-c, 255-c)
        pygame.draw.circle(game.screen, color, [x, y], game.chessboard.grid_size // 6)
        pygame.display.update()
    if changePos is True:
        node.pos_i = mi
        node.pos_j = mj
#        print maxsc
    return maxsc


def score_in_table(table, color, (i, j), printSc=False, valueType=0):
    situation = deepcopy(table.table)
    score = 0
    for item in sub_structure.same_color_situation_in_table((i, j), color, situation):
        ori = [0 if x == 2 else x for x in item]
        nxt = [1 if x == 2 else x for x in item]
        score += vv[values[tuple(nxt)]] - vv[values[tuple(ori)]]
    for item in sub_structure.same_color_situation_in_table((i, j), -color, situation):
        ori = [0 if x == 2 else x for x in item]
        nxt = [1 if x == 2 else x for x in item]
        gainOpo = vv2[values[tuple(nxt)]] - vv2[values[tuple(ori)]]
        if gainOpo < 14000 and valueType == 1:
            gainOpo /= 2
        score += int(gainOpo*(random.random()*0.02+0.3+225/225*0*valueType-0.1*(color+1)*(1-table.num/225)))
    if printSc:
        print (i, j), score
    return score


def valueFunc5(node, game, printSc=False):
    maxsc = -10000000
    for i, j in node.table.temp:
        newtable = deepcopy(node.table)
        newtable.table[i][j] = node.status
        newnode = NODE(newtable, node.deep, -node.status)
        newnode.table.temp = deepcopy(node.table.temp)
        newnode.table.returnaval(i, j)
        sc = valueFunc4(newnode, game, False)
        sc = score_in_table(node.table, node.status, (i, j)) - sc * 2
        if sc > maxsc:
            maxsc = sc
            mi = i
            mj = j
    node.pos_i = mi
    node.pos_j = mj
#    print maxsc
    return
