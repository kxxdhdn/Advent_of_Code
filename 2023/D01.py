#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path
import re

## Current file direction
cfd = Path(__file__).parent.absolute()

## Read input
f = open(str(cfd)+'/data/D01_input.txt', 'r')
lines = f.readlines()

## Part one counts
cval = 0 # sum of calibration values
for l in lines:
    # print(l.split()[0])
    digits = [x for x in l.split()[0] if x.isdigit()]
    ## Sum up
    cval += int(digits[0] + digits[-1])

## Part one answer
print("The sum of all of the calibration values is {}.\n".format(cval))

## Part two preparation
num = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
dict_num = {n: i+1 for i, n in enumerate(num)}
for i in range(9):
    dict_num[str(i+1)] = i+1
# print(dict_num)
num_all = list(dict_num.keys())
pattern = num_all[0]
for n in num_all:
    pattern += "|"+n
# print(pattern)

## Part two pre-test
example = "7twoneight8nnine" # expected: 721889
print("Example: ", example)
print("Expected output: 721889\nActual output: ", 
      "".join([re.sub(x, str(dict_num[x]), x) for x in re.findall(rf'(?=({pattern}))', example)]), 
      "\n")

## Part two counts
cval2 = 0 # corrected sum of calibration values
for l in lines:
    ## Digitize each line
    digits = [re.sub(x, str(dict_num[x]), x) for x in re.findall(rf'(?=({pattern}))', l)]
    # print(l, digits, '\n')
    ## Sum up
    cval2 += int(digits[0] + digits[-1])

## Part two answer
print("The corrected sum of all of the calibration values is {}.\n".format(cval2))
