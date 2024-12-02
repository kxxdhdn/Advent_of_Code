#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path
import pandas as pd

## Current file direction
cfd = Path(__file__).parent.absolute()

## Read input
num_levels = 8
df = pd.read_csv(str(cfd)+'/data/D02_input.txt',
                 sep='\s+',
                 header=None,
                 names=['Lv'+str(i) for i in range(num_levels)])

def check_report(r):
    r = pd.Series(r).dropna() if not isinstance(r, pd.Series) else r.dropna()
    diff = r.diff().dropna()
    # diff = pd.Series(r.iloc[i+1] - r.iloc[i] for i in range(len(r)-1))
    safe = ((diff > 0).all() or (diff < 0).all()) and 0 < diff.abs().max() < 4
    return safe, diff

num_safe = 0
num_safe_with_dampener = 0
for j, report in df.iterrows():
    ## Without Problem Dampener
    safe, diff = check_report(report)
    num_safe += safe

    ## With Problem Dampener
    num_safe_with_dampener += safe
    if not safe:
        num_pos = (diff > 0).sum()
        num_neg = (diff < 0).sum()
        num_bad = min(num_pos, num_neg)

        ## All increasing or all decreasing
        if num_bad==0:
            unsafe = (diff.abs() < 1) | (diff.abs() > 3)
            ## Count unsafe adjacent level pairs
            num_bad += unsafe.sum()
            ## Localize unsafe adjacent levels (on the right)
            ibad = unsafe[unsafe].index[0]

        if num_bad==1:
            ## Localize unsafe increment level (on the right)
            if num_pos==1:
                ibad = (diff > 0).idxmax()
            if num_neg==1:
                ibad = (diff < 0).idxmax()
            ## Append unsafe levels on the left
            ibad_left = report.index[report.index.get_loc(ibad)-1]
            ## Drop unsafe level on the right or left
            for col_to_drop in [ibad, ibad_left]:
                if check_report(report.drop(col_to_drop))[0]:
                    num_safe_with_dampener += 1
                    break

print(f'Number of safe reports: {num_safe}')
print(f'Number of safe reports with dampener: {num_safe_with_dampener}')