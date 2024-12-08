#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path
import itertools

## Current file direction
cfd = Path(__file__).parent.absolute()

## Read input
f = open(str(cfd)+'/data/D07_input.txt', 'r')
lines = f.read().splitlines()

def total_calib(calib, ops):
    result = 0
    for key in calib:
        val = calib[key]
        num_op = len(val) - 1
        all_cases = []
        for op in itertools.product(ops, repeat=num_op):
            ## Standard evaluation
            # equation = ''.join(str(val[i]) + op[i] for i in range(num_op)) + str(val[-1])
            # all_cases.append(eval(equation))

            ## Left-to-right evalution
            res = val[0]
            for i in range(num_op):
                if op[i]=='+':
                    res += val[i+1]
                elif op[i]=='*':
                    res *= val[i+1]
                elif op[i]=='||':
                    res = int(f'{res}{val[i+1]}')
            all_cases.append(res)
        if key in all_cases:
            result += key
    return result

calibration = {int(calib[0]): [int(v) for v in calib[1].split(' ')] for calib in [line.split(': ') for line in lines]}
ops = ['+', '*']
result = total_calib(calibration, ops)

print(f'Total calibration result with + and *: {result}.')

ops = ['+', '*', '||']
result = total_calib(calibration, ops)

print(f'Total calibration result with +, *, and ||: {result}.')