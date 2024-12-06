#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path
import numpy as np

## Current file direction
cfd = Path(__file__).parent.absolute()

## Read input
f = open(str(cfd)+'/data/D06_input.txt', 'r')
lines = f.read().splitlines()
lines = np.array([[l for l in line] for line in lines])

def walk(iloc, fc):
    iloc = list(iloc)
    if fc=='^':
        iloc[0] += -1
    if fc=='>':
        iloc[1] += +1
    if fc=='v':
        iloc[0] += 1
    if fc=='<':
        iloc[1] += -1
    return tuple(iloc)

def mapping(istart, walkmap):
    mapshape = walkmap.shape
    iguard = istart
    facing = ['^', '<', 'v', '>']
    fc = facing[0]
    fcmap = walkmap.copy()
    loop = False
    inmap = True
    while inmap and (not loop):
        if walkmap[iguard]=='X' and fcmap[iguard]==fc:
            loop = True
        walkmap[iguard] = 'X'
        fcmap[iguard] = fc
        inext = walk(iguard, fc)
        inmap = all(0<=i<bound for i, bound in zip(inext, mapshape))
        if inmap:
            if walkmap[inext]=='#':
                fc = facing[facing.index(fc)-1]
                inext = walk(iguard, fc)
                inmap = all(0<=i<bound for i, bound in zip(inext, mapshape))
                if inmap:
                    if walkmap[inext]=='#':
                        # Walk backward
                        fc = facing[facing.index(fc)-1]
                        iguard = walk(iguard, fc)
                    else:
                        iguard = inext
            else:
                iguard = inext
    return walkmap, loop

istart = tuple(i[0] for i in np.where(lines=='^'))
mapped_area, is_loop = mapping(istart, lines)

countX = len(np.where(mapped_area=='X')[0])
print(f'The guard will visit {countX} distinct positions before leaving the mapped area.')

ind = [tuple(i) for i in np.array(np.where(lines!=('#' or '^'))).T]
countLoop = 0
for iloc in ind:
    new_map = lines.copy()
    new_map[iloc] = '#'
    _, is_loop = mapping(istart, new_map)
    if is_loop:
        countLoop += 1

print(f'We could choose {countLoop} positions for the obstruction.')