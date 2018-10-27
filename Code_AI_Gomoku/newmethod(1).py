# -*- coding: utf-8 -*-
"""
Created on Sat Jun 10 17:20:34 2017

@author: admin
"""

from table import TABLE

from copy import deepcopy
import random, sub_structure
import numpy as np
from value_function import NODE
from vv import values
values[()]='d'

def divine(table,row):
    temp=[]
    new=[]
    situation=deepcopy(table)
    judge=situation[row]
    for i in range(len(judge)):
        if judge[i]==-1:
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


def returnrowvalue(table):

    dim=15
    summary={}
    summ=[]
    tem=0
    maxj=-100000
    res=[]
    temp=[]
    for i in range(dim):

        divide=divine(table,i)

        for x in divide:
            if len(x)>9:

                for i in range(len(x)-8):
                    temp.append(x[i:(i+9)])
                for i in range(len(x)-8):
                    tem=vv[values[tuple(temp[i])]]
                    if tem>maxj:
                        maxj=tem
                        res=temp[i]
                summ.append(values[tuple(res)])

            else:
                summ.append(values[tuple(x)])
    newsum=set(summ)
    for item in newsum:
        summary[item]=summ.count(item)
    return summary







