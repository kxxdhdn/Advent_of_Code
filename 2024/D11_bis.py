#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path
from multiprocessing import Pool

## Current file direction
cfd = Path(__file__).parent.absolute()

## Read input
with open(str(cfd) + '/data/D11_input.txt', 'r') as f:
    lines = f.read().splitlines()[0].split(' ')

def digitsplit(digit):
    sd = str(digit)
    if len(sd)%2==0:
        len2 = len(sd)//2
        return sd[:len2], str(int(sd[len2:]))
    else:
        raise ValueError('Number of digits is not even!')

def listsplit10(lst, max_len):
    num_sub = 10
    sub_len = max(1, max_len//num_sub)
    return [lst[i:i+sub_len] for i in range(0, len(lst), sub_len)]

def stonecount(stones):
    iex = 0
    for i, stone in enumerate(stones):
        i += iex
        if i>0:
            new_stones = stones[:i]
        else:
            new_stones = []
        try:
            new_stones.extend(list(digitsplit(stone)))
            iex += 1
        except ValueError:
            if stone=='0':
                new_stones.append('1')
            else:
                new_stones.append(str(int(stone) * 2024))
        if i<len(stones):
            new_stones.extend(stones[i+1:])
        stones = new_stones
    return stones, iex

num_blinks = 25
num_stones = len(lines)
sublines = [lines]
MAX_LENGTH = 10000
for i in range(num_blinks):
    print(f'Iteration {i}: {num_stones} stones')

    jex = 0
    for j, subline in enumerate(sublines):
        j += jex
        if j>0:
            new_sublines = sublines[:j]
        else:
            new_sublines = []

        subline, num_ex = stonecount(subline) # blink
        num_stones += num_ex # count
        if len(subline)>MAX_LENGTH:
            subsublines = listsplit10(subline, MAX_LENGTH)
            new_sublines.extend(subsublines)
            jex += len(subsublines) - 1
        else:
            new_sublines.append(subline)

        if j<len(sublines):
            new_sublines.extend(sublines[j+1:])
        sublines = new_sublines
    # print(sublines)

print(f'There will be {num_stones} stones after blinking {num_blinks} times.')