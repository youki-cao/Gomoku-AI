#!/usr/bin/env python
# encoding: utf-8

# from evaluate import evaluate_line
from table import TABLE,row,col, black, white,space
from copy import deepcopy
import random
import numpy as np
from value_function import NODE
import value_function
from vv import values
vv={'l2a': 90, 'l2c': 60, 'l2b': 75, 'l3b': 7500, 'd': 0, 'l3a': 8600, 'l4': 200000, 'w': 1000000, 'l1': 3, 'd4': 5000, 'd2': 5, 'd3': 100, 'd1': 1}
values[(1, 0, 0, 0, 1, 1, 0, 0, 1)]='l2a'
values[()]='d'
values[(1, 0, 0, 1, 1, 0, 0, 0, 1)]='l2a'
from newmethod import returnrowvalue
import pygame

count = 0

fastScore = [0, 1, 10, 100, 1000, 99999]

def evaluate_line(line):
    status = 1
    score = {1:[0, 0], -1:[0, 0]}
    for _ in range(2):
        for i in range(0, len(line)-4):
            tlist = line[i:i+5]
            if -status not in line[i:i+5]:
                tsum = list(tlist).count(status)
                score[status][0] += fastScore[tsum]
                if tsum >= 4:
                    score[status][1] += 50
        status = -status
    return score


def evaluate(new_table, status):
    vecs = []
    # 1.1 '---' *15
    for i in xrange(0, row):
        vecs.append(new_table[i])
    # 1.2 '|' * 15
    for j in xrange(0, col):
        vecs.append([new_table[i][j] for i in range(0, row)])

    # 1.3 '\' *21
    vecs.append([new_table[x][x] for x in range(0, row)])
    for i in xrange(1, row - 4):
        vec = [new_table[x][x - i] for x in range(i, row)]
        vecs.append(vec)
        vec = [new_table[y - i][y] for y in range(i, col)]
        vecs.append(vec)
        # print [(y-i,y) for y in range(i, col)]

    # 1.4 '/'*21
    # vecs.append([new_tab;e[x][row-x-1] for x in range(0, row)])
    # print [(x, row-x-1) for x in xrange(0, row)]
    for i in xrange(4, row - 1):
        vec = [new_table[x][i - x] for x in xrange(i, -1, -1)]
        vecs.append(vec)
        vec = [new_table[x][col - x + row - i - 2] for x in xrange(row - i - 1, row)]
        vecs.append(vec)
        # print [(x,i-x) for x in xrange(i,-1,-1)]
        # print [(x,col-x+row-i-2) for x in xrange(row-i-1, row)]

    table_score = 0
    for vec in vecs:
        score = evaluate_line(vec)
        if status == black:

            table_score += score[white][0] - score[black][0] - score[black][1]
        else:

            table_score += score[black][0] - score[white][0] - score[white][1]

    return table_score * (random.random() * 0.2 + 0.9)


def get_score2(current_table, status):
    '''
    score = 0
    table_list = returnrowvalue(node.table.table, node.status)
    for key in table_list:
        score += vv[key] * table_list[key]
    another_list = returnrowvalue(node.table.table, -node.status)
    # for key in another_list:
    #     score -= vv[key] * another_list[key]
    return score
    '''
    return - evaluate(current_table, status)


def get_score(current_table, status):

    score = 0
    table_list = returnrowvalue(current_table, status)
    for key in table_list:
        score += vv[key] * table_list[key]
    another_list = returnrowvalue(current_table, status)
    for key in another_list:
        score -= vv[key] * another_list[key]
    return score



def generate_node(table, status, deep, temp, next_node, dist=2):
    # print "origin table", table
    if status == white:
        next_status = black
    else:
        next_status = white

    # print "1:", table[6]
    new_table = table + []
    # print "2:", table[6]
    x = next_node[0]
    y = next_node[1]
    new_table[x][y] = status
    # print "3:", table[6]
    new_deep = deep + 1
    new_temp = temp + []
    for k in range(max(x - dist, 0), min(x + dist + 1, 15)):
        for m in range(max(y - dist, 0), min(y + dist + 1, 15)):
            if new_table[k][m] == space and (k, m) not in new_temp:
                new_temp.append((k, m))
    if (x, y) in new_temp:
        new_temp.remove((x, y))
    # print "new_table1", new_table
    return new_table, new_deep, next_status, new_temp


def alphaBeta(table, status, deep, temp, level_num, game, dist=2, alpha=-1000000, beta=1000000):

    global count
    count += 1
    if deep >= level_num:
        score = get_score2(table, status)
        # print score
        return score

    for next_node in temp:
        Cx = next_node[0]
        Cy = next_node[1]
        xx = game.chessboard.start_x + Cy * game.chessboard.grid_size
        yy = game.chessboard.start_y + Cx * game.chessboard.grid_size
        pygame.draw.circle(game.screen, (255-80*deep, 80*deep, 255-80*deep), [xx, yy], game.chessboard.grid_size // 6)
        pygame.display.update()
        ttable = [x + [] for x in table]
        # print ttable
        new_table, new_deep, new_status, new_temp = generate_node(ttable, status, deep, temp, next_node, dist)

        # print "new_table2", new_table
        new_score = -alphaBeta(new_table, new_status, new_deep, new_temp, level_num, game, dist, -beta, -alpha)

        if new_score > beta:
            return new_score
        if new_score > alpha:
            alpha = new_score
            pos_i = next_node[0]
            pos_j = next_node[1]
    if deep == 0:
        return pos_i, pos_j
    return alpha


def new_alphabeta(table, status, deep, temp, level_num, game, dist=2, alpha=-1000000, beta=1000000):
    global count
    count += 1
    if deep >= level_num:
        score = get_score2(table, status)
        # print score
        return score


    print "deep0:", deep
    if deep == 0:
        num_remain = len(temp) / 2 + 1
        temp_dict = dict()
        small_score = 1000000
        small_index = -1000000

    print "temp0", temp

    for next_node in temp:
        print "next_node", next_node
        print "deep", deep
        Cx = next_node[0]
        Cy = next_node[1]
        xx = game.chessboard.start_x + Cy * game.chessboard.grid_size
        yy = game.chessboard.start_y + Cx * game.chessboard.grid_size
        pygame.draw.circle(game.screen, (255 - 80 * deep, 80 * deep, 255 - 80 * deep), [xx, yy],
                           game.chessboard.grid_size // 6)
        pygame.display.update()
        ttable = [x + [] for x in table]
        # print ttable
        new_table, new_deep, new_status, new_temp = generate_node(ttable, status, deep, temp, next_node, dist)
        print "new temp", new_temp
        print "new deep", new_deep
        # print "new_table2", new_table
        new_score = -new_alphabeta(new_table, new_status, new_deep, new_temp, level_num, game, dist, -beta, -alpha)

        if new_score >= beta:
            return new_score

        if deep == 0:
            if len(temp_dict) < num_remain:
                temp_dict[next_node] = new_score
                if new_score < small_score:
                    small_score = new_score
                    small_index = next_node
            else:
                if new_score > small_score:
                    temp_dict[next_node] = new_score
                    temp_dict.pop(small_index)
                    small_index, small_score = min(temp_dict.items(), key=lambda x: x[1])

        if new_score >= alpha:
            alpha = new_score
            pos_i = next_node[0]
            pos_j = next_node[1]

        print "bingo"
    if deep == 0:
        return list(temp_dict.keys())
    return alpha



def new_alphabeta_final(table, status, deep, temp, level_num, game, dist=2, alpha=-1000000, beta=1000000):
    global count
    count += 1
    if deep >= level_num:
        score = get_score2(table, status)
        # print score
        return score


    print "deep0:", deep
    if deep == 0:
        num_remain = len(temp) / 2 + 1
        temp_dict = dict()
        small_score = 1000000
        small_index = -1000000

    print "temp0", temp

    for next_node in temp:
        print "next_node", next_node
        print "deep", deep
        Cx = next_node[0]
        Cy = next_node[1]
        xx = game.chessboard.start_x + Cy * game.chessboard.grid_size
        yy = game.chessboard.start_y + Cx * game.chessboard.grid_size
        pygame.draw.circle(game.screen, (255 - 80 * deep, 80 * deep, 255 - 80 * deep), [xx, yy],
                           game.chessboard.grid_size // 6)
        pygame.display.update()
        ttable = [x + [] for x in table]
        # print ttable
        new_table, new_deep, new_status, new_temp = generate_node(ttable, status, deep, temp, next_node, dist)
        print "new temp", new_temp
        print "new deep", new_deep
        # print "new_table2", new_table
        new_score = -new_alphabeta(new_table, new_status, new_deep, new_temp, level_num, game, dist, -beta, -alpha)

        if new_score >= beta:
            return new_score

        if deep == 0:
            if len(temp_dict) < num_remain:
                temp_dict[next_node] = new_score
                if new_score < small_score:
                    small_score = new_score
                    small_index = next_node
            else:
                if new_score > small_score:
                    temp_dict[next_node] = new_score
                    temp_dict.pop(small_index)
                    small_index, small_score = min(temp_dict.items(), key=lambda x: x[1])

        if new_score >= alpha:
            alpha = new_score
            pos_i = next_node[0]
            pos_j = next_node[1]

        print "bingo"
    if deep == 0:
        return pos_i, pos_j
    return alpha




def alpha_beta_prunning(table, status, deep, temp, level_num, game, dist=2, alpha=-1000000, beta=1000000):

    '''
    for i in range(1, level_num + 1):
        new_temp = new_alphabeta(table, status, deep, temp, i, game, dist, alpha=-1000000, beta=1000000)
        print "over", i
        temp = new_temp
        print temp
    '''
    new_temp = new_alphabeta(table, status, deep, temp, 2, game, dist, alpha=-1000000, beta=1000000)
    temp = new_temp
    print temp
    pos_i, pos_j = new_alphabeta_final(table, status, deep, temp, level_num, game, dist, alpha=-1000000, beta=1000000)
    return pos_i, pos_j


def new_negaScout(table, status, deep, temp, level_num, game, dist=2, alpha=-1000000, beta=1000000):

    global count
    count += 1
    if deep >= level_num:
        score = get_score2(table, status)
        # print score
        return score

    # print "deep0:", deep
    if deep == 0:
        num_remain = len(temp) / 2 + 1
        temp_dict = dict()
        small_score = 1000000
        small_index = -1000000

    first_next_node = temp[0]
    Cx = first_next_node[0]
    Cy = first_next_node[1]
    xx = game.chessboard.start_x + Cy * game.chessboard.grid_size
    yy = game.chessboard.start_y + Cx * game.chessboard.grid_size
    pygame.draw.circle(game.screen, (100, 100, 100), [xx, yy],
                       game.chessboard.grid_size // 6)
    pygame.display.update()
    ttable = [x + [] for x in table]
    first_table, first_deep, first_status, first_temp = generate_node(ttable, status, deep, temp, first_next_node, dist)
    first_value = -negaScout(first_table, first_status, first_deep, first_temp, level_num, game, dist, -beta, -alpha)

    if first_value >= beta:
        return first_value
    if deep == 0:
        temp_dict[first_next_node] = first_value
    if first_value > alpha:
        alpha = first_value
        pos_i = first_next_node[0]
        pos_j = first_next_node[1]

    for i in range(0, len(temp)):
        next_node = temp[i]
        Cx = next_node[0]
        Cy = next_node[1]
        xx = game.chessboard.start_x + Cy * game.chessboard.grid_size
        yy = game.chessboard.start_y + Cx * game.chessboard.grid_size
        pygame.draw.circle(game.screen, (255-80*deep, 80*deep, 255-80*deep), [xx, yy], game.chessboard.grid_size // 6)
        pygame.display.update()
        ttable = [x + [] for x in table]
        # print ttable
        new_table, new_deep, new_status, new_temp = generate_node(ttable, status, deep, temp, next_node, dist)

        # print "new_table2", new_table
        new_score = -negaScout(new_table, new_status, new_deep, new_temp, level_num, game, dist, -alpha - 1, -alpha)

        if new_score > alpha and new_score < beta:
            new_score = -negaScout(new_table, new_status, new_deep, new_temp, level_num, game, dist, -beta, -alpha - 1)
        if new_score >= beta:
            return new_score
        if deep == 0:
            if len(temp_dict) < num_remain:
                temp_dict[next_node] = new_score
                if new_score < small_score:
                    small_score = new_score
                    small_index = next_node
            else:
                if new_score > small_score:
                    temp_dict[next_node] = new_score
                    temp_dict.pop(small_index)
                    small_index, small_score = min(temp_dict.items(), key=lambda x: x[1])

        if new_score > alpha:
            alpha = new_score
            pos_i = next_node[0]
            pos_j = next_node[1]
    if deep == 0:
        return list(temp_dict.keys())
    return alpha


def negaScout(table, status, deep, temp, level_num, game, dist=2, alpha=-1000000, beta=1000000):
    global count
    count += 1
    if deep >= level_num:
        score = get_score2(table, status)
        # print score
        return score

    first_next_node = temp[0]
    Cx = first_next_node[0]
    Cy = first_next_node[1]
    xx = game.chessboard.start_x + Cy * game.chessboard.grid_size
    yy = game.chessboard.start_y + Cx * game.chessboard.grid_size
    pygame.draw.circle(game.screen, (100, 100, 100), [xx, yy],
                       game.chessboard.grid_size // 6)
    pygame.display.update()
    ttable = [x + [] for x in table]
    first_table, first_deep, first_status, first_temp = generate_node(ttable, status, deep, temp, first_next_node, dist)
    first_value = -negaScout(first_table, first_status, first_deep, first_temp, level_num, game, dist, -beta, -alpha)

    if first_value >= beta:
        return first_value
    if first_value > alpha:
        alpha = first_value
        pos_i = first_next_node[0]
        pos_j = first_next_node[1]

    for i in range(0, len(temp)):
        next_node = temp[i]
        Cx = next_node[0]
        Cy = next_node[1]
        xx = game.chessboard.start_x + Cy * game.chessboard.grid_size
        yy = game.chessboard.start_y + Cx * game.chessboard.grid_size
        pygame.draw.circle(game.screen, (255-80*deep, 80*deep, 255-80*deep), [xx, yy], game.chessboard.grid_size // 6)
        pygame.display.update()
        ttable = [x + [] for x in table]
        # print ttable
        new_table, new_deep, new_status, new_temp = generate_node(ttable, status, deep, temp, next_node, dist)

        # print "new_table2", new_table
        new_score = -negaScout(new_table, new_status, new_deep, new_temp, level_num, game, dist, -alpha - 1, -alpha)

        if new_score > alpha and new_score < beta:
            new_score = -negaScout(new_table, new_status, new_deep, new_temp, level_num, game, dist, -beta, -alpha - 1)
        if new_score >= beta:
            return new_score
        if new_score > alpha:
            alpha = new_score
            pos_i = next_node[0]
            pos_j = next_node[1]
    if deep == 0:
        return pos_i, pos_j
    return alpha


def negaScout_prunning(table, status, deep, temp, level_num, game, dist=2):
    new_temp = new_negaScout(table, status, deep, temp, 1, game, dist, alpha=-1000000, beta=1000000)
    temp = new_temp
    # print temp
    pos_i, pos_j = negaScout(table, status, deep, temp, level_num, game, dist, alpha=-1000000, beta=1000000)
    return pos_i, pos_j


def alpha_beta(node, level_num, game, dist=2):
    # print "hahha"
    # print node.table.table
    pos_i, pos_j = negaScout_prunning(node.table.table, node.status, node.deep, node.table.temp, level_num, game, dist)
    # pos_i, pos_j = negaScout(node.table.table, node.status, node.deep, node.table.temp, level_num, game, dist)

    node.pos_i = pos_i
    node.pos_j = pos_j
    # print count
    return 0



