#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path
import re
from multiprocessing import Pool

## Current file direction
cfd = Path(__file__).parent.absolute()

## Read input
with open(str(cfd) + '/data/D13_input.txt', 'r') as f:
    lines = f.read().split('\n\n')

def read_craw_machine(entry, Xshift=0):
    digits = list(map(int, re.findall(r'\d+', entry)))
    return {
        'A': (digits[0], digits[1]),
        'B': (digits[2], digits[3]),
        'X': (digits[4]+Xshift, digits[5]+Xshift),
    }

def analyse_craw_machine(cm):
    win = False
    tokens = 0
    for nx in range(cm['X'][0]//cm['A'][0]+1):
        ny, e = divmod(cm['X'][0]-cm['A'][0]*nx, cm['B'][0])
        if e==0 and cm['X'][1]==cm['A'][1]*nx+cm['B'][1]*ny:
            t = 3 * nx + ny
            tokens = t if not win else min(t, tokens)
            win = True
    return tokens

def parallel_analysis_unit(args):
    cm, nx = args
    win = False
    tokens = float('inf')
    ny, e = divmod(cm['X'][0]-cm['A'][0]*nx, cm['B'][0])
    if e==0 and cm['X'][1]==cm['A'][1]*nx+cm['B'][1]*ny:
        tokens = min(tokens, 3 * nx + ny)
        win = True
    return tokens

craw_machines = [read_craw_machine(line) for line in lines]
total_tokens = 0
for cm in craw_machines:
    total_tokens += analyse_craw_machine(cm)

    # nx_range = range(cm['X'][0]//cm['A'][0]+1)
    # print(nx_range)
    # with Pool() as pool:
    #     possible_tokens = pool.map(parallel_analysis_unit, ((cm, nx) for nx in nx_range))
    # tokens = min(possible_tokens)
    # total_tokens += tokens if tokens!=float('inf') else 0

print(f'The fewest tokens one would have to spend to win all possible prizes are {total_tokens}.')

Xshift = 10000000000000
crazy_craw_machines = [read_craw_machine(line, Xshift) for line in lines]
total_tokens = 0
for cm in crazy_craw_machines:
    # total_tokens += analyse_craw_machine(cm)

    nx_range = range(cm['X'][0]//cm['A'][0]+1)
    print(nx_range)
    with Pool() as pool:
        possible_tokens = pool.map(parallel_analysis_unit, ((cm, nx) for nx in nx_range))
    tokens = min(possible_tokens)
    total_tokens += tokens if tokens!=float('inf') else 0

print(f'To win all possible prizes of crazy craw machines, you will need at least {total_tokens} tokens.')
