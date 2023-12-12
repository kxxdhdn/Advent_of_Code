#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path
from copy import deepcopy
import numpy as np

## Current file direction
cfd = Path(__file__).parent.absolute()

## Read input
f = open(str(cfd)+'/data/d8_input.txt', 'r')
lines = f.readlines()

nav = lines[0][:-1] # navigation
net = [] # network
for l in lines[2:]:
    net.append(l[:-1])

## Part one counts
pos = 'AAA' # starting position
for row in net:
    if row[:3]==pos:
        s = net.index(row) # starting position index
steps = 0 # current steps
while pos!='ZZZ':
    for x in nav:
        ## Let's go!
        steps += 1
        ## Next position
        if x=='L':
            pos = net[s][7:10]
        elif x=='R':
            pos = net[s][12:15]
        else:
            print("Error: Wrong instruction!\n")
            exit()
        for row in net:
            if row[:3]==pos:
                s = net.index(row) # update position index
        ## Destination check
        if pos=='ZZZ':
            break

## Part one answer
print("{} steps are required to reach ZZZ.\n".format(steps))

## Part two counts
grpZ = dict() # steps of end-of-Z first appearances
grpA = dict() # starting positions
for row in net:
    if row[2]=='A':
        grpA.update({row[:3]: net.index(row)})
ss = 0 # current mutual steps
flag = True
while flag:
    for x in nav:
        # print(x, ss, grpA)
        lstZ = list(grpZ.keys())
        lstA = list(grpA.keys())
        ## Let's go together!
        ss += 1
        ## Next positions
        grpA0 = deepcopy(grpA)
        for p in grpA0.keys():
            if x =='L':
                pn = net[grpA0[p]][7:10]
            elif x=='R':
                pn = net[grpA0[p]][12:15]
            else:
                print("Error: Wrong instruction!\n")
                exit()
            grpA[pn] = grpA.pop(p) # update position
            for row in net:
                if row[:3]==pn:
                    grpA[pn] = net.index(row) # update position indices
            ## Detect end-of-Z appearance
            if pn[-1]=='Z' and (pn not in lstZ):
                print(ss, pn)
                grpZ.update({pn: ss})
        ## Destination check
        if all([p[-1]=='Z' for p in lstA]):
            flag = False
            break
        ## Alternative method: least common multiple
        if len(lstZ)==len(lstA):
            ss = np.lcm.reduce(np.array(list(grpZ.values())))
            flag = False
            break

## Part two answer
print("It takes {} steps before I am only on nodes that end with Z.\n".format(ss))
