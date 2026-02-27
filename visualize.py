import pygame, time

def show_stats(maze,path,screen,time_taken,algorythm_time,visited_cells,path_length):
        white_cells = maze.white_cells()
        old_surface = screen.copy()
        screen = pygame.display.set_mode((1200, 1000))
        screen.blit(old_surface, (0, 0))
        pygame.display.flip()
        font_title = pygame.font.SysFont('segoeui', 22, bold=True)
        font_stat  = pygame.font.SysFont('segoeui', 18)

        panel_x = 1010
        stats = [
            ("Visited cells",  str(len(visited_cells))),
            ("Path length",    str(path_length)),
            ("Time",           f"{time_taken:.3f} s"),
            ("Algorithm Time", f"{algorythm_time:.3f} s"),
            ('Efficiency',     f"{path_length/len(visited_cells)*100:.2f}%" if path_length > 0 else "N/A"),
            ("Explored",       f"{len(visited_cells)}/{white_cells}")
        ]
        
        for i, (label, value) in enumerate(stats):
            y = 50 + i * 100
            lbl = font_title.render(label, True, (180, 180, 200))
            val = font_stat.render(value, True, (255, 255, 255))
            screen.blit(lbl, (panel_x, y))
            screen.blit(val, (panel_x, y + 28))
            pygame.draw.line(screen, (60, 60, 80), (panel_x, y + 55), (1190, y + 55), 1)

        pygame.display.flip()



def visualize_solver(maze, solver):

    
    
   
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
    algorythm_time_total = 0.0

    def step_callback(current_cell_solver, open_list):
        nonlocal visited_cells, frame_counter, algorythm_time_total
        
        draw_start = time.time()

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
        algorythm_time_total += time.time() - draw_start
        
    time_start = time.time()
    path = solver(maze, step_callback=step_callback)
    time_end = time.time()
    
    time_taken = time_end - time_start
    algorythm_time = time_taken - algorythm_time_total

    if path:
        for i, j in path:
            pygame.draw.rect(screen, COLOR_FINAL_PATH, (int(j*cell_size), int(i*cell_size), int(cell_size)+1, int(cell_size)+1))
    pygame.display.flip()
    show_stats(maze, path, screen, time_taken,algorythm_time, visited_cells, len(path))
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                
                running = False
        clock.tick(30)
    
  
    

    



