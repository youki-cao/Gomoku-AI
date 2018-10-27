# -*- coding: utf-8 -*-
from sub_structure import same_color_situation_in_table
from copy import deepcopy
from vv import values
from newmethod import returnrowvalue
from value_function4 import valueFunc4
from minmax_play import alpha_beta
from mcts import mcts
from table import TABLE
import pygame

def VCTFv4(node, game):
    global depth
    depth = 5000
    x, y = VCF(node.table, node.status, game, True)
    if (x, y) != (-1, -1):
        node.pos_i = x
        node.pos_j = y
        print 'Found VCF'
        return
    x, y = VCT(node.table, node.status, game, True)
    if (x, y) != (-1, -1):
        node.pos_i = x
        node.pos_j = y
        print 'Found VCT'
        return
    valueFunc4(node, game, changePos=True, printSc=False, valueType=0)

def VCTFab(node, game):
    global depth
    depth = 5000
    x, y = VCF(node.table, node.status, game, True)
    if (x, y) != (-1, -1):
        node.pos_i = x
        node.pos_j = y
        print 'Found VCF'
        return
    x, y = VCT(node.table, node.status, game, True)
    if (x, y) != (-1, -1):
        node.pos_i = x
        node.pos_j = y
        print 'Found VCT'
        return
    alpha_beta(node, 2, game, dist=2)

def VCTFmc(node, game):
    global depth
    depth = 5000
    x, y = VCF(node.table, node.status, game, True)
    if (x, y) != (-1, -1):
        node.pos_i = x
        node.pos_j = y
        print 'Found VCF'
        return
    x, y = VCT(node.table, node.status, game, True)
    if (x, y) != (-1, -1):
        node.pos_i = x
        node.pos_j = y
        print 'Found VCT'
        return
    mcts(node, game)

def VCF(table, status, game, Draw=False, deep=5):

    global depth
    depth -= 1
    if depth < 0:
        return (-1, -1)
    if deep == 0:
        return(-1, -1)
    if table.Five[status]:
        return table.Five[status][0]
    if table.Five[-status]:
#        print 'opponent has Five'
        return (-1, -1)
    if table.DFour[status] == []:
#        print 'we have no Die Four'
        return (-1, -1)
    table.VCFqueue = table.DFour[status] + []
    while table.VCFqueue:
        Cx, Cy = table.VCFqueue.pop()
        if Draw:
            xx = game.chessboard.start_x + Cy * game.chessboard.grid_size
            yy = game.chessboard.start_y + Cx * game.chessboard.grid_size
            pygame.draw.circle(game.screen, (0, 255, 0), [xx, yy], game.chessboard.grid_size // 6)
            pygame.display.update()
        checkNode = deepcopy(table)
        checkNode.move(Cx, Cy, status)
        if len(list(set(checkNode.Five[status]))) > 1:
            return (Cx, Cy)
        x, y = checkNode.Five[status][0]
        checkNode.move(x, y, -status)
        mx, my = VCF(checkNode, status, game, deep=deep-1)
        if (mx, my) != (-1, -1):
            return (Cx, Cy)
#    print 'Used up Die Fours'
    return (-1, -1)


def finddupl(lst):
    """找出 lst 中有重复的项
        (与重复次数无关，且与重复位置无关)
    """
    exists, dupl = set(), set()
    for item in lst:
        if item in exists:
            dupl.add(item)
        else:
            exists.add(item)
    return list(dupl)


def VCT(table, status, game, Draw=False, deep=3):
    global depth
    depth -= 1
    if depth < 0:
        return (-1, -1)
    if deep == 0:
        return (-1, -1)
    if table.Five[status]:
        return table.Five[status][0]
    if table.Five[-status] or finddupl(table.DFour[-status]):
#        print 'opponent has Five'
        return (-1, -1)
    if table.DFour[status] == []:
#        print 'we have no Die Four'
        return (-1, -1)
    table.VCFqueue = table.DFour[status] + table.LThree[status]
    while table.VCFqueue:
        if depth < 0:
            return (-1, -1)
        flag = 0
        Cx, Cy = table.VCFqueue.pop()
        xx = game.chessboard.start_x + Cy * game.chessboard.grid_size
        yy = game.chessboard.start_y + Cx * game.chessboard.grid_size
        pygame.draw.circle(game.screen, (255-depth*255/5000, depth*255/5000, 255-depth*255/5000), [xx, yy], game.chessboard.grid_size // 6)
        pygame.display.update()
        checkNode = deepcopy(table)
        checkNode.move(Cx, Cy, status)
        if len(list(set(checkNode.Five[status]))) > 1:
            return (Cx, Cy)
        for x, y in finddupl(checkNode.DFour[status])+checkNode.Five[status]+checkNode.DFour[-status]:
            tempNode = deepcopy(checkNode)
            tempNode.move(x, y, -status)
            mx, my = VCF(tempNode, status, game, deep=deep)
            nx, ny = VCT(tempNode, status, game, deep=deep-1)
            if (mx, my) == (-1, -1) and (nx, ny) == (-1, -1):
                flag = 1
                break
        if not flag:
            return (Cx, Cy)
#    print 'Used up Die Fours'
    return (-1, -1)