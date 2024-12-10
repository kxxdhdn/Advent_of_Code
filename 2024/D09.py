#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path

## Current file direction
cfd = Path(__file__).parent.absolute()

## Read input
f = open(str(cfd)+'/data/D09_input.txt', 'r')

disk_map = f.read().splitlines()[0]
blocks = []
ifile = 0
for i, num in enumerate(disk_map):
    if i%2==0:
        blocks.extend([ifile] * int(num))
        ifile += 1
    else:
        blocks.extend(['.'] * int(num))
print('String length: ', len(blocks))
blocks_bis = blocks.copy()

ind_last_block = [i for i,val in enumerate(blocks) if isinstance(val, int)][-1]
ind_first_free = blocks.index('.')
while ind_first_free<ind_last_block:
    blocks[ind_first_free] = blocks[ind_last_block]
    blocks[ind_last_block] = '.'
    ind_last_block = [i for i,val in enumerate(blocks) if isinstance(val, int)][-1]
    ind_first_free = blocks.index('.')
    # print(ind_first_free, ind_last_block)
# print(blocks)

checksum = 0
for i in range(ind_last_block+1):
    checksum += i * blocks[i]
print(f'The resulting filesystem checksum is {checksum}.')

def file_free_partition(blocks):
    file_dict, free_dict = {}, {}
    file_size, free_size = 0, 0
    i0 = 0
    for i, val in enumerate(blocks):
        block_start = val!=blocks[i-1]
        if block_start:
            i0 = i
        if i<len(blocks)-1:
            block_end = val!=blocks[i+1]
        if i==len(blocks)-1:
            block_end = True
        if isinstance(val, int):
            file_size += 1
            if block_end:
                file_dict[i0] = file_size
                block_end, file_size = False, 0
        else:
            free_size += 1
            if block_end:
                free_dict[i0] = free_size
                block_end, free_size = False, 0
    return file_dict, free_dict

file_dict, free_dict = file_free_partition(blocks_bis)
for i in range(len(file_dict)):
    ifile = len(file_dict) - i - 1
    file_ind = list(file_dict.keys())[ifile]
    for free_ind, free_size in free_dict.items():
        file_size = file_dict[file_ind]
        if file_size<=free_size and file_ind>free_ind:
            for j in range(file_dict[file_ind]):
                if j<file_size:
                    blocks_bis[free_ind+j] = ifile
                    blocks_bis[file_ind+j] = '.'
            break
    _, free_dict = file_free_partition(blocks_bis) # only update free_dict
# print(blocks_bis)

checksum_bis = 0
for i in range(len(blocks_bis)):
    if isinstance(blocks_bis[i], int):
        checksum_bis += i * blocks_bis[i]
print(f'The resulting filesystem checksum is {checksum_bis}.')