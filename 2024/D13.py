#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path
import re

## Current file direction
cfd = Path(__file__).parent.absolute()

## Read input
with open(str(cfd) + '/data/D13_input.txt', 'r') as f:
    lines = f.read().split('\n\n')

def analyse_craw_machine(cm):
    dxa, dya, dxb, dyb, x, y = cm
    na, ea = divmod(x*dyb - y*dxb, dxa*dyb - dya*dxb)
    nb, eb = divmod(x*dya - y*dxa, dxb*dya - dyb*dxa)
    return 3 * na + nb if ea==0 and eb==0 else 0

craw_machines = [list(map(int, re.findall(r'\d+', line))) for line in lines]
total_tokens = 0
for cm in craw_machines:
    total_tokens += analyse_craw_machine(cm)

print(f'The fewest tokens one would have to spend to win all possible prizes are {total_tokens}.')

shift = 10000000000000
crazy_craw_machines = [[d if i<4 else d+shift for i,d in enumerate(cm)] for cm in craw_machines]
total_tokens = 0
for cm in crazy_craw_machines:
    total_tokens += analyse_craw_machine(cm)

print(f'To win all possible prizes of crazy craw machines, you will need at least {total_tokens} tokens.')