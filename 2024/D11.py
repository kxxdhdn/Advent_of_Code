#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path

## Current file direction
cfd = Path(__file__).parent.absolute()

## Read input
with open(str(cfd) + '/data/D11_input.txt', 'r') as f:
    lines = f.read().splitlines()[0].split(' ')

def stonecount(stone, stonedict, count=1):
    stonedict[int(stone)] = stonedict.get(int(stone), 0) + count
    return stonedict

def stoneblink(stonedict):
    newdict = {}
    for stone, count in stonedict.items():
        s = str(stone)
        half, mid = divmod(len(s), 2)
        if mid==0:
            newdict = stonecount(s[:half], newdict, count)
            newdict = stonecount(s[half:], newdict, count)
        else:
            newdict = stonecount(1, newdict, count) if stone==0 else stonecount(stone*2024, newdict, count)
    return newdict

stonedict = {}
for stone in lines:
    stonedict = stonecount(stone, stonedict)

# stonedict = {0:1}
num_blinks = 75
num_stones = sum(stonedict.values())
for i in range(num_blinks):
    print(f'Iteration {i}: {num_stones} stones')

    stonedict = stoneblink(stonedict)
    # print(stonedict, '\n')

    num_stones = sum(stonedict.values())

print(f'There will be {num_stones} stones after blinking {num_blinks} times.')