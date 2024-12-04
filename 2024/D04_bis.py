#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path
import numpy as np

## Current file direction
cfd = Path(__file__).parent.absolute()

## Read input
f = open(str(cfd)+'/data/D04_input.txt', 'r')
lines = f.readlines()
lines = np.array([[l for l in line[:-1]] for line in lines])

def ind_neighbors(arr, itarget):
    Nrow, Ncol = arr.shape
    ind = [] # absolute
    # indz = [] # relative to zero
    for y in range(max(0,itarget[0]-1), min(Nrow,itarget[0]+2)):
        for x in range(max(0,itarget[1]-1), min(Ncol,itarget[1]+2)):
            dy = y-itarget[0]
            dx = x-itarget[1]
            if (dy!=0) or (dx!=0):
                ind.append((y, x))
                # indz.append((dy,dx))
    return np.array(ind)#, np.array(indz)

def puzzle_solver(text, word):
    ind0 = np.array(np.where(lines==word[0])).T
    involved = np.full(lines.shape, False)
    count = 0
    for i0 in ind0:
        i0 = tuple(i0)
        indPrev = [i0]
        solved = True
        for c in word[1:]:
            indNext = []
            delta_filter = []
            for i, iPrev in enumerate(indPrev):
                iNext = [ind for ind in ind_neighbors(lines, iPrev) if lines[tuple(ind)]==c]
                delta = [tuple(a-b for a, b in zip(ind, iPrev)) for ind in iNext]
                if c==word[1]:
                    delta_filter = delta
                    indNext.extend(iNext)
                else:
                    for j, d in enumerate(delta):
                        if d==delta0[i]:
                            delta_filter.append(d)
                            indNext.append(iNext[j])
            delta0 = delta_filter
            indPrev = indNext
            if not indPrev:
                solved = False
                break
        if solved:
            for iPrev in indPrev:
                involved[tuple(iPrev)] = True
            count += 1
    return count, involved

word = ['X', 'M', 'A', 'S']
count, involved = puzzle_solver(lines, word)

for y in range(lines.shape[0]):
    for x in range(lines.shape[1]):
        if not involved[y,x]:
            lines[y,x] = '.'

print(f'XMAS appear {count} times.')
