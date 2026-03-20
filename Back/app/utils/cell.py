class Cell:
    def __init__(self, x: int, y: int, walkable: bool = True):
        self.x = x
        self.y = y
        self.parent = None  
        self.walkable = walkable
        self.visited = False

    def __eq__(self, other):
        return isinstance(other, Cell) and self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

    def __repr__(self):
        return f"Cell({self.x}, {self.y})"

    
    