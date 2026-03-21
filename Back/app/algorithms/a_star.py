# Use relative imports so pytest works when run from Back/ or project root
from ..utils.cell import Cell
from ..utils.maze import Maze
import math
import heapq

def is_valid(x, y, maze):
    return 0 <= x < maze.height and 0 <= y < maze.width

def is_unblocked(cell):
    return cell.walkable

def is_destination(cell, maze):
    return (cell.x, cell.y) == maze.end

def calculate_h_cost(cell, maze):
    end_x, end_y = maze.end
    return abs(cell.x - end_x) + abs(cell.y - end_y)  # Manhattan distance

def trace_path(cell):
    path = []
    while cell is not None:
        path.append((cell.x, cell.y))
        cell = cell.parent
    return path[::-1]

def print_path(path):
    for x, y in path:
        print(f"({x}, {y})", end=" ")
    print("\nPath length:", len(path))

def a_star_search(maze, step_callback=None):
    start_x, start_y = maze.start
    end_x, end_y = maze.end

    start_cell = maze.grid[start_x][start_y]
    end_cell = maze.grid[end_x][end_y]

 
    for row in maze.grid:
        for cell in row:
            cell.g = float('inf')
            cell.h = 0
            cell.f = float('inf')
            cell.parent = None
            cell.visited = False

    start_cell.g = 0
    start_cell.h = calculate_h_cost(start_cell, maze)
    start_cell.f = start_cell.h

    open_list = []
   
    heapq.heappush(open_list, (start_cell.f, start_cell.h, id(start_cell), start_cell))

    directions = [(0,1),(0,-1),(1,0),(-1,0)]

    while open_list:
        _, _, _, current = heapq.heappop(open_list)
        current.visited = True

        if step_callback:
            step_callback((current.x, current.y), open_list)

        if is_destination(current, maze):
            return trace_path(current)

        for dx, dy in directions:
            nx, ny = current.x + dx, current.y + dy
            if is_valid(nx, ny, maze):
                neighbor = maze.grid[nx][ny]
                if not neighbor.visited and is_unblocked(neighbor):
                    g_new = current.g + 1
                    h_new = calculate_h_cost(neighbor, maze)
                    f_new = g_new + h_new

                    if f_new < neighbor.f:
                        neighbor.g = g_new
                        neighbor.h = h_new
                        neighbor.f = f_new
                        neighbor.parent = current
                        heapq.heappush(open_list, (neighbor.f, neighbor.h, id(neighbor), neighbor))

    print("Failed to find destination")
    return None