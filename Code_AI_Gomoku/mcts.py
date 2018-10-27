# -*- coding: utf-8 -*-
"""
Created on Mon Jun 26 18:38:52 2017

@author: admin
"""

from table import TABLE,row,col, black, white,space
from copy import deepcopy
import random, sub_structure, pygame
import numpy as np
from value_function import NODE
from vv import values
from value_function4 import score_in_table, valueFunc4

def get_player(players):
    p = players.pop(0)
    players.append(p)
    return p


def weight_choice(weight):
    t = random.randint(0, sum(weight) - 1)
    for i, val in enumerate(weight):
        t -= val
        if t < 0:
            return i


def mcts(node, game):
    clock = pygame.time.Clock()
    winplayer=node.status
    if winplayer==white:
        players=[winplayer,black]
    else:
        players=[winplayer,white]
    playerstemp=players
    if node.table.temp == []:
        return
    maxiteration=100
    mofangjushu=10
    alpha = 0.1
    winrate={}
    for x, y in node.table.temp:
        winrate[(x, y)] = 0
    for n in range(mofangjushu):
        weight = []
        currentplayer=get_player(players)
        for x, y in node.table.temp:
            weight.append(int((1 + winrate[(x, y)]) * score_in_table(node.table, currentplayer, (x, y))))
        o, p = node.table.temp[weight_choice(weight)]
        rate=0
        situation = deepcopy(node.table)
        situation.move(o, p, currentplayer)
        players = playerstemp
        for m in range(maxiteration):
            weight = []
            currentplayer=get_player(players)
            for i, j in situation.temp:
                weight.append(score_in_table(situation, currentplayer, (i, j)))
            m1,m2 = situation.temp[weight_choice(weight)]
            situation.move(m1,m2,currentplayer)

            if situation.judge(m1,m2,currentplayer)==True:
                if currentplayer==winplayer:
                    rate += 1
                else:
                    rate -= 1
                break
        winrate[(o, p)] = rate*alpha + winrate[(o, p)]*0.9
        pygame.time.wait(100)
        xx = game.chessboard.start_x + p * game.chessboard.grid_size
        yy = game.chessboard.start_y + o * game.chessboard.grid_size
        color = 127 + int(125*winrate[o, p])
        pygame.draw.circle(game.screen, color, [xx, yy], game.chessboard.grid_size // 6)
        pygame.display.update()



    winscore=max(winrate.items(), key=lambda x: x[1])[1]
    for x,y in winrate.keys():
        if winrate[(x,y)]==winscore:
            node.pos_i = x
            node.pos_j= y
    if abs(winscore)<0.001:
        valueFunc4(node, game)
    return




