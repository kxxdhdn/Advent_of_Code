#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path
from copy import deepcopy
import numpy as np

## Current file direction
cfd = Path(__file__).parent.absolute()

## Read input
# with open(str(cfd)+'/data/test.txt', 'r') as f:
with open(str(cfd)+'/data/D12_input.txt', 'r') as f:
    universe = f.read().split('\n')[:-1] # empty line in the end
    # universe = [[v for v in l] for l in universe]
    universe = np.array([np.array([v for v in l]) for l in universe])
# print(universe)
