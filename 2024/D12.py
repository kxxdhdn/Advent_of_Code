#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path

## Current file direction
cfd = Path(__file__).parent.absolute()

## Read input
with open(str(cfd) + '/data/D12_input.txt', 'r') as f:
    lines = [[x for x in row] for row in f.read().splitlines()]

def find_regions(grid):
    def dfs(x, y, label):
        # If out of bounds or not the target character, return
        if x < 0 or x >= len(grid) or y < 0 or y >= len(grid[0]) or visited[x][y] or grid[x][y] != target:
            return
        # Mark the cell as visited
        visited[x][y] = True
        # Label the current cell
        regions[label].append((x, y))
        # Explore neighbors
        dfs(x + 1, y, label)
        dfs(x - 1, y, label)
        dfs(x, y + 1, label)
        dfs(x, y - 1, label)
    visited = [[False] * len(grid[0]) for _ in range(len(grid))]
    regions = {}
    label_counter = 0

    for i,row in enumerate(grid):
        for j,x in enumerate(row):
            if not visited[i][j]:  # If the cell is not visited
                target = x
                label_counter += 1
                regions[label_counter] = []
                dfs(i, j, label_counter)
    return regions

def perimeter_increment(iloc, grid):
    pi = 0
    x, y = iloc
    current_value = grid[x][y]
    
    # Define the directions for neighbors: up, down, left, right
    d = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    for dx, dy in d:
        nx, ny = x + dx, y + dy
        # Check if neighbor is within bounds and different from current cell
        if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]):
            if grid[nx][ny] != current_value:
                pi += 1
        else:
            # Out of bounds implies a boundary increment
            pi += 1
    
    return pi

def side_increment(iloc, grid):
    si = 0
    x, y = iloc
    current_value = grid[x][y]
    
    # Define the directions for neighbors: up, down, left, right
    d = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    d1 = [(0, -1), (0, -1), (-1, 0), (-1, 0)]
    d2 = [(-1, -1), (1, -1), (-1, -1), (-1, 1)]

    for j, (dx, dy) in enumerate(d):
        nx, ny = x + dx, y + dy
        neighbor_in_grid = 0<=nx<len(grid) and 0<=ny<len(grid[0])
        if neighbor_in_grid:
            neighbor_value = grid[nx][ny]
        nx1, ny1 = x + d1[j][0], y + d1[j][1]
        test_in_grid = 0<=nx1<len(grid) and 0<=ny1<len(grid[0])
        if test_in_grid:
            test_value = grid[nx1][ny1]
        nx2, ny2 = x + d2[j][0], y + d2[j][1]
        test_ne_in_grid = 0<=nx2<len(grid) and 0<=ny2<len(grid[0])
        if test_ne_in_grid:
            test_ne_value = grid[nx2][ny2]

        if not neighbor_in_grid:
            if (not test_in_grid) or (test_in_grid and test_value!=current_value):
                si += 1
        elif neighbor_in_grid and neighbor_value!=current_value:
            if not test_in_grid:
                si += 1
            elif test_in_grid:
                if test_value!=current_value or test_ne_value==test_value:
                    si += 1

    return si

area = {}
perimeter = {}
side = {}
regions = find_regions(lines)
for i,x in regions.items():
    area[i] = len(x)
    for iloc in x:
        perimeter[i] = perimeter.get(i, 0) + perimeter_increment(iloc, lines)
        side[i] = side.get(i, 0) + side_increment(iloc, lines)
# print(area)
# print(perimeter)
# print(side)
price = {a:area[a]*perimeter[a] for a in area}
price_discount = {a:area[a]*side[a] for a in area}

print(f'The total price of fencing all regions on the map is {sum(price.values())}.')
print(f'The total price with bulk discount is {sum(price_discount.values())}.')
