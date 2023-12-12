#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path

## Current file direction
cfd = Path(__file__).parent.absolute()

f = open(str(cfd)+'/data/d10_input.txt', 'r')
lines = f.readlines()
