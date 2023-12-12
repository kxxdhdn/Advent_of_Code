#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path
from copy import deepcopy
import numpy as np

## Current file direction
cfd = Path(__file__).parent.absolute()

## Read input
# with open(str(cfd)+'/data/test.txt', 'r') as f:
with open(str(cfd)+'/data/d11_input.txt', 'r') as f:
    universe = f.read().split('\n')[:-1] # empty line in the end
    # universe = [[v for v in l] for l in universe]
    universe = np.array([np.array([v for v in l]) for l in universe])
# print(universe)

## Universe expansion
Ux = input("Enter the expansion unit: ") # expansion unit for part two counts
print("Ux = {}\n".format(Ux))
Ux = int(float(Ux))
Ux1 = 1

univ0 = deepcopy(universe) # cache original universe
Nx0 = len(univ0[0]) # col size
Ny0 = len(univ0) # row size
# print(Ny0, Nx0, univ0[0][:Nx0])
## Insert row
nrow = []
irow = 0
for y in range(Ny0):
    if not '#' in univ0[y,:]:
        nrow.append(y+irow)
        irow += Ux1
for n in nrow:
    universe = np.insert(universe, n, ['!']*universe.shape[1], axis=0)
    # universe = np.insert(universe, n, np.full([Ux, universe.shape[1]], '.'), axis=0)
## Insert col
ncol = []
icol = 0
for x in range(Nx0):
    if not '#' in univ0[:,x]:
        ncol.append(x+icol)
        icol += Ux1
for n in ncol:
    universe = np.insert(universe, n, ['!']*universe.shape[0], axis=1)
    # universe = np.insert(universe, n, np.full([Ux, universe.shape[0]], '.'), axis=1)
univ = deepcopy(universe) # cache expanded universe
Nx = len(univ[0]) # col size
Ny = len(univ) # row size
# print(Ny, Nx, univ[0][:Nx])
## Galaxy localization
gal = 0
pos = {}
for y in range(Ny):    
    for x in range(Nx):
        if univ[y][x]=='#':
            gal += 1
            # universe[y][x] = gal
            pos.update({gal: [x, y]})

## Part one counts
lengths = 0
for i in range(gal):
    i += 1
    for j in range(i,gal):
        j += 1
        lengths += sum([abs(a - b) for a, b in zip(pos[i], pos[j])])
        ## Expanded positions
        x0, x1 = min(pos[i][0], pos[j][0]), max(pos[i][0], pos[j][0])
        y0, y1 = min(pos[i][1], pos[j][1]), max(pos[i][1], pos[j][1])
        uniques, counts = np.unique(
            universe[y0, x0:x1], 
            return_counts=True)
        horiz = dict(zip(uniques, counts))
        uniques, counts = np.unique(
            universe[y0:y1, x0], 
            return_counts=True)
        vert = dict(zip(uniques, counts))
        # print(i, j, [abs(a - b) for a, b in zip(pos[i], pos[j])], horiz, vert)
        Nh, Nv = 0, 0
        if '!' in horiz:
            Nh = horiz['!']
        if '!' in vert:
            Nv = vert['!']
        print(Nh, Nv)
        lengths += (Nh + Nv) * (Ux-2)

## Part one answer (input Ux=1)
## Part two answer
print("With an expansion unit of {}, the sum of the lengths of the shortest path "
      "between every pair of galaxies is {}.\n".format(Ux, lengths))
