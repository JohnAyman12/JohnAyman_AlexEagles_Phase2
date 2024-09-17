from flask import Flask, jsonify, request
from flask_cors import CORS
import random
from collections import deque
import networkx as nx

app = Flask(__name__)
CORS(app)


def genaret_random_grid(rows_num: int, cols_num: int, start: tuple, end: tuple, difficulty: str):
    '''
    generating random grid
    O refers to obstcle and . refers to available
    S refers to starting posotopn and E  refers to end position
    '''
    obstacles = 0
    if difficulty == "easy":
        obstacles = 3
    elif difficulty == "medium":
        obstacles = 5
    elif difficulty == "hard":
        obstacles = 7

    generated_obstacles = 0

    arr = []
    cells = ['o', '.']
    for i in range(rows_num):
        col = []
        generated_obstacles = 0
        for j in range(cols_num):
            if generated_obstacles == obstacles:
                while j < 8:
                    if (i, j) == start:
                        col.append('S')
                    elif (i, j) == end:
                        col.append('E')
                    else:
                        col.append('.')
                    j += 1
                break
            elif (i, j) == start:
                col.append('S')
            elif (i, j) == end:
                col.append('E')
            else:
                col.append(random.choice(cells))
            if col[-1] == 'o':
                generated_obstacles += 1
        arr.append(col)
    return arr


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

# Dummy maze generation function (you'll modify this with your existing maze logic)


def generate_maze(difficulty):
    rows = 8
    cols = 8
    start = (5, 4)
    end = (2, 7)
    grid = genaret_random_grid(rows, cols, start, end, difficulty)
    while not grid_is_solvable(grid):
        grid = genaret_random_grid(rows, cols, start, end, difficulty)
    # print("Out")
    global generated_grid
    generated_grid = grid
    # print(difficulty)
    return grid
    # Example: return a simple maze (replace with your own logic)
    # Maze with 0s as open and 1s as wallsgrid = genaret_random_grid(rows, cols, start, end)

# API to generate the maze
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
                global start
                start = (i, j)
            elif grid[i][j] == 'E':
                global end
                end = (i, j)

    # second step: apply A* using networkX to find shortest path
    try:
        path = nx.astar_path(grid_graph, start, end)
        return path
    except nx.NetworkXNoPath:
        return None

@app.route('/generate-maze', methods=['GET'])
def generate_maze_api():
    # Get difficulty from request
    difficulty = request.args.get('difficulty', 'easy')
    print(f"Received difficulty: {difficulty}")
    maze = generate_maze(difficulty)
    return jsonify({'maze': maze})

# API to solve the maze (dummy implementation)


@app.route('/solve-maze', methods=['POST'])
def solve_maze_api():
    maze_solution = find_path(generated_grid)
    maze_solution.pop(0)
    maze_solution.pop()
    return jsonify({'solution': maze_solution})

if __name__ == '__main__':
    app.run(debug=True)
