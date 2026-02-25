from cell import *
from maze import *
import math
import heapq
    
def is_valid(cell, maze):
    return cell.x >= 0 and cell.x < maze.height and cell.y >= 0 and cell.y < maze.width
    
def is_unblocked(cell, maze):

    if not is_valid(cell, maze):
        return False
    return maze.grid[cell.x][cell.y] == 0
    
def is_destination(cell, maze):
    return (cell.x, cell.y) == maze.end
              
def calculate_h_cost(cell, maze):
    cell.h_cost = math.sqrt((cell.x - maze.end[0]) ** 2 + (cell.y - maze.end[1]) ** 2)

def trace_path(cell,cell_details, maze):
    path = []
    while cell is not None:
        path.append((cell.x, cell.y))
        parent_i, parent_j = cell.parent_i, cell.parent_j
        if parent_i == -1 and parent_j == -1:
                break
        cell = cell_details[parent_i][parent_j]
    return path[::-1]
def plt_show_maze(maze, path=None):
    img = np.array(maze.grid)
    
    # jeśli path, oznacz ją jako 0.5
    if path:
        for x, y in path:
            img[x][y] = 0.5

    plt.figure(figsize=(10,10))
    plt.imshow(img, cmap='gray')
    plt.axis('off')
    plt.show()

def print_path(path):
    for x, y in path:
        print(f"({x}, {y})", end=" ")
    print("\nPath length:", len(path))

# A* Search Algorithm
def a_star_search(maze,step_callback=None):
    start_x, start_y = maze.start
    end_x, end_y = maze.end

    closed_list = [[False for _ in range(maze.width)] for _ in range(maze.height)]
    cell_details = [[Cell(i, j) for j in range(maze.width)] for i in range(maze.height)]

    cell_details[start_x][start_y].g_cost = 0
    cell_details[start_x][start_y].f_cost = 0

    open_list = []
    heapq.heappush(open_list, (0, (start_x, start_y)))

    directions = [(0,1),(0,-1),(1,0),(-1,0)]

    while open_list:
        f, (i,j) = heapq.heappop(open_list)
        closed_list[i][j] = True

        if step_callback:
            step_callback((i,j), open_list)

        if (i,j) == maze.end:
            return trace_path(cell_details[i][j], cell_details, maze)

        for dx, dy in directions:
            ni, nj = i + dx, j + dy
            if 0 <= ni < maze.height and 0 <= nj < maze.width and not closed_list[ni][nj]:
                if maze.grid[ni][nj] == 0:  
                    g_new = cell_details[i][j].g_cost + math.sqrt(dx**2 + dy**2)
                    h_new = math.sqrt((ni - end_x)**2 + (nj - end_y)**2)
                    f_new = g_new + h_new

                    if cell_details[ni][nj].f_cost == float('inf') or cell_details[ni][nj].f_cost > f_new:
                        cell_details[ni][nj].g_cost = g_new
                        cell_details[ni][nj].h_cost = h_new
                        cell_details[ni][nj].f_cost = f_new
                        cell_details[ni][nj].parent_i = i
                        cell_details[ni][nj].parent_j = j
                        heapq.heappush(open_list, (f_new, (ni,nj)))

    print("Failed to find destination")
    return None

