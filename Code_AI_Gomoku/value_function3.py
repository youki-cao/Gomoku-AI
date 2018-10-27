
#!/usr/bin/env python
# encoding: utf-8

from table import TABLE,row,col, black, white,space
#from evaluate import evaluate_line
from copy import deepcopy
import random
import numpy as np
from value_function import NODE
import value_function


def valueFunc3(node):
    maxsc = -100000
    for i, j in node.table.temp:
        sc = value_function.score_in_table(node.table.table, node.status, (i, j)) -\
             value_function.score_in_table(node.table.table, -node.status, (i, j))
        if sc > maxsc:
            maxsc = sc
            mi = i
            mj = j
    node.pos_i = mi
    node.pos_j = mj
    return
