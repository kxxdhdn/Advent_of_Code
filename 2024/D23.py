#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path
from itertools import count

## Current file direction
cfd = Path(__file__).parent.absolute()

## Read input
with open(str(cfd) + '/data/D23_input.txt', 'r') as f:
    lines = f.read().splitlines()
connexions = [sorted(line.split('-')) for line in lines]

inter3co = {}
for j, c in enumerate(connexions):
    for i, com in enumerate(c):
        for pair in connexions[:j]+connexions[j+1:]:
            if com in pair:
                key = set(pair)
                key.update([c[1-i]])
                # print(key)
                key = tuple(sorted(key))
                if key in inter3co:
                    inter3co[key] = True
                else:
                    if sorted([c[1-i], pair[1-pair.index(com)]]) in connexions:
                        inter3co[key] = False
inter3co = {k:v for k, v in inter3co.items() if v} # drop False
num_start_t = 0
for inter3 in inter3co:
    for com in inter3:
        if com[0]=='t':
            num_start_t += 1
            break

print(f'{num_start_t} contain at least one computer with a name that starts with t.')

computers = set()
for c in connexions:
    computers.update(c)
computers = list(computers)
interMAXco = {}
for i, com in enumerate(computers[:-1]):
    if i%100==0:
        print(f'{i+1} / {len(computers)-1}\n...')
    elif i==len(computers)-2:
        print(f'{i+1} / {len(computers)-1}')
    interMAXco[com] = set([com])
    for j, com2 in enumerate(computers[:i]+computers[i+1:]):
        add = True
        for com3 in interMAXco[com]:
            if sorted([com2, com3]) not in connexions:
                add = False
        if add:
            interMAXco[com].update([com2])
max_connected = [v for v in interMAXco.values() if len(v)==max([len(vv) for vv in interMAXco.values()])]

print(f'LAN party password: {','.join(sorted(max_connected[0]))}')