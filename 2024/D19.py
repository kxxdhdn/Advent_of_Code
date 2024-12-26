#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path
from functools import cache

## Current file direction
cfd = Path(__file__).parent.absolute()

## Read input
with open(str(cfd) + '/data/D19_input.txt', 'r') as f:
    lines = f.read().splitlines()

stripes, _, *patterns = lines
stripes = stripes.split(", ")

@cache
def is_possible(pattern, op):
    return not pattern or op(
        is_possible(pattern[len(stripe) :], op)
        for stripe in stripes
        if pattern.startswith(stripe)
    )

for op in any, sum:
    count = sum(is_possible(pattern, op) for pattern in patterns)
    print(f'There are {count} possible designs (single/multiple ways).')