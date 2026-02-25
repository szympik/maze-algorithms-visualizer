from cell import *
from maze import *
from a_star import *
import time

def main():
    maze = Maze(10,10)
    maze.display_maze()
    path = a_star_search(maze)
    if path:
        print("Path found:")
        print_path(path)
    else:
        print("No path found.")


if __name__ == "__main__":
    start_time = time.time()
    main()
    end_time = time.time()
    print(f"Execution time: {end_time - start_time:.4f} seconds")