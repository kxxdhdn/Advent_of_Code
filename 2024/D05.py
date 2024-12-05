#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path
import numpy as np

## Current file direction
cfd = Path(__file__).parent.absolute()

## Read input
f = open(str(cfd)+'/data/D05_input.txt', 'r')
lines = f.read().splitlines()
ordering = np.array([(int(line[0:line.index('|')]), int(line[line.index('|')+1:])) for line in lines if '|' in line])
updates = [[int(page) for page in line.split(',')] for line in lines if ',' in line]

def check_ordering(update, ordering):
    ordered = True
    for j, page in enumerate(update):
        ind_o = np.array(np.where(ordering==page)).T
        for ind in ind_o:
            if ind[1]==0 and ordering[ind[0], 1-ind[1]] in update[:j]:
                ordered = False
                break
            if ind[1]==1 and ordering[ind[0], 1-ind[1]] in update[j+1:]:
                ordered = False
                break
        if not ordered:
            break
    return ordered

result = 0
updates_misordered = []
for update in updates:
    ordered = check_ordering(update, ordering)

    if ordered:
        result += update[int((len(update)-1)/2)]
    else:
        updates_misordered.append(update)

print(f'Sum of middle page number from correctly-ordered updates: {result}')

def swap_pages(update, p1, p2):
    i1, i2 = update.index(p1), update.index(p2)
    update[i2], update[i1] = p1, p2
    return update

def reorder_update(update, ordering):
    ordered = check_ordering(update, ordering)
    while not ordered:
        swapped = False
        for j, page in enumerate(update):
            ind_o = np.array(np.where(ordering==page)).T
            for ind in ind_o:
                if ind[1]==0 and ordering[ind[0], 1-ind[1]] in update[:j]:
                    update = swap_pages(update, page, ordering[ind[0], 1-ind[1]])
                    swapped = True
                    ordered = check_ordering(update, ordering)
                    break
                if ind[1]==1 and ordering[ind[0], 1-ind[1]] in update[j+1:]:
                    update = swap_pages(update, page, ordering[ind[0], 1-ind[1]])
                    swapped = True
                    ordered = check_ordering(update, ordering)
                    break
            if swapped:
                break
    return update

result = 0
for update in updates_misordered:
    update = reorder_update(update, ordering)

    result += update[int((len(update)-1)/2)]

print(f'Sum of middle page number from corrected updates: {result}')
