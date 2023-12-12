import random
import pygame
import sys
from pygame.math import Vector2


class SARPE:
    def __init__(self):
        self.corp = [Vector2(5, 10), Vector2(6, 10), Vector2(7, 10)]
        self.directie = Vector2(1, 0)
        self.bucata_noua = False

    def draw_snake(self):
        for block in self.corp:
            x_pozitie = int(block.x * cell_size)
            y_pozitie = int(block.y * cell_size)
            corp_rect = pygame.Rect(x_pozitie, y_pozitie, cell_size, cell_size)
            pygame.draw.rect(screen, (58, 192, 100), corp_rect)

    def move_snake(self):
        if self.bucata_noua:
            copie_corp = self.corp[:]
            copie_corp.insert(0, copie_corp[0] + self.directie)
            self.corp = copie_corp[:]
            self.bucata_noua = False
        else:
            copie_corp = self.corp[:-1]
            copie_corp.insert(0, copie_corp[0] + self.directie)
            self.corp = copie_corp[:]

    def bucata_corp(self):
        self.bucata_noua = True


class MANCARE:
    def __init__(self):
        self.randomize()

    def draw_fruit(self):
        fruit_rect = pygame.Rect(int(self.pozitie.x * cell_size), int(self.pozitie.y * cell_size), cell_size, cell_size)
        pygame.draw.rect(screen, (255, 30, 30), fruit_rect)

    def randomize(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pozitie = Vector2(self.x, self.y)


def game_over():
    pygame.quit()
    sys.exit()


class MAIN:
    def __init__(self):
        self.sarpe = SARPE()
        self.mancare = MANCARE()

    def update(self):
        self.sarpe.move_snake()
        self.coliziune()
        self.pierdut()

    def draw_everything(self):
        self.mancare.draw_fruit()
        self.sarpe.draw_snake()

    def coliziune(self):
        if self.mancare.pozitie == self.sarpe.corp[0]:
            self.mancare.randomize()
            self.sarpe.bucata_corp()

    def pierdut(self):
        if not 0 <= self.sarpe.corp[0].x < cell_number or not 0 <= self.sarpe.corp[0].y < cell_number:
            game_over()

        for block in self.sarpe.corp[1:]:
            if block == self.sarpe.corp[0]:
                game_over()


pygame.init()
cell_size = 40
cell_number = 20
screen = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size))
clock = pygame.time.Clock()

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)

main_game = MAIN()

# ecranul de joc
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SCREEN_UPDATE:
            main_game.update()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                main_game.sarpe.directie = Vector2(0, -1)
            if event.key == pygame.K_d:
                main_game.sarpe.directie = Vector2(1, 0)
            if event.key == pygame.K_s:
                main_game.sarpe.directie = Vector2(0, 1)
            if event.key == pygame.K_a:
                main_game.sarpe.directie = Vector2(-1, 0)

    screen.fill((175, 30, 70))
    main_game.draw_everything()
    pygame.display.update()
    clock.tick(60)
