import random
from collections import deque
import networkx as nx
from colorama import Fore


def genaret_random_grid(rows_num: int, cols_num: int, start: tuple, end: tuple):
    '''
    generating random grid
    O refers to obstcle and . refers to available
    S refers to starting posotopn and E  refers to end position
    '''
    arr = []
    cells = ['o', '.']
    for i in range(rows_num):
        col = []
        for j in range(cols_num):
            if (i, j) == start:
                col.append('S')
            elif (i, j) == end:
                col.append('E')
            else:
                col.append(random.choice(cells))
        arr.append(col)
    return arr


def print_grid(grid: list):
    '''print the grid'''
    rows, cols = len(grid), len(grid[0])
    for i in range(rows):
        for j in range(cols):
            if (grid[i][j] == 'o'):
                print(Fore.RED + grid[i][j], end=' ')
            elif (grid[i][j] == '*'):
                print(Fore.GREEN + grid[i][j], end=' ')
            elif (grid[i][j] == '.'):
                print(Fore.WHITE + grid[i][j], end=' ')
            else:
                print(Fore.MAGENTA + grid[i][j], end=' ')
        print()


def grid_is_solvable(grid: list):
    '''use BFS to check if the given grid is solvable'''
    rows, cols = len(grid), len(grid[0])
    start = end = None
    # Getting the positions of starting point and ending point
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == 'S':
                start = (i, j)
            elif grid[i][j] == 'E':
                end = (i, j)
            if (start is not None) and (end is not None):
                break
        if (start is not None) and (end is not None):
            break
    # apply BFS to ensure the grid is solvable
    deq = deque([start])
    visited = set()
    visited.add(start)
    while deq:
        current = deq.popleft()
        if current == end:
            return True  # path found

        # array to check the neighbour cells to right, left, bottom, top
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        for direction in directions:
            new_row, new_col = current[0] + \
                direction[0], current[1] + direction[1]
            if 0 <= new_row < rows and 0 <= new_col < cols and grid[new_row][new_col] != 'o' and (new_row, new_col) not in visited:
                deq.append((new_row, new_col))
                visited.add((new_row, new_col))
    return False  # no path found


def find_path(grid: list):
    '''
    finding the path to E with A* algorithm using networkX to apply it
    '''
    # first step: generating graph from the list to apply A* on
    grid_graph = nx.Graph()
    rows, cols = len(grid), len(grid[0])
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] != 'o':
                grid_graph.add_node((i, j))
                if i > 0 and grid[i-1][j] != 'o':
                    grid_graph.add_edge((i, j), (i-1, j))
                if i < rows-1 and grid[i+1][j] != 'o':
                    grid_graph.add_edge((i, j), (i+1, j))
                if j > 0 and grid[i][j-1] != 'o':
                    grid_graph.add_edge((i, j), (i, j-1))
                if j < cols-1 and grid[i][j+1] != 'o':
                    grid_graph.add_edge((i, j), (i, j+1))

            if grid[i][j] == 'S':
                start = (i, j)
            elif grid[i][j] == 'E':
                end = (i, j)

    # second step: apply A* using networkX to find shortest path
    try:
        path = nx.astar_path(grid_graph, start, end)
        return path
    except nx.NetworkXNoPath:
        return None


def draw_path(grid: list, path: list):
    rows, cols = len(grid), len(grid[0])
    for i in range(rows):
        for j in range(cols):
            if ((i, j) in path) and grid[i][j] != 'S' and grid[i][j] != 'E':
                grid[i][j] = '*'
    print_grid(grid)


rows = 8
cols = 8
start = (5, 4)
end = (2, 7)

grid = genaret_random_grid(rows, cols, start, end)
while not grid_is_solvable(grid):
    grid = genaret_random_grid(rows, cols, start, end)

draw_path(grid, find_path(grid))
