#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path
import numpy as np

## Current file direction
cfd = Path(__file__).parent.absolute()

## Read input
f = open(str(cfd)+'/data/D04_input.txt', 'r')
lines0 = f.readlines()
lines = np.array([[l for l in line[:-1]] for line in lines0])
Nrows, Ncols = lines.shape

def ind_neighbors(arr, itarget):
    Nrows, Ncols = arr.shape
    ind = [] # absolute
    # indz = [] # relative to zero
    for y in range(max(0,itarget[0]-1), min(Nrows,itarget[0]+2)):
        for x in range(max(0,itarget[1]-1), min(Ncols,itarget[1]+2)):
            dy = y-itarget[0]
            dx = x-itarget[1]
            if (dy!=0) or (dx!=0):
                ind.append((y, x))
                # indz.append((dy,dx))
    return np.array(ind)#, np.array(indz)

indX = np.array(np.where(lines=='X')).T
involved = np.full(lines.shape, False)
count = 0
for iX in indX:
    iX = tuple(iX)
    indM = np.array([ind for ind in ind_neighbors(lines, iX) if lines[tuple(ind)]=='M'])
    for iM in indM:
        iM = tuple(iM)
        indA = np.array([ind for ind in ind_neighbors(lines, iM) if lines[tuple(ind)]=='A'])
        for iA in indA:
            iA = tuple(iA)
            indS = np.array([ind for ind in ind_neighbors(lines, iA) if lines[tuple(ind)]=='S'])
            for iS in indS:
                iS = tuple(iS)
                dXM = [a - b for a, b in zip(iX, iM)]
                dMA = [a - b for a, b in zip(iM, iA)]
                dAS = [a - b for a, b in zip(iA, iS)]
                ## XMAS puzzle
                if dXM==dMA and dMA==dAS:
                    for i in (iX,iM,iA,iS):
                        involved[i] = True
                    count += 1

for y in range(Nrows):
    for x in range(Ncols):
        if not involved[y,x]:
            lines[y,x] = '.'

print(f'XMAS appear {count} times.')

## X-MAS puzzel
def check_x_mas(arr, itarget):
    ul = arr[itarget[0]-1,itarget[1]-1]
    br = arr[itarget[0]+1,itarget[1]+1]
    bl = arr[itarget[0]+1,itarget[1]-1]
    ur = arr[itarget[0]-1,itarget[1]+1]
    ulbr, blur = False, False
    if ul=='M' and br=='S':
        ulbr = True
    if ul=='S' and br=='M':
        ulbr = True
    if bl=='M' and ur=='S':
        blur = True
    if bl=='S' and ur=='M':
        blur = True
    if ulbr and blur:
        return True
    else:
        return False

lines = np.array([[l for l in line[:-1]] for line in lines0])

indA = np.array(np.where(lines=='A')).T
indA = np.array([iA for iA in indA if all(iA!=0) and iA[0]<Nrows-1 and iA[1]<Ncols-1])
involved = np.full(lines.shape, False)
count = 0
for iA in indA:
    iA = tuple(iA)
    if check_x_mas(lines, iA):
        iul = (iA[0]-1, iA[1]-1)
        ibr = (iA[0]+1, iA[1]+1)
        ibl = (iA[0]+1, iA[1]-1)
        iur = (iA[0]-1, iA[1]+1)
        for i in (iA, iul, ibr, ibl, iur):
            involved[i] = True
        count += 1

for y in range(Nrows):
    for x in range(Ncols):
        if not involved[y,x]:
            lines[y,x] = '.'

print(f'X-MAS appear {count} times.')