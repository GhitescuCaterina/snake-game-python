# import turtle
import random

import pygame
import sys
from pygame.math import Vector2


class MANCARE:
    def __init__(self):
        self.x = random.randint(0, cell_number-1)
        self.y = random.randint(0, cell_number-1)
        self.pozitie = Vector2(self.x, self.y)

    def draw_fruit(self):
        fruit_rect = pygame.Rect(int(self.pozitie.x*cell_size), int(self.pozitie.y*cell_size), cell_size, cell_size)
        pygame.draw.rect(screen, (255, 30, 30), fruit_rect)


pygame.init()
cell_size = 40
cell_number = 20
screen = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size))
clock = pygame.time.Clock()

fruit = MANCARE()

# ecranul de joc
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    screen.fill((175, 30, 70))
    fruit.draw_fruit()
    pygame.display.update()
    clock.tick(60)
