import pygame
import os
from grid import Grid

# set the window position relative to the screen upper left corner
os.environ["SDL_VIDEO_WINDOW_POS"] = "%d,%d" % (200, 80)

# create the window surface and set the window caption
surface = pygame.display.set_mode((1000, 720))
pygame.display.set_caption("Sudoku")

pygame.font.init()
game_font = pygame.font.SysFont("Comic Sans MS", 40)

grid = Grid(pygame, game_font)
running = True

# the game loop
while running:
    
    # check for input events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:  # check for left mouse button click
                pos = pygame.mouse.get_pos()
                grid.get_mouse_click(pos[0], pos[1])
       
       
    # clear the window surface to block
    surface.fill((0, 0, 0))

    # draw the grid here
    grid.draw_all(pygame, surface)

    # update the window surface
    pygame.display.flip()