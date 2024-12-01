#!/usr/bin/env python
# -*- coding: utf-8 -*-


from pathlib import Path
import pandas as pd

## Current file direction
cfd = Path(__file__).parent.absolute()

## Read input
df = pd.read_csv(str(cfd)+'/data/D01_input.txt',
                 sep='\s+',
                 header=None,
                 names=['L1','L2'])

l1_sorted = df['L1'].sort_values().reset_index(drop=True)
l2_sorted = df['L2'].sort_values().reset_index(drop=True)

total_distance = 0
for i in range(len(l1_sorted)):
	total_distance += abs(l1_sorted[i] - l2_sorted[i])
print(f'Total diatance: {total_distance}')

similarity = 0
for i, val in enumerate(df['L1']):
	similarity += val * (df['L2']==val).sum()
print(f'Similarity score: {similarity}')