#!/usr/bin/env python
# encoding: utf-8

from table import TABLE,row,col, black, white,space
#from evaluate import evaluate_line
from copy import deepcopy
import random

class NODE():
    def __init__(self, table,deep,  status):
        self.table = table
        self.status = status
        self.deep = deep
        self.pos_i = -1
        self.pos_j = -1


def randPos(node):
    i, j = random.choice(node.table.temp)
    node.pos_i = i
    node.pos_j = j
    return


if __name__=='__main__':
    table = TABLE()
    node = NODE(table, 2, black)
    randPos(node)



