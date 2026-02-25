from collections import deque
import random
import matplotlib.pyplot as plt
import numpy as np
class Maze:
    def __init__(self, width, height):
        self.width = 2*width + 1
        self.height = 2*height + 1
        self.grid = [[1 for _ in range(self.width)] for _ in range(self.height)]
        self.start = (0, 1)
        self.end = (self.height - 1, self.width - 2)

    
    def create_maze(self):
        stack = [(1, 1)]
        visited = set()
        visited.add((1, 1))

        while stack:
            x, y = stack[-1]
            self.grid[x][y] = 0  

            
            neighbors = []
            for dx, dy in [(0,2),(0,-2),(2,0),(-2,0)]:
                nx, ny = x + dx, y + dy
                if 1 <= nx < self.height-1 and 1 <= ny < self.width-1 and (nx, ny) not in visited:
                    neighbors.append((nx, ny))

            if neighbors:
                nx, ny = random.choice(neighbors)
                
                self.grid[x + (nx-x)//2][y + (ny-y)//2] = 0
                visited.add((nx, ny))
                stack.append((nx, ny))
            else:
                
                stack.pop()

        self.grid[0][1] = 0
        self.grid[self.height-1][self.width-2] = 0

        return self.grid


    def display_maze(self):
        for row in self.grid:
            print("".join("#" if cell == 1 else "." for cell in row))
    
    def size(self):
        return self.width, self.height