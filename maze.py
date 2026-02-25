class Maze:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.maze = self.create_maze()
        self.destination_x = height - 1
        self.destination_y = width - 1

    def create_maze(self):
        grid = [
        [1, 0, 1, 1, 1, 0, 1, 1, 1, 1],
        [1, 0, 1, 0, 1, 0, 1, 0, 1, 1],
        [1, 0, 1, 0, 1, 0, 1, 0, 1, 1],
        [1, 0, 1, 0, 1, 0, 1, 0, 1, 1],
        [1, 0, 1, 0, 1, 0, 1, 0, 1, 1],
        [1, 0, 1, 0, 1, 0, 1, 0, 1, 1],
        [1, 0, 1, 0, 1, 0, 1, 0, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 0, 1, 1],
        [1, 0, 1, 0, 1, 0, 1, 0, 0, 1],
        [1, 1, 1, 0, 1, 1, 1, 0, 1, 1]
        ]
        return grid

    def display_maze(self):
        for row in self.maze:
            print(' '.join(str(cell) for cell in row))
    
    def size(self):
        return self.width, self.height