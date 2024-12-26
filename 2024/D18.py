#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path
import networkx as nx

## Current file direction
cfd = Path(__file__).parent.absolute()

## Read input
with open(str(cfd) + '/data/D18_input.txt', 'r') as f:
    lines = f.read().splitlines()

## Dijkstra
Nx = Ny = 70
G = nx.grid_2d_graph(Nx+1, Ny+1)
corrupted = [tuple(map(int, line.split(","))) for line in lines]
for i, pos in enumerate(corrupted):
    G.remove_node(pos)
    ## The first kilobyte 
    if i == 1023:
        min_steps = nx.shortest_path_length(G, (0, 0), (Nx, Ny))
        print(f'The minimum number of steps needed to reach the exit is {min_steps}.')
    elif not nx.has_path(G, (0, 0), (Nx, Ny)):
        print(f'The first byte to prevent the exit from being reachable is {pos}.')
        break