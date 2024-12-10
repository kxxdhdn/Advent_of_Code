#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path
import re

## Current file direction
cfd = Path(__file__).parent.absolute()

## Read input
f = open(str(cfd)+'/data/D09_input.txt', 'r')

disk_map = f.read().splitlines()[0]
blocks = ''
ifile = 0
for i, num in enumerate(disk_map):
    if i%2==0:
        blocks += str(ifile)[-1] * int(num)
        ifile += 1
    else:
        blocks += '.' * int(num)
print('String length: ', len(blocks))

ind_last_block = list(re.finditer(r'\d', blocks))[-1].start()
ind_first_free = blocks.find('.')
while ind_first_free<ind_last_block:
    blocks = blocks[:ind_first_free] + blocks[ind_last_block] + blocks[ind_first_free+1:]
    blocks = blocks[:ind_last_block] + '.' + blocks[ind_last_block+1:]
    ind_last_block = list(re.finditer(r'\d', blocks))[-1].start()
    ind_first_free = blocks.find('.')
    # print(ind_first_free, ind_last_block)
# print(blocks)

checksum = 0
for i in range(ind_last_block+1):
    checksum += i * int(blocks[i])

print(f'The resulting filesystem checksum is {checksum}.')