def visualize_solver(maze, solver, delay=0.05):
    import pygame, time
    pygame.init()
    screen = pygame.display.set_mode((1000, 1000))
    pygame.display.set_caption("Maze Solver Visualization")
    clock = pygame.time.Clock()
    cell_size = 1000 / maze.width
    
    # Kolory
    COLOR_WALL = (0,0,0)
    COLOR_PATH = (255,255,255)
    COLOR_VISITED = (255,0,0)
    COLOR_CURRENT = (65,105,225)
    COLOR_FINAL_PATH = (0,255,0)

    
    for i in range(maze.height):
        for j in range(maze.width):
            color = COLOR_PATH if maze.grid[i][j] == 0 else COLOR_WALL
            pygame.draw.rect(screen, color, (int(j*cell_size), int(i*cell_size), int(cell_size)+1, int(cell_size)+1))
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
            pygame.draw.rect(screen, COLOR_VISITED, (int(j*cell_size), int(i*cell_size), int(cell_size)+1, int(cell_size)+1))
        
        i, j = current_cell_solver
        pygame.draw.rect(screen, COLOR_CURRENT, (int(j*cell_size), int(i*cell_size), int(cell_size)+1, int(cell_size)+1))
        
        frame_counter += 1
        if frame_counter % 5 == 0:  
            pygame.display.flip()
            clock.tick(60)  
    time_start = time.time()
    path = solver(maze, step_callback=step_callback)
    time_end = time.time()
    
    if path:
        for i, j in path:
            pygame.draw.rect(screen, COLOR_FINAL_PATH, (int(j*cell_size), int(i*cell_size), int(cell_size)+1, int(cell_size)+1))
    pygame.display.flip()
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        clock.tick(30)
    print("Number of steps:", len(visited_cells))
    print("Path length:", len(path))
    

    return time_end - time_start,visited_cells,path