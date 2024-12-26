#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path
import networkx as nx
from itertools import combinations

## Current file direction
cfd = Path(__file__).parent.absolute()

## Read input
with open(str(cfd) + '/data/D20_input.txt', 'r') as f:
    lines = f.read().splitlines()

## Dijkstra
G = nx.grid_2d_graph(len(lines), len(lines[0]))
for i, row in enumerate(lines):
    for j, x in enumerate(row):
        z = (i, j)
        if x=='#':
            G.remove_node(z)
        if x=='S':
            start = z
        # if x=='E':
        #     end = z

distance = nx.single_source_dijkstra_path_length(G, start)

def cheat(dc):
    count = 0
    for ((x1, y1), d1), ((x2, y2), d2) in combinations(distance.items(), 2):
        d = abs(x1 - x2) + abs(y1 - y2)
        dd = d2 - d1 - d
        if d<=dc and dd>=100:
            count += 1
    return count

print(f'{cheat(2)} cheats would save us at least 100 picoseconds.')

print(f'Using the updated cheating rules: {cheat(20)} cheats.')