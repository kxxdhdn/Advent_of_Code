#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path
import re

## Current file direction
cfd = Path(__file__).parent.absolute()

## Read input
f = open(str(cfd)+'/data/D03_input.txt', 'r')
lines = f.readlines()

# Define the regular expression pattern
pattern_mul = r"\bmul\((\d+),(\d+)\)"
pattern_do = r"do\(\)"
pattern_dont = r"don't\(\)"

results = 0
results_enabled = 0
enabled = True
for line in lines:
    ## Find all matches in the text
    matches_mul = re.finditer(pattern_mul, line)
    matches_mul = list(matches_mul)

    ## Compute multiplications
    for mul in matches_mul:
        results += int(mul.group(1)) * int(mul.group(2))

    ## Compute enabled multiplications
    matches_do = re.finditer(pattern_do, line)
    matches_dont = re.finditer(pattern_dont, line)
    list_mul = [x.start() for x in matches_mul]
    list_do = [x.start() for x in matches_do]
    list_dont = [x.start() for x in matches_dont]
    list_all = sorted(list_mul + list_do + list_dont)

    for i in list_all:
        if i in list_dont:
            enabled = False
        if i in list_do:
            enabled = True
        if i in list_mul:
            mul = list(matches_mul)[list_mul.index(i)]
            if enabled:
                results_enabled += int(mul.group(1)) * int(mul.group(2))

print(f'The sum of all multiplications is {results}')
print(f'The sum of all enabled multiplications is {results_enabled}')