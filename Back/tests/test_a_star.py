import pytest
from ..app.utils.maze import Maze
from ..app.algorithms.a_star import a_star_search

def test_dummy():
    assert True

def test_a_star_finds_path_in_empty_maze():
    maze = Maze(2)  
    for row in maze.grid:
        for cell in row:
            cell.walkable = True 

    path = a_star_search(maze)
    assert path is not None
    assert path[0] == maze.start
    assert path[-1] == maze.end

def test_a_star_no_path_when_blocked():
    maze = Maze(2)
    for row in maze.grid:
        for cell in row:
            cell.walkable = False  # Wszystko zablokowane
    sx, sy = maze.start
    ex, ey = maze.end
    maze.grid[sx][sy].walkable = True
    maze.grid[ex][ey].walkable = True

    path = a_star_search(maze)
    assert path is None

def test_a_star_start_equals_end():
    maze = Maze(2)
    maze.start = (1, 1)
    maze.end = (1, 1)
    maze.grid[1][1].walkable = True

    path = a_star_search(maze)
    assert path == [(1, 1)]