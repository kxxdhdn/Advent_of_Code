#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path
import re

## Current file direction
cfd = Path(__file__).parent.absolute()

## Read input
f = open(str(cfd)+'/data/D09_input.txt', 'r')
lines = f.readlines()

xp_right = 0 # sum of right-extrapolated values
xp_left = 0 # sum of left-extrapolated values
for l in lines:
    seq0 = [int(x) for x in l.split()] # first/original sequence
    # print(seq0)
    seq_end = [] # last values of all sequence (upper -> lower)
    seq_start = [] # first values of all sequence
    seq = seq0
    while not all(v==0 for v in seq):
        seq_end.append(seq[-1])
        seq_start.append(seq[0])
        Nv = len(seq) # number of values in the sequence
        if (Nv==1 and seq[0]!=0):
            raise Error('Not a convergent sequence. ')
        else:
            delta = []
            for i in range(Nv-1):
                delta.append(seq[i+1] - seq[i])
            seq = delta # new sequence
    
    ## Part one counts
    xp_right += sum(seq_end)

    ## Part two counts
    # print(seq_start)
    d0 = 0 # left-extrapolated difference
    for i in range(len(seq_start)):
        v0 = seq_start[-1-i] - d0 # left-extrapolated value
        # print(d0, v0)
        d0 = v0 # upper sequence left-most difference
    xp_left += v0
    # exit()

## Part one answer
print("The sum of right-extrapolated values is {}.\n".format(xp_right))

## Part two answer
print("The sum of left-extrapolated values is {}.\n".format(xp_left))
