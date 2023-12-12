#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path
from copy import deepcopy
# import numpy as np

## Current file direction
cfd = Path(__file__).parent.absolute()

## Read input
with open(str(cfd)+'/data/test.txt', 'r') as f:
# with open(str(cfd)+'/data/d10_input.txt', 'r') as f:
    mapipes = f.read().split('\n')[:-1] # empty line in the end
    mapipes = [[v for v in l] for l in mapipes]
    # mapipes = np.array([np.array([v for v in l]) for l in mapipes])
# print(mapipes)
map0 = deepcopy(mapipes) # cache original map


## Part one counts
Nx = len(map0[0]) # col size
Ny = len(map0) # row size
# print(Ny, Nx, map0[0][:Nx])
## Numerize the starting position
for y, row in enumerate(map0):
    if 'S' in row:
        y0, x0 = y, row.index('S')
# if len(np.argwhere(map0=='S'))>1:
#     print("Warning: More than one starting position!\n")
# y0, x0 = np.argwhere(map0=='S')[0]
print("The starting position is ({}, {})".format(x0, y0))
mapipes[y0][x0] = 0 # numerisation
## Numerize the four possible itineraries
Niter = 4
counters = [1]*Niter # number of steps of all itineraries
pos = [[x0, y0] for _ in range(Niter)] # current positions of all itineraries
flags = [True]*Niter # False when an itinerary stops
## Boost operations
pos0 = deepcopy(pos) # cache current position
for i in range(Niter):
    x, y = pos0[i] # current position
    if i==0:
        pn = map0[y-1][x] # next pipe if go up
        if y0-1<0 or pn=='J' or pn=='-' or pn=='L' or pn=='.':
            flags[i] = False # stop
        else: # step forward
            mapipes[y-1][x] = counters[i]
            pos[i][1] += -1 # update position
            print(1, i, 'S up', pos[i])
    if i==1:
        pn = map0[y+1][x] # next pipe if go down
        if y0+1>=Ny or pn=='7' or pn=='-' or pn=='F' or pn=='.':
            flags[i] = False # stop
        else: # step forward
            mapipes[y+1][x] = counters[i]
            pos[i][1] += 1 # update position
            print(1, i, 'S down', pos[i])
    if i==2:
        pn = map0[y][x-1] # next pipe if go left
        if x0-1<0 or pn=='J' or pn=='|' or pn=='7' or pn=='.':
            flags[i] = False # stop
        else: # step forward
            mapipes[y][x-1] = counters[i]
            pos[i][0] += -1 # update position
            print(1, i, 'S left', pos[i])
    if i==3:
        pn = map0[y][x+1] # next pipe if go right
        if x0+1>=Nx or pn=='L' or pn=='|' or pn=='F' or pn=='.':
            flags[i] = False # stop
        else: # step forward
            mapipes[y][x+1] = counters[i]
            pos[i][0] += 1 # update position
            print(1, i, 'S right', pos[i])
## Regular operations
steps = 1
while any(flags):
    steps += 1
    ## Simultaneously go four directions
    prev = deepcopy(pos0) # cache previous position
    pos0 = deepcopy(pos) # cache current position
    # map0 = deepcopy(mapipes) # cache current mapipes
    for i in range(Niter):
        if flags[i]:
            counters[i] += 1
            x, y = pos0[i] # current position
            if map0[y][x]=='J':
                if prev[i][1]==y-1: # next go left
                    pn = map0[y][x-1]
                    if pn=='J' or pn=='|' or pn=='7' or pn=='.':
                        flags[i] = False # stop
                    else: # step forward
                        mapipes[y][x-1] = counters[i]
                        pos[i][0] += -1 # update position
                        print(steps, i, 'J left', pos[i])
                if prev[i][0]==x-1: # next go up
                    pn = map0[y-1][x]
                    if pn=='J' or pn=='-' or pn=='L' or pn=='.':
                        flags[i] = False # stop
                    else: # step forward
                        mapipes[y-1][x] = counters[i]
                        pos[i][1] += -1 # update position
                        print(steps, i, 'J up', pos[i])
            if map0[y][x]=='7':
                if prev[i][1]==y+1: # next go left
                    pn = map0[y][x-1]
                    if pn=='J' or pn=='|' or pn=='7' or pn=='.':
                        flags[i] = False # stop
                    else: # step forward
                        mapipes[y][x-1] = counters[i]
                        pos[i][0] = x-1 # update position
                        print(steps, i, '7 left', pos[i])
                if prev[i][0]==x-1: # next go down
                    pn = map0[y+1][x]
                    if pn=='7' or pn=='-' or pn=='F' or pn=='.':
                        flags[i] = False # stop
                    else: # step forward
                        mapipes[y+1][x] = counters[i]
                        pos[i][1] = y+1 # update position
                        print(steps, i, '7 down', pos[i])
            if map0[y][x]=='L':
                if prev[i][1]==y-1: # next go right
                    pn = map0[y][x+1]
                    if pn=='L' or pn=='|' or pn=='F' or pn=='.':
                        flags[i] = False # stop
                    else: # step forward
                        mapipes[y][x+1] = counters[i]
                        pos[i][0] = x+1 # update position
                        print(steps, i, 'L right', pos[i])
                if prev[i][0]==x+1: # next go up
                    pn = map0[y-1][x]
                    if pn=='J' or pn=='-' or pn=='L' or pn=='.':
                        flags[i] = False # stop
                    else: # step forward
                        mapipes[y-1][x] = counters[i]
                        pos[i][1] = y-1 # update position
                        print(steps, i, 'L up', pos[i])
            if map0[y][x]=='F':
                if prev[i][1]==y+1: # next go right
                    pn = map0[y][x+1]
                    if pn=='L' or pn=='|' or pn=='F' or pn=='.':
                        flags[i] = False # stop
                    else: # step forward
                        mapipes[y][x+1] = counters[i]
                        pos[i][0] = x+1 # update position
                        print(steps, i, 'F right', pos[i])
                if prev[i][0]==x+1: # next go down
                    pn = map0[y+1][x]
                    if pn=='7' or pn=='-' or pn=='F' or pn=='.':
                        flags[i] = False # stop
                    else: # step forward
                        mapipes[y+1][x] = counters[i]
                        pos[i][1] = y+1 # update position
                        print(steps, i, 'F down', pos[i])
            if map0[y][x]=='|':
                if prev[i][1]==y-1: # next go down
                    pn = map0[y+1][x]
                    if pn=='7' or pn=='-' or pn=='F' or pn=='.':
                        flags[i] = False # stop
                    else: # step forward
                        mapipes[y+1][x] = counters[i]
                        pos[i][1] = y+1 # update position
                        print(steps, i, '| down', pos[i])
                if prev[i][1]==y+1: # next go up
                    pn = map0[y-1][x]
                    if pn=='J' or pn=='-' or pn=='L' or pn=='.':
                        flags[i] = False # stop
                    else: # step forward
                        mapipes[y-1][x] = counters[i]
                        pos[i][1] = y-1 # update position
                        print(steps, i, '| up', pos[i])
            if map0[y][x]=='-':
                if prev[i][0]==x+1: # next go left
                    pn = map0[y][x-1]
                    if pn=='J' or pn=='|' or pn=='7' or pn=='.':
                        flags[i] = False # stop
                    else: # step forward
                        mapipes[y][x-1] = counters[i]
                        pos[i][0] = x-1 # update position
                        print(steps, i, '- left', pos[i])
                if prev[i][0]==x-1: # next go right
                    pn = map0[y][x+1]
                    if pn=='L' or pn=='|' or pn=='F' or pn=='.':
                        flags[i] = False # stop
                    else: # step forward
                        mapipes[y][x+1] = counters[i]
                        pos[i][0] = x+1 # update position
                        print(steps, i, '- right', pos[i])
    
    ## Force quit (two itineraries encounter)
    if all(pos.count(p)==2 for p in pos) or pos.count(pos[0])==4:
        flags = [False]*Niter

## Part one answer
Nstep = max(counters)
print("It takes {} steps along the loop to get from the starting position "
      "to the point farthest from the starting position.\n".format(str(Nstep)))

## Part two counts
tiles = []
i = 0
for y in range(Ny):
    for x in range(Nx):
        if isinstance(mapipes[y][x], str):
            pu = mapipes[max(y-1,0)][x]
            pl = mapipes[y][max(x-1,0)]
            iu, il = 0, 0
            if str(pu)[0]=='T': # check up
                iu = int(pu[1:])
            if str(pl)[0]=='T': # check left
                il = int(pl[1:])
            if iu<il and iu>0:
                mapipes[y][x] = 'T'+ str(iu)
                ## Correct left
                # if il in tiles:
                #     tiles.remove(il)
                #     print("coucou", tiles, il)
                for iy in range(Ny):
                    for ix in range(Nx):
                        if mapipes[iy][ix]=='T' + str(il):
                            mapipes[iy][ix] = 'T'+ str(iu)
            elif iu>il and il>0:
                mapipes[y][x] = 'T'+ str(il)
                ## Correct up
                # if iu in tiles:
                #     tiles.remove(iu)
                #     print("doudou", tiles, iu)
                for iy in range(Ny):
                    for ix in range(Nx):
                        if mapipes[iy][ix]=='T' + str(iu):
                            mapipes[iy][ix] = 'T' + str(il)
            elif (iu>0 and il==0) or (iu>0 and iu==il):
                mapipes[y][x] = 'T'+ str(iu)
            elif iu==0:
                if il>0:
                    mapipes[y][x] = 'T'+ str(il)
                else: # il==0
                    i += 1
                    tiles.append(i)
                    mapipes[y][x] = 'T'+str(i)
## Exclude tile groups touching the edges
edges = []
for y in range(Ny):
    p = str(mapipes[y][0])
    if p[0]=='T':
        ie = int(p[1:])
        if ie not in edges:
            edges.append(ie)
    p = str(mapipes[y][Nx-1])
    if p[0]=='T':
        ie = int(p[1:])
        if ie not in edges:
            edges.append(ie)
for x in range(Nx):
    p = str(mapipes[0][x])
    if p[0]=='T':
        ie = int(p[1:])
        if ie not in edges:
            edges.append(ie)
    p = str(mapipes[Ny-1][x])
    if p[0]=='T':
        ie = int(p[1:])
        if ie not in edges:
            edges.append(ie)
print('edges: ', edges)
# tiles = list(range(1,i+1))
for i in edges:
    if i in tiles:
        tiles.remove(i)

## Exclude tile groups going across odd number of vertical lines
for y in range(Ny):
    for x in range(Nx):
        if str(mapipes[y][x])[0]=='T':
            for 

print('tiles: ', tiles)
tilestr = ['T'+str(i) for i in tiles]

Ntile = 0
for y in range(Ny):
    for x in range(Nx):
        if mapipes[y][x] in tilestr:
            Ntile += 1

## Part two answer
print("{} tiles are enclosed by the loop.".format(str(Ntile)))
print(mapipes)
