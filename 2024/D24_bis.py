#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path
from itertools import combinations

## Current file direction
cfd = Path(__file__).parent.absolute()

## Read input
with open(str(cfd) + '/data/D24_input.txt', 'r') as f:
    lines = f.read().splitlines()

def gate_operation(c, gates):
    if c[1]=='AND':
        gates[c[4]] = gates[c[0]] and gates[c[2]]
    elif c[1]=='OR':
        gates[c[4]] = gates[c[0]] or gates[c[2]]
    elif c[1]=='XOR':
        gates[c[4]] = gates[c[0]] ^ gates[c[2]]
    return gates

def run(gates, connexions):
    unfinished = True
    while unfinished:
        unfinished = False
        for c in connexions:
            if c[0] in gates and c[2] in gates:
                gates = gate_operation(c, gates)
            else:
                unfinished = True
    zgates = {k:v for k,v in sorted(gates.items()) if k[0]=='z'}
    binum = ''
    for z in zgates:
        binum = str(gates[z]) + binum
    return int(binum, 2)

gates_init = {line.split(':')[0]:int(line.split(':')[1]) for line in lines if ':' in line}
connexions = [line.split(' ') for line in lines if '->' in line]
gates = gates_init
decnum = run(gates, connexions)

print(f'Output decimal number: {decnum}')

gates = gates_init
xgates = {k:v for k,v in sorted(gates.items()) if k[0]=='x'}
binum = ''
for x in xgates:
    binum = str(gates[x]) + binum
decx = int(binum, 2)
ygates = {k:v for k,v in sorted(gates.items()) if k[0]=='y'}
binum = ''
for y in ygates:
    binum = str(gates[y]) + binum
decy = int(binum, 2)

con2 = combinations(connexions, 2)
con2 = list(con2)
print(len(con2))
for j, p4 in enumerate(combinations(con2, 4)):
    # if j%10==0:
    #     print(f'{j} / {len(pair4)}')
    gates = gates_init
    connex = connexions.copy()
    for c2 in p4:
        for i, c in enumerate(connex):
            if c==c2[0]:
                connex[i][4] = c2[1][4]
            if c==c2[1]:
                connex[i][4] = c2[0][4]
    decnum = run(gates, connex)
    if decnum==decx+decy:
        swires = [c[4] for c2 in p4 for c in c2]
        break

print(f'Wires to be swapped: {','.join(sorted(swires))}')