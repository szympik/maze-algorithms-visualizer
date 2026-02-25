from importlib.resources import path
from cell import *
from maze import *
from a_star import *
import time
from visualize import visualize_solver

def main():
    maze = Maze(100,100)
    maze.create_maze()
    visualize_solver(maze, a_star_search,5,0.1)
if __name__ == "__main__":
    main()
    