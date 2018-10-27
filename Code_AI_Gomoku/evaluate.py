#!/usr/bin/env python
# encoding: utf-8

from table import black, white,space, dead

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


if __name__ == '__main__':
    line = [1, 1, 0, 0, 0, 0, -1, -1, -1, 0, 0, 0, 0, 0, 0]
    print line
    score = evaluate_line(line)
    print 'black:', score[black]
    print 'white:', score[white]
