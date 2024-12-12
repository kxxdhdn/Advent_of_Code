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

def stoneblink(stones):
    MAX_LENGTH = 1000000
    num_extra_stones = 0
    new_stones = []
    for stone in stones:
        try:
            new_stones.extend(list(digitsplit(stone)))
            num_extra_stones += 1
        except ValueError:
            if stone=='0':
                new_stones.append('1')
            else:
                new_stones.append(str(int(stone) * 2024))
    if len(new_stones) > MAX_LENGTH:
        substones = listsplit10(new_stones, MAX_LENGTH)
        return substones, num_extra_stones
    else:
        return [new_stones], num_extra_stones

num_blinks = 25
num_stones = len(lines)
sublines = [lines]
for i in range(num_blinks):
    print(f'Iteration {i}: {num_stones} stones')

    with Pool() as pool:
        results = pool.map(stoneblink, sublines)

    new_sublines = []
    for result in results:
        new_sublines.extend(result[0])
        num_stones += result[1]

    sublines = new_sublines
    # print(sublines)

print(f'There will be {num_stones} stones after blinking {num_blinks} times.')