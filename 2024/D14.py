#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path
import re

## Current file direction
cfd = Path(__file__).parent.absolute()

## Read input
with open(str(cfd) + '/data/D14_input.txt', 'r') as f:
    lines = f.readlines()
# pattern = r'p=(\d+),(\d+) v=(-?\d+),(-?\d+)'

robots = [[*map(int, re.findall(r'-?\d+',line))] for line in lines]

def safety_factor(t):
    # Nx, Ny = 11, 7
    Nx, Ny = 101, 103
    c1 = c2 = c3 = c4 = 0
    for x, y, dx, dy in robots:
        x = (x + t*dx) % Nx
        y = (y + t*dy) % Ny
        c1 += x<Nx//2 and y<Ny//2
        c2 += x>Nx//2 and y<Ny//2
        c3 += x<Nx//2 and y>Ny//2
        c4 += x>Nx//2 and y>Ny//2
    return c1*c2*c3*c4

sf = safety_factor(100)

print(f'The safety factor will be {sf} after 100 seconds.')

t0 = min(range(10_000), key=safety_factor)

print(f'The robots will display the Easter egg after {t0} seconds.')