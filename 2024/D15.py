#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path
import numpy as np

## Current file direction
cfd = Path(__file__).parent.absolute()

## Read input
with open(str(cfd) + '/data/D15_input.txt', 'r') as f:
    state_init, moves = f.read().strip().split('\n\n')

def ilocate(target, grid):
    # return [(i,j) for i,row in enumerate(grid) for j,pos in enumerate(row) if pos==target]
    return np.array(np.where(grid==target)).T

imove = {'<':(0,-1), '>':(0,1), '^':(-1,0), 'v':(1,0)}

state = np.array([[pos for pos in row] for row in state_init.splitlines()])
for m in [m for row in moves.splitlines() for m in row]:
    irobot = tuple(ilocate('@', state)[0])
    inext = (irobot[0]+imove[m][0], irobot[1]+imove[m][1])
    if state[inext]=='.':
        state[inext] = '@'
        state[irobot] = '.'
    elif state[inext]=='O':
        ii = inext
        while state[ii]=='O':
            ii = (ii[0]+imove[m][0], ii[1]+imove[m][1])
        if state[ii]=='.':
            state[ii] = 'O'
            state[inext] = '@'
            state[irobot] = '.'

    # print(f'Move {m}:\n', state, '\n')

state_final = state
iboxes = ilocate('O', state_final)
coords = [100 * i + j for i, j in iboxes]

print(f'The sum of all boxes GPS coordinates is {sum(coords)}.')

## Scaled case
state = []
for row in state_init.splitlines():
    srow = []
    for pos in row:
        if pos=='@':
            srow.extend([pos, '.'])
        elif pos=='O':
            srow.extend(['[', ']'])
        else:
            srow.extend([pos, pos])
    state.append(srow)
state = np.array(state)

for m in [m for row in moves.splitlines() for m in row]:
    irobot = tuple(ilocate('@', state)[0])
    inext = (irobot[0]+imove[m][0], irobot[1]+imove[m][1])
    if state[inext]=='.':
        state[inext] = '@'
        state[irobot] = '.'
    else:
        if imove[m][0]==0:#np.isin(m, ['<', '>']):
        # elif np.logical_or(state[inext]==']' and m=='<', state[inext]=='[' and m=='>'):
            ii = inext
            state_old = state.copy()
            while np.isin(state[ii], ['[', ']']):
                state[ii] = ']' if state[ii]=='[' else '['
                ii = (ii[0], ii[1]+imove[m][1]) # imove[m][0] = 0
            if state[ii]=='.':
                state[ii] = '[' if m=='<' else ']'
                state[inext] = '@'
                state[irobot] = '.'
            else:
                state = state_old # do NOT move
        elif imove[m][1]==0:#np.isin(m, ['^', 'v']):
            '''
            Find such block and move it globally
    
            ..  ..   # '..' attached to previous line '[]' #   []  []
            [] .[]   # '[]' attached to previous line '[]' #   [] [].
            [].[]    #                                     #   .[][]
             [][]    #                                     #    .[].
              []     # '[]' attached to robot              #     .@
               @     #                                     #      .
    
            '''
            im0 = imove[m][0] # imove[m][1] = 0
            irow, icol = irobot
            clear = {icol:False}
            connected = np.full(state.shape, False)
            connected[irobot] = True
            stay = False # do NOT move
            while not all(clear.values()):
                irow += im0
                clear0 = clear.copy()
                for k, v in clear.items():
                    if not v:
                        if state[irow,k]=='[':
                            clear0[k+1] = False
                            connected[irow,k:k+2] = True
                        elif state[irow,k]==']':
                            clear0[k-1] = False
                            connected[irow,k-1:k+1] = True
                        elif state[irow,k]=='.':
                            clear0[k] = True
                        else:
                            stay = True
                            break
                if stay:
                    break
                clear = clear0
            if not stay:
                state_old = state.copy()
                imin = min(irobot[0], irow)
                imax = max(irobot[0], irow) + 1
                for i in range(imin, imax):
                    # Find missed elements on both sides of brackets
                    ind = []
                    for j in range(state_old.shape[1]):
                        if state_old[i,j]=='[' and np.isin(state_old[i-im0,j], ['@','[', ']']) and connected[i-im0,j]:
                            ind.extend([j,j+1])
                        if state_old[i,j]==']' and np.isin(state_old[i-im0,j], ['@','[',']']) and connected[i-im0,j]:
                            ind.extend([j,j-1])
                    ind = np.where(connected[i])
                    state[i+im0][ind] = state_old[i][ind]
                    ind = np.where(np.logical_and(connected[i], ~connected[i-im0]))
                    state[i][ind] = '.'
                # print(connected)
                # print(state, 'coucou')
                # exit()
    
    # print(f'Move {m}:\n', state, '\n')

state_final = state
iboxes = ilocate('[', state_final)
coords = [100 * i + j for i, j in iboxes]

print(f'The sum of all scaled boxes GPS coordinates is {sum(coords)}.')