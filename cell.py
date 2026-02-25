class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.parent_i = -1
        self.parent_j = -1    
        self.g_cost = float('inf')          
        self.f_cost = float('inf') 
        self.h_cost = 0    

    def cell_details(self):
        return (self.x, self.y, self.parent_i, self.parent_j, self.g_cost, self.f_cost, self.h_cost)
    