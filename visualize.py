def visualize_solver(maze, solver, cell_size=10, delay=0.05):
    import pygame, time
    pygame.init()
    screen = pygame.display.set_mode((maze.width*cell_size, maze.height*cell_size))
    pygame.display.set_caption("Maze Solver Visualization")
    clock = pygame.time.Clock()

    # Kolory
    COLOR_WALL = (0,0,0)
    COLOR_PATH = (255,255,255)
    COLOR_VISITED = (255,0,0)
    COLOR_CURRENT = (65,105,225)
    COLOR_FINAL_PATH = (0,255,0)

  
    for i in range(maze.height):
        for j in range(maze.width):
            color = COLOR_PATH if maze.grid[i][j] == 0 else COLOR_WALL
            pygame.draw.rect(screen, color, (j*cell_size, i*cell_size, cell_size, cell_size))
    pygame.display.flip()

    visited_cells = set()
    frame_counter = 0

    def step_callback(current_cell_solver, open_list):
        nonlocal visited_cells, frame_counter
        
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        
        
        if current_cell_solver not in visited_cells:
            visited_cells.add(current_cell_solver)
            i, j = current_cell_solver
            pygame.draw.rect(screen, COLOR_VISITED, (j*cell_size, i*cell_size, cell_size, cell_size))
        
        
        i, j = current_cell_solver
        pygame.draw.rect(screen, COLOR_CURRENT, (j*cell_size, i*cell_size, cell_size, cell_size))
        
       
        frame_counter += 1
        if frame_counter % 5 == 0:  
            pygame.display.flip()
            clock.tick(60)  

    path = solver(maze, step_callback=step_callback)

    
    if path:
        for i, j in path:
            pygame.draw.rect(screen, COLOR_FINAL_PATH, (j*cell_size, i*cell_size, cell_size, cell_size))
    pygame.display.flip()
    
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        clock.tick(30)
    print("Number of steps:", len(visited_cells))
    print("Path length:", len(path))
    pygame.quit()
    