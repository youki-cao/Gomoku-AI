# -*- coding: utf-8 -*-
"""
Created on Sat Jun 10 17:20:34 2017

@author: admin
"""


from copy import deepcopy
import random, sub_structure
import numpy as np
from vv import values
vv={'l2a': 90, 'l2c': 60, 'l2b': 75, 'l3b': 7500, 'd': 0, 'l3a': 8600, 'l4': 200000, 'w': 1000000, 'l1': 3, 'd4': 9000, 'd2': 5, 'd3': 100, 'd1': 1}
values[(1, 0, 0, 0, 1, 1, 0, 0, 1)]='l2a'
values[()]='d'
values[(1, 0, 0, 1, 1, 0, 0, 0, 1)]='l2a'
def divine(row, status):
    temp=[]
    new=[]
    judge=deepcopy(row)
    for i in range(len(judge)):
        if judge[i]==-status:
            temp.append(i)
    if temp==[]:
        new=[judge]
    else:
        if temp[0]==0:
            new.append(())
        else:
            new.append(judge[0:temp[0]])
        if temp[len(temp)-1]+1==len(judge) :
            new.append(())
        else:
            new.append(judge[(temp[len(temp)-1]+1):(len(judge))])
        for i in range(0,len(temp)-2):
            new.append(judge[(temp[i]+1):(temp[i+1])])
    return new

def getCorner(table):
    toReturn = []
    for s in range(29):
        t = []
        for j in range(15):
            if s-j<=14 and s>=j:
                t.append(table[s-j][j])
        toReturn.append(t)
    return toReturn

def getCorner2(table):
    toReturn = []
    for s in range(-14,15):
        t = []
        for j in range(15):
            if s+j<=14 and s+j>=0:
                t.append(table[s+j][j])
        toReturn.append(t)
    return toReturn


def returnrowvalue(table, status):
    dim=15
    summary={}
    summ=[]
    newtable = deepcopy(table)
    for i in range(dim):
        divide=divine(newtable[i], status)
        maxj = -100000
        temp=[]
        res=[]
        for x in divide:
            if len(x)>9:
                for j in range(len(x)-8):
                    temp.append(x[j:(j+9)])
                for j in range(len(temp)):
                    tem=vv[values[tuple(np.dot(temp[j], status))]]
                    if tem>maxj:
                        maxj=tem
                        res=temp[j]
                summ.append(values[tuple(np.dot(res, status))])

            else:
                summ.append(values[tuple(np.dot(x, status))])


    for i in getCorner(newtable):
        divide=divine(i, status)
        maxj = -100000
        temp=[]
        res=[]
        for x in divide:
            if len(x)>9:
                for j in range(len(x)-8):
                    temp.append(x[j:(j+9)])
                for j in range(len(temp)):
                    tem=vv[values[tuple(np.dot(temp[j], status))]]
                    if tem>maxj:
                        maxj=tem
                        res=temp[j]
                summ.append(values[tuple(np.dot(res, status))])
            else:
                summ.append(values[tuple(np.dot(x, status))])
    for i in getCorner2(newtable):
        divide=divine(i, status)
        maxj = -100000
        temp=[]
        res=[]
        for x in divide:
            if len(x)>9:
                for j in range(len(x)-8):
                    temp.append(x[j:(j+9)])
                for j in range(len(temp)):
                    tem=vv[values[tuple(np.dot(temp[j], status))]]
                    if tem>maxj:
                        maxj=tem
                        res=temp[j]
                summ.append(values[tuple(np.dot(res, status))])

            else:
                summ.append(values[tuple(np.dot(x, status))])
                values[tuple(np.dot(x, status))]
    newtable = np.transpose(newtable)
    for i in range(dim):
        divide=divine(list(newtable[i]), status)
        maxj = -100000
        temp=[]
        res=[]
        for x in divide:
            if len(x)>9:
                for j in range(len(x)-8):
                    temp.append(x[j:(j+9)])
                for j in range(len(temp)):
                    tem=vv[values[tuple(np.dot(temp[j], status))]]
                    if tem>maxj:
                        maxj=tem
                        res=temp[j]
                summ.append(values[tuple(np.dot(res, status))])

            else:
                summ.append(values[tuple(np.dot(x, status))])
    for item in summ:
        if item in summary:
            summary[item] += 1
        else:
            summary[item] = 1

    return summary
#def gettoFive(line):
#    if len(line)>=5:
#        for i in range(0, len(line)-4):
#            if sum(line[i:(i+5)])==4:
#                return i + line[i:(i+5)].index(0)
#

#for key in values:
#    if values[key] == 'd4':
#        if not gettoFive(key):
#            print key

#
#for key in dict:
#    score += vv[key]*dict[key]

