#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path
import networkx as nx

## Current file direction
cfd = Path(__file__).parent.absolute()

## Read input
with open(str(cfd) + '/data/D16_input.txt', 'r') as f:
    lines = f.read().splitlines()

dirs = (1, -1, 1j, -1j)

## Dijkstra
G = nx.DiGraph()
for i, row in enumerate(lines):
    for j, x in enumerate(row):
        if x == "#":
            continue
        z = i + 1j * j
        if x=='S':
            start = (z, 1j)
        if x=='E':
            end = z
        for dz in dirs:
            G.add_node((z, dz))

for z, dz in G.nodes:
    if (z+dz, dz) in G.nodes:
        G.add_edge((z, dz), (z+dz, dz), weight=1)
    for rot in (-1j, 1j):
        G.add_edge((z, dz), (z, dz*rot), weight=1000)

for dz in dirs:
    G.add_edge((end, dz), 'end', weight=0)

score = nx.shortest_path_length(G, start, 'end', weight='weight')
print(f'The lowest score is {score}.')

tiles = set()
for path in nx.all_shortest_paths(G, start, 'end', weight='weight'):
    for node in path[:-1]:
        tiles.add(node[0])

print(f'{len(tiles)} are part of at least one of the best paths.')