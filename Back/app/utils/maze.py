import random
from .cell import Cell

class Maze:
    def __init__(self, size):
        self.width = 2 * size + 1
        self.height = 2 * size + 1
        self.grid = [
            [Cell(x, y, walkable=False) for y in range(self.width)]
            for x in range(self.height)
        ]
        self.start = (0, 1)
        self.end = (self.height - 1, self.width - 2)

    def create_maze(self):
        stack = [(1, 1)]
        visited = set()
        visited.add((1, 1))

        while stack:
            x, y = stack[-1]
            self.grid[x][y].walkable = True

            neighbors = []
            for dx, dy in [(0, 2), (0, -2), (2, 0), (-2, 0)]:
                nx, ny = x + dx, y + dy
                if (
                    1 <= nx < self.height - 1
                    and 1 <= ny < self.width - 1
                    and (nx, ny) not in visited
                ):
                    neighbors.append((nx, ny))

            if neighbors:
                nx, ny = random.choice(neighbors)
                mx, my = x + (nx - x) // 2, y + (ny - y) // 2
                self.grid[mx][my].walkable = True
                visited.add((nx, ny))
                stack.append((nx, ny))
            else:
                stack.pop()

        self.grid[self.start[0]][self.start[1]].walkable = True
        self.grid[self.end[0]][self.end[1]].walkable = True

        return self.grid

    def maze_to_json(self):
        return [
            [0 if not cell.walkable else 1 for cell in row]
            for row in self.grid
        ]
    
    def json_to_maze(self, json_maze):
        self.grid = [
            [Cell(x, y, walkable=bool(value)) for y, value in enumerate(row)]
            for x, row in enumerate(json_maze)
        ]
        self.height = len(self.grid)
        self.width = len(self.grid[0]) if self.grid else 0
        self.start = (0, 1) if self.width > 1 else (0, 0)
        self.end = (self.height - 1, self.width - 2) if self.width > 1 else (self.height - 1, self.width - 1)
        return self.grid
    
    def size(self):
        return self.width, self.height

    def white_cells(self):
        return sum(cell.walkable for row in self.grid for cell in row)