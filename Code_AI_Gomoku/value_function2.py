
#!/usr/bin/env python
# encoding: utf-8

from table import TABLE,row,col, black, white,space
#from evaluate import evaluate_line
from copy import deepcopy
import random, pygame
import numpy as np
from value_function import NODE
import value_function


def valueFunc2(node, game):
    maxsc = 10000000
    for i, j in node.table.temp:
        newtable = deepcopy(node.table)
        newtable.table[i][j] = node.status
        newnode = NODE(newtable, node.deep, -node.status)
        newnode.table.temp = deepcopy(node.table.temp)
        newnode.table.temp.remove((i, j))
        newnode.table.returnaval(i, j)
        sc = value_function.valueFunc1(newnode, game, False)
        print i, j, sc
        if sc < maxsc:
            maxsc = sc
            mi = i
            mj = j
        if -sc > 100000:
            color = (255, 0, 0)
        else:
            c = 127 + int((np.log(abs(sc)+1.1))*(-0.5+(sc<0)))*25
            color = (c, 255-c, 255-c)
        x = game.chessboard.start_x + j * game.chessboard.grid_size
        y = game.chessboard.start_y + i * game.chessboard.grid_size
        pygame.draw.circle(game.screen, color, [x, y], game.chessboard.grid_size // 6)
        pygame.display.update()
    node.pos_i = mi
    node.pos_j = mj
    return
