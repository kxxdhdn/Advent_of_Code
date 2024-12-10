#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path

## Current file direction
cfd = Path(__file__).parent.absolute()

## Read input
f = open(str(cfd)+'/data/D10_input.txt', 'r')
lines = [[int(l) for l in line] for line in f.read().splitlines()]

def bounded(loc, tmap):
    Ni, Nj = len(tmap), len(tmap[0])
    if 0<=loc[0]<Ni and 0<=loc[1]<Nj:
        return True
    else:
        return False

trailheads = list(([i, j] for i,row in enumerate(lines) for j,x in enumerate(row) if x==0))
go = [[-1,0], [1,0], [0,-1], [0,1]]
scores = 0
ratings = 0
for th in trailheads:
    num_br = 0
    branches = {num_br:[th]}
    trails = {num_br:True}
    next_step = 1
    while next_step<10:
        for i in range(num_br+1):
            if trails[i]:
                flag = 0
                for g in go:
                    nl = [x+g[ii] for ii,x in enumerate(branches[i][next_step-1])] # next loc
                    if bounded(nl, lines) and lines[nl[0]][nl[1]]==next_step:
                        flag += 1
                        if flag==1:
                            branches[i].append(nl)
                        else:
                            num_br += 1
                            branches[num_br] = branches[i][0:-1]
                            branches[num_br].append(nl)
                            trails[num_br] = True
                if flag==0:
                    trails[i] = False
        if any(trails.values()):
            next_step += 1
        else:
            break
    num_br_unique = len(set([tuple(val[-1]) for val in branches.values() if len(val)==10]))
    scores += num_br_unique
    ratings += sum(trails.values())

print(f'The sum of the scores of all trailheads is {scores}.')
print(f'The sum of the ratings of all trailheads is {ratings}.')
