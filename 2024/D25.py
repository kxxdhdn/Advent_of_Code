#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path

## Current file direction
cfd = Path(__file__).parent.absolute()

## Read input
with open(str(cfd) + '/data/D25_input.txt', 'r') as f:
    lines = f.read().split('\n\n')

locks, keys = [], []
for line in lines:
    unit = line.splitlines()
    val = [0] * len(unit[0])
    for row in unit[1:-1]:
        for i in range(len(row)):
            if row[i]=='#':
                val[i] += 1
    if all(u=='#' for u in unit[0]) and all(u=='.' for u in unit[-1]):
        locks.append(val)
    if all(u=='.' for u in unit[0]) and all(u=='#' for u in unit[-1]):
        keys.append(val)

count = 0
for lock in locks:
    for key in keys:
        trying = [sum(pair) for pair in zip(lock, key)]
        if all(x<=5 for x in trying):
            count += 1

print(f'{count} unique lock/key pairs fit together.')