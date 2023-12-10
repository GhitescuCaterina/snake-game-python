import random
import pygame
import sys
from pygame.math import Vector2


class SARPE:
    def __init__(self):
        self.corp = [Vector2(5, 10), Vector2(6, 10), Vector2(7, 10)]
        self.directie = Vector2(1, 0)

    def draw_snake(self):
        for block in self.corp:
            x_pozitie = int(block.x * cell_size)
            y_pozitie = int(block.y * cell_size)
            corp_rect = pygame.Rect(x_pozitie, y_pozitie, cell_size, cell_size)
            pygame.draw.rect(screen, (58, 192, 100), corp_rect)

    def move_snake(self):
        copie_corp = self.corp[:-1]
        copie_corp.insert(0, copie_corp[0] + self.directie)
        self.corp = copie_corp[:]


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
sarpe = SARPE()

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE,150)

# ecranul de joc
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SCREEN_UPDATE:
            sarpe.move_snake()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                sarpe.direction = Vector2(0, -1)
            if event.key == pygame.K_d:
                sarpe.direction = Vector2(1, 0)
            if event.key == pygame.K_s:
                sarpe.direction = Vector2(0, 1)
            if event.key == pygame.K_a:
                sarpe.direction = Vector2(-1, 0)

    screen.fill((175, 30, 70))
    fruit.draw_fruit()
    sarpe.draw_snake()
    pygame.display.update()
    clock.tick(60)
