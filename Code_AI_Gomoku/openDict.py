# -*- coding: utf-8 -*-
"""
Created on Mon Jun 26 20:19:09 2017

@author: dell
"""
from VCT import VCTFab, VCTFv4, VCTFmc
global openDict
openDict = {}
f = open('openDict2.txt', 'r')
for line in f :
    tableO = line.split('.')
    t = []
    for item in tableO[0:15]:
        row = item.split(',')
        row.pop()
        row = [int(x) for x in row]
        t.append(row)
    x, y = [int(x) for x in tableO[15].split(',')]
    openDict[tuple(map(tuple, t))] = (x, y)
f.close()

def rotate(table):
    return map(list,zip(*table[::-1]))

def transpose(table):
    return zip(*table)

def rt(i, j, x, y):
    if i:
        x, y = y, x
    while j:
        dx = x - 7
        dy = y - 7
        y = 7 - dx
        x = 7 + dy
        j -= 1
    return (x, y)

def findOpen(table):
    global openDict
    for i in range(2):
        for j in range(4):
            if tuple(map(tuple, table)) in openDict:
                x, y = openDict[tuple(map(tuple, table))]
                if i:
                    return rt(i, j, x, y)
                return rt(i, 4 - j, x, y)
            table = rotate(table)
        table = transpose(table)
    return (-1, -1)

def ovv4(node, game):
    x, y = findOpen([x+[] for x in node.table.table])
    if (x, y) != (-1, -1):
        node.pos_i = x
        node.pos_j = y
        print 'Found in Opening LIB'
        return
    VCTFv4(node, game)
    return

def ovab(node, game):
    x, y = findOpen([x+[] for x in node.table.table])
    if (x, y) != (-1, -1):
        node.pos_i = x
        node.pos_j = y
        print 'Found in Opening LIB'
        return
    VCTFab(node, game)
    return

def ovmc(node, game):
    x, y = findOpen([x+[] for x in node.table.table])
    if (x, y) != (-1, -1):
        node.pos_i = x
        node.pos_j = y
        print 'Found in Opening LIB'
        return
    VCTFmc(node, game)
    return
