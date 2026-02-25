from cell import *
from maze import *
import math
import heapq
    
def is_valid(cell, maze):
    return cell.x >= 0 and cell.x < maze.height and cell.y >= 0 and cell.y < maze.width
    
def is_unblocked(cell, maze):

    if not is_valid(cell, maze):
        return False
    return maze.maze[cell.x][cell.y] == 1
    
def is_destination(cell, maze):
    return cell.x == maze.destination_x and cell.y == maze.destination_y
              
def calculate_h_cost(cell, maze):
    cell.h_cost = math.sqrt((cell.x - maze.destination_x) ** 2 + (cell.y - maze.destination_y) ** 2)

def trace_path(cell,cell_details, maze):
    path = []
    while cell is not None:
        path.append((cell.x, cell.y))
        parent_i, parent_j = cell.parent_i, cell.parent_j
        if parent_i == -1 and parent_j == -1:
                break
        cell = cell_details[parent_i][parent_j]
    return path[::-1]
    
def print_path(path):
    for x, y in path:
        print(f"({x}, {y})", end=" ")
    print("\nPath length:", len(path))

# A* Search Algorithm
def a_star_search(maze):
    closed_list = [[False for _ in range(maze.width)] for _ in range(maze.height)]
    cell_details = [[Cell(i, j) for j in range(maze.width)] for i in range(maze.height)]
    cell_details[0][0].g_cost = 0
    cell_details[0][0].f_cost = 0
    star_cell = Cell(0, 0).cell_details()
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0),
                  (1, 1), (1, -1), (-1, 1), (-1, -1)]

    open_list = []
    heapq.heappush(open_list, (0, star_cell))

    found_dest = False

    while open_list:
        p = heapq.heappop(open_list)
        i, j = p[1][0], p[1][1]
        closed_list[i][j] = True
        
        print(f"Processing cell: ({i}, {j}) with f_cost: {cell_details[i][j].f_cost:.2f}") # Debug print
        
        for direction in directions:
            new_i, new_j = i + direction[0], j + direction[1]
            if is_unblocked(Cell(new_i, new_j), maze):
                
                
                if not closed_list[new_i][new_j]:
                
                
                    print(f"  Checking neighbor: ({new_i}, {new_j})") # Debug print
                    
                    if is_destination(cell_details[new_i][new_j], maze):
                        
                        print(f"Destination found at: ({new_i}, {new_j})") # Debug print
                        cell_details[new_i][new_j].parent_i = i  
                        cell_details[new_i][new_j].parent_j = j  
                        found_dest = True
                        return trace_path(cell_details[new_i][new_j],cell_details, maze)
                    else:
                        g_cost = cell_details[i][j].g_cost + math.sqrt(direction[0] ** 2 + direction[1] ** 2)
                        h_cost = math.sqrt((new_i - maze.destination_x) ** 2 + (new_j - maze.destination_y) ** 2)
                        f_cost = g_cost + h_cost

                        if cell_details[new_i][new_j].f_cost == float('inf') or cell_details[new_i][new_j].f_cost > f_cost:
                            
                            print(f"  Updating neighbor: ({new_i}, {new_j}) with new f_cost: {f_cost:.2f}") # Debug print
                            
                            cell_details[new_i][new_j].g_cost = g_cost
                            cell_details[new_i][new_j].h_cost = h_cost
                            cell_details[new_i][new_j].f_cost = f_cost
                            cell_details[new_i][new_j].parent_i = i
                            cell_details[new_i][new_j].parent_j = j
                            heapq.heappush(open_list, (f_cost, (new_i, new_j)))
    if not found_dest:
        print("Failed to find the Destination Cell")
        return None

