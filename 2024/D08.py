#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path
import itertools

## Current file direction
cfd = Path(__file__).parent.absolute()

## Read input
f = open(str(cfd)+'/data/D08_input.txt', 'r')
lines = f.read().splitlines()
lines = [[l for l in line] for line in lines]
Ni, Nj = len(lines), len(lines[0])
antinodes = lines.copy()
antennas = list(set(x for row in lines for x in row if x!='.'))
dict_antennas = {x: [(i, j) for i, row in enumerate(lines) for j, val in enumerate(row) if val == x] for x in antennas}
for a in dict_antennas:
    for pair in itertools.combinations(range(len(dict_antennas[a])), 2):
        x0, x1 = dict_antennas[a][pair[0]], dict_antennas[a][pair[1]]
        i01, j01 = x1[0] * 2 - x0[0], x1[1] * 2 - x0[1]
        if 0<=i01<Ni and 0<=j01<Nj:
            antinodes[i01][j01] = '#'
        i10, j10 = x0[0] * 2 - x1[0], x0[1] * 2 - x1[1]
        if 0<=i10<Ni and 0<=j10<Nj:
            antinodes[i10][j10] = '#'

num_antinodes = sum(row.count('#') for row in antinodes)
print(f'{num_antinodes} locations contain an antinodes.')

## New model with resonant hramonics
for a in dict_antennas:
    for pair in itertools.combinations(range(len(dict_antennas[a])), 2):
        x0, x1 = dict_antennas[a][pair[0]], dict_antennas[a][pair[1]]
        bounded = [True, True]
        count = 0
        while any(bounded):
            if bounded[0]:
                i01, j01 = x1[0]*(count+1) - x0[0]*count, x1[1]*(count+1) - x0[1]*count
                if 0<=i01<Ni and 0<=j01<Nj:
                    antinodes[i01][j01] = '#'
                else:
                    bounded[0] = False
            if bounded[1]:
                i10, j10 = x0[0]*(count+1) - x1[0]*count, x0[1]*(count+1) - x1[1]*count
                if 0<=i10<Ni and 0<=j10<Nj:
                    antinodes[i10][j10] = '#'
                else:
                    bounded[1] = False
            count += 1

num_antinodes_with_resonant = sum(row.count('#') for row in antinodes)
print(f'{num_antinodes_with_resonant} locations contain an antinodes.')