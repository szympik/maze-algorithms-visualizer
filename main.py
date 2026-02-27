from importlib.resources import path
from cell import *
from maze import *
from a_star import *
import time
from visualize import visualize_solver
import pygame, time

BG        = (18,  18,  30)
ACCENT    = (99, 102, 241)
ACCENT2   = (129, 140, 248)
SURFACE   = (30,  30,  50)
SURFACE2  = (42,  42,  65)
TEXT      = (220, 220, 240)
TEXT_DIM  = (120, 120, 160)
GREEN_BTN = (34, 197, 94)
GREEN_HOV = (22, 163, 74)

def draw_rounded_rect(surface, color, rect, radius=10, width=0):
    pygame.draw.rect(surface, color, rect, width, border_radius=radius)

class InputBox:
    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.font = pygame.font.SysFont('segoeui', 22)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.unicode.isdigit():
                self.text += event.unicode

    def draw(self, screen):
        border_color = ACCENT if self.active else SURFACE2
        draw_rounded_rect(screen, SURFACE, self.rect, radius=8)
        draw_rounded_rect(screen, border_color, self.rect, radius=8, width=2)
        txt_surface = self.font.render(self.text, True, TEXT)
        screen.blit(txt_surface, (self.rect.x + 12, self.rect.y + (self.rect.h - txt_surface.get_height())//2))

class Dropdown:
    def __init__(self, x, y, w, h, options, font):
        self.rect = pygame.Rect(x, y, w, h)
        self.options = options
        self.selected = 0
        self.font = font
        self.active = False
        self.option_rects = []
        self.hovered = -1

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            elif self.active:
                for i, opt_rect in enumerate(self.option_rects):
                    if opt_rect.collidepoint(event.pos):
                        self.selected = i
                        self.active = False
                        break
                else:
                    self.active = False
        if event.type == pygame.MOUSEMOTION and self.active:
            self.hovered = -1
            for i, opt_rect in enumerate(self.option_rects):
                if opt_rect.collidepoint(event.pos):
                    self.hovered = i

    def draw(self, screen):
        # Główny przycisk
        bg = ACCENT if self.active else SURFACE
        draw_rounded_rect(screen, bg, self.rect, radius=8)
        draw_rounded_rect(screen, ACCENT, self.rect, radius=8, width=2)
        txt = self.font.render(self.options[self.selected], True, TEXT)
        screen.blit(txt, (self.rect.x + 12, self.rect.y + (self.rect.h - txt.get_height())//2))
        arrow_txt = "▲" if self.active else "▼"
        arrow = self.font.render(arrow_txt, True, TEXT_DIM)
        screen.blit(arrow, (self.rect.x + self.rect.w - 36, self.rect.y + (self.rect.h - arrow.get_height())//2))

    def draw_overlay(self, screen):
        # Rysowane na samej górze - zachodzi na resztę UI
        if not self.active:
            return
        self.option_rects = []
        for i, option in enumerate(self.options):
            opt_rect = pygame.Rect(self.rect.x, self.rect.y + (i+1)*self.rect.h, self.rect.w, self.rect.h)
            self.option_rects.append(opt_rect)
            bg_opt = ACCENT2 if i == self.hovered else SURFACE2
            draw_rounded_rect(screen, bg_opt, opt_rect, radius=6)
            draw_rounded_rect(screen, ACCENT, opt_rect, radius=6, width=1)
            opt_txt = self.font.render(option, True, TEXT)
            screen.blit(opt_txt, (opt_rect.x + 12, opt_rect.y + (opt_rect.h - opt_txt.get_height())//2))

def menu():
    pygame.init()
    screen = pygame.display.set_mode((700, 560))
    pygame.display.set_caption("Maze Solver")
    clock = pygame.time.Clock()
    
    font_title  = pygame.font.SysFont('segoeui', 56, bold=True)
    font_label  = pygame.font.SysFont('segoeui', 20)
    font_option = pygame.font.SysFont('segoeui', 22)
    font_sub    = pygame.font.SysFont('segoeui', 16)

    CX = 350  # środek okna
    
    size_input       = InputBox(CX - 100, 195, 200, 44, '10')
    solver_dropdown  = Dropdown(CX - 150, 295, 300, 44, ["A*", "BFS", "DFS"], font_option)
    creator_dropdown = Dropdown(CX - 150, 390, 300, 44, ["DFS Backtracking"], font_option)

    start_rect = pygame.Rect(CX - 100, 475, 200, 52)
    start_hovered = False

    running = True
    while running:
        screen.fill(BG)
        
       
        pygame.draw.line(screen, SURFACE2, (50, 100), (650, 100), 1)

        # Tytuł
        title = font_title.render("Maze Solver", True, ACCENT2)
        screen.blit(title, (CX - title.get_width()//2, 24))
        sub = font_sub.render("Configure and visualize maze solving algorithms", True, TEXT_DIM)
        screen.blit(sub, (CX - sub.get_width()//2, 85))

        # Sekcje
        for label_txt, y in [("MAZE SIZE", 165), ("SOLVER", 265), ("GENERATOR", 360)]:
            lbl = font_label.render(label_txt, True, ACCENT2)
            screen.blit(lbl, (CX - 150, y))

        # Komponenty (bez overlayów)
        size_input.draw(screen)
        solver_dropdown.draw(screen)
        creator_dropdown.draw(screen)

        # Przycisk START
        btn_color = GREEN_HOV if start_hovered else GREEN_BTN
        draw_rounded_rect(screen, btn_color, start_rect, radius=10)
        start_text = font_option.render("▶   START", True, (255, 255, 255))
        screen.blit(start_text, (start_rect.centerx - start_text.get_width()//2,
                                  start_rect.centery - start_text.get_height()//2))
    
        solver_dropdown.draw_overlay(screen)
        creator_dropdown.draw_overlay(screen)

        pygame.display.flip()
        
        # Obsługa zdarzeń
        mx, my = pygame.mouse.get_pos()
        start_hovered = start_rect.collidepoint(mx, my)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            
            size_input.handle_event(event)
            # Zamknij drugi dropdown jeśli otwieramy pierwszy i odwrotnie
            if event.type == pygame.MOUSEBUTTONDOWN:
                if solver_dropdown.rect.collidepoint(event.pos):
                    creator_dropdown.active = False
                if creator_dropdown.rect.collidepoint(event.pos):
                    solver_dropdown.active = False

            solver_dropdown.handle_event(event)
            creator_dropdown.handle_event(event)
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_rect.collidepoint(event.pos):
                    try:
                        size = int(size_input.text) if size_input.text else 50
                        size = max(5, min(size, 500))
                    except ValueError:
                        size = 50
                    
                    pygame.quit()
                    maze = Maze(size)
                    maze.create_maze()
                    
                    solver_name = solver_dropdown.options[solver_dropdown.selected]
                    if solver_name == "A*":
                       
                        visualize_solver(maze, a_star_search)
                    # elif solver_name == "BFS":
                    #     time_taken = visualize_solver(maze, bfs_search, 0.1)
                    
                    return
                
        clock.tick(60)



def main():
    menu()

if __name__ == "__main__":
    main()