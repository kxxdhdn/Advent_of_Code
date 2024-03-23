#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path
import re

## Current file direction
cfd = Path(__file__).parent.absolute()

## Read input
f = open(str(cfd)+'/data/D02_input.txt', 'r')
lines = f.readlines()

sum_iG = 0
sum_power = 0
for l in lines:
    iG = int(re.findall('Game (\d+)', l)[0])
    lr = [int(x) for x in re.findall('(\d+) red', l)]
    lg = [int(x) for x in re.findall('(\d+) green', l)]
    lb = [int(x) for x in re.findall('(\d+) blue', l)]
    # print('\n', l)
    # print(iG, '\nr', ir, '\ng', ig, '\nb', ib)
    
    ## Check each game
    flag = 0
    flag += next((ir for ir in lr if ir>12), 0)
    flag += next((ig for ig in lg if ig>13), 0)
    flag += next((ib for ib in lb if ib>14), 0)
    # print(flag)

    ## Part one counts
    if flag==0:
        sum_iG += iG

    ## Part two counts
    sum_power += max(lr) * max(lg) * max(lb)

## Part one answer
print("The sum of the IDs of the possible games is {}.\n".format(sum_iG))

## Part two answer
print("The sum of the power of all sets is {}.\n".format(sum_power))
