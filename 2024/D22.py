#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path
# import itertools

## Current file direction
cfd = Path(__file__).parent.absolute()

## Read input
with open(str(cfd) + '/data/D22_input.txt', 'r') as f:
    lines = list(map(int, f.readlines()))

def mix(num1, num2):
    return num1 ^ num2

def prune(num):
    return num % 16777216

def next_secret(s):
    s = prune(mix(s*64, s))
    s = prune(mix(s//32, s))
    return prune(mix(s*2048, s))

Nstep = 2000
secrets = lines
for i in range(Nstep):
    secrets = [next_secret(s) for s in secrets]

print(f'The sum of the {Nstep}th secret number is {sum(secrets)}.')

Nseq = 4
# sequences = list(itertools.product(range(-9, 10), repeat=Nseq))
for i in range(Nstep):
    if i==0:
        secrets = [lines]
        changes = []
    else:
        s0 = []
        c = []
        for s in secrets[-1]:
            s0.append(next_secret(s))
            c.append(next_secret(s) % 10 - s % 10)
        secrets.append(s0)
        changes.append(c)
secrets = list(map(list, zip(*secrets)))
changes = list(map(list, zip(*changes)))
sequences = set()
for c in changes:
    sequences.update(tuple(c[j:j+Nseq]) for j in range(len(c)-Nseq+1))

ind = {seq:[] for seq in sequences}
for i, c in enumerate(changes):
    used_seq_i = set()
    for j in range(len(c)-Nseq+1):
        seq = tuple(c[j:j+Nseq])
        if seq in ind and (seq, i) not in used_seq_i:
            ind[seq].append((i, j))
            used_seq_i.add((seq, i))

nb = {}
for seq in sequences:
    num_bananas = 0
    for i, j in ind[seq]:
        # if len(ind[seq])>2:
        #     print(seq, ind[seq], i, j, secrets[i][j+Nseq] % 10)
        num_bananas += secrets[i][j+Nseq] % 10
    nb[seq] = num_bananas

print(f'I can get {max(nb.values())} bananas.')