#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path
from copy import deepcopy
import numpy as np

## Current file direction
cfd = Path(__file__).parent.absolute()

## Read input
with open(str(cfd)+'/data/test.txt', 'r') as f:
# with open(str(cfd)+'/data/D16_input.txt', 'r') as f:
    contrap = f.read().split('\n')[:-1] # empty line in the end
    # contrap = [[v for v in l] for l in contrap]
    contrap = np.array([np.array([v for v in l]) for l in contrap])
# print(contrap)

Ny, Nx = contrap.shape
prevdir = np.empty(contrap.shape, dtype=str) # previous beam direction
bmfront = np.full(contrap.shape, False) # Is the front of a light beam?
pathmap = np.full(contrap.shape, '.') # beam path map
active = True # Do active branches exist?
## Boot up
print("The beam enters in the top-left corner from the left "
      "and heading to the right.\n")
bmfront[0][0] = True
prevdir[0][0] = '>'
endbm = 0 # number of ended light beams
Nscan = 0
while active:
    Nscan += 1
    print("Scan no. ", Nscan)
    for y in range(Ny):
        for x in range(Nx):
            if bmfront[y][x]: # only proceed beam front at each map scan
                t = contrap[y][x] # current tile
                for d in prevdir[y][x]: # previous beam directions
                    if t=='.':
                        if d=='>':
                            try:
                                prevdir[y][x+1].append('>')
                                bmfront[y][x+1] = True
                            except:
                                endbm += 1
                                print("No. {} light beam ended.\n".format(endbm))
                        elif d=='^':
                            try:
                                prevdir[y-1][x].append('^')
                                bmfront[y-1][x] = True
                            except:
                                endbm += 1
                                print("No. {} light beam ended.\n".format(endbm))
                        elif d=='<':
                            try:
                                prevdir[y][x-1].append('<')
                                bmfront[y][x-1] = True
                            except:
                                endbm += 1
                                print("No. {} light beam ended.\n".format(endbm))
                        elif d=='v':
                            try:
                                prevdir[y+1][x].append('v')
                                bmfront[y+1][x] = True
                            except:
                                endbm += 1
                                print("No. {} light beam ended.\n".format(endbm))
                        ## Update path map
                        if pathmap[y][x]=='.' and len(prevdir[y][x])==1:
                            pathmap[y][x] = prevdir[y][x][0]
                        else:
                            pathmap[y][x] = '2'
                    elif t=='/':
                        if d=='>':
                            try: 
                                prevdir[y-1][x].append('^')
                                bmfront[y-1][x] = True
                            except:
                                endbm += 1
                                print("No. {} light beam ended.\n".format(endbm))
                        elif d=='^':
                            try:
                                prevdir[y][x+1].append('>')
                                bmfront[y][x+1] = True
                            except:
                                endbm += 1
                                print("No. {} light beam ended.\n".format(endbm))
                        elif d=='<':
                            try:
                                prevdir[y][x-1].append('v')
                                bmfront[y][x-1] = True
                            except:
                                endbm += 1
                                print("No. {} light beam ended.\n".format(endbm))
                        elif d=='v':
                            try:
                                prevdir[y+1][x].append('<')
                                bmfront[y+1][x] = True
                            except:
                                endbm += 1
                                print("No. {} light beam ended.\n".format(endbm))
                        ## Update path map
                        pathmap[y][x] = t
                    elif t=='\\':
                        if d=='>':
                            try:
                                prevdir[y][x+1].append('v')
                                bmfront[y][x+1] = True
                            except:
                                endbm += 1
                                print("No. {} light beam ended.\n".format(endbm))
                        elif d=='v':
                            try:
                                prevdir[y+1][x].append('>')
                                bmfront[y+1][x] = True
                            except:
                                endbm += 1
                                print("No. {} light beam ended.\n".format(endbm))
                        elif d=='<':
                            try:
                                prevdir[y][x-1].append('^')
                                bmfront[y][x-1] = True
                            except:
                                endbm += 1
                                print("No. {} light beam ended.\n".format(endbm))
                        elif d=='^':
                            try:
                                prevdir[y-1][x].append('<')
                                bmfront[y-1][x] = True
                            except:
                                endbm += 1
                                print("No. {} light beam ended.\n".format(endbm))
                        ## Update path map
                        pathmap[y][x] = t
                    elif t=='-':
                        if d=='^' or d=='v':
                            try:
                                prevdir[y][x-1].append('<')
                                bmfront[y][x-1] = True
                            except:
                                endbm += 1
                                print("No. {} light beam ended.\n".format(endbm))
                            try:
                                prevdir[y][x+1].append('>')
                                bmfront[y][x+1] = True
                            except:
                                endbm += 1
                                print("No. {} light beam ended.\n".format(endbm))
                        ## Update path map
                        pathmap[y][x] = t
                    elif t=='|':
                        if d=='>' or d=='<':
                            try:
                                prevdir[y-1][x].append('^')
                                bmfront[y-1][x] = True
                            except:
                                endbm += 1
                                print("No. {} light beam ended.\n".format(endbm))
                            try:
                                prevdir[y+1][x].append('v')
                                bmfront[y+1][x] = True
                            except:
                                endbm += 1
                                print("No. {} light beam ended.\n".format(endbm))
                        ## Update path map
                        pathmap[y][x] = t
                ## Update light beam front
                bmfront[y][x] = False
    ## Check active light beams
    if not any(bmfront.flatten()):
        active = False

## Part one counts
Ne = 0
for y in range(Ny):
    for x in range(Nx):
        if pathmap[y][x]!='.':
            Ne += 1

## Part one answer
print("{} tiles end up being energized.\n".format(Ne))
